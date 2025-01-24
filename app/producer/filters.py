from django_filters import rest_framework as filters
from producer.models import Producer


class ProducerFilter(filters.FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')
    cpf_cnpj = filters.CharFilter(field_name='cpf_cnpj', lookup_expr='icontains')

    class Meta:
        model = Producer
        fields = ['cpf_cnpj', 'name']
