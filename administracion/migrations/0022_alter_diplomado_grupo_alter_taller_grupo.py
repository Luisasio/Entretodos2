# Generated by Django 5.1.7 on 2025-05-14 18:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administracion', '0021_alter_curso_grupo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='diplomado',
            name='grupo',
            field=models.CharField(max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='taller',
            name='grupo',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
