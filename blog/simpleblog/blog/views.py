from django.shortcuts import render
from .models import Article


def home(request):
    return render(request, 'blog/index.html')


def tools(request):
    articles = Article.objects.order_by('-date')
    return render(request, 'blog/tools.html', {'articles': articles})
