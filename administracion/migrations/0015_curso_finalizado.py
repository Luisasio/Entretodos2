# Generated by Django 5.1.7 on 2025-04-12 19:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administracion', '0014_diplomado_publicado'),
    ]

    operations = [
        migrations.AddField(
            model_name='curso',
            name='finalizado',
            field=models.BooleanField(default=False),
        ),
    ]
