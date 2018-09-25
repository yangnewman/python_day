from django.contrib.auth.hashers import check_password, make_password
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render

# Create your views here.
from django.urls import reverse

from users.models import SuperUser, UserArticle

from utils.functions import is_login



# def create(request):
#
#     if request.method== 'GET':
#
#         username = 'admin'
#         password = '123456'
#         password = make_password(password)
#         SuperUser.objects.create(username=username, password=password)
#         return HttpResponse('创建用户')



def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('userpwd')

        # if not all([username, password]):
        #     # 如果不填写完整
        #     error_msg = '用户名或者密码未填，请重新输入'
        #
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

@is_login
# 文章
def article (request):

    if request.method == 'GET':

        return render(request, 'article.html')

@is_login
# 公告
def notice (request):

    if request.method == 'GET':

        return render(request, 'notice.html')

@is_login
# 栏目
def category(request):

        if request.method == 'GET':
            return render(request, 'category.html')

@is_login
# 添加文章
def add_article(request):
    if request.method == 'GET':
        return render(request, 'add-article.html')


    if request.method == 'POST':

        title = request.POST.get('art_title')
        content = request.POST.get('art_content')

        UserArticle.objects.create(art_title=title, art_content=content)
        # 跳转页面
        # return HttpResponseRedirect(reverse('user:article'))
        return render(request, 'add-article.html')




