from django.contrib import admin
from .models import Notification


class NotificationAdmin(admin.ModelAdmin):

    list_display = (
        'from_user',
        'to_user',
        'notification_type',
        'created'
    )


admin.site.register(Notification, NotificationAdmin)
