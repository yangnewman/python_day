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

    # 文章
    url(r'^article/', views.article, name='article'),

    # 公告
    url(r'^notice/', views.notice, name='notice'),


    # 栏目
    url(r'^category/', views.category, name='category'),

    # 添加文章
    url(r'^add_article/', views.add_article, name='add_article'),

]





