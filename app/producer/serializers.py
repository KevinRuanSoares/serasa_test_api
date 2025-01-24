from rest_framework import serializers
from .models import Producer


class ProducerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Producer
        fields = ['cpf_cnpj', 'name', 'id', 'created_at', 'updated_at']
        read_only_fields = ('id', 'created_at', 'updated_at')
