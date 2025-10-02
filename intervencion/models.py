from django.db import models

from expediente.models import Expediente
from profesional.models import Profesional

class TipoIntervencion(models.Model):
    tipo_intervencion = models.CharField(max_length=100, verbose_name=("Tipo de intervención"), blank=True, null=True)
    estado = models.BooleanField(default=True)
    
    def __str__(self):
        return self.tipo_intervencion
    
    class Meta:
        verbose_name = 'Tipo de intervención'
        verbose_name_plural = 'Tipos de intervenciones'

class Intervencion(models.Model):
    expediente = models.ForeignKey(Expediente, on_delete=models.CASCADE, related_name='intervencion_expediente')
    profesional = models.ForeignKey(Profesional, on_delete=models.CASCADE, related_name='intervencion_profesional')
    tipo_intervencion = models.ForeignKey(TipoIntervencion, on_delete=models.CASCADE, related_name='intervencion_tipo_intervencion')
    fecha_intervencion = models.DateField('Fecha de la intervención', auto_now=False, auto_now_add=False, blank=True, null=True)
    observacion = models.TextField('Observaciones', blank=True, null=True)

    def __str__(self):
        return f"Intervención {self.id} - {self.tipo_intervencion} - {self.expediente}"
    
    class Meta:
        verbose_name = 'Intervención'
        verbose_name_plural = 'Intervenciones'
        ordering = ['-fecha_intervencion']

