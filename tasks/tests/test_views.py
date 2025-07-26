from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from tasks.models import Task

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


    def test_toggle_task_completion_on(self):
        # First toggle: should mark complete
        response = self.client.post(reverse('task-toggle', args=[self.task.id]))
        self.assertEqual(response.status_code, 302)
        self.task.refresh_from_db()
        self.assertTrue(self.task.is_completed)

    def test_toggle_task_completion_off(self):
        self.task.is_completed = True
        self.task.save()

        # Second toggle: should unmark complete
        response = self.client.post(reverse('task-toggle', args=[self.task.id]))
        self.assertEqual(response.status_code, 302)
        self.task.refresh_from_db()
        self.assertFalse(self.task.is_completed)

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