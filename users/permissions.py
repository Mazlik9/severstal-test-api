from rest_framework.permissions import BasePermission


class IsAuthenticatedUserSelf(BasePermission):
    """
    Переопределенные permissions для user-self эндпоинтов.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)
