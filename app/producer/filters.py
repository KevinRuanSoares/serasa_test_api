from django_filters import rest_framework as filters
from producer.models import Producer, Farm, Crop, Harvest, PlantedCrop


class ProducerFilter(filters.FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')
    cpf_cnpj = filters.CharFilter(field_name='cpf_cnpj', lookup_expr='icontains')

    class Meta:
        model = Producer
        fields = ['cpf_cnpj', 'name']


class FarmFilter(filters.FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')
    city = filters.CharFilter(field_name='city', lookup_expr='icontains')
    state = filters.CharFilter(field_name='state', lookup_expr='iexact')
    producer = filters.CharFilter(field_name='producer__id', lookup_expr='exact')

    class Meta:
        model = Farm
        fields = ['name', 'city', 'state', 'producer']


class CropFilter(filters.FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = Crop
        fields = ['name']


class HarvestFilter(filters.FilterSet):
    year = filters.CharFilter(field_name='year', lookup_expr='exact')
    farm = filters.CharFilter(field_name='farm__id', lookup_expr='exact')

    class Meta:
        model = Harvest
        fields = ['year', 'farm']


class PlantedCropFilter(filters.FilterSet):
    harvest = filters.CharFilter(field_name='harvest__id', lookup_expr='exact')
    crop = filters.CharFilter(field_name='crop__id', lookup_expr='exact')

    class Meta:
        model = PlantedCrop
        fields = ['harvest', 'crop']
