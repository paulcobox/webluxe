# Generated by Django 5.0.6 on 2024-07-16 03:18

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Instructors',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, verbose_name='Nombre')),
                ('tags_about_me', models.CharField(max_length=500, verbose_name='Tags Acerca de Mi')),
                ('tags_mission', models.CharField(max_length=500, verbose_name='Tags Mision')),
                ('specialty', models.CharField(max_length=250, verbose_name='Especialidad')),
                ('about_me', ckeditor.fields.RichTextField(verbose_name='Acerca de Mi')),
                ('mission', ckeditor.fields.RichTextField(verbose_name='Mi Mision')),
                ('image', models.ImageField(blank=True, upload_to='images', verbose_name='Imagen de Instructor')),
                ('is_active', models.BooleanField(default=False, verbose_name='¿Activo?')),
                ('facebook', models.URLField(blank=True, max_length=500, null=True, verbose_name='Facebook')),
                ('tiktok', models.URLField(blank=True, max_length=500, null=True, verbose_name='Tiktok')),
                ('instagram', models.URLField(blank=True, max_length=500, null=True, verbose_name='Instagram')),
                ('youtube', models.URLField(blank=True, max_length=500, null=True, verbose_name='Youtube')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Creación')),
                ('modified_date', models.DateTimeField(auto_now=True, verbose_name='Fecha de Modificación')),
            ],
            options={
                'verbose_name': 'Instructor',
                'verbose_name_plural': 'Instructores',
            },
        ),
    ]
