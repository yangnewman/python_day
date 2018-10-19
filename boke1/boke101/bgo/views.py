from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render

# Create your views here.
from django.urls import reverse

from bgo.forms import ArticleForm
from users.models import SuperUser
from bgo.models import UserArticle
from utils.functions import is_login


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

# 添加文章
@is_login
def add_article(request):
    if request.method == 'GET':

        return render(request, 'add-article.html')

    if request.method == 'POST':
        # 表单验证他们是否填写
        form = ArticleForm(request.POST, request.FILES)
        # 如果已经填写完毕
        if form.is_valid():

            # 获取对象
            # data = form.cleaned_data
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            tags = form.cleaned_data['tags']
            image = request.FILES.get('upload_img')
            describe = form.cleaned_data['describe']
            # 向数据库里添加数据
            UserArticle.objects.create(art_des=describe,
                                       art_title=title,
                                       art_content=content, 
                                       art_tags=tags,
                                       art_img=image)
            # 添加成功后跳转页面
            return HttpResponseRedirect(reverse('bgo:article'))
        else:
            # 如果没有就返回错误信息
            return render(request, 'add-article.html', {'form':form})


@is_login
# 文章
def article (request):

    if request.method == 'GET':

        articles = UserArticle.objects.all()

        return render(request, 'article.html', {'articles':articles})


@is_login
# 删除文章
def delete_article(request):

    if request.method == 'POST':

        id = request.POST.get('id')
        # 删除对象
        UserArticle.objects.filter(pk=id).first().delete()

        return JsonResponse({'code':'200', 'msg':'请求成功'})










