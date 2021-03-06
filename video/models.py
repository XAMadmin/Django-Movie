from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.safestring import mark_safe

# Create your models here.


class UserInfo(AbstractUser):
    forbidden = models.BooleanField(default=False, verbose_name='是否禁用')


class Category(models.Model):
    category_name = models.CharField(max_length=50, verbose_name='类型')

    def __str__(self):
        return self. category_name

    class Meta:
        verbose_name = '类型'
        verbose_name_plural = verbose_name


class MovieInfo(models.Model):
    title = models.CharField(max_length=50, verbose_name='片名')
    user = models.ForeignKey(UserInfo, related_name='user', on_delete=models.DO_NOTHING, verbose_name='用户')
    category = models.ForeignKey(Category, related_name='movies', on_delete=models.DO_NOTHING, verbose_name='类型')
    cover = models.ImageField(upload_to='./media/cover/', verbose_name='封面')
    movie_url = models.FileField(upload_to='./media/movie/', verbose_name='视频')
    pub_time = models.DateTimeField(auto_now_add=True, verbose_name='发布时间')
    click_num = models.IntegerField(default=0, verbose_name='观看次数')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '电影'
        verbose_name_plural = verbose_name


    def thumb_image(self):
        if not self.cover:
            return "无图片"
        else:
            return mark_safe('<img src="/media/%s" style="height: 60px;width:100px; border-radius: 5px;">' % (self.cover))

    
    thumb_image.short_description = '封面'


    def categroy_show(self):
        return self.category.category_name

    categroy_show.short_description = '分类'


class MessageInfo(models.Model):
    username = models.CharField(max_length=50, verbose_name='留言人')
    comment = models.TextField(max_length=200, verbose_name='留言')
    comment_time = models.DateTimeField(auto_now_add=True, verbose_name='留言时间')
    message_id = models.ForeignKey(MovieInfo, related_name='messages',
                                   on_delete=models.DO_NOTHING, blank=True, null=True, verbose_name='电影名称')

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = '留言'
        verbose_name_plural = verbose_name





