import os
import tempfile
from pathlib import Path
from unittest.mock import patch

from django.conf import settings
from django.core import mail
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, override_settings, TestCase
from django.urls import reverse

from . import models, forms


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


class CashierViewTests(TestCase):

    def test_cashier_view_form_valid(self):
        # Create a test file
        test_file = SimpleUploadedFile("test_file.jpg", b"file_content", content_type="image/jpeg")

        # Pass the test file in the POST data
        response = self.client.post(reverse("cashier"), {"file": test_file})
        self.assertEqual(response.status_code, 302)

        # Check if the file was created in the database
        self.assertEqual(models.File.objects.count(), 1)

        # Check if the scan was created in the database
        self.assertEqual(models.Scan.objects.count(), 1)

        # Check if the created file has the correct attributes
        file = models.File.objects.first()
        self.assertEqual(file.file.name, "test_file.jpg")

        # Check if the created scan has the correct attributes
        scan = models.Scan.objects.first()
        self.assertEqual(scan.image, file)

        # Check if the file_name is set in the cookies
        self.assertTrue('file_name' in response.cookies)

    def test_cashier_view_form_invalid(self):
        # Pass an empty file in the POST data
        response = self.client.post(reverse("cashier"), {})
        self.assertEqual(response.status_code, 302)

        # Check if the file was not created in the database
        self.assertEqual(models.File.objects.count(), 0)

        # Check if the scan was not created in the database
        self.assertEqual(models.Scan.objects.count(), 0)

        # Check if the file_name is not set in the cookies
        self.assertFalse('file_name' in response.cookies)

    def tearDown(self):
        # Get all the File objects created during tests
        files = models.File.objects.all()

        # Iterate through the files and delete the corresponding image files
        for file in files:
            file_path = os.path.join(settings.MEDIA_ROOT, file.file.name)
            if os.path.exists(file_path):
                os.remove(file_path)

        # Delete the File objects from the database
        models.File.objects.all().delete()

class TransactionViewTests(TestCase):

    def setUp(self):
        # Create a test user
        self.user = models.User.objects.create(username='test_user')

        # Create a test position
        self.position = models.Position.objects.create(name='test_position', price=42)

    def test_transaction_view(self):
        # Create a test file
        test_file = SimpleUploadedFile("test_file.jpg", b"file_content", content_type="image/jpeg")

        # Pass the test file in the POST data
        response = self.client.post(reverse("cashier"), {"file": test_file})
        self.assertEqual(response.status_code, 302)

        # Get the file_name from the cookies
        file_name = response.cookies['file_name'].value

        # POST data for the TransactionView
        data = {
            'user': self.user.pk,
            'positions': [self.position.pk],
            'total_check': 42
        }

        # Send a POST request to the TransactionView
        response = self.client.post(reverse("transaction"), data)

        # Check if the response has a successful status code
        self.assertEqual(response.status_code, 302)

        # Check if the transaction was created in the database
        self.assertEqual(models.Transaction.objects.count(), 1)

        # Check if the created transaction has the correct attributes
        transaction = models.Transaction.objects.first()
        self.assertEqual(transaction.user, self.user)
        self.assertEqual(transaction.positions, [{'name': 'test_position', 'price': 42}])
        self.assertEqual(transaction.total_check, 42)


    def tearDown(self):
        # Remove the test image file
        file_name = self.client.cookies['file_name'].value
        FILE_PATH = Path('uploads') / f'{file_name}'
        if FILE_PATH.exists():
            FILE_PATH.unlink()
