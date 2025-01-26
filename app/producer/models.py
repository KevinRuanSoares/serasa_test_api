from django.db import models
from utils.base_model import BaseModel
from django.core.validators import MinValueValidator
from utils.document_validator import validate_cpf_cnpj


class Producer(BaseModel):
    cpf_cnpj = models.CharField(
        max_length=18, validators=[validate_cpf_cnpj]
    )
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'producers'

    def __str__(self):
        return self.name


class Farm(BaseModel):
    name = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=2)  # Ex: SP, MG
    total_area = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0)]
    )
    arable_area = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0)]
    )
    vegetation_area = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0)]
    )
    producer = models.ForeignKey(
        Producer, related_name="farms", on_delete=models.CASCADE
    )

    class Meta:
        db_table = 'farms'

    def __str__(self):
        return self.name

    @property
    def producer_name(self):
        return self.producer.name


class Crop(BaseModel):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'crops'

    def __str__(self):
        return self.name


class Harvest(BaseModel):
    year = models.CharField(max_length=4)  # Example: 2021
    farm = models.ForeignKey(
        Farm, related_name="harvests", on_delete=models.CASCADE
    )

    class Meta:
        db_table = 'harvests'

    def __str__(self):
        return f"{self.year} - {self.farm.name}"

    @property
    def farm_name(self):
        return self.farm.name


class PlantedCrop(BaseModel):
    harvest = models.ForeignKey(
        Harvest, related_name="planted_crops", on_delete=models.CASCADE
    )
    crop = models.ForeignKey(
        Crop, related_name="planted_crops", on_delete=models.CASCADE
    )

    class Meta:
        db_table = 'planted_crops'

    def __str__(self):
        return f"{self.crop.name} ({self.harvest.year})"

    @property
    def crop_name(self):
        return self.crop.name

    @property
    def harvest_year(self):
        return self.harvest.year

    @property
    def farm_name(self):
        return self.harvest.farm.name
