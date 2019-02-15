from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.IsAuthenticatedOrReadOnly):
    """
    Permission for trip viewset based on object properties
    """

    def has_object_permission(self, request, view, obj):
        if (
            request.user.is_anonymous
            and obj.is_public
            and request.method in permissions.SAFE_METHODS
        ):
            return True
        # If user is authenticated and object author return true
        elif (
            request.user.is_authenticated
            and request.user == obj.author
        ):
            return True
        # If user is authenticated is not object author
        # and method is safe return true
        elif (
            request.user.is_authenticated
            and request.user != obj.author
            and obj.is_public
            and request.method in permissions.SAFE_METHODS
        ):
            return True
        # If user is not authenticated and method is safe return true

        return False


class IsTripAuthorOrReadOnly(IsAuthorOrReadOnly):
    """Extension"""

    def has_object_permission(self, request, view, obj):
        obj = obj.trip
        return super(
            IsTripAuthorOrReadOnly,
            self
        ).has_object_permission(request, view, obj)
