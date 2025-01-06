# Generated by Django 5.0.6 on 2025-01-06 03:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content_site', '0002_remove_banner_course_delete_missionvision_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Invitated',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_name', models.CharField(max_length=100, verbose_name='Nombre del Alumno')),
                ('student_email', models.EmailField(max_length=254, verbose_name='Correo Electrónico del Amigo')),
                ('friend_name', models.CharField(max_length=100, verbose_name='Nombre del Amigo')),
                ('friend_phone', models.CharField(max_length=15, verbose_name='Teléfono del Amigo')),
                ('notes', models.TextField(blank=True, null=True, verbose_name='Clase Seleccionada')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Registro')),
            ],
        ),
    ]