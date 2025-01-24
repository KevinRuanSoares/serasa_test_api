from django.db import models
from utils.base_model import BaseModel
from django.core.validators import MinValueValidator
from utils.document_validator import validate_cpf_cnpj

class Producer(BaseModel):
    cpf_cnpj = models.CharField(
        max_length=18, unique=True, validators=[validate_cpf_cnpj]
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