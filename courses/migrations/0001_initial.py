# Generated by Django 5.0.6 on 2024-07-16 03:18

import ckeditor.fields
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('instructors', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250, unique=True, verbose_name='Titulo')),
                ('schedule', models.CharField(max_length=250, unique=True, verbose_name='Horario')),
                ('month', models.IntegerField(choices=[(1, 'Enero'), (2, 'Febrero'), (3, 'Marzo'), (4, 'Abril'), (5, 'Mayo'), (6, 'Junio'), (7, 'Julio'), (8, 'Agosto'), (9, 'Septiembre'), (10, 'Octubre'), (11, 'Noviembre'), (12, 'Diciembre')], max_length=50, verbose_name='Mes')),
                ('price', models.IntegerField(verbose_name='Precio de Curso')),
                ('image', models.ImageField(blank=True, upload_to='images/course', verbose_name='Imagen Card')),
                ('image_fiz', models.ImageField(blank=True, upload_to='images/course', verbose_name='Imagen Ficha Inferior Izq')),
                ('image_fid', models.ImageField(blank=True, upload_to='images/course', verbose_name='Imagen Ficha Inferior Der')),
                ('video', models.FileField(blank=True, upload_to='videos/course', verbose_name='Video Ficha')),
                ('body', ckeditor.fields.RichTextField(verbose_name='Contenido')),
                ('place', ckeditor.fields.RichTextField(verbose_name='Lugar')),
                ('is_active', models.BooleanField(default=False, verbose_name='¿Activo?')),
                ('is_like', models.BooleanField(default=False, verbose_name='Curso que puede gustar')),
                ('type', models.CharField(choices=[('Virtual', 'Virtual'), ('Presencial', 'Presencial'), ('Grabada', 'Grabada'), ('Privada', 'Privada')], max_length=50, verbose_name='Tipo')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Creación')),
                ('modified_date', models.DateTimeField(auto_now=True, verbose_name='Fecha de Modificación')),
                ('instructor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='course', to='instructors.instructors', verbose_name='Profesor')),
            ],
            options={
                'verbose_name': 'Curso',
                'verbose_name_plural': 'Cursos',
            },
        ),
    ]