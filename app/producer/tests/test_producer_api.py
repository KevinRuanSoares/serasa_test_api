from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient
from producer.models import Producer
from user.models import Role
from producer.serializers import ProducerSerializer

LIST_CREATE_PRODUCER_URL = reverse('producer:list_create')


def create_user(**params):
    """Create and return a new user."""
    return get_user_model().objects.create_user(**params)


def detail_url(producer_id):
    """Return the URL for a specific producer."""
    return reverse('producer:update_retrieve', kwargs={'id': producer_id})


class PublicProducerApiTests(TestCase):
    """Test the public access to the producer API."""

    def setUp(self):
        self.client = APIClient()

    def test_authentication_required(self):
        """Test that authentication is required to access the API."""
        res = self.client.get(LIST_CREATE_PRODUCER_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateProducerApiTests(TestCase):
    """Test authenticated access to the producer API."""
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

    def test_list_producers(self):
        """Test listing producers."""
        Producer.objects.create(name='Producer 1', cpf_cnpj='18.200.327/0001-72')
        Producer.objects.create(name='Producer 2', cpf_cnpj='27.162.364/0001-24')

        res = self.client.get(LIST_CREATE_PRODUCER_URL)

        producers = Producer.objects.filter(is_deleted=False)
        serializer = ProducerSerializer(producers, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['results'], serializer.data)

    def test_create_producer(self):
        """Test creating a new producer."""
        payload = {
            'name': 'New Producer',
            'cpf_cnpj': '79.839.483/0001-72',
        }

        res = self.client.post(LIST_CREATE_PRODUCER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        producer = Producer.objects.get(id=res.data['id'])
        self.assertEqual(producer.name, payload['name'])
        self.assertEqual(producer.cpf_cnpj, payload['cpf_cnpj'])

    def test_retrieve_producer(self):
        """Test retrieving a specific producer."""
        producer = Producer.objects.create(name='Producer 1', cpf_cnpj='123.456.789-01')

        url = detail_url(producer.id)
        res = self.client.get(url)

        serializer = ProducerSerializer(producer)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_update_producer(self):
        """Test updating a producer."""
        producer = Producer.objects.create(name='Producer 1', cpf_cnpj='123.456.789-01')

        payload = {'name': 'Updated Producer'}
        url = detail_url(producer.id)
        res = self.client.patch(url, payload)

        producer.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(producer.name, payload['name'])

    def test_delete_producer(self):
        """Test soft deleting a producer."""
        producer = Producer.objects.create(name='Producer 1', cpf_cnpj='123.456.789-01')

        url = detail_url(producer.id)
        res = self.client.delete(url)

        producer.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertTrue(producer.is_deleted)

    def test_list_producers_with_pagination(self):
        """Test listing producers with pagination."""
        Producer.objects.create(name='Producer 1', cpf_cnpj='123.456.789-01')
        Producer.objects.create(name='Producer 2', cpf_cnpj='987.654.321-09')

        res = self.client.get(LIST_CREATE_PRODUCER_URL, {'page': 1, 'page_size': 1})

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data['results']), 1)

    def test_list_producers_with_filter(self):
        """Test filtering producers by name."""
        Producer.objects.create(name='Producer 1', cpf_cnpj='123.456.789-01')
        Producer.objects.create(name='Producer 2', cpf_cnpj='987.654.321-09')

        res = self.client.get(LIST_CREATE_PRODUCER_URL, {'name': 'Producer 1'})

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data['results']), 1)
        self.assertEqual(res.data['results'][0]['name'], 'Producer 1')

    def test_list_producers_with_ordering(self):
        """Test ordering producers by name."""
        Producer.objects.create(name='Producer B', cpf_cnpj='123.456.789-01')
        Producer.objects.create(name='Producer A', cpf_cnpj='987.654.321-09')

        res = self.client.get(LIST_CREATE_PRODUCER_URL, {'ordering': 'name'})

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        names = [producer['name'] for producer in res.data['results']]
        self.assertEqual(names, ['Producer A', 'Producer B'])
