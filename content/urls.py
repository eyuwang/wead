from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='contenthome'),
    url(r'article/list/$', views.listarticle, name='listarticle'),
    url(r'article/add/$', views.addarticle, name='addarticle'),
    url(r'article/edit/(?P<aid>[0-9]+)/$', views.editarticle, name='editarticle'),
    url(r'article/delete/(?P<aid>[0-9]+)/$', views.deletearticle, name='deletearticle'),
    url(r'article/show/(?P<aid>[0-9]+)/$', views.showarticle, name='showarticle'),
    url(r'article/addm/$', views.addarticles, name='addarticles'),
]