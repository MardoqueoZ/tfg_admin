# Generated by Django 5.0.3 on 2024-05-15 21:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('mascotas', '0003_remove_mascota_edad_mascota_fecha_nacimiento'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tratamiento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('descripcion', models.TextField()),
                ('fecha_inicio', models.DateField()),
                ('estado', models.CharField(max_length=100)),
                ('veterinario', models.CharField(max_length=100)),
                ('fecha_fin', models.DateField(blank=True, null=True)),
                ('mascota', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mascotas.mascota')),
            ],
        ),
    ]
