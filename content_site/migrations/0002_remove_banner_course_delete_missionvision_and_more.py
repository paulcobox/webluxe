# Generated by Django 5.0.6 on 2024-09-25 00:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content_site', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='banner',
            name='course',
        ),
        migrations.DeleteModel(
            name='MissionVision',
        ),
        migrations.AddField(
            model_name='testimony',
            name='imagen',
            field=models.ImageField(blank=True, upload_to='images/testimony', verbose_name='Imagen'),
        ),
        migrations.DeleteModel(
            name='Banner',
        ),
    ]