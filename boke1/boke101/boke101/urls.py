"""boke101 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from boke101 import settings
from django.conf.urls import url, include

from django.contrib import admin
from django.contrib.staticfiles.urls import static

from utils.upload_image import upload_image

urlpatterns = [

    url(r'^admin/', admin.site.urls),

    url(r'^user/', include('users.urls', namespace='user')),

    url(r'^bgo/', include('bgo.urls', namespace='bgo')),

    # 上传图片路径
    url(r'^util/upload/(?P<dir_name>[^/]+)$', upload_image, name='upload_image'),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)