from django.db import models

# Create your models here.


class SuperUser(models.Model):

    username = models.CharField(max_length=10, unique=True, verbose_name='帐号')
    password = models.CharField(max_length=255, unique=True, verbose_name='密码')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='修改时间')

    class Meta:
        db_table = 'super_user'



















