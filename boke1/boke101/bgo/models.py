
# Create your models here.
from django.db import models

# Create your models here.



class UserArticle(models.Model):

    art_title = models.CharField(max_length=99, null=True, verbose_name='文章标题')
    art_content = models.TextField(null=True, verbose_name='文章内容')
    art_tags = models.CharField(max_length=99, null=True, verbose_name='文章标签')
    art_img = models.ImageField(upload_to='upload', null=True, verbose_name='文章图片')

    art_des = models.CharField(max_length=200, null=True, verbose_name='文章描述')
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='修改时间')
    click_time = models.IntegerField(default=0, verbose_name='点击次数')


    class Meta:
        db_table = 'user_article'
