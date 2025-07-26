from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from tasks.models import Task, TaskSession
from datetime import timedelta


class TaskTotalTimeTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='durationuser', password='testpass')
        self.client.login(username='durationuser', password='testpass')

        self.task = Task.objects.create(title='Total Time Task', user=self.user)

    def test_total_time_displayed_for_task(self):
        now = timezone.now()

        TaskSession.objects.create(task=self.task, start_time=now - timedelta(minutes=30), end_time=now - timedelta(minutes=20))
        TaskSession.objects.create(task=self.task, start_time=now - timedelta(minutes=10), end_time=now)

        response = self.client.get(reverse('task-list'))

        # Total duration should be 10 + 10 = 20 minutes
        # Accept the custom duration filter output (0:20:00 total)
        self.assertContains(response, '20:00 total')