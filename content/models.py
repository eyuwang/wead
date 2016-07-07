from __future__ import unicode_literals

from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=200, default="")
    code = models.IntegerField(null=True, blank=True)
    parent = models.ForeignKey("Category", null=True, blank=True)
    added = models.DateTimeField('date added',null=True,auto_now_add=True)

    def __str__(self):
        return self.name.encode('utf-8').strip()

class Article(models.Model):
    category = models.ForeignKey(Category)
    title = models.CharField(max_length=120)
    author = models.CharField(max_length=30)
    content = models.TextField('Content')
    added = models.DateTimeField('date added',null=True,auto_now_add=True)
    num_like = models.IntegerField(null=True, default=0)
    num_read = models.IntegerField(null=True, default=0)
    num_frwd = models.IntegerField(null=True, default=0)
    num_para = models.IntegerField(null=True, default=0)

    def __str__(self):
        return '%s: %s' % (self.author.encode('utf-8').strip(),
                           self.title.encode('utf-8').strip())

