from django.db import models
from account.models import User 
from taggit.managers import TaggableManager


def library_to(instance, filename):
    return "libraries/{0}/{1}".format(instance.name, filename)


def author_to(instance, filename):
    return "authors/{0}/{1}".format(instance.name, filename)


class Author(models.Model):
   name        = models.CharField('Name', max_length=300)
   photo       = models.ImageField(upload_to=author_to, blank=True, null=True)
   country     = models.CharField('Country', max_length=50, null=True)
   birth_date  = models.DateField('Birth date', null=True, blank=True)
   death_date  = models.DateField('Death date', null=True, blank=True)
   descreption = models.TextField('Descreption', null=True, blank=True)

   def __str__(self):
       return self.name


class Category(models.Model):
   name = models.CharField('name', max_length=50, unique=True, blank=False)

   def __str__(self):
       return self.name


class Book(models.Model):
   name        = models.CharField('Name', max_length=150, null=False, blank=False)
   file       = models.FileField(upload_to=library_to, blank=True, null=True)
   language    = models.CharField('Language', max_length=50, blank=True, null=True)
   status    = models.CharField('Status', max_length=50, blank=True, null=True)
   pages       = models.IntegerField('Pages')
   descreption = models.TextField('Descreption', null=True, blank=True)
   added_date  = models.DateField(auto_now_add=True)
   category    = models.ForeignKey('Category', on_delete=models.CASCADE)
   author      = models.ForeignKey('Author', on_delete=models.CASCADE)

   tags = TaggableManager()

   def __str__(self):
       return self.name

class Comment(models.Model):
    book      = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='comments')
    user      = models.ForeignKey(User, on_delete=models.CASCADE, null=True) 
    rating    = models.CharField('Rating', max_length=50, blank=True, null=True)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return 'Comment {} by {}'.format(self.body, self.user)