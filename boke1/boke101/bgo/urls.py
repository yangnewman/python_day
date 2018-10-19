
from django.conf.urls import url

from bgo import views

urlpatterns = [
# 文章
    url(r'^article/', views.article, name='article'),

    # 公告
    url(r'^notice/', views.notice, name='notice'),

    # 栏目
    url(r'^category/', views.category, name='category'),

    # 添加文章
    url(r'^add_article/', views.add_article, name='add_article'),
    # 删除文章
    url(r'^delete_article/', views.delete_article, name='delete_article'),

]