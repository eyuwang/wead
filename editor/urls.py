from django.conf.urls import url

from editor import views

urlpatterns = [
    #url(r'^$', views.editor, name='editor_index'),
    url(r'^$', views.editor1, name='editor_index'),
    url(r'^articles/$', views.show_writer_articles_list, name='show_writer_articles_list'),
    url(r'^articles/(?P<article_id>\d+)/$', views.show_writer_article, name='show_writer_article'),
    url(r'^articles/(?P<article_id>\d+)/edit/$', views.edit_writer_article, name='edit_writer_article'),
    url(r'^articles/(?P<article_id>\d+)/like/$', views.like_article, name='like_article'),
    url(r'^articles/add/$', views.add_writer_article, name='add_writer_article'),
    url(r'^articles/ad/preview/(?P<article_id>\d+)/$', views.ad_placement_preview, name='ad_preview'),
    url(r'^account/member/$', views.show_member_benefits, name='show_member_benefits'),
    url(r'^account/subscribe/$', views.show_subscriber_benefits, name='show_subscriber_benefits'),
    url(r'^account/show/$', views.show_account, name='show_account'),
    url(r'^account/upload/$', views.upload_file, name='upload_file'),
    url(r'^source/dispatch/$', views.dispatch_ad_source, name='dispatch_ad_source'),
    url(r'^source/lib/$', views.pick_articles_from_lib, name='pick_articles_from_lib'),
    url(r'^source/lib/articles/show/(?P<article_id>\d+)/$', views.lib_show_article, name='show_article_from_lib'),
    url(r'^source/lib/articles/(?P<article_id>\d+)/like/$', views.like_lib_article, name='like_lib_article'),
    url(r'^source/lib/preview/(?P<article_id>\d+)/$', views.lib_ad_placement_preview, name='lib_ad_preview'),
    url(r'^source/lib/preview/refresh/(?P<template_id>\d+)/(?P<logo_filename>.*)/$', views.lib_ad_placement_preview_refresh, name='lib_ad_preview_refresh'),
    url(r'^external/categories/load/$', views.load_categories_from_lib, name='load_categories_from_lib'),
    url(r'^external/category/suggest/$', views.load_articles_from_category, name='load_articles_from_category'),
    url(r'^external/articles/load/hot/$', views.load_hot_articles_from_lib, name='load_hot_articles_from_lib'),
    url(r'^users/load/hot/$', views.load_hot_users, name='load_hot_users'),

    url(r'^404/$', views.handler404, name='not_found'),
]
