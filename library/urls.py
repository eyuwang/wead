from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='libraryhome'),
    url(r'photo/list/$', views.listphoto, name='listphoto'),
    url(r'photo/add/$', views.addphoto, name='addphoto'),
    url(r'photo/edit/(?P<pid>[0-9]+)/$', views.editphoto, name='editphoto'),
    url(r'photo/delete/(?P<pid>[0-9]+)/$', views.deletephoto, name='deletephoto'),
    url(r'photo/show/(?P<pid>[0-9]+)/$', views.showphoto, name='showphoto'),
    url(r'photo/addm/$', views.addphotos, name='addphotos'),
    url(r'audio/list/$', views.listphoto, name='listaudio'),
    url(r'audio/add/$', views.addphoto, name='addaudio'),
    url(r'audio/edit/(?P<pid>[0-9]+)/$', views.editphoto, name='editaudio'),
    url(r'audio/delete/(?P<pid>[0-9]+)/$', views.deletephoto, name='deleteaudio'),
    url(r'audio/show/(?P<pid>[0-9]+)/$', views.showphoto, name='showaudio'),
    url(r'audio/addm/$', views.addaudios, name='addaudios'),
]