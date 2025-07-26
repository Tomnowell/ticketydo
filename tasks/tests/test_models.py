from django.test import TestCase
from django.contrib.auth.models import User
from ..models import Task

class TaskModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='tom', password='testpass')

    def test_string_representation(self):
        task = Task.objects.create(user=self.user, title='Do laundry')
        self.assertEqual(str(task), 'Do laundry')