from django.db import models


# Create your models here.
class TipoSolicitud(models.Model):
    tipo_solicitud = models.CharField(max_length=50, verbose_name="Tipo de Solicitud")
    estado = models.BooleanField(default=True)
    
    def __str__(self):
        return self.tipo_solicitud
    
    
class GrupoEtario(models.Model):
    grupo_etario = models.CharField(max_length=50, verbose_name="Grupo Etario")
    estado = models.BooleanField(default=True)
    
    def __str__(self):
        return self.grupo_etario
    
    
class ResumenIntervencion(models.Model):
    resumen_intervencion = models.CharField(max_length=50, verbose_name="Resumen de Intervención")
    estado = models.BooleanField(default=True)
    
    def __str__(self):
        return self.resumen_intervencion    
    
    
class TipoPatrocinio(models.Model):
    tipo_patrocinio = models.CharField(max_length=50, verbose_name="Tipo de Patrocinio")
    estado = models.BooleanField(default=True)
    
    def __str__(self):
        return self.tipo_patrocinio


class MediosIngreso(models.Model):
    medios_ingreso = models.CharField(max_length=50, verbose_name="Medios de Ingreso")
    estado = models.BooleanField(default=True)
    
    def __str__(self):
        return self.medios_ingreso

    
class Expediente(models.Model):
    pass    
            