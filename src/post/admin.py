from django.contrib import admin

from .models import Post, Comment, Vote, Answer


class VoteAdmin(admin.ModelAdmin):
    list_display = ('voter', 'value', 'post', 'comment')

admin.site.register(Post)
admin.site.register(Answer)
admin.site.register(Comment)
admin.site.register(Vote, VoteAdmin)
