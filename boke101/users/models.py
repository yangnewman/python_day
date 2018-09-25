from django.db import models

# Create your models here.


class SuperUser(models.Model):

    username = models.CharField(max_length=10, unique=True, verbose_name='帐号')
    password = models.CharField(max_length=255, unique=True, verbose_name='密码')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='修改时间')

    class Meta:
        db_table = 'super_user'


#
# class UserTicket(models.Model):
#
#     user = models.ForeignKey(SuperUser)
#     ticket = models.CharField(max_length=30)
#     create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
#
#     class Meta:
#         db_table = 'user_ticket'


# class Test(models.Model):
#
#
#     gogo = models.CharField(max_length=10, null=True)
#     didi = models.CharField(max_length=222, null=True)
#
#     class Meta:
#         db_table = 'test1'


class UserArticle(models.Model):

    art_title = models.CharField(max_length=99, null=True)
    art_content = models.TextField(null=True)
    art_tags = models.CharField(max_length=99, null=True)

    class Meta:
        db_table = 'user_article'


















