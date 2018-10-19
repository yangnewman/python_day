from django.contrib.auth.hashers import check_password, make_password
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render

# Create your views here.
from django.urls import reverse

from users.models import SuperUser
from bgo.models import UserArticle
from utils.functions import is_login


def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')

    if request.method == 'POST':
        # 获取请求的对象
        username = request.POST.get('username')
        password = request.POST.get('userpwd')
        # if not all([username, password]):
        #     # 如果不填写完整
        #     error_msg = '用户名或者密码未填，请重新输入'
        #     return render(request, 'login.html', {'errors':error_msg})
        # 在数据库中获取当前用户名字相同的对象
        user = SuperUser.objects.filter(username = username).first()
        # 判断是否存在
        if user:
            # 校验密码是否正确
            if check_password(password, user.password):

                # 当密码正确就赋予一个cookies值
                request.session['user_id'] = user.id
                request.session.set_expiry(7200)
                return HttpResponseRedirect(reverse('user:index'))
            else:
                # 密码不正确的时候
                error_msg = '密码错误'
                return render(request, 'login.html', {'errors':error_msg})
        else:
            error_msg = '用户名不存在'
            return render(request, 'login.html', {'errors':error_msg})


@is_login
# 首页
def index(request):
    if request.method == 'GET':

        request.session.get('user_id')

        return render(request, 'index.html')

@is_login
# 注销
def logout(request):
    if request.method == 'GET':

        request.session.flush()

        return HttpResponseRedirect(reverse('user:login'))





