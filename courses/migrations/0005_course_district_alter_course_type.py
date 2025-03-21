# Generated by Django 5.0.6 on 2024-07-21 20:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0004_feature'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='district',
            field=models.CharField(blank=True, max_length=250, null=True, unique=True, verbose_name='Distrito'),
        ),
        migrations.AlterField(
            model_name='course',
            name='type',
            field=models.CharField(choices=[('Virtual', 'Virtual'), ('Presencial', 'Presencial'), ('Grabada', 'Grabada'), ('Personalizado', 'Personalizado')], max_length=50, verbose_name='Tipo'),
        ),
    ]
