# Generated by Django 5.0.3 on 2024-05-16 02:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('consultas', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='consulta',
            old_name='diagnostico',
            new_name='indicacion',
        ),
        migrations.RemoveField(
            model_name='consulta',
            name='indicaciones',
        ),
    ]