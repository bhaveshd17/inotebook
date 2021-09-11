# Generated by Django 3.2.7 on 2021-09-11 12:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('inotebook_backend', '0003_rename_data_notes_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notes',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]