# Generated by Django 5.1.7 on 2025-03-22 04:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administracion', '0002_curso_hora_fin_curso_hora_inicio'),
    ]

    operations = [
        migrations.AddField(
            model_name='curso',
            name='cupos',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
