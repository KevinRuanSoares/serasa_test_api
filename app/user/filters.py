from django.contrib.auth import (
    get_user_model,
)
from django_filters import rest_framework as filters


class UserFilter(filters.FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')
    email = filters.CharFilter(field_name='email', lookup_expr='icontains')
    cpf = filters.CharFilter(field_name='cpf', lookup_expr='icontains')
    roles = filters.CharFilter(field_name='roles__name', lookup_expr='icontains')

    class Meta:
        model = get_user_model()
        fields = ['name', 'email', 'cpf', 'roles']
