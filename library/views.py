from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from django.conf import settings
from .models import Library, Photo, Audio
from .forms import PhotoForm, PhotosForm
from jtool.tools import get_libchain, get_libraries

import os
import time

@login_required
def index(request):
    context = {
        'plibraries': get_libraries('photo'),
        'alibraries': get_libraries('audio'),
        'photos': Photo.objects.all(),
        'audios': Audio.objects.all(),
    }
    return render(request, "index_library.html", context=context)

@login_required
def listphoto(request):
    context = {
        'entries': Photo.objects.all()
    }
    return render(request, 'listphoto.html', context=context)
    
@login_required
def addphoto(request):
    libraries = get_libraries('photo')
    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            print('is valid')
            library = form.cleaned_data['library']
            author = form.cleaned_data['author']
            title = form.cleaned_data['title']
            ctime = time.strftime("%Y%m%d%H%M%S")
            file = request.FILES['file']
            fname, fext = os.path.splitext(file.name)
            newname = '%s_0%s' % (ctime, fext)
            with open('%s%s/%s' % (settings.BASE_DIR, settings.MEDIA_ROOT, newname), 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)
            photo = Photo.objects.get_or_create(
                    library = Library.objects.get(id=library),
                    author = author,
                    title = title,
                    oldname = file,
                    newname = newname
                )
            return redirect('/internal/library/photo/list/')
        else:
            return HttpResponse('error during upload')
    else:
        form = PhotoForm()
    context = {
        'libraries': libraries
    }
    return render(request, 'addphoto.html', context=context)
    
@login_required
def editphoto(request,pid):
    photo = Photo.objects.get(id=pid)
    if request.method == 'POST':
        photo.author = request.POST['author']
        photo.title = request.POST['title']
        photo.save()
        return redirect('/internal/library/photo/list/')
    context = {
        'photo': photo
    }
    return render(request, 'editphoto.html', context=context)

@login_required
def deletephoto(request, pid):
    Photo.objects.get(id=pid).delete()
    return redirect('/internal/library/photo/list/')

@login_required
def showphoto(request,pid):
    photo = Photo.objects.get(id=pid)
    context = {
        'entry': photo,
        'libchain': ' -> '.join(get_libchain(photo.library))
    }
    return render(request, 'showphoto.html', context=context)
 
@login_required
def addphotos(request):
    libraries = get_libraries('photo')
    if request.method == 'POST':
        form = PhotosForm(request.POST, request.FILES)
        if form.is_valid():
            library = form.cleaned_data['library']
            ctime = time.strftime("%Y%m%d%H%M%S")
            for count, x in enumerate(request.FILES.getlist('files')):
                def process_file(f):
                    fname, fext = os.path.splitext(f.name)
                    newname = '%s_%s%s' % (ctime, str(count), fext)
                    with open('%s%s/%s' % (settings.BASE_DIR, settings.MEDIA_ROOT, newname), 'wb+') as destination:
                        for chunk in f.chunks():
                            destination.write(chunk)
                    photo = Photo.objects.get_or_create(
                            library = Library.objects.get(id=library),
                            author = 'user',
                            title = f.name,
                            oldname = f,
                            newname = newname
                        )
                process_file(x)
        return redirect('/internal/library/photo/list/')
    else:
        form = PhotosForm()
    context = {
        'libraries': get_libraries('photo')
    }
    return render(request, 'addphotos.html', context=context)

@login_required
def listaudio(request):
    context = {
        'entries': Audio.objects.all()
    }
    return render(request, 'listaudio.html', context=context)
    
@login_required
def addaudio(request):
    libraries = get_libraries('audio')
    if request.method == 'POST':
        form = AudioForm(request.POST, request.FILES)
        if form.is_valid():
            print('is valid')
            library = form.cleaned_data['library']
            author = form.cleaned_data['author']
            title = form.cleaned_data['title']
            ctime = time.strftime("%Y%m%d%H%M%S")
            file = request.FILES['file']
            fname, fext = os.path.splitext(file.name)
            newname = '%s_0%s' % (ctime, fext)
            with open('%s%s/%s' % (settings.BASE_DIR, settings.MEDIA_ROOT, newname), 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)
            audio = Audio.objects.get_or_create(
                    library = Library.objects.get(id=library),
                    author = author,
                    title = title,
                    oldname = file,
                    newname = newname
                )
            return redirect('/internal/library/audio/list/')
        else:
            return HttpResponse('error during upload')
    else:
        form = AudioForm()
    context = {
        'libraries': libraries
    }
    return render(request, 'addaudio.html', context=context)
    
@login_required
def editaudio(request,pid):
    audio = Audio.objects.get(id=pid)
    if request.method == 'POST':
        audio.author = request.POST['author']
        audio.title = request.POST['title']
        audio.save()
        return redirect('/internal/library/audio/list/')
    context = {
        'audio': audio
    }
    return render(request, 'editaudio.html', context=context)

@login_required
def deleteaudio(request, pid):
    Audio.objects.get(id=pid).delete()
    return redirect('/internal/library/audio/list/')

@login_required
def showaudio(request,pid):
    audio = Audio.objects.get(id=pid)
    context = {
        'entry': audio,
        'libchain': ' -> '.join(get_libchain(audio.library))
    }
    return render(request, 'showaudio.html', context=context)
 
@login_required
def addaudios(request):
    libraries = get_libraries('audio')
    if request.method == 'POST':
        form = AudiosForm(request.POST, request.FILES)
        if form.is_valid():
            library = form.cleaned_data['library']
            ctime = time.strftime("%Y%m%d%H%M%S")
            for count, x in enumerate(request.FILES.getlist('files')):
                def process_file(f):
                    fname, fext = os.path.splitext(f.name)
                    newname = '%s_%s%s' % (ctime, str(count), fext)
                    with open('%s/%s' % (settings.MEDIA_ROOT, newname), 'wb+') as destination:
                        for chunk in f.chunks():
                            destination.write(chunk)
                    audio = Audio.objects.get_or_create(
                            library = Library.objects.get(id=library),
                            author = 'user',
                            title = f.name,
                            oldname = f,
                            newname = newname
                        )
                process_file(x)
        return redirect('/internal/library/audio/list/')
    else:
        form = AudiosForm()
    context = {
        'libraries': libraries
    }
    return render(request, 'addaudios.html', context=context)
