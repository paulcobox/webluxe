# Generated by Django 5.0.6 on 2024-07-16 04:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0002_course_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='place',
            field=models.CharField(max_length=250, unique=True, verbose_name='Lugar'),
        ),
    ]
