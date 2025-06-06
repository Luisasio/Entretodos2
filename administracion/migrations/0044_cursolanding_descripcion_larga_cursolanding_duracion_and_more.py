# Generated by Django 5.1.7 on 2025-06-01 22:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administracion', '0043_cursolanding'),
    ]

    operations = [
        migrations.AddField(
            model_name='cursolanding',
            name='descripcion_larga',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='cursolanding',
            name='duracion',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='cursolanding',
            name='programa_pdf',
            field=models.FileField(blank=True, null=True, upload_to='curso_landing/programas/'),
        ),
        migrations.AddField(
            model_name='cursolanding',
            name='responsable',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='cursolanding',
            name='subtitulo',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
