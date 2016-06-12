from os import walk
from utils.shortcuts import render_to
from .forms import ArticleForm, UploadFileForm
from .models import Articles, Users
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django_wysiwyg import clean_html


# Helpers
def _get_paragraph_count(article):
    return len(article.split('\r\n\r\n'))

def _logged_in(request):
    if request.user.username:
        return 1
    return 0

@render_to('editor.html')                                                
@login_required
def editor(request):
    writer_articles_list = Articles.objects.all()
    paginator = Paginator(writer_articles_list, 25)

    page = request.GET.get('page')
    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        articles = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        articles = paginator.page(paginator.num_pages)

    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article_title = form.cleaned_data['title']
            article_content = form.cleaned_data['content']
            user, created = Users.objects.get_or_create(
                username = request.user.username,
            )

            # If user updates article
            try:
                article = Articles.objects.get(
                    author = user,
                    title = article_title
                )
                article.content = article_content
                # Parse article paragraph count
                article.num_para = _get_paragraph_count(article_content) 
                article.save()
            except Articles.DoesNotExist:
                Articles.objects.get_or_create(
                    author = user,
                    title = article_title,
                    content = article_content,
                    num_para = _get_paragraph_count(article_content) 
                )

            writer_articles_list = Articles.objects.all()
            paginator = Paginator(writer_articles_list, 25)

            page = request.GET.get('page')
            try:
                articles = paginator.page(page)
            except PageNotAnInteger:
                # If page is not an integer, deliver first page.
                articles = paginator.page(1)
            except EmptyPage:
                # If page is out of range (e.g. 9999), deliver last page of results.
                articles = paginator.page(paginator.num_pages)

            return {
                'form': form,
                'article_content': clean_html(article_content),
                'article_title': clean_html(article_title),
                'articles_list': articles,
                'logged_in': _logged_in(request)
            }
    else:
        form = ArticleForm()

    return {
        'form': form,
        'articles_list': articles ,
        'logged_in': _logged_in(request)
    }

@render_to('show_writer_articles.html')                                                
@login_required
def show_writer_articles_list(request):
    writer_articles_list = Articles.objects.all()
    paginator = Paginator(writer_articles_list, 25)

    page = request.GET.get('page')
    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        articles = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        articles = paginator.page(paginator.num_pages)

    user = Users.objects.get(username=request.user.username)

    return {
        'articles_list': articles,
        'logged_in': _logged_in(request),
        'user': user
    }

@render_to('editor.html')                                                
@login_required
def edit_writer_article(request, article_id):
    try:
        writer_article = Articles.objects.get(id=article_id)
        form = ArticleForm(
            instance = writer_article
        )
    except Articles.DoesNotExist:
        form = ArticleForm()

    return {
        'form': form,
        'logged_in': _logged_in(request)
    }

@render_to('editor.html')                                                
@login_required
def add_writer_article(request):
    form = ArticleForm()
    return {
        'form': form,
        'logged_in': _logged_in(request)
    }

@render_to('show_writer_article.html')                                                
@login_required
def show_writer_article(request, article_id):
    try:
        writer_article = Articles.objects.get(id=article_id)
        writer_article.num_read += 1
        writer_article.save()

        user = Users.objects.get(username=request.user.username)
        files_uploaded = []
        for (_, _, filenames) in walk('static/uploads/%s' % user.username):
            files_uploaded.extend(filenames)
            break

        return {
            'article_exists': 1,
            'article_content': writer_article.content,
            'article_title': writer_article.title,
            'article_id': article_id,
            'article_like': writer_article.num_like,
            'article_read': writer_article.num_read,
            'article_para': writer_article.num_para,
            'logged_in': _logged_in(request),
            'files_uploaded': files_uploaded,
            'user': user,
            'has_uploads': len(files_uploaded)
        }
    except Articles.DoesNotExist:
        form = ArticleForm()
        return {
            'article_exists': 0,
            'form': form,
            'logged_in': _logged_in(request)
        }

@login_required
@render_to('show_user.html')                                                
def show_account(request):
    try:
        user = Users.objects.get(username=request.user.username)
        files_uploaded = []
        for (_, _, filenames) in walk('static/uploads/%s' % user.username):
            files_uploaded.extend(filenames)
            break
    except:
        print 'no user yet!'

    return {
        'user': user,
        'files_uploaded': files_uploaded,
        'has_uploads': len(files_uploaded)
    }

@login_required
@render_to('file_upload.html')                                                
def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return {
                'uploaded': 1,
                'form': form,
                'user': request.user.username
            }
    else:
        form = UploadFileForm()
    return {
        'uploaded': 0,
        'form': form ,
        'user': request.user.username
    }

def like_article(request, article_id):
    writer_article = Articles.objects.get(id=article_id)
    writer_article.num_like += 1
    writer_article.save()
    return HttpResponse(writer_article.num_like, content_type="text/plain")
