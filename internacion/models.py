from django.db import models
from core.models import Auditoria


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
    
    
class Internacion(Auditoria):
    pass