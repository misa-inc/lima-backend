from django.contrib import admin

from .models import Trivia, Comment, Vote


class VoteAdmin(admin.ModelAdmin):
    list_display = ('voter', 'value', 'trivia', 'comment')

admin.site.register(Trivia)
admin.site.register(Comment)
admin.site.register(Vote, VoteAdmin)
