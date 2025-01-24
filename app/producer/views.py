from rest_framework import generics, permissions, filters
from user.auth import (
    CheckTokenAuthentication,
)
from django_filters.rest_framework import DjangoFilterBackend
from producer.serializers import (
    ProducerSerializer,
    FarmSerializer,
    CropSerializer,
    HarvestSerializer,
    PlantedCropSerializer
)
from producer.models import Producer, Farm, Crop, Harvest, PlantedCrop
from producer.filters import ProducerFilter, FarmFilter, CropFilter, HarvestFilter, PlantedCropFilter
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


class FarmManagementView(generics.ListCreateAPIView):
    """Manage farms in the system. Allows listing and creating farms."""
    serializer_class = FarmSerializer
    authentication_classes = [CheckTokenAuthentication]
    permission_classes = [permissions.IsAuthenticated, (IsAdmin | IsSuperAdmin)]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = FarmFilter
    ordering_fields = ['name', 'city', 'state', 'total_area']
    ordering = ['name']
    pagination_class = CustomPagination

    def get_queryset(self):
        return Farm.objects.exclude(is_deleted=True)


class FarmRetrieveUpdateView(generics.RetrieveUpdateDestroyAPIView):
    """Manage retrieving, updating, and deleting farms."""
    serializer_class = FarmSerializer
    authentication_classes = [CheckTokenAuthentication]
    permission_classes = [permissions.IsAuthenticated, (IsAdmin | IsSuperAdmin)]
    queryset = Farm.objects.exclude(is_deleted=True)
    lookup_field = 'id'

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()


class CropManagementView(generics.ListCreateAPIView):
    serializer_class = CropSerializer
    authentication_classes = [CheckTokenAuthentication]
    permission_classes = [permissions.IsAuthenticated, (IsAdmin | IsSuperAdmin)]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = CropFilter
    ordering_fields = ['name', 'created_at', 'updated_at']
    ordering = ['name']
    pagination_class = CustomPagination

    def get_queryset(self):
        return Crop.objects.exclude(is_deleted=True)


class CropRetrieveUpdateView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CropSerializer
    authentication_classes = [CheckTokenAuthentication]
    permission_classes = [permissions.IsAuthenticated, (IsAdmin | IsSuperAdmin)]
    queryset = Crop.objects.exclude(is_deleted=True)
    lookup_field = 'id'

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()


class HarvestManagementView(generics.ListCreateAPIView):
    serializer_class = HarvestSerializer
    authentication_classes = [CheckTokenAuthentication]
    permission_classes = [permissions.IsAuthenticated, (IsAdmin | IsSuperAdmin)]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = HarvestFilter
    ordering_fields = ['year', 'farm', 'created_at', 'updated_at']
    ordering = ['year']
    pagination_class = CustomPagination

    def get_queryset(self):
        return Harvest.objects.exclude(is_deleted=True)


class HarvestRetrieveUpdateView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = HarvestSerializer
    authentication_classes = [CheckTokenAuthentication]
    permission_classes = [permissions.IsAuthenticated, (IsAdmin | IsSuperAdmin)]
    queryset = Harvest.objects.exclude(is_deleted=True)
    lookup_field = 'id'

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()


class PlantedCropManagementView(generics.ListCreateAPIView):
    serializer_class = PlantedCropSerializer
    authentication_classes = [CheckTokenAuthentication]
    permission_classes = [permissions.IsAuthenticated, (IsAdmin | IsSuperAdmin)]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = PlantedCropFilter
    ordering_fields = ['harvest', 'crop', 'created_at', 'updated_at']
    ordering = ['harvest']
    pagination_class = CustomPagination

    def get_queryset(self):
        return PlantedCrop.objects.exclude(is_deleted=True)


class PlantedCropRetrieveUpdateView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PlantedCropSerializer
    authentication_classes = [CheckTokenAuthentication]
    permission_classes = [permissions.IsAuthenticated, (IsAdmin | IsSuperAdmin)]
    queryset = PlantedCrop.objects.exclude(is_deleted=True)
    lookup_field = 'id'

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()
