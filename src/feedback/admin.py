from django.contrib import admin

from .models import Feedback, Comment, Vote


class VoteAdmin(admin.ModelAdmin):
    list_display = ('voter', 'value', 'post', 'comment')

admin.site.register(Feedback)
admin.site.register(Comment)
admin.site.register(Vote, VoteAdmin)
