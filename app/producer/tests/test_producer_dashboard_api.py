from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient
from user.models import Role
from producer.models import Farm, Producer, PlantedCrop, Crop, Harvest

DASHBOARD_URL = reverse('producer:dashboard-data')


def create_user(**params):
    """Create and return a new user."""
    return get_user_model().objects.create_user(**params)


class DashboardApiTests(TestCase):
    """Test the dashboard data API."""

    fixtures = ['roles.json']

    def setUp(self):
        role_admin = Role.objects.get(pk='bdb80a3e-7458-4548-95f7-1b84c7b79cda')
        self.admin_user = create_user(
            email='admin@example.com',
            password='testpass123',
            name='Admin User',
            cpf='111.111.111-11',
        )
        self.admin_user.roles.add(role_admin)
        self.admin_user.save()

        self.client = APIClient()
        self.client.force_authenticate(user=self.admin_user)

        # Create a producer
        self.producer = Producer.objects.create(
            name='Producer 1',
            cpf_cnpj='18.200.327/0001-72'
        )

        # Create crops
        self.crop_soja = Crop.objects.create(name='Soja')
        self.crop_milho = Crop.objects.create(name='Milho')

        # Create farms
        self.farm_1 = Farm.objects.create(
            name='Fazenda 1',
            city='City 1',
            state='SP',
            total_area=100.00,
            arable_area=70.00,
            vegetation_area=30.00,
            producer=self.producer
        )
        self.farm_2 = Farm.objects.create(
            name='Fazenda 2',
            city='City 2',
            state='MG',
            total_area=200.00,
            arable_area=150.00,
            vegetation_area=50.00,
            producer=self.producer,
            is_deleted=True
        )

        # Create a harvest
        self.harvest = Harvest.objects.create(
            year='2023',
            farm=self.farm_1
        )

        # Create planted crops
        self.planted_crop_1 = PlantedCrop.objects.create(
            harvest=self.harvest,
            crop=self.crop_soja
        )
        self.planted_crop_2 = PlantedCrop.objects.create(
            harvest=self.harvest,
            crop=self.crop_milho,
            is_deleted=True
        )

    def test_retrieve_dashboard_data(self):
        """Test retrieving dashboard data."""
        res = self.client.get(DASHBOARD_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        # Test farms by state
        farms_by_state = res.data['farms_by_state']
        self.assertEqual(len(farms_by_state), 1)  # Only 'SP', because 'MG' is deleted
        self.assertEqual(farms_by_state[0]['state'], 'SP')
        self.assertEqual(farms_by_state[0]['count'], 1)

        # Test crop distribution
        crops_distribution = res.data['crops_distribution']
        self.assertEqual(len(crops_distribution), 1)  # Only 'Soja', 'Milho' is deleted
        self.assertEqual(crops_distribution[0]['crop'], 'Soja')
        self.assertEqual(crops_distribution[0]['count'], 1)

        # Test land use
        land_use = res.data['land_use']
        self.assertEqual(float(land_use['total_area']), 100.00)
        self.assertEqual(float(land_use['arable_area']), 70.00)
        self.assertEqual(float(land_use['vegetation_area']), 30.00)
