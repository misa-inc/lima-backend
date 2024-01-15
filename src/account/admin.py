from django.contrib import admin

from .models import User

# Register your models here.


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "phone", 
        "full_name", "is_staff",
        "author", "is_special_user",
        'sex', 'otp',
        'avatar', 'active',
        'is_verified', 'is_active',
        'is_staff', 'is_admin',
        'is_banned', 'slug',
        'tos', 'created_at'
    )
    list_filter = (
        "is_staff", "is_superuser", 
        "groups", 'active',
        'is_verified', 'is_active',
        'is_staff', 'is_admin',
        'is_banned', 'tos',
        'is_deleted'
    )
    search_fields = (
         "full_name", 
        "phone", 'username', 'email'
    )
    ordering = (
        "-is_superuser", "-is_staff", 
        "-pk",
    )
    list_per_page = 25


