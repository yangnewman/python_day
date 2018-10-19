from django.conf.urls import url
from rest_framework.routers import SimpleRouter
from home import views

router = SimpleRouter()

# router.register(r'^article', views.)


urlpatterns = [

    url(r'^index/', views.index, name='index'),
    url(r'^about/', views.about, name='about'),
    url(r'^info/', views.info, name='info'),

]


