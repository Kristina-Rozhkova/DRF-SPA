from rest_framework import permissions


class IsModer(permissions.BasePermission):
    """
    Проверяет, является ли пользователь модератором
    """
    message = 'Такие операции может производить только модератор.'

    def has_permission(self, request, view):
        return request.user.groups.filter(name='Модератор').exists()


class IsOwner(permissions.BasePermission):
    """
    Проверяет, является ли пользователь владельцем
    """

    def has_object_permission(self, request, view, obj):
        if obj.owner == request.user:
            return True
        return False