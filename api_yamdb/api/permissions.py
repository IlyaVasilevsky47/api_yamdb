from http import HTTPStatus

from rest_framework import permissions


class Admin_ReadOnly_Permission(permissions.BasePermission):
    """
    Или пользователь является админом,
    или можно только посмотреть
    """
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return (
                request.user.is_admin
                or request.method in permissions.SAFE_METHODS
            )
        return request.method in permissions.SAFE_METHODS


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
        if request.user.is_authenticated:
            return (
                obj.author == request.user
                or request.user.is_admin
                or request.user.is_moderator
                or request.method in permissions.SAFE_METHODS
            )
        return request.method in permissions.SAFE_METHODS


class Admin_Auth_Permission(permissions.BasePermission):
    """Доступ к контенту только админу или аутентифицированным"""
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and request.user.is_admin
        )


class PUT_username_not_allowed(permissions.BasePermission):
    """
    PUT-запрос к `/api/v1/users/{username}/`
    не предусмотрен и возвращает статус 405.
    """
    def has_object_permission(self, request, view, obj):
        if request.method == 'PUT':
            return HTTPStatus.METHOD_NOT_ALLOWED
        # return super().has_object_permission(request, view, obj)
