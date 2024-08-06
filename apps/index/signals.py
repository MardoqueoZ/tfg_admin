from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group
from apps.index.models import Usuario

@receiver(post_save, sender=Usuario)
def asignar_grupo_usuario(sender, instance, created, **kwargs):
    # Asignar el grupo de "usuario" al usuario recién creado
    if created:
        usuario = Group.objects.get(name='usuario')
        instance.groups.add(usuario)