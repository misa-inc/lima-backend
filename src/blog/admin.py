from django.contrib import admin

from .models import Blog, Comment

# Register your models here.

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'slug', 
        'author', 'special', 
        'status', 'visits',
    )
    search_fields = (
        'title', 'author__first_name', 
        'category__title',
    )
    list_filter = (
        'status', 'special', 
        'publish',
    )
    exclude = (
        "slug",
    )
    radio_fields = {
        "status": admin.HORIZONTAL
    }
    list_per_page = 25


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'name', 
        'create', 'updated', 
        'body',
    )
    list_filter = (
        "create",
    )
    search_fields = (
        "name", "body",
    )
    list_per_page = 25    