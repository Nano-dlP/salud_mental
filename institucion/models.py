from django.db import models

from core.models import Localidad

# Create your models here.

class TipoInstitucion(models.Model):
    tipo_institucion = models.CharField(max_length=100, verbose_name='Tipo de Institución', blank=True, null=True)
    estado = models.BooleanField(default=True, verbose_name='Estado')

    def __str__(self):
        return self.tipo_institucion

    class Meta:
        verbose_name = 'Tipo de Institución'
        verbose_name_plural = 'Tipos de Instituciones'


class Institucion(models.Model):
    institucion = models.CharField(max_length=100, verbose_name='Institución', blank=True, null=True)
    domicilio_calle = models.CharField(max_length=50, verbose_name='Domicilio Calle', blank=True, null=True)
    domicilio_numero = models.CharField(max_length=10, verbose_name='Domicilio Número', blank=True, null=True)
    domicilio_piso = models.CharField(max_length=10, verbose_name='Domicilio Piso', blank=True, null=True)
    domicilio_depto = models.CharField(max_length=10, verbose_name='Domicilio Depto', blank=True, null=True)
    localidad = models.ForeignKey(Localidad, on_delete=models.CASCADE, verbose_name='Localidad', blank=True, null=True, related_name='institucion_localidad', default=None)
    telefono = models.CharField(max_length=20, verbose_name='Teléfono', blank=True, null=True)
    email = models.EmailField(max_length=254, verbose_name='Email', blank=True, null=True)
    cuit = models.CharField(max_length=20, verbose_name='CUIT', blank=True, null=True)
    tipo_institucion = models.ForeignKey(TipoInstitucion, on_delete=models.CASCADE, verbose_name='Tipo de Institución', blank=True, null=True, related_name='instituciones_tipo_institucion', default=None)
    estado = models.BooleanField(default=True, verbose_name='Estado')

    def __str__(self):
        return self.institucion

    class Meta:
        verbose_name = 'Institución'
        verbose_name_plural = 'Instituciones'



