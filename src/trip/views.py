from django.db.models import Q
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication

from .models import Trip
from .serializers import TripSerializer
from .permissions import IsAuthorOrReadOnly


class TripViewSet(viewsets.ModelViewSet):
    """Manage trips in database"""
    serializer_class = TripSerializer
    queryset = Trip.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthorOrReadOnly,)

    def get_queryset(self):
        user = self.request.user
        queryset = self.queryset
        if not user.is_anonymous:
            # Filter all non public trips that aren't signed to request.user
            queryset = queryset.filter(Q(author=user.id) | Q(is_public=True))
            return queryset
        queryset = queryset.filter(is_public=True)
        return queryset

    def perform_create(self, serializer):
        """Create new trip"""
        # Assign request user to new trip
        serializer.save(author=self.request.user)
