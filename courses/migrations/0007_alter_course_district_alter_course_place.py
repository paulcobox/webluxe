# Generated by Django 5.0.6 on 2024-07-28 22:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0006_alter_course_schedule'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='district',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name='Distrito'),
        ),
        migrations.AlterField(
            model_name='course',
            name='place',
            field=models.CharField(max_length=250, verbose_name='Lugar'),
        ),
    ]