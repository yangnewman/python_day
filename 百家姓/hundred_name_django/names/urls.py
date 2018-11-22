
from django.conf.urls import url
from rest_framework.routers import SimpleRouter

from names import views
# 引入路由
router = SimpleRouter()

# 使用router注册的地址
router.register(r'^hundred_name', views.HundredsView)
# router.register(r'^name', views.NamesView)

urlpatterns = [

    # 首页
    url(r'^index/', views.index, name='index'),

    # 姓名分页
    url(r'^name_list/(.+)/', views.name_list, name='name_list'),

    # 姓名信息展示
    url(r'^detail/(.+)/', views.detail, name='detail'),

    # 搜索
    url(r'^search/(.+)/', views.search, name='search'),


]

urlpatterns += router.urls





