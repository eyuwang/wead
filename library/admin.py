from django.contrib import admin

from .models import Library
from .forms import LibraryForm

class LibraryAdmin(admin.ModelAdmin):
    fields = ('type','name','description','code','parent')
    list_display = ('type','name','description','code','parent')
    form = LibraryForm
admin.site.register(Library, LibraryAdmin)

