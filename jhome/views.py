from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from content.models import Category, Article
from library.models import Library, Photo
from jtool.tools import get_categories, get_libraries

@login_required
def index(request):
    context = {
        'categories': get_categories(),
        'plibraries': get_libraries('photo'),
        'alibraries': get_libraries('audio'),
        'articles': Article.objects.all(),
        'photos': Photo.objects.all(),
    }
    return render(request, 'index_home.html', context=context)
