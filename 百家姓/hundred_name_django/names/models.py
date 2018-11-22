from django.db import models

# Create your models here.


# create table names(
# 		id int auto_increment,
# 		name varchar(50) not null,
# 		url varchar(50) not null,
# 		sex_man varchar(50) not null,
# 		sex_woman varchar(50) not null,
# 		name_poetry varchar(255) not null,
# 		name_explain varchar(512) not null,
# 		name_five_lines varchar(50) not null,
# 		name_three varchar(50) not null,
# 		name_configure varchar(50) not null,
# 		name_analysis varchar(512) not null,
# 		primary key (id)
# 	) engine= InnoDB default charset=utf8;


# Create your models here.


import datetime

from django.db import models


# 姓名信息
class NamesInfo(models.Model):

    name = models.CharField(max_length=50, null=True, verbose_name='姓名')
    url = models.CharField(max_length=50, null=True, verbose_name='地址')
    sex_man = models.CharField(max_length=50, null=True, verbose_name='男用概率')
    sex_woman = models.CharField(max_length=50, null=True, verbose_name='女用概率')
    name_poetry = models.CharField(max_length=255, null=True, verbose_name='姓名诗')
    name_explain = models.CharField(max_length=512, null=True, verbose_name='姓名总解')
    name_five_lines = models.CharField(max_length=50, null=True, verbose_name='五行')
    name_three = models.CharField(max_length=50, null=True, verbose_name='三才配置')
    name_configure = models.CharField(max_length=50, null=True, verbose_name='五格')
    name_analysis = models.CharField(max_length=512, null=True, verbose_name='五格分析')

    class Meta:
        db_table = 'names'


# 百家姓
class HundredNameInfo(models.Model):

    title = models.CharField(max_length=50, null=True, verbose_name='姓')
    url = models.CharField(max_length=50, null=True, verbose_name='地址')
    nums = models.CharField(max_length=50, null=True, verbose_name='数量')

    class Meta:
        db_table = 'hundred_name'




