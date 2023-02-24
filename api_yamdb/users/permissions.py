from rest_framework import permissions
from . models import ReviewUser


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
    Определение прав для:
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


# class User_Admin_Permission(permissions.BasePermission):
#     def has_permission(self, request, view):
#         if request.method in permissions.SAFE_METHODS:
#             return True
        
#         return bool(request.user and request.user.is_staff)

#     def has_object_permission(self, request, view, obj):
#         if request.method in permissions.SAFE_METHODS:
#             return True
#         return obj.user == request.user

# class ModeratorPermission(permissions.BasePermission):
#     """Права модератора"""
#     def has_permission(self, request, view):
#         return (
#             request.method in permissions.SAFE_METHODS
#             or request.user.is_authenticated
#         )
        
#     def has_object_permission(self, request, view, obj):
#         return (
#             request.method in permissions.SAFE_METHODS
#             or request.user.is_moderator
#             and request.user.is_authenticated
#         )
