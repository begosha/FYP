import os
import tempfile
from unittest.mock import patch
from urllib.parse import urlencode

from django.core import mail
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings, TestCase
from django.urls import reverse

from . import models, forms


from django.test import TestCase
from django.urls import reverse


class PositionViewTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Create sample positions for testing
        for i in range(10):
            models.Position.objects.create(name=f'Position {i}')

    def setUp(self):
        self.url = reverse('positions')

    def test_position_view_get_request(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'positions.html')
        self.assertIsInstance(response.context['form'], forms.SimpleSearchForm)
        self.assertEqual(len(response.context['positions']), 5)

    def test_position_view_search_query(self):
        search_value = 'Position 1'
        response = self.client.get(self.url, {'search': search_value})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['query'], f'search={search_value.replace(" ", "+")}')
        positions = response.context['positions']
        self.assertTrue(all(position.name.lower().startswith(search_value.lower()) for position in positions))

    def test_position_view_invalid_search_query(self):
        search_value = 'Invalid query'
        response = self.client.get(self.url, {'search': search_value})
        self.assertEqual(response.status_code, 200)
        positions = response.context['positions']
        self.assertEqual(len(positions), 0)


class MainViewTestCase(TestCase):
    def setUp(self):
        self.url = reverse('main')

    def test_main_view_uses_correct_template(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_main_view_form_submission(self):
        form_data = {
            'name': 'John Doe',
            'email': 'john.doe@example.com',
            'subject': 'Test Subject',
            'message': 'Test message',
        }
        response = self.client.post(self.url, data=form_data)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Test Subject')
        self.assertEqual(mail.outbox[0].body, 'Test message\nfrom: John Doe john.doe@example.com')
        self.assertEqual(mail.outbox[0].from_email, 'begoshaaaa@gmail.com')
        self.assertEqual(mail.outbox[0].to, ['begoshaaaa@gmail.com'])

    def test_main_view_form_submission_invalid(self):
        form_data = {
            'name': 'John Doe',
            'email': 'invalid-email',
            'subject': 'Test Subject',
            'message': 'Test message',
        }
        response = self.client.post(self.url, data=form_data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(mail.outbox), 0)


class CashierViewTestCase(TestCase):
    def setUp(self):
        self.url = reverse('cashier')

    def test_cashier_view_uses_correct_template(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cash_register.html')

    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    @patch('object_detection.detect.run')
    def test_cashier_view_form_submission(self, mock_run):
        test_image = tempfile.NamedTemporaryFile(suffix='.jpg', dir=tempfile.gettempdir(), delete=False)
        with open(test_image.name, 'wb') as f:
            f.write(b'\x00' * 256)

        with open(test_image.name, 'rb') as img:
            uploaded_file = SimpleUploadedFile(name='test.jpg', content=img.read(), content_type='image/jpeg')
            form_data = {
                'file': uploaded_file,
            }
            response = self.client.post(self.url, data=form_data, format='multipart')

        self.assertEqual(response.status_code, 302)
        self.assertEqual(models.File.objects.count(), 1)
        self.assertEqual(models.Scan.objects.count(), 1)
        # mock_run.assert_called_once()

        os.remove(test_image.name)
        tempfile.gettempdir()

    def test_cashier_view_form_submission_invalid(self):
        form_data = {
        }
        response = self.client.post(self.url, data=form_data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(models.File.objects.count(), 0)
        self.assertEqual(models.Scan.objects.count(), 0)
