from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from producer.models import Producer, Farm, Crop, Harvest, PlantedCrop


class ProducerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Producer
        fields = ['cpf_cnpj', 'name', 'id', 'created_at', 'updated_at']
        read_only_fields = ('id', 'created_at', 'updated_at')

    def validate_cpf_cnpj(self, value):
        """
        Valida que o CPF/CNPJ é único entre os produtores que não estão com is_deleted=True,
        ignorando a instância atual ao atualizar.
        """
        queryset = Producer.objects.filter(cpf_cnpj=value, is_deleted=False)
        if self.instance:
            # Exclui a instância atual da validação
            queryset = queryset.exclude(id=self.instance.id)

        if queryset.exists():
            raise serializers.ValidationError(
                _("CPF/CNPJ já está em uso para um produtor ativo.")
            )
        return value


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


class CropSerializer(serializers.ModelSerializer):

    class Meta:
        model = Crop
        fields = ['id', 'name', 'created_at', 'updated_at']
        read_only_fields = ('id', 'created_at', 'updated_at')


class HarvestSerializer(serializers.ModelSerializer):

    class Meta:
        model = Harvest
        fields = ['id', 'year', 'farm', 'created_at', 'updated_at']
        read_only_fields = ('id', 'created_at', 'updated_at')


class PlantedCropSerializer(serializers.ModelSerializer):

    class Meta:
        model = PlantedCrop
        fields = ['id', 'harvest', 'crop', 'created_at', 'updated_at']
        read_only_fields = ('id', 'created_at', 'updated_at')
