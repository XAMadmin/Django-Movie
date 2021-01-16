from django.urls import path
from video import views
# from django.conf.urls.static import static
# from django.conf import settings

app_name = 'video'
urlpatterns = [
    # path('page_index/', views.page_index, name='page_index'),
    path('index/', views.index, name='index'),
    path('detail_parse/<int:pk>', views.detail_parse, name='detail_parse'),
    path('about/', views.about, name='about'),
    path('test_resp/', views.stream_video, name='test_resp'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('send_message/', views.send_message, name='send_message'),
    path('register/', views.register, name='register'),

]


# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# http://127.0.0.1:8000/video/detail_parse/3
