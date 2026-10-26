from rest_framework import permissions


class IsCreatorOrReadOnly(permissions.BasePermission):
    """Anyone authenticated can read; only the creator can edit or delete."""

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.created_by == request.user