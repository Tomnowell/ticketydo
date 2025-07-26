from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from tasks.models import Task

class TaskCreationTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='tom', password='testpass')
        self.client.login(username='tom', password='testpass')

    def test_get_create_task_form(self):
        response = self.client.get(reverse('task-create'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<form')

    def test_post_valid_task(self):
        data = {
            'title': 'Write more tests',
            'description': 'Ensure test coverage is high',
            'estimated_minutes': 25
        }
        response = self.client.post(reverse('task-create'), data)
        self.assertEqual(response.status_code, 302)  # redirect after creation
        self.assertEqual(Task.objects.count(), 1)
        self.assertEqual(Task.objects.first().title, 'Write more tests')

    def test_post_invalid_task(self):
        data = {
            'title': '',  # Invalid: required
            'description': 'Missing title!',
            'estimated_minutes': 25
        }
        response = self.client.post(reverse('task-create'), data)
        self.assertEqual(response.status_code, 200)  # form redisplayed
        self.assertFormError(response.context['form'], 'title', 'This field is required.')

    