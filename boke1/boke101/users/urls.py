from django.conf.urls import url

from users import views

urlpatterns = [
    # 首页
    url(r'^index/', views.index, name='index'),

    # 登录
    url(r'^login/', views.login, name='login'),
    # 创建用户
    # url(r'^create/', views.create, name='create'),
    # 注销
    url(r'^logout', views.logout, name='logout'),



]





