# Generated by Django 5.1.7 on 2025-03-22 04:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administracion', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='curso',
            name='hora_fin',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='curso',
            name='hora_inicio',
            field=models.TimeField(blank=True, null=True),
        ),
    ]
