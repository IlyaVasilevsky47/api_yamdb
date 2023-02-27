from rest_framework import permissions

from users.models import ReviewUser


class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        return request.method in permissions.SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        if obj.author == request.user:
            return True
        return request.method in permissions.SAFE_METHODS


from rest_framework import permissions

from .models import ReviewUser


class Admin_ReadOnly_Permission(permissions.BasePermission):
    """
    Или пользователь является админом,
    или можно только посмотреть
    """
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_admin
            and request.user.is_authenticated
        )


class All_Permission(permissions.BasePermission):
    """
    Определение прав внесения изменений:
    ReadOnly, Author, Admin, Moderator, Auth
    """
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )
        
    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.user == request.user
            or request.user.is_admin
            or request.user.is_moderator
        )


class Admin_Auth_Permission(permissions.BasePermission):
    """Доступ к контенту только админу или аутентифицированным"""
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and request.user.is_admin
        )