# Generated by Django 5.0.6 on 2024-08-02 04:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0008_remove_course_month_course_image_banner_top_and_more'),
        ('leads', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lead',
            name='course_of_interest',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='lead', to='courses.course', verbose_name='Curso de Interes'),
        ),
    ]
