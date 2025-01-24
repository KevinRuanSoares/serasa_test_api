from rest_framework import permissions
from user.choices import SELLER, ADMIN, SUPER_ADMIN


def create_permission_class(permission_type):
    class Permission(permissions.BasePermission):
        def has_permission(self, request, view):
            return request.user.roles.filter(name=permission_type).exists()

        def has_object_permission(self, request, view, obj):
            if request.method in permissions.SAFE_METHODS:
                return True
            return request.user.roles.filter(name=permission_type).exists()
    return Permission


IsSuperAdmin = create_permission_class(SUPER_ADMIN)
IsAdmin = create_permission_class(ADMIN)
IsSeller = create_permission_class(SELLER)
