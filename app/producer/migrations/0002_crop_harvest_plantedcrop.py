# Generated by Django 4.0.10 on 2025-01-24 17:51

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('producer', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Crop',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'crops',
            },
        ),
        migrations.CreateModel(
            name='Harvest',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('year', models.CharField(max_length=4)),
                ('farm', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='harvests', to='producer.farm')),
            ],
            options={
                'db_table': 'harvests',
            },
        ),
        migrations.CreateModel(
            name='PlantedCrop',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('crop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='planted_crops', to='producer.crop')),
                ('harvest', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='planted_crops', to='producer.harvest')),
            ],
            options={
                'db_table': 'planted_crops',
            },
        ),
    ]
