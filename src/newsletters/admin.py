from django.contrib import admin

from .models import Newsletter, Article

admin.site.register(Newsletter)
admin.site.register(Article)