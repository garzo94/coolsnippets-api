from rest_framework import permissions

class IsOwnerPermissions(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return obj.owner == request.user

        # Write permissions are only allowed to the owner of the snippet.
        return obj.owner == request.user