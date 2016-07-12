# -*- coding: utf-8 -*
import json
import collections
import random

from os import walk
from utils.shortcuts import render_to
from utils.JSONResponse import JsonResponse
from .forms import ArticleForm, UploadFileForm
from .models import Articles, Users, ArticleEdited
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import redirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.safestring import mark_safe
from django_wysiwyg import clean_html
from content.models import Category, Article


# Helpers
def _get_paragraph_count(article):
    return len(article.split('\r\n\r\n'))

def _logged_in(request):
    if request.user.username:
        return 1
    return 0

def _truncate_words(text, num_words):
    text_truncated = ""
    for idx, word in enumerate(text):
        if idx <= num_words:
            text_truncated += word
        else:
            text_truncated += '...'
            break
    return text_truncated

def _get_logo_size():
    return 'style="width:280px;height:176px;"'

def _center_logo():
    return 'class="img-responsive center-block"'

@render_to('test.html')
def test(request):
    return {
    }


@render_to('home.html')
def home(request):
    return {
        'logged_in': _logged_in(request)
    }


@render_to('editor.html')
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

@render_to('show_subscriber_benefits.html')
def show_subscriber_benefits(request):
    return {
        'logged_in': _logged_in(request)
    }

@render_to('show_member_benefits.html')
def show_member_benefits(request):
    return {
        'logged_in': _logged_in(request)
    }

@render_to('show_writer_articles.html')
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

@render_to('show_user.html')
@login_required
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

@render_to('show_source.html')
def dispatch_ad_source(request):
    return {
    }


@render_to('file_upload.html')
@login_required
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

@render_to('ad_preview.html')
def ad_placement_preview(request, article_id):
    if request.method == 'POST':
        article = Articles.objects.get(id=article_id)
        content = article.content
        num_para = article.num_para
        content_builder = ""
        ad_placement_positions = json.loads(request.body)
        ad_placement_processed = []
        para_index = 0 # begining of article

        for para in content.split('\r\n\r\n'):
            para_processed = False

            # process head
            if para_index == 0:
                for logo in ad_placement_positions:
                    logo_filename, position, place_at_para = logo
                    if position and int(position) == 1:
                        if not para_processed:
                            content_builder += '%s %s' % ('<img src="/static/uploads/%s/%s" %s %s/>' % (
                                                    request.user.username,
                                                    logo_filename,
                                                    _center_logo(),
                                                    _get_logo_size()
                                                 ),
                                                 para)
                            para_processed = True
                        else:
                            content_builder += '<img src="/static/uploads/%s/%s" %s %s/>' % (
                                                request.user.username,
                                                logo_filename,
                                                _center_logo(),
                                                _get_logo_size()
                                            )
                        ad_placement_processed.append(logo)
                    if para_index + 1 == int(place_at_para):
                        if not para_processed:
                            content_builder += '%s %s' % (
                                            para,
                                            '<img src="/static/uploads/%s/%s" %s %s/>' % (
                                                request.user.username,
                                                logo_filename,
                                                _center_logo(),
                                                _get_logo_size()
                                            ))
                            para_processed = True
                        else:
                            content_builder += '<img src="/static/uploads/%s/%s" %s %s/>' % (
                                            request.user.username,
                                            logo_filename,
                                            _center_logo(),
                                            _get_logo_size()
                                        )
                        ad_placement_processed.append(logo)
                if not para_processed:
                    content_builder += para
                    para_processed = True

            # process body
            else:
                for logo in ad_placement_positions:
                    logo_filename, position, place_at_para = logo
                    if position and int(position) == 2:
                        if para_index + 1 == int(place_at_para):
                            if not para_processed:
                                content_builder += '%s %s' % (
                                                para,
                                                '<img src="/static/uploads/%s/%s" %s %s/>' % (
                                                    request.user.username,
                                                    logo_filename,
                                                    _center_logo(),
                                                    _get_logo_size()
                                                ))
                                para_processed = True
                            else:
                                content_builder += '<img src="/static/uploads/%s/%s" %s %s/>' % (
                                                    request.user.username,
                                                    logo_filename,
                                                    _center_logo(),
                                                    _get_logo_size()
                                                )
                            ad_placement_processed.append(logo)
                if not para_processed:
                    content_builder += para
                    para_processed = True

            # process end
            if para_index + 1 == num_para:
                for logo in ad_placement_positions:
                    logo_filename, position, place_at_para = logo
                    if position and int(position) == 3:
                        content_builder += '<img src="/static/uploads/%s/%s" %s %s/>' % (
                                            request.user.username,
                                            logo_filename,
                                            _center_logo(),
                                            _get_logo_size()
                                         )
                if not para_processed:
                    content_builder += para
                    para_processed = True


            para_index += 1

    return {
        'article_logo_placed': mark_safe(content_builder),
        'article_title': article.title
    }

def like_article(request, article_id):
    writer_article = Articles.objects.get(id=article_id)
    writer_article.num_like += 1
    writer_article.save()
    return HttpResponse(writer_article.num_like, content_type="text/plain")

def like_lib_article(request, article_id):
    lib_article = Article.objects.get(id=article_id)
    lib_article.num_like += 1
    lib_article.save()
    return HttpResponse(lib_article.num_like, content_type="text/plain")

def like_edited_article(request, article_id):
    edited_article = ArticleEdited.objects.get(id=article_id)
    edited_article.num_like += 1
    edited_article.save()
    return HttpResponse(edited_article.num_like, content_type="text/plain")

@render_to('pick_from_lib.html')
def pick_articles_from_lib(request):
    return {}

@render_to('lib_ad_preview.html')
@login_required
def lib_ad_placement_preview(request, article_id):
    article = Article.objects.get(id=article_id)
    files_uploaded = []
    for (_, _, filenames) in walk('static/uploads/%s' % request.user.username):
        files_uploaded.extend(filenames)
        break


    return {
        'lib_article': article,
        'files_uploaded': files_uploaded
    }

def load_articles_from_category(request):
    import sys
    reload(sys)
    sys.setdefaultencoding("utf-8")

    category = request.GET['category']
    articles = Article.objects.filter(category__name=category)
    html = """
        <script>
            $('#suggest_more').click(function() {
              $.ajax({
                    url: '/external/category/suggest/',
                    type: "GET",
                    data: {"category": "%s"},
                    dateType: "json",
                    contentType: "application/json; charset=UTF-8",
                    beforeSend: function(xhr, request) {
                        $('#articles_suggested').replaceWith('<span id="articles_suggested"><p class="bg-primary">Loading...</p></span>');
                    },
                    success: function(xdata, status, response){
                        $('#articles_suggested').replaceWith('<span id="articles_suggested" class="center">' + xdata + '</span>');
                    },
                    complete: function(response) {
                    }
                });
            });
        </script>
    """ % category

    if articles:
        if len(articles) > 16:
            suggested = random.sample(articles, 16)
        else:
            suggested = articles

        html += """
            <div class="container">
                <button id="suggest_more" type="button" class="btn btn-sm btn-success pull-right">没有中意的，换一批文章</button>
                <div class="col-md-15">
                    <table class="table table-striped">
                    <thead>
                      <tr>
                        <th>标题
                            <span class="glyphicon glyphicon-list-alt" aria-hidden="true"></span>
                        </th>
                        <th>作者
                            <span class="glyphicon glyphicon-user" aria-hidden="true"></span>
                        </th>
                        <th>类别
                            <span class="glyphicon glyphicon-list" aria-hidden="true"></span>
                        </th>
                      </tr>
                    </thead>
                    <tbody>"""
        for article in suggested:
            html += """
                      <tr>
                        <td>
                            <a href="/source/lib/preview/%s/">%s</a>
                        </td>
                        <td>
                            %s
                        </td>
                        <td>
                            %s
                        </td>
                      </tr>""" % (article.id, article.title, article.author, article.category)
        html += """
                    </tbody>
                  </table>
              </div>
            </div>
        """

    response = HttpResponse(html, content_type="text/html")
    response['Content-Length'] = len(response.content)
    response['Cache-Control'] ='no-cache, no-store'
    return response

def load_sample_articles_from_lib(category_name):
    """
    Load 3 sample articles from lib
    """
    import sys
    reload(sys)
    sys.setdefaultencoding("utf-8")

    html = ''
    articles = Article.objects.filter(category__name=category_name)
    if articles:
        if len(articles) > 3:
            suggested = random.sample(articles, 3)
        else:
            suggested = articles

        html += """<ul class="list-unstyled">"""
        for article in suggested:
            html += """
                      <li>
                          <a href="/source/lib/articles/show/%s/">%s</a>
                      </li>""" % (article.id, _truncate_words(article.title, 6))
        html += """   <li class="pull-left"> &gt;&gt;
                          <a href="/source/lib/preview/2/">进入频道</a>
                      </li>
                   </ul>"""

    return html

def load_hot_articles_from_lib(request):
    """
    Load hot articles
    """
    import sys
    reload(sys)
    sys.setdefaultencoding("utf-8")

    top_n = []
    top_n_lib = []
    top_n_writer = []

    index = 0
    lib_articles = Article.objects.order_by('-num_read')[:13]
    for lib_article in lib_articles:
        # URI, title, num_read
        top_n_lib.append(['/source/lib/articles/show/%s/' % lib_article.id,
                            _truncate_words(lib_article.title, 10), lib_article.num_read])
        index += 1

    index = 0
    writer_articles = Articles.objects.order_by('-num_read')[:13]
    for writer_article in writer_articles:
        # URI, title, num_read
        top_n_writer.append(['/editor/articles/%s/' % writer_article.id,
                            _truncate_words(writer_article.title, 10), writer_article.num_read])
        index += 1

    index = 1
    html = '<ol id="hot_articles" class="list-unstyled"><h6 class="bg-primary">文库文章</h6>'
    for article in top_n_lib:
        if index <= 3:
            num_class = 'number_circle_%s' % index
        else:
            num_class = 'number_circle_regular'
        if index < 10:
            idx = '0%s' % index
        else:
            idx = index

        html += """
                  <li>
                      <span class="%s">%s</span>
                      <a href="%s">%s</a>
                      <span class="badge">%s</span>
                  </li>""" % (num_class, idx, article[0], article[1], article[2])
        index += 1
    html += "</ol>"

    index = 1
    html += '<ol id="hot_articles" class="list-unstyled"><h6 class="bg-primary">写手文章</h6>'
    for article in top_n_writer:
        if index <= 3:
            num_class = 'number_circle_%s' % index
        else:
            num_class = 'number_circle_regular'
        if index < 10:
            idx = '0%s' % index
        else:
            idx = index


        html += """
                  <li>
                      <span class="%s">%s</span>
                      <a href="%s">%s</a>
                      <span class="badge">%s</span>
                  </li>""" % (num_class, idx, article[0], article[1], article[2])
        index += 1
    html += "</ol>"

    response = HttpResponse(html, content_type="text/html")
    response['Content-Length'] = len(response.content)
    response['Cache-Control'] ='no-cache, no-store'
    return response

def load_hot_users(request):
    """
    Load some hot users
    """
    import sys
    reload(sys)
    sys.setdefaultencoding("utf-8")

    #FIXME: add hotness to users
    users = Users.objects.all()
    html = '<ol id="hot_users" class="list-unstyled">'
    for user in users:
        html += """
                  <li>
                      <img width="23" height="23" src="/static/media/images/icons/User.png" />
                      <a href="#">%s</a>
                  </li>""" % (user.username)
    html += "</ol>"
    response = HttpResponse(html, content_type="text/html")
    response['Content-Length'] = len(response.content)
    response['Cache-Control'] ='no-cache, no-store'
    return response

def load_categories_from_lib(request):
    """
    Load in categories
    """
    import sys
    reload(sys)
    sys.setdefaultencoding("utf-8")

    fang = '生活面面观'
    wen = '一览众山小'
    sheng = '世界掌中看'
    qi = '其它'

    content = collections.OrderedDict([
        (fang, []),
        (wen, []),
        (sheng, []),
        (qi, [])
    ])
    categories = Category.objects.all()
    for category in categories:
        if category.parent:
            if category.parent.name == fang:
                content[fang].append(category)
            elif category.parent.name == wen:
                content[wen].append(category)
            elif category.parent.name == sheng:
                content[sheng].append(category)
            else:
                content[qi].append(category)
        else:
            content[qi].append(category)

    html = """
            <script>
                $('img.cate-icon').on('click', function() {
                  var category = this.id
                  $.ajax({
                        url: '/external/category/suggest/',
                        type: "GET",
                        data: {"category": category},
                        dateType: "json",
                        contentType: "application/json; charset=UTF-8",
                        beforeSend: function(xhr, request) {
                            $('#articles_suggested').replaceWith('<span id="articles_suggested">Loading...</span>');
                        },
                        success: function(xdata, status, response){
                            $('#articles_suggested').replaceWith('<span id="articles_suggested" class="center">' + xdata + '</span>');
                        },
                        complete: function(response) {
                        }
                    });
                });
            </script>
    """
    for category, category_objs in content.iteritems():
        index = 0
        html += "<h2 class='bg-primary'>%s</h2>" % category
        html += "<table class='table'>"
        for obj in category_objs:
            # 4 categories per row
            _, remainder = divmod(index, 4)
            if remainder == 0:
                # start a new row
                html += """
                    <tr>
                        <td width="25%%">
                          <img id="%(category)s" class="img-circle cate-icon" width="75" height="75" src="/static/media/images/icons/%(category)s.png" alt="文库种类" />

                          <div class="caption">
                             <span>%(sample)s</span>
                          </div>
                        </td>
                """ % {
                'category': obj.name,
                'sample': load_sample_articles_from_lib(obj.name)
                }
            elif remainder == 3:
                # ends a row
                html += """
                        <td width="25%%">
                          <img id="%(category)s" class="img-circle cate-icon" width="75" height="75" src="/static/media/images/icons/%(category)s.png" alt="文库种类" />

                          <div class="caption">
                             <span>%(sample)s</span>
                          </div>
                        </td>
                    </tr>
                """ % {
                'category': obj.name,
                'sample': load_sample_articles_from_lib(obj.name)
                }
            else:
                # in the same row
                html += """
                        <td width="25%%">
                          <img id="%(category)s" class="img-circle cate-icon" width="75" height="75" src="/static/media/images/icons/%(category)s.png" alt="文库种类" />

                          <div class="caption">
                             <span>%(sample)s</span>
                          </div>
                        </td>
                """ % {
                'category': obj.name,
                'sample': load_sample_articles_from_lib(obj.name)
                }
            index += 1

        # padding the empty spots
        if index == 1:
            for i in range(3):
                html += """
                    <td width="25%%"></td>
                """
            html += "</tr>"
        elif index == 2:
            for i in range(2):
                html += """
                    <td width="25%%"></td>
                """
            html += "</tr>"
        elif index == 3:
            html += """
               <td width="25%%"></td>
             </tr>
            """
        html += "</table>"

    html += "<a href='#' class='pull-right'>更多类别...</a>"
    response = HttpResponse(html, content_type="text/html")
    response['Content-Length'] = len(response.content)
    response['Cache-Control'] ='no-cache, no-store'
    return response

def lib_ad_placement_preview_refresh(request, template_id, logo_filename):
    """
    Insert logo to template chosen
    """
    html = ""
    if request.method == 'POST':
        body = json.loads(request.body)
        if int(template_id) == 1:
            # head
            html += '<img src="/static/uploads/%s/%s" %s %s/>' % (
                        request.user.username,
                        logo_filename,
                        _center_logo(),
                        _get_logo_size()
                    )
            html += """
                <h4 id="article_title" class="text-center">%s</h4>
                <div id="article_body" class="container">%s</div>
            """ % (body['article_title'], body['article_body'])
        elif int(template_id) == 2:
            # bottom
            html += """
                <h4 id="article_title" class="text-center">%s</h4>
                <div id="article_body" class="container">%s</div>
            """ % (body['article_title'], body['article_body'])
            html += '<img src="/static/uploads/%s/%s" %s %s/>' % (
                        request.user.username,
                        logo_filename,
                        _center_logo(),
                        _get_logo_size()
                    )
        elif int(template_id) == 3:
            # wrap text around image
            html = """
              <img src="/static/uploads/%s/%s" %s class="pull-left gap-right"/>
              <h4 id="article_title" class="text-center">%s</h4>
              <div id="article_body" class="container">%s</div>
            """ % (
                request.user.username,
                logo_filename,
                _get_logo_size(),
                body['article_title'],
                body['article_body']
            )
        elif int(template_id) == 4:
            # wrap text around image
            html = """
              <img src="/static/uploads/%s/%s" %s class="pull-right gap-right"/>
              <h4 id="article_title" class="text-center">%s</h4>
              <div id="article_body" class="container">%s</div>
            """ % (
                request.user.username,
                logo_filename,
                _get_logo_size(),
                body['article_title'],
                body['article_body']
            )

    response = HttpResponse(html, content_type="text/html")
    response['Content-Length'] = len(response.content)
    response['Cache-Control'] ='no-cache, no-store'
    return response

@render_to('show_lib_article.html')
def lib_show_article(request, article_id):
    """
    Show lib article content
    """
    try:
        lib_article = Article.objects.get(id=article_id)
        lib_article.num_read += 1
        lib_article.save()

        return {
            'article_content': lib_article.content,
            'article_title': lib_article.title,
            'article_author': lib_article.author,
            'article_id': article_id,
            'article_like': lib_article.num_like,
            'article_read': lib_article.num_read,
            'article_para': lib_article.num_para,
        }
    except Article.DoesNotExist:
        # 404
        return redirect('not_found', permanent=True)

def handler404(request):
    response = render_to_response('404.html', {},
                   context_instance=RequestContext(request))
    response.status_code = 404
    return response

@render_to('publish_article.html')
def show_published_article(request, article_id):
    try:
        article = ArticleEdited.objects.get(id=article_id)
        article.num_read += 1
        article.save()

        return {
            'edited_article': mark_safe(article.content),
            'article_read': article.num_read,
            'article_like': article.num_like,
            'article_id': article_id,
            'title': article.title,
            'ad_logo_num': random.choice(range(2)),
            'is_lib_article': article.is_lib_article
        }
    except ArticleEdited.DoesNotExist:
        return redirect('not_found', permanent=True)

def publish_edited_article(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        article = ArticleEdited(content=body['html'])
        article.title = body['article_title']
        article.is_lib_article = int(body['is_lib_article'])
        article.save()

        url = reverse('show_published_article', args=[article.id])
        return HttpResponse(url, content_type="text/plain")
