import datetime
import json
import time

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase

from notifications.models import Client, Mailing, Message


class ClientApiTestCase(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(username='admin', password='admin')
        self.client1 = Client.objects.create(phone_number='79999999999', tag='test', timezone='Europe/Moscow')
        self.client2 = Client.objects.create(phone_number='79999999998', tag='test', timezone='Europe/Moscow')
        self.client.force_authenticate(user=self.admin)

    def test_get_clients(self):
        response = self.client.get(reverse('clients-list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_get_client(self):
        response = self.client.get(reverse('clients-detail', args=(self.client1.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['phone_number'], self.client1.phone_number)
        self.assertEqual(response.data['tag'], self.client1.tag)
        self.assertEqual(response.data['timezone'], self.client1.timezone)
        self.assertEqual(response.data['operator_code'], self.client1.operator_code)

    def test_create_client(self):
        response = self.client.post(reverse('clients-list'),
                                    data={'phone_number': '79999999997', 'tag': 'test', 'timezone': 'Europe/Moscow'})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['phone_number'], '79999999997')
        self.assertEqual(response.data['tag'], 'test')
        self.assertEqual(response.data['timezone'], 'Europe/Moscow')
        self.assertEqual(Client.objects.get(phone_number=response.data['phone_number']).operator_code, '999')

    def test_update_client(self):
        response = self.client.put(reverse('clients-detail', args=(self.client1.id,)),
                                   data={'phone_number': '79999999997', 'tag': 'test', 'timezone': 'Europe/Moscow'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['phone_number'], '79999999997')
        self.assertEqual(response.data['tag'], 'test')
        self.assertEqual(response.data['timezone'], 'Europe/Moscow')
        self.assertEqual(Client.objects.get(phone_number=response.data['phone_number']).operator_code, '999')

        response = self.client.patch(reverse('clients-detail', args=(self.client1.id,)),
                                   data={'phone_number': '79999999991'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['phone_number'], '79999999991')
        self.assertEqual(response.data['tag'], 'test')
        self.assertEqual(response.data['timezone'], 'Europe/Moscow')
        self.assertEqual(Client.objects.get(phone_number=response.data['phone_number']).operator_code, '999')

    def test_delete_client(self):
        response = self.client.delete(reverse('clients-detail', args=(self.client1.id,)))
        self.assertEqual(response.status_code, 204)
        response = self.client.delete(reverse('clients-detail', args=(self.client1.id,)))
        self.assertEqual(response.status_code, 404)


class MailingApiTestCase(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(username='admin', password='admin')
        self.client.force_authenticate(user=self.admin)
        self.client1 = Client.objects.create(phone_number='79999999999', tag='test', timezone='Europe/Moscow')
        self.client2 = Client.objects.create(phone_number='79999999998', tag='test', timezone='Europe/Moscow')
        self.mailing1 = Mailing.objects.create(start_time=datetime.datetime.utcnow(), end_time='2024-01-01T00:00:00Z',
                                               text='test', filter_params={'tag': 'test'})

    def test_get_mailings(self):
        response = self.client.get(reverse('mailing-list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_get_mailing(self):
        response = self.client.get(reverse('mailing-detail', args=(self.mailing1.id,)))
        self.assertEqual(response.status_code, 200)

    def test_create_mailing(self):
        filter_params = json.dumps({'tag': ['test']})

        response = self.client.post(reverse('mailing-list'),
                                    data={'start_time': datetime.datetime.utcnow(),
                                          'end_time': '2024-01-01T00:00:00Z',
                                          'text': 'test',
                                          'filter_params': filter_params})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Mailing.objects.get(start_time=response.data['start_time']).text, 'test')



