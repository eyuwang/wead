from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from .models import Category, Article
from .forms import ArticleForm, ArticlesForm

from jtool.tools import get_catchain, get_categories

import os
try:
    import simplejson as json
except:
    import json

@login_required
def index(request):
    context = {
        'categories': get_categories(),
        'articles': Article.objects.all()
    }
    return render(request, "index_content.html", context=context)

@login_required
def listarticle(request):
    context = {
        'entries': Article.objects.all()
    }
    return render(request, "listarticle.html", context=context)

@login_required
def addarticle(request):
    err = ''
        
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            category = form.cleaned_data['category']
            author = form.cleaned_data['author']
            title = form.cleaned_data['title']
            body = form.cleaned_data['body']
            article = Article.objects.get_or_create(
                category = Category.objects.get(id=category),
	        author = author,
	        title = title,
	        body = body
	    )
            return redirect('/internal/content/article/list/')
        else:
            return HttpResponse('Error')
    else:
        form = ArticleForm()
    
    context = {
        'form': form,
        'categories': get_categories(),
        'err': err
    }
    return render(request, "addarticle.html", context=context)

@login_required
def editarticle(request, aid):
    err = ''
    article = Article.objects.get(id=aid)
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            author = form.cleaned_data['author']
            title = form.cleaned_data['title']
            body = form.cleaned_data['body']
            article.author = author
            article.title = title
            article.body = body
            article.save()
            return redirect('/internal/content/article/list/')
        else:
            return HttpResponse('Error')
    else:
        form = ArticleForm()
    context = {
        'form': form,
        'article': Article.objects.get(id=aid),
        'err': err
    }
    return render(request, 'editarticle.html', context=context)

@login_required
def showarticle(request, aid):
    article = Article.objects.get(id=aid)
    context = {
        'entry': article,
        'catchain': ' -> '.join(get_catchain(article.category))
    }
    return render(request, 'showarticle.html', context=context)

@login_required
def deletearticle(request, aid):
    Article.objects.get(id=aid).delete()
    return redirect('/internal/content/article/list/')
    
@login_required
def addarticles(request):
    err = ''
    if request.method == 'POST':
        form = ArticlesForm(request.POST)
        if form.is_valid():
            category = form.cleaned_data['category']
            body = form.cleaned_data['body']

            category = Category.objects.get(id=category)

            save_content(category, body)
            
            return redirect('/internal/content/article/list/')
        else:
            return HttpResponse('Error')
    else:
        form = ArticlesForm()
    categories = get_categories()
    context = {
        'form': form,
        'categories': categories,
        'err': err
    }
    return render(request, 'addarticles.html', context=context)

def isInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False
    
def save_chunk(category, chunk, hasNoAuthor):
    if len(chunk)>=3:
	title=chunk[0]
	if hasNoAuthor:
            author=''	    
	    poem='\n'.join(chunk[1:])
	else:
	    author=chunk[1]
	    poem='\n'.join(chunk[2:])

        article = Article.objects.get_or_create(
                category = category,
                author = author,
                title = title,
                body = poem
            )
        return 0
    return -1

def save_content(category, body):
    # 100, 200, 300 - format: title, author, content
    # articles are separated by blank lines
    # 500 - number, title, content

    lines = body.splitlines()

    chunk=[]
    lnum = 0
  
    # decide from the first line whether there is author
    hasNoAuthor = 0
    startLine = 0
    while lnum<len(lines):
        line = lines[lnum].strip()
        if len(line) > 0:
            if isInt(line):
                hasNoAuthor = 1
            break
        else:
            startLine = startLine + 1
    
    lines = lines[startLine:]
    
    if hasNoAuthor:
        while lnum<len(lines):
            line = lines[lnum].strip()
            if len(line)>0:
                if isInt(line):
                    if lnum>0:
                        save_chunk(category, chunk, hasNoAuthor)
                        chunk=[]
                else:
                    chunk.append(line)
            lnum = lnum+1
        save_chunk(category, chunk, hasNoAuthor)
    else:
        while lnum<len(lines):
            line = lines[lnum].strip()
            if len(line)>0:
                chunk.append(line)
            else:
                save_chunk(category, chunk, hasNoAuthor)
                chunk=[]
            lnum = lnum+1
        save_chunk(category, chunk, hasNoAuthor)
