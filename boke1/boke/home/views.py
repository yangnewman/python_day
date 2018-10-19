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
        return render(request, 'info.html', {'articles':articles})






