from django.apps import AppConfig
import os


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    def ready(self):
        from django.contrib.auth import get_user_model
        from django.db.utils import OperationalError
        from django.db import connections

        try:
            # Check DB is available (avoid running during migration)
            connections['default'].cursor()
        except OperationalError:
            return

        User = get_user_model()
        username = os.environ.get('DJANGO_SUPERUSER_USERNAME')
        email = os.environ.get('DJANGO_SUPERUSER_EMAIL')
        password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')

        if username and password and not User.objects.filter(username=username).exists():
            print("Creating admin user...")
            User.objects.create_superuser(username=username, email=email, password=password)
