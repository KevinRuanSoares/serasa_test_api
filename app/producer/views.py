from rest_framework import generics, permissions, filters
from user.auth import (
    CheckTokenAuthentication,
)
from django_filters.rest_framework import DjangoFilterBackend
from producer.serializers import ProducerSerializer
from producer.models import Producer
from producer.filters import ProducerFilter
from user.permissions import IsSuperAdmin, IsAdmin
from utils.pagination import CustomPagination


class ProducerManagementView(generics.ListCreateAPIView):
    """Manage users in the system. Allows listing, creating, and updating users."""
    serializer_class = ProducerSerializer
    authentication_classes = [CheckTokenAuthentication]
    permission_classes = [permissions.IsAuthenticated, (IsAdmin | IsSuperAdmin)]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = ProducerFilter
    ordering_fields = ['cpf_cnpj', 'name', 'created_at', 'updated_at']
    ordering = ['name']
    pagination_class = CustomPagination

    def get_queryset(self):
        """Return the queryset excluding the logged-in user."""
        return Producer.objects.exclude(
            is_deleted=True
        )


class ProducerRetrieveUpdateView(generics.RetrieveUpdateDestroyAPIView):
    """Manage retrieving and updating users in the system."""
    serializer_class = ProducerSerializer
    authentication_classes = [CheckTokenAuthentication]
    permission_classes = [permissions.IsAuthenticated, (IsAdmin | IsSuperAdmin)]
    queryset = Producer.objects.exclude(is_deleted=True)
    lookup_field = 'id'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()
