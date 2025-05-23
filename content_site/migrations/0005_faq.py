# Generated by Django 5.0.6 on 2025-05-22 04:06

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content_site', '0004_testimony_google_url'),
    ]

    operations = [
        migrations.CreateModel(
            name='FAQ',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=500, verbose_name='Pregunta')),
                ('answer', ckeditor.fields.RichTextField(verbose_name='Respuesta')),
                ('category', models.CharField(choices=[('principiantes', 'Principiantes'), ('adultos', 'Adultos'), ('modalidades', 'Modalidades'), ('ubicacion', 'Ubicación'), ('ropa', 'Ropa y Horarios'), ('general', 'General')], default='general', max_length=100, verbose_name='Categoría')),
                ('is_active', models.BooleanField(default=True, verbose_name='¿Activo?')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Creación')),
                ('modified_date', models.DateTimeField(auto_now=True, verbose_name='Fecha de Modificación')),
            ],
            options={
                'verbose_name': 'Pregunta Frecuente',
                'verbose_name_plural': 'Preguntas Frecuentes',
                'ordering': ['category', 'question'],
            },
        ),
    ]
