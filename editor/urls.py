from django.conf.urls import url

from editor import views

urlpatterns = [
    url(r'^$', views.editor, name='editor_index'),
    url(r'^articles/$', views.show_writer_articles_list, name='show_writer_articles_list'),
    url(r'^articles/(?P<article_id>\d+)/$', views.show_writer_article, name='show_writer_article'),
    url(r'^articles/(?P<article_id>\d+)/edit/$', views.edit_writer_article, name='edit_writer_article'),
    url(r'^articles/(?P<article_id>\d+)/like/$', views.like_article, name='like_article'),
    url(r'^articles/add/$', views.add_writer_article, name='add_writer_article'),
    url(r'^account/show/$', views.show_account, name='show_account'),
    url(r'^account/upload/$', views.upload_file, name='upload_file'),
]
