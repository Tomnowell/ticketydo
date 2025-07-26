from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from tasks.models import Task, TaskSession
from django.utils import timezone
from time import sleep

class TaskTimerTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='tom', password='testpass')
        self.client.login(username='tom', password='testpass')
        self.task = Task.objects.create(
            user=self.user,
            title='Focus Task',
            estimated_minutes=25,
            is_completed=False
        )

    def test_start_timer_creates_session(self):
        response = self.client.post(reverse('task-start-timer', args=[self.task.id]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(TaskSession.objects.count(), 1)
        session = TaskSession.objects.first()
        self.assertEqual(session.task, self.task)
        self.assertIsNotNone(session.start_time)
        self.assertIsNone(session.end_time)

    def test_stop_timer_sets_end_time(self):
        # Start a session
        self.client.post(reverse('task-start-timer', args=[self.task.id]))
        session = TaskSession.objects.get(task=self.task, end_time__isnull=True)

        # Stop the session
        response = self.client.post(reverse('task-stop-timer', args=[self.task.id]))
        self.assertEqual(response.status_code, 302)

        session.refresh_from_db()
        self.assertIsNotNone(session.end_time)

    def test_stop_timer_when_none_running_does_nothing(self):
        response = self.client.post(reverse('task-stop-timer', args=[self.task.id]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(TaskSession.objects.count(), 0)