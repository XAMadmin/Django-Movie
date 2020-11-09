from django.db import models
from django.contrib.auth.models import AbstractUser

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



