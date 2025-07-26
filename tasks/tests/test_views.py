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

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from tasks.models import Task

class TaskCompleteTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='tom', password='testpass')
        self.client.login(username='tom', password='testpass')
        self.task = Task.objects.create(
            user=self.user,
            title='Incomplete Task',
            estimated_minutes=25,
            is_completed=False
        )

    def test_mark_task_as_complete(self):
        response = self.client.post(
            reverse('task-complete', args=[self.task.id])
        )
        self.assertEqual(response.status_code, 302)  # Expect redirect
        self.task.refresh_from_db()
        self.assertTrue(self.task.is_completed)

    def test_cannot_complete_other_users_task(self):
        other_user = User.objects.create_user(username='someone_else', password='pass')
        other_task = Task.objects.create(
            user=other_user,
            title='Other User Task',
            is_completed=False
        )
        response = self.client.post(
            reverse('task-complete', args=[other_task.id])
        )
        self.assertEqual(response.status_code, 404)  # Not yours, not allowed
        other_task.refresh_from_db()
        self.assertFalse(other_task.is_completed)