from django.contrib import admin
from video.models import UserInfo, MovieInfo, Category, MessageInfo
from django.contrib.auth.admin import UserAdmin
# # Register your models here.

admin.site.site_header = '视频随心享'
admin.site.site_title = '视频随心享后台管理'
admin.site.index_title = '欢迎使用视频随心享'

@admin.register(UserInfo)
class UserInfoAdmin(UserAdmin):
    list_display = ['username', 'is_superuser', 'forbidden', 'is_staff','last_login']
    fieldsets = (
        ('基本信息',{'fields':['username', 'password']}),
        ('高级',{
            'fields':['is_staff', 'is_active', 'is_superuser', 'forbidden'],
            'classes': ('collapse',)  # 是否折叠显示
        })


    )

@admin.register(MovieInfo)
class MovieInfoAdmin(admin.ModelAdmin):
    list_display = ['id','thumb_image','title', 'categroy_show','user', 'pub_time', 'click_num']
    list_filter = ['category']
    search_fields = ['title']
    ordering = ['id']
    list_per_page = 5



@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['category_name']


@admin.register(MessageInfo)
class MessageInfoAdmin(admin.ModelAdmin):
    list_display = ['username', 'comment', 'comment_time', 'message_id']



