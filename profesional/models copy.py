from django.db import models
from django.contrib.auth.models import User

from core.models import Tipo_Documento, Sede, AreaProfesional, Profesion


class Profesinal(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profesional_usuario', verbose_name=("Profesinal"))
    tipo_documento = models.ForeignKey(Tipo_Documento, on_delete=models.CASCADE, verbose_name=("Documento tipo"))
    numero_documento = models.CharField(max_length=20, unique=True, verbose_name=("Número de documento"))
    profesion = models.ForeignKey(Profesion, on_delete=models.CASCADE, verbose_name=("Profesión"), related_name='profesional_profesion')
    area_profesional = models.ForeignKey(AreaProfesional, on_delete=models.CASCADE, verbose_name=("Área profesional"), related_name='profesional_area_profesional', blank=True, null=True)
    sede = models.ForeignKey(Sede, verbose_name=("Sede"), on_delete=models.CASCADE, related_name='profesional_sede')
    estado = models.BooleanField(default=True, verbose_name=("Estado"))

    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name
    
    class Meta:
        verbose_name = 'Profesinal'
        verbose_name_plural = 'Profesinales'