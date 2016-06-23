from __future__ import unicode_literals

from django.db import models

class Library(models.Model):
    type = models.CharField(max_length=30)
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=200, default="")
    code = models.IntegerField(null=True, blank=True)
    parent = models.ForeignKey("Library", null=True, blank=True)
    added = models.DateTimeField('date added',null=True,auto_now_add=True)

    def __str__(self):
        return self.name.encode('utf-8').strip()

class Photo(models.Model):
    library = models.ForeignKey(Library)
    title = models.CharField(max_length=120,null=True,blank=True)
    author = models.CharField(max_length=30,null=True,blank=True)
    oldname = models.CharField('Old file name',max_length=30)
    newname = models.CharField('New file name',max_length=30)
    added = models.DateTimeField('date added',null=True,auto_now_add=True)
    
    def __str__(self):
        return '%s: %s' % (self.author.encode('utf-8').strip(), 
                           self.title.encode('utf-8').strip())
                           
class Audio(models.Model):
    library = models.ForeignKey(Library)
    title = models.CharField(max_length=120,null=True,blank=True)
    author = models.CharField(max_length=30,null=True,blank=True)
    oldname = models.CharField('Old file name',max_length=30)
    newname = models.CharField('New file name',max_length=30)
    added = models.DateTimeField('date added',null=True,auto_now_add=True)
    
    def __str__(self):
        return '%s: %s' % (self.author.encode('utf-8').strip(), 
                           self.title.encode('utf-8').strip())
