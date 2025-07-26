from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    estimated_minutes = models.PositiveIntegerField(default=25)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    def total_duration_minutes(self):
        total = timedelta()
        for session in self.sessions.all():
            if session.end_time:
                total += (session.end_time - session.start_time)
        return int(total.total_seconds() / 60)
    
class TaskSession(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='sessions')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)

# in models.py

