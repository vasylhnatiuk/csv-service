from datetime import timedelta, datetime

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from service.models import Client, Category

from django.utils import timezone


class ClientListViewTests(APITestCase):
    def setUp(self):
        self.category1 = Category.objects.create(name='category1')
        self.category2 = Category.objects.create(name='category2')

        # Create more clients for testing pagination
        for _ in range(15):
            Client.objects.create(category=self.category1, gender='Male', birth_date='1990-01-01')
            Client.objects.create(category=self.category2, gender='Female', birth_date='1995-01-01')

    def test_filter_by_category(self):
        url = reverse('client-list')
        response = self.client.get(url + '?category=category1')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 10)  # Pagination limit
        print()
        self.assertTrue(all(client['category']['id'] == self.category1.id for client in response.data['results']))

    def test_filter_by_gender(self):
        url = reverse('client-list')
        response = self.client.get(url + '?gender=Male')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 10)  # Pagination limit
        self.assertTrue(all(client['gender'] == 'Male' for client in response.data['results']))

    def test_filter_by_dob(self):
        url = reverse('client-list')
        response = self.client.get(url + '?dob=1990-01-01')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 10)  # Pagination limit
        self.assertTrue(all(client['birth_date'] == '1990-01-01' for client in response.data['results']))

    def test_filter_by_age(self):
        today = timezone.now().date()
        birth_date_min = today - timedelta(days=30 * 365)
        birth_date_max = today - timedelta(days=29 * 365)
        url = reverse('client-list')
        response = self.client.get(url + f'?age=30')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 10)  # Pagination limit

        # Convert birth_date strings to datetime.date objects for comparison
        birth_dates_in_range = [datetime.strptime(client['birth_date'], '%Y-%m-%d').date() for client in
                                response.data['results']]

        self.assertTrue(all(birth_date_min <= birth_date <= birth_date_max for birth_date in birth_dates_in_range))

    def test_filter_by_age_range(self):
        url = reverse('client-list')
        response = self.client.get(url + '?age_range=25-30')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 10)

