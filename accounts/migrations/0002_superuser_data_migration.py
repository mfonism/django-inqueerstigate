from django.conf import settings
from django.db import migrations

from ..models import User


def create_default_superuser(apps, schema_editor):
    User.objects.create_superuser(
        email=settings.DEFAULT_SUPERUSER_EMAIL,
        password=settings.DEFAULT_SUPERUSER_PASSWORD,
    )


def destroy_default_superuser(apps, schema_editor):
    User.objects.get(email=settings.DEFAULT_SUPERUSER_EMAIL).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(create_default_superuser, destroy_default_superuser)
    ]
