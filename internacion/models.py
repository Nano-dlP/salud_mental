from django.db import models

from expediente.models import ExpedienteInstitucion

# Create your models here.
class MotivoInternacion(models.Model):
    motivo_internacion = models.CharField(max_length=50, verbose_name="Motivo de Internación")
    estado = models.BooleanField(default=True)

    def __str__(self):
        return self.motivo_internacion
    

class MotivoAlta(models.Model):
    motivo_alta = models.CharField(max_length=50, verbose_name="Motivo de Alta")
    estado = models.BooleanField(default=True)
    
    def __str__(self):
        return self.motivo_alta
    
    
class ModalidadSuicidio(models.Model):
    modalidad_suicidio = models.CharField(max_length=50, verbose_name="Modalidad de Suicidio")
    estado = models.BooleanField(default=True)
    
    def __str__(self):
        return self.modalidad_suicidio
    
    
class TipoAdiccion(models.Model):
    tipo_adiccion = models.CharField(max_length=50, verbose_name="Tipo de Adicción")
    estado = models.BooleanField(default=True)
    
    def __str__(self):
        return self.tipo_adiccion
    
    
class Internacion(models.Model):
    expediente_institucion = models.ForeignKey(ExpedienteInstitucion, on_delete=models.CASCADE, related_name='internacion_expedienteinstitucion', blank=True, null=True)
    fecha_internacion = models.DateField('Fecha de internación', auto_now=False, auto_now_add=False, blank=True, null=True) 
    fecha_alta = models.DateField('Fecha de alta o derivación', auto_now=False, auto_now_add=False, blank=True, null=True) 
    motivo_internacion = models.ForeignKey(MotivoInternacion, on_delete=models.CASCADE, related_name='internacion_motivo_internacion', blank=True, null=True)
    motivo_alta = models.ForeignKey(MotivoAlta, on_delete=models.CASCADE, related_name='internacion_motivo_alta', blank=True, null=True)
    requisitos = models.CharField('Requisitos', max_length=50, blank=True, null=True)
    intento_suicidio = models.BooleanField('Intento de suicidio?', default=False)
    modalidad_suicidio = models.ForeignKey(ModalidadSuicidio, on_delete=models.CASCADE, related_name='internacion_modalidad_suicidio', blank=True, null=True)
    posse_adiccion = models.BooleanField('Posee adicciones?', default=False)
    tipo_adiccion = models.ForeignKey(TipoAdiccion, on_delete=models.CASCADE, related_name='internacion_tipo_adiccion', blank=True, null=True)
    fecha_cumplimiento = models.DateTimeField('Fecha de cumplimiento', auto_now=False, auto_now_add=False, blank=True, null=True)
    