from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User

from tasks.models import Task, TaskSession


class TaskListTimerUITests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='timeruser', password='testpass')
        self.client.login(username='timeruser', password='testpass')

        self.task = Task.objects.create(title='Timer Task', user=self.user)

    def test_task_list_shows_start_button_when_no_timer(self):
        response = self.client.get(reverse('task-list'))

        self.assertContains(response, '▶ Start Timer')
        self.assertNotContains(response, '⏹ Stop Timer')

    def test_task_list_shows_stop_button_when_timer_running(self):
        TaskSession.objects.create(task=self.task, start_time=timezone.now())

        response = self.client.get(reverse('task-list'))

        self.assertContains(response, '⏹ Stop Timer')
        self.assertNotContains(response, '▶ Start Timer')

    def test_task_list_displays_time_since_start(self):
        start_time = timezone.now() - timezone.timedelta(minutes=5)
        TaskSession.objects.create(task=self.task, start_time=start_time)

        response = self.client.get(reverse('task-list'))

        self.assertContains(response, '5\xa0minutes')  # \xa0 is a non-breaking space