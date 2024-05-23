from django.db import migrations

def insert_default_groups(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Group.objects.create(name='administrador')

class Migration(migrations.Migration):

    dependencies = [
        ('index', '0002_alter_usuario_table'),
    ]

    operations = [
        migrations.RunPython(insert_default_groups),
    ]
