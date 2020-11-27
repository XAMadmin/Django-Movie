from django.shortcuts import render, HttpResponse, redirect, HttpResponseRedirect
from django.core.paginator import Paginator, PageNotAnInteger, InvalidPage
from video.models import MovieInfo, Category, MessageInfo
import json
import re
import os
import mimetypes
from wsgiref.util import FileWrapper
from django.http import StreamingHttpResponse
from django.contrib import auth


def index(request):
    username = request.session.get("username", '')
    search_name = request.GET.get('search_name', '')
    page_num = request.GET.get('page_num', 1)
    category_id = request.GET.get('category_num', "0")
    categroys = Category.objects.all()
    if category_id != '0':
        category = Category.objects.get(id=int(category_id))
        if search_name:
            movies = category.movies.all().filter(title__contains=search_name)
        else:
            movies = category.movies.all()
    else:
        if search_name:
            movies = MovieInfo.objects.all().filter(title__contains=search_name)
        else:
            movies = MovieInfo.objects.all()
    paginator = Paginator(movies, 8)
    try:
        page = paginator.page(int(page_num))
    except PageNotAnInteger:
        page = paginator.page(1)
    except InvalidPage:
        return render(request, '404.html')
    except Exception as e:
        page = paginator.page(1)
    current_page_num = page.number
    page_range = list(range(max(current_page_num - 2, 1), current_page_num)) + list(range(current_page_num,
                                                                                          min(current_page_num + 2,
                                                                                              paginator.num_pages) + 1))

    if page_range[0] - 1 >= 2:
        page_range.insert(0, '...')
    if paginator.num_pages - page_range[-1] >= 2:
        page_range.append('...')
    if page_range[0] != 1:
        page_range.insert(0, 1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)
    context = {"catagroys": categroys, "page_range": page_range,
               "page": page, "category_num": int(category_id),
               "search_name": search_name, "username": username}
    return render(request, 'index.html', context)


def detail_parse(request, pk):
    username = request.session.get("username", "")
    movies = MovieInfo.objects.all().order_by('-click_num')[0:5]
    try:
        movie = MovieInfo.objects.get(pk=pk)
        msgs = movie.messages.all().order_by("-id")
        if username:
            movie.click_num += 1
            movie.save()
    except Exception as e:
        data = {"errno": 4101, 'errmsg': '数据库错误:{}'.format(e)}
        return HttpResponse(json.dumps(data))
    data = {
        "errno": 0,
        "errmsg": '数据获取成功',
        "movie": movie,
        "msgs": msgs,
        "movies": movies,
        "username": username
    }
    # res = render(request, 'detail.html', data)
    # res["content-type"] = 'video/mp4'
    # return res
    return render(request, 'detail.html', data)


def about(request):
    return render(request, 'about.html')


def file_iterator(file_name, chunk_size=8192, offset=0, length=None):
    with open(file_name, "rb") as f:
        f.seek(offset, os.SEEK_SET)
        remaining = length
        while True:
            bytes_length = chunk_size if remaining is None else min(remaining, chunk_size)
            data = f.read(bytes_length)

            if not data:
                break
            if remaining:
                remaining -= len(data)
            yield data


def stream_video(request):
    """将视频文件以流媒体的方式响应"""
    range_header = request.META.get('HTTP_RANGE', '').strip()
    range_re = re.compile(r'bytes\s*=\s*(\d+)\s*-\s*(\d*)', re.I)
    range_match = range_re.match(range_header)
    path = request.GET.get('path')
    # 这里根据实际情况改变，我的views.py在core文件夹下但是folder_path却只到core的上一层，media也在core文件夹下
    folder_path = os.getcwd().replace('\\', '/')
    # path=folder_path+'/core/'+path # path就是template ？后面的参数的值
    path = folder_path + path
    size = os.path.getsize(path)

    content_type, encoding = mimetypes.guess_type(path)
    content_type = content_type or 'application/octet-stream'
    if range_match:
        first_byte, last_byte = range_match.groups()
        first_byte = int(first_byte) if first_byte else 0
        last_byte = first_byte + 1024 * 1024 * 10
        if last_byte >= size:
            last_byte = size - 1
        length = last_byte - first_byte + 1
        resp = StreamingHttpResponse(file_iterator(path, offset=first_byte,
                                                   length=length), status=206, content_type=content_type)
        resp['Content-Length'] = str(length)
        resp['Content-Range'] = 'bytes %s-%s/%s' % (first_byte, last_byte, size)
    else:
        resp = StreamingHttpResponse(FileWrapper(open(path, 'rb')), content_type=content_type)
        resp['Content-Length'] = str(size)
    resp['Accept-Ranges'] = 'bytes'
    return resp


def login(request):

    if request.method == 'GET':
        return render(request, 'login.html')

    elif request.method == 'POST':
        info = json.loads(request.body.decode('utf-8'))
        # username = request.POST.get("username")
        # password = request.POST.get("password")

        username = info.get("username")
        password = info.get("password")
        print(username)
        print(password)

        request.session.set_expiry(60*60)
        user = auth.authenticate(username=username, password=password)
        print(user)
        if user:
            request.session["username"] = username
            data = {"errno": '0', 'errmsg': 'ok,登录成功！', "username": username}
            return HttpResponse(json.dumps(data))
        else:
            data = {"errno": '4101', 'errmsg': 'err, 用户名或密码错误！'}
            return HttpResponse(json.dumps(data))
    else:
        data = {"errno": 500, 'errmsg': '服务请求错误！'}
        return HttpResponse(json.dumps(data))


def logout(request):
    request.session.flush()
    refer = request.META.get("HTTP_REFERER", "")
    if not refer:
        return redirect('video:index')
    return HttpResponseRedirect(refer)


def send_message(request):
    movie_id = request.GET.get("movie_id", "")
    username = request.GET.get("username", "")
    comment = request.GET.get("comment", "")
    if all([movie_id, username, comment]):
        movie = MovieInfo.objects.get(id=movie_id)
        db = MessageInfo(username=username, comment=comment)
        db.message_id = movie
        db.save()
        count = movie.messages.all().order_by("-id").count()
        messages = {
            "username": username,
            "comment": comment,
            "count": count
        }

        data = {"errno": 0,  "errmsg": "OK！", "msgs": messages}
        return HttpResponse(json.dumps(data))
    else:
        data = {"errno": 4001, 'errmsg': '参数不完全！'}
        return HttpResponse(json.dumps(data))


# def index(request):
#
#     if request.method == 'GET':
#         fp = File.objects.all()
#         return render(request, 'index.html', {'data': fp})
#     elif request.method == 'POST':
#
#         file_obj = request.FILES.get('sub_file')
#         if file_obj:
#             file_name = file_obj.name
#             path = settings.MEDIA_ROOT + file_name
#             with open(path, 'wb') as f:
#                 for ck in file_obj.chunks():
#                     f.write(ck)
#             file = File(file=file_name)
#             file.save()
#             fp = File.objects.all()
#             return render(request, 'index.html', {'data': fp})
#         else:
#             return HttpResponse("上传失败！！")
#
#
#     else:
#         return HttpResponse("提交方式错误！！")








