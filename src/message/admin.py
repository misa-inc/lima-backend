from django.contrib import admin
from .models import PrivateChat, Message


class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'sender', 'text', 'day', 'month', 'year', 'time')


class PrivateChatAdmin(admin.ModelAdmin):
    list_display = ('id', 'user1', 'user2', 'is_active')


admin.site.register(PrivateChat, PrivateChatAdmin)
admin.site.register(Message, MessageAdmin)