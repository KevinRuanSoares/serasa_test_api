# Generated by Django 4.0.10 on 2025-01-26 01:34

from django.db import migrations, models
import utils.document_validator


class Migration(migrations.Migration):

    dependencies = [
        ('producer', '0002_crop_harvest_plantedcrop'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producer',
            name='cpf_cnpj',
            field=models.CharField(max_length=18, validators=[utils.document_validator.validate_cpf_cnpj]),
        ),
    ]
