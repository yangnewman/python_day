from django.core.paginator import Paginator
from django.shortcuts import render

from home.models import UserArticle

# Create your views here.



def index(request):

    if request.method == 'GET':
        articles = UserArticle.objects.all()
        return render(request, 'index.html', {'articles':articles})


def about(request):
    if request.method == 'GET':
        return render(request, 'about.html')


def info(request):
    if request.method == 'GET':

        articles = UserArticle.objects.all()
        paginator = Paginator(articles, 1)
        page_num = int(request.GET.get('page', 1))
        page_num_next = page_num + 1
        page_num_previous = page_num - 1

        # 当前页内容
        pages= paginator.page(page_num)
        # 总页码
        pages_all = pages.paginator.num_pages
        # 下一页内容
        if page_num_next > pages_all:
            pages_next = ''
        else:
            pages_next = paginator.page(page_num_next)
        # 上一页内容
        if page_num_previous:
            pages_previous = paginator.page(page_num_previous)
        else:
            pages_previous = ''
        return render(request, 'info.html', {'pages':pages,
                                             'pages_next':pages_next,
                                             'pages_previous':pages_previous})





