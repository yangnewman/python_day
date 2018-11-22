from urllib import request

from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render
from names.models import HundredNameInfo, NamesInfo
# Create your views here.
from rest_framework import mixins, viewsets
from names.serializers import NamesSerializer, HundredsSerializer


class HundredsView(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  mixins.DestroyModelMixin,
                  viewsets.GenericViewSet):

    # 返回数据
    queryset = HundredNameInfo.objects.all()
    # 序列化结果
    serializer_class = HundredsSerializer


def index(request):
    if request.method == 'GET':
        return render(request, 'index.html')


def name_list(request, name):

    if request.method == 'GET':
        page_number = int(request.GET.get('page', 1))
        # 使用切片 实现功能
        # users = Users.objects.all()[2*(page_number-1):2*page_number]
        # page_num = page.paginator.page_number
        names = NamesInfo.objects.filter(name__startswith=str(name))
        # 使用paginator进行分页
        paginator = Paginator(names, 200)
        # 获取所在页的所有对象
        pages = paginator.page(page_number)
        # 获取页码列表
        page_range = pages.paginator.page_range


        return render(request, 'name_page.html', {'pages':pages})


def detail(request, name):
    if request.method == 'GET':
        name_info = NamesInfo.objects.filter(name=str(name)).first()
        if name_info:

            analysis = name_info.name_analysis

            list3 = []
            list1 = analysis.split('),')
            for item in list1:
                if item[0] == ' ':
                    item = item[1:]
                if item[-1] != ')':
                    item += ')'
                list3.append(item)
        else:
            list3 = []
        return render(request, 'detail.html', {'name_info': name_info, 'analysis_list': list3})


def search(request, name):

    if request.method == 'GET':
        page_number = int(request.GET.get('page', 1))
        # 使用切片 实现功能
        # users = Users.objects.all()[2*(page_number-1):2*page_number]
        # page_num = page.paginator.page_number
        names = NamesInfo.objects.filter(name__contains=str(name))
        # 使用paginator进行分页
        paginator = Paginator(names, 200)
        # 获取所在页的所有对象
        pages = paginator.page(page_number)
        # 获取页码列表
        page_range = pages.paginator.page_range

        return render(request, 'search_page.html', {'pages':pages})






