import os
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from .models import ExpedienteDocumento


@receiver(post_delete, sender=ExpedienteDocumento)
def eliminar_archivo_documento(sender, instance, **kwargs):
    """
    Elimina el archivo físico cuando se borra el objeto.
    """
    if instance.archivo and instance.archivo.path:
        if os.path.isfile(instance.archivo.path):
            os.remove(instance.archivo.path)


@receiver(pre_save, sender=ExpedienteDocumento)
def reemplazar_archivo_documento(sender, instance, **kwargs):
    """
    Si se sube un nuevo archivo en lugar de otro, elimina el anterior.
    """
    if not instance.pk:
        # Si es un objeto nuevo, no hay nada que eliminar
        return

    try:
        documento_anterior = ExpedienteDocumento.objects.get(pk=instance.pk)
    except ExpedienteDocumento.DoesNotExist:
        return

    # Si el archivo cambió
    if documento_anterior.archivo and documento_anterior.archivo != instance.archivo:
        if os.path.isfile(documento_anterior.archivo.path):
            os.remove(documento_anterior.archivo.path)
