from django.conf.urls import url

from editor import views

urlpatterns = [
    url(r'^$', views.editor, name='editor_index'),
    url(r'^articles/$', views.show_writer_articles_list, name='show_writer_articles_list'),
    url(r'^articles/(?P<article_id>\d+)/$', views.show_writer_article, name='show_writer_article'),
    url(r'^articles/(?P<article_id>\d+)/edit/$', views.edit_writer_article, name='edit_writer_article'),
    url(r'^articles/(?P<article_id>\d+)/like/$', views.like_article, name='like_article'),
    url(r'^articles/add/$', views.add_writer_article, name='add_writer_article'),
    url(r'^articles/ad/preview/(?P<article_id>\d+)/$', views.ad_placement_preview, name='ad_preview'),
    url(r'^account/show/$', views.show_account, name='show_account'),
    url(r'^account/upload/$', views.upload_file, name='upload_file'),
    url(r'^source/dispatch/$', views.dispatch_ad_source, name='dispatch_ad_source'),
    url(r'^source/lib/$', views.pick_articles_from_lib, name='pick_articles_from_lib'),
    url(r'^external/categories/load/$', views.load_categories_from_lib, name='load_categories_from_lib'),

]
