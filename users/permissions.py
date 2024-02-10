from rest_framework.permissions import BasePermission

from users.models import UserRoles


class IsModerator(BasePermission):
    message = 'Вы модератор'

    def has_permission(self, request, view):
        if request.user.role == UserRoles.MODERATOR:
            return False
        return True


class IsUser(BasePermission):
    message = 'Вы не владельцем'

    def has_object_permission(self, request, view, obj):
        if request.user == obj.user:
            return True
        return False