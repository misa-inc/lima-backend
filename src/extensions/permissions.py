from rest_framework.permissions import BasePermission, SAFE_METHODS
from account.models import User


class IsSuperUser(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)


class IsActiveOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS or
            request.user and
            request.user.is_active
        )


class UserIsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return request.user == User.objects.get(pk=view.kwargs['pk'])


class IsStaffOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS or
            request.user and
            request.user.is_staff
        )


class IsAuthorOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        return obj.author == request.user


class IsSuperUserOrStaffReadOnly(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS and
            request.user and
            request.user.is_staff or
            request.user and
            request.user.is_superuser
        )


class IsSuperSignupOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.method in ('GET', 'HEAD', 'OPTIONS', "POST") or
            request.user and
            request.user.is_superuser
        )


class IsSuperUser(BasePermission):
    message = 'You Must Be SuperUser'

    def has_permission(self, request, view):
        return bool(
            request.user.is_authenticated and request.user.is_superuser
        )


class IsSuperUserOrReadOnly(BasePermission):
    
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        return bool(
            request.user.is_authenticated and request.user.is_superuser
        )


class IsSuperUserOrAuthor(BasePermission):
    message = 'You Must Be SuperUser or Author'

    def has_permission(self, request, view):
        return bool(
            request.user.is_authenticated and request.user.is_superuser or
            request.user.is_authenticated and request.user.author
        )


class IsSuperUserOrAuthorOrReadOnly(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        return bool(
            request.user.is_authenticated and request.user.is_superuser or
            request.user.is_authenticated and obj.author == request.user 
        )


class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.owner == request.user
    

class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            if obj.owner == request.user:
                return True

        elif request.method in ['PUT', 'PATCH']:
            if obj.owner == request.user:
                return True
            elif obj.guests.all():
                for guest in obj.guests.all():
                    if request.user.id == guest.id:
                        return True
            return False