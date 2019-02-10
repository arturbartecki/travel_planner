from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Trip
from .serializers import TripSerializer


class TripViewSet(viewsets.ModelViewSet):
    """Manage trips in database"""
    serializer_class = TripSerializer
    queryset = Trip.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        user = self.request.user
        queryset = self.queryset
        if not user.is_anonymous:
            q1 = queryset.filter(author=user.id)
            q2 = queryset.filter(is_public=True)
            queryset = q1 | q2
            return queryset
        queryset = queryset.filter(is_public=True)
        return queryset
