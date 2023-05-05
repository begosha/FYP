from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .views import UserList
from calculator import models


class UserListTestCase(TestCase):
    def setUp(self):
        # Create test users
        self.user1 = User.objects.create_user(username='user1', password='testpassword', first_name='John', last_name='Doe')
        self.user2 = User.objects.create_user(username='user2', password='testpassword', first_name='Jane', last_name='Doe')
        self.user3 = User.objects.create_user(username='user3', password='testpassword', first_name='Alice', last_name='Smith')

        self.url = reverse('users')

    def test_user_list_view_uses_correct_template(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user_list.html')

    def test_user_list_view_displays_users(self):
        response = self.client.get(self.url)
        users_in_response = response.context_data['user_objects']
        self.assertIn(self.user1, users_in_response)
        self.assertIn(self.user2, users_in_response)
        self.assertIn(self.user3, users_in_response)

    def test_user_list_view_search(self):
        search_url = f"{self.url}?search=Doe"
        response = self.client.get(search_url)
        users_in_response = response.context_data['user_objects']
        self.assertIn(self.user1, users_in_response)
        self.assertIn(self.user2, users_in_response)
        self.assertNotIn(self.user3, users_in_response)

    def test_user_list_view_pagination(self):
        # Update the paginate_by value in UserList view to 2 for testing
        UserList.paginate_by = 2

        response = self.client.get(self.url)
        users_in_response = response.context_data['user_objects']
        self.assertIn(self.user1, users_in_response)
        self.assertIn(self.user2, users_in_response)
        self.assertNotIn(self.user3, users_in_response)

        response = self.client.get(f"{self.url}?page=2")
        users_in_response = response.context_data['user_objects']
        self.assertNotIn(self.user1, users_in_response)
        self.assertNotIn(self.user2, users_in_response)
        self.assertIn(self.user3, users_in_response)


class UserDetailTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword', first_name='John', last_name='Doe')
        self.transaction1 = models.Transaction.objects.create(user=self.user, is_paid=True)
        self.transaction2 = models.Transaction.objects.create(user=self.user, is_paid=False)
        self.transaction3 = models.Transaction.objects.create(user=self.user, is_paid=True)

        self.url = reverse('detail', args=[self.user.pk])

    def test_user_detail_view_uses_correct_template(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user_detail.html')

    def test_user_detail_view_displays_user(self):
        response = self.client.get(self.url)
        self.assertEqual(response.context_data['user_obj'], self.user)

    def test_user_detail_view_transactions(self):
        response = self.client.get(self.url)
        self.assertEqual(len(response.context_data['transactions']), 3)

    def test_user_detail_view_filter_transactions(self):
        paid_filter_url = f"{self.url}?is_paid=true"
        response = self.client.get(paid_filter_url)
        transactions = response.context_data['transactions']
        self.assertEqual(len(transactions), 2)
        for transaction in transactions:
            self.assertTrue(transaction.is_paid)

