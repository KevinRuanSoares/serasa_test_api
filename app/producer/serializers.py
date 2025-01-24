from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from producer.models import Producer, Farm


class ProducerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Producer
        fields = ['cpf_cnpj', 'name', 'id', 'created_at', 'updated_at']
        read_only_fields = ('id', 'created_at', 'updated_at')


class FarmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Farm
        fields = [
            'id',
            'name',
            'city',
            'state',
            'total_area',
            'arable_area',
            'vegetation_area',
            'producer',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ('id', 'created_at', 'updated_at')

    def validate(self, data):
        # Verifica se as áreas estão presentes no payload
        total_area = data.get('total_area', getattr(self.instance, 'total_area', None))
        arable_area = data.get('arable_area', getattr(self.instance, 'arable_area', None))
        vegetation_area = data.get('vegetation_area', getattr(self.instance, 'vegetation_area', None))

        # Validação da soma das áreas
        if arable_area and vegetation_area and total_area:
            if arable_area + vegetation_area > total_area:
                raise serializers.ValidationError(
                    _("The sum of the arable and vegetation areas cannot exceed the total area of ​​the farm.")
                )

        return data

    def create(self, validated_data):
        return super().create(validated_data)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
