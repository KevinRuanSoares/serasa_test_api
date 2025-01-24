from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient
from producer.models import Crop, Harvest, PlantedCrop, Farm, Producer
from producer.serializers import CropSerializer, HarvestSerializer, PlantedCropSerializer
from user.models import Role

LIST_CREATE_CROP_URL = reverse('producer:list_create_crop')
LIST_CREATE_HARVEST_URL = reverse('producer:list_create_harvest')
LIST_CREATE_PLANTED_CROP_URL = reverse('producer:list_create_planted_crop')


def crop_detail_url(crop_id):
    return reverse('producer:update_retrieve_crop', kwargs={'id': crop_id})


def harvest_detail_url(harvest_id):
    return reverse('producer:update_retrieve_harvest', kwargs={'id': harvest_id})


def planted_crop_detail_url(planted_crop_id):
    return reverse('producer:update_retrieve_planted_crop', kwargs={'id': planted_crop_id})


def create_user(**params):
    """Create and return a new user."""
    return get_user_model().objects.create_user(**params)


class PublicCropApiTests(TestCase):
    """Test public access to the Crop API."""

    def setUp(self):
        self.client = APIClient()

    def test_authentication_required(self):
        """Test that authentication is required to access the Crop API."""
        res = self.client.get(LIST_CREATE_CROP_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateCropApiTests(TestCase):
    """Test authenticated access to the Crop API."""

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

    def test_list_crops(self):
        """Test listing crops."""
        Crop.objects.create(name='Corn')
        Crop.objects.create(name='Soybean')

        res = self.client.get(LIST_CREATE_CROP_URL)

        crops = Crop.objects.all()
        serializer = CropSerializer(crops, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['results'], serializer.data)

    def test_create_crop(self):
        """Test creating a new crop."""
        payload = {'name': 'Wheat'}
        res = self.client.post(LIST_CREATE_CROP_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        crop = Crop.objects.get(id=res.data['id'])
        self.assertEqual(crop.name, payload['name'])


class PrivateHarvestApiTests(TestCase):
    """Test authenticated access to the Harvest API."""

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
        self.producer = Producer.objects.create(name='Producer 1', cpf_cnpj='123.456.789-01')

    def test_list_harvests(self):
        """Test listing harvests."""
        farm = Farm.objects.create(
            name='Farm 1',
            city='City 1',
            state='SP',
            total_area=100,
            arable_area=70,
            vegetation_area=30,
            producer=self.producer
        )
        Harvest.objects.create(year='2022', farm=farm)
        Harvest.objects.create(year='2023', farm=farm)

        res = self.client.get(LIST_CREATE_HARVEST_URL)

        harvests = Harvest.objects.all()
        serializer = HarvestSerializer(harvests, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['results'], serializer.data)

    def test_create_harvest(self):
        """Test creating a new harvest."""
        farm = Farm.objects.create(
            name='Farm 1',
            city='City 1',
            state='SP',
            total_area=100,
            arable_area=70,
            vegetation_area=30,
            producer=self.producer
        )
        payload = {'year': '2024', 'farm': farm.id}
        res = self.client.post(LIST_CREATE_HARVEST_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        harvest = Harvest.objects.get(id=res.data['id'])
        self.assertEqual(harvest.year, payload['year'])


class PrivatePlantedCropApiTests(TestCase):
    """Test authenticated access to the PlantedCrop API."""

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
        self.producer = Producer.objects.create(name='Producer 1', cpf_cnpj='123.456.789-01')

    def test_list_planted_crops(self):
        """Test listing planted crops."""
        crop = Crop.objects.create(name='Corn')
        farm = Farm.objects.create(
            name='Farm 1',
            city='City 1',
            state='SP',
            total_area=100,
            arable_area=70,
            vegetation_area=30,
            producer=self.producer
        )
        harvest = Harvest.objects.create(year='2023', farm=farm)
        PlantedCrop.objects.create(harvest=harvest, crop=crop)

        res = self.client.get(LIST_CREATE_PLANTED_CROP_URL)

        planted_crops = PlantedCrop.objects.all()
        serializer = PlantedCropSerializer(planted_crops, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['results'], serializer.data)

    def test_create_planted_crop(self):
        """Test creating a new planted crop."""
        crop = Crop.objects.create(name='Soybean')
        farm = Farm.objects.create(
            name='Farm 2',
            city='City 2',
            state='MG',
            total_area=150,
            arable_area=100,
            vegetation_area=50,
            producer=self.producer
        )
        harvest = Harvest.objects.create(year='2023', farm=farm)
        payload = {'harvest': harvest.id, 'crop': crop.id}
        res = self.client.post(LIST_CREATE_PLANTED_CROP_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        planted_crop = PlantedCrop.objects.get(id=res.data['id'])
        self.assertEqual(planted_crop.harvest, harvest)
        self.assertEqual(planted_crop.crop, crop)
