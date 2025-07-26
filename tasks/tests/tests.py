from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from ..models import Task

class TaskViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='tom', password='testpass')
        self.task = Task.objects.create(
            user=self.user,
            title='Test Task',
            description='This is a test task.',
            estimated_minutes=25,
            is_completed=False
        )

    def test_task_list_redirects_if_not_logged_in(self):
        response = self.client.get(reverse('task-list'))
        self.assertRedirects(response, '/users/login/?next=/')

    def test_task_list_view_for_logged_in_user(self):
        self.client.login(username='tom', password='testpass')
        response = self.client.get(reverse('task-list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Task')

class TaskModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='tom', password='testpass')

    def test_string_representation(self):
        task = Task.objects.create(user=self.user, title='Do laundry')
        self.assertEqual(str(task), 'Do laundry')