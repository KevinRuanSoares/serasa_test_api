from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient
from producer.models import Producer
from producer.models import Farm
from producer.serializers import FarmSerializer
from user.models import Role


LIST_CREATE_FARM_URL = reverse('producer:list_create_farm')


def detail_url(farm_id):
    """Return the URL for a specific farm."""
    return reverse('producer:update_retrieve_farm', kwargs={'id': farm_id})


def create_user(**params):
    """Create and return a new user."""
    return get_user_model().objects.create_user(**params)


class PublicFarmApiTests(TestCase):
    """Test the public access to the farm API."""

    def setUp(self):
        self.client = APIClient()

    def test_authentication_required(self):
        """Test that authentication is required to access the API."""
        res = self.client.get(LIST_CREATE_FARM_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateFarmApiTests(TestCase):
    """Test authenticated access to the farm API."""

    fixtures = ['roles.json']

    def setUp(self):
        role_admin = Role.objects.get(pk='bdb80a3e-7458-4548-95f7-1b84c7b79cda')
        self.producer = Producer.objects.create(name='Producer 1', cpf_cnpj='123.456.789-01')

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

    def test_list_farms(self):
        """Test listing farms."""
        Farm.objects.create(
            name='Farm 1',
            city='City 1',
            state='SP',
            total_area=100.0,
            arable_area=70.0,
            vegetation_area=30.0,
            producer=self.producer
        )
        Farm.objects.create(
            name='Farm 2',
            city='City 2',
            state='MG',
            total_area=200.0,
            arable_area=150.0,
            vegetation_area=50.0,
            producer=self.producer
        )

        res = self.client.get(LIST_CREATE_FARM_URL)

        farms = Farm.objects.all()
        serializer = FarmSerializer(farms, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['results'], serializer.data)

    def test_create_farm(self):
        """Test creating a new farm."""
        payload = {
            'name': 'New Farm',
            'city': 'City 3',
            'state': 'RJ',
            'total_area': 300.0,
            'arable_area': 200.0,
            'vegetation_area': 100.0,
            'producer': self.producer.id
        }

        res = self.client.post(LIST_CREATE_FARM_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        farm = Farm.objects.get(id=res.data['id'])
        self.assertEqual(farm.name, payload['name'])
        self.assertEqual(farm.city, payload['city'])
        self.assertEqual(farm.state, payload['state'])

    def test_retrieve_farm(self):
        """Test retrieving a specific farm."""
        farm = Farm.objects.create(
            name='Farm 1',
            city='City 1',
            state='SP',
            total_area=100.0,
            arable_area=70.0,
            vegetation_area=30.0,
            producer=self.producer
        )

        url = detail_url(farm.id)
        res = self.client.get(url)

        serializer = FarmSerializer(farm)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_update_farm(self):
        """Test updating a farm."""
        farm = Farm.objects.create(
            name='Farm 1',
            city='City 1',
            state='SP',
            total_area=100.0,
            arable_area=70.0,
            vegetation_area=30.0,
            producer=self.producer
        )

        payload = {'name': 'Updated Farm', 'city': 'Updated City'}
        url = detail_url(farm.id)
        res = self.client.patch(url, payload)

        farm.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(farm.name, payload['name'])
        self.assertEqual(farm.city, payload['city'])

    def test_delete_farm(self):
        """Test soft deleting a farm."""
        farm = Farm.objects.create(
            name='Farm 1',
            city='City 1',
            state='SP',
            total_area=100.0,
            arable_area=70.0,
            vegetation_area=30.0,
            producer=self.producer
        )

        url = detail_url(farm.id)
        res = self.client.delete(url)

        farm.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertTrue(farm.is_deleted)

    def test_list_farms_with_filter(self):
        """Test filtering farms by name."""
        Farm.objects.create(
            name='Farm 1',
            city='City 1',
            state='SP',
            total_area=100.0,
            arable_area=70.0,
            vegetation_area=30.0,
            producer=self.producer
        )
        Farm.objects.create(
            name='Farm 2',
            city='City 2',
            state='MG',
            total_area=200.0,
            arable_area=150.0,
            vegetation_area=50.0,
            producer=self.producer
        )

        res = self.client.get(LIST_CREATE_FARM_URL, {'name': 'Farm 1'})

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data['results']), 1)
        self.assertEqual(res.data['results'][0]['name'], 'Farm 1')

    def test_list_farms_with_ordering(self):
        """Test ordering farms by name."""
        Farm.objects.create(
            name='Farm B',
            city='City 1',
            state='SP',
            total_area=100.0,
            arable_area=70.0,
            vegetation_area=30.0,
            producer=self.producer
        )
        Farm.objects.create(
            name='Farm A',
            city='City 2',
            state='MG',
            total_area=200.0,
            arable_area=150.0,
            vegetation_area=50.0,
            producer=self.producer
        )

        res = self.client.get(LIST_CREATE_FARM_URL, {'ordering': 'name'})

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        names = [farm['name'] for farm in res.data['results']]
        self.assertEqual(names, ['Farm A', 'Farm B'])
