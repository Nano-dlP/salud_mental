from django.db import models
from django.conf import settings


from core.models import Tipo_Documento, Sede, AreaProfesional, Profesion


class Profesional(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profesional_usuario', verbose_name=("Profesional"))
    tipo_documento = models.ForeignKey(Tipo_Documento, on_delete=models.CASCADE, verbose_name=("Documento tipo"))
    profesion = models.ForeignKey(Profesion, on_delete=models.CASCADE, verbose_name=("Profesión"), related_name='profesional_profesion', null=True, blank=True)
    area_profesional = models.ForeignKey(AreaProfesional, on_delete=models.CASCADE, verbose_name=("Área profesional"), related_name='profesional_area_profesional', blank=True, null=True)
    sede = models.ForeignKey(Sede, verbose_name=("Sede"), on_delete=models.CASCADE, related_name='profesional_sede')
    estado = models.BooleanField(default=True, verbose_name=("Estado"))

    