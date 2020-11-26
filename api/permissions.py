from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS or
                obj.author_id == request.user.id)


class UserAdministrator(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser or request.user.is_admin


class UserAdministratorOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_admin)


class OwnerAdministratorOrModeratorOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return (request.user.is_admin or request.user.is_moderator
                or obj.author_id == request.user.id)
