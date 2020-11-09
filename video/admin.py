from django.contrib import admin
from video.models import UserInfo, MovieInfo, Category
# # Register your models here.


@admin.register(UserInfo)
class UserInfoAdmin(admin.ModelAdmin):
    list_display = ['username', 'is_superuser', 'forbidden', 'last_login']


@admin.register(MovieInfo)
class MovieInfoAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'pub_time', 'click_num']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['category_name']


