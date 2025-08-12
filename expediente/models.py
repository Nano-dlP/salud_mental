from django.db import models
from django.utils import timezone
from core.models import Sede, Rol
from persona.models import Persona
from institucion.models import Institucion


# Create your models here.
class TipoSolicitud(models.Model):
    tipo_solicitud = models.CharField(max_length=50, verbose_name="Tipo de Solicitud")
    estado = models.BooleanField(default=True)
    
    def __str__(self):
        return self.tipo_solicitud
    
    class Meta:
        verbose_name = 'Tipo de solicitud'
        verbose_name_plural = 'Tipos de solicitudes'


class GrupoEtario(models.Model):
    grupo_etario = models.CharField(max_length=50, verbose_name="Grupo Etario")
    estado = models.BooleanField(default=True)
    
    def __str__(self):
        return self.grupo_etario
    
    class Meta:
        verbose_name = 'Grupo Etario'
        verbose_name_plural = 'Grupos etarios'


    
class ResumenIntervencion(models.Model):
    resumen_intervencion = models.CharField(max_length=50, verbose_name="Resumen de Intervención")
    estado = models.BooleanField(default=True)
    
    def __str__(self):
        return self.resumen_intervencion    
    
    class Meta:
        verbose_name = 'Resumen de Intervención'
        verbose_name_plural = 'Resumenes de intervenciones'


    
class TipoPatrocinio(models.Model):
    tipo_patrocinio = models.CharField(max_length=50, verbose_name="Tipo de Patrocinio")
    estado = models.BooleanField(default=True)
    
    def __str__(self):
        return self.tipo_patrocinio

    class Meta:
        verbose_name = 'Tipo de patrocinio'
        verbose_name_plural = 'Tipos de patrocinios'



class MedioIngreso(models.Model):
    medio_ingreso = models.CharField(max_length=50, verbose_name="Medio de Ingreso")
    estado = models.BooleanField(default=True)
    
    def __str__(self):
        return self.medio_ingreso
    
    class Meta:
        verbose_name = 'Medio de Ingreso'
        verbose_name_plural = 'Medios de Ingresos'



class EstadoExpediente(models.Model):
    estado_expediente = models.CharField(max_length=100, verbose_name="Estado el expediente")
    estado = models.BooleanField(default=True)
    
    def __str__(self):
        return self.estado_expediente
    
    class Meta:
        verbose_name = 'Estado del expediente'
        verbose_name_plural = 'Estado de los expedientes'


class Expediente(models.Model):
    numero = models.PositiveIntegerField("Número de expediente")
    anio = models.PositiveIntegerField("Año del expediente", default=2025)
    abreviatura = models.ForeignKey(Sede, on_delete=models.CASCADE, related_name='expediente_abreviatura_sede')
    fecha_creacion = models.DateField("Fecha de creación", auto_now_add=True)
    identificador = models.CharField("Identificador del expediente", max_length=100, unique=True, editable=False)

    sede = models.ForeignKey(Sede, on_delete=models.PROTECT, verbose_name='Sede')
    medio_ingreso = models.ForeignKey(MedioIngreso, on_delete=models.CASCADE, blank=True, null=True)
    expediente_fisico = models.BooleanField(default=False)
    tipo_solicitud = models.ForeignKey(TipoSolicitud, on_delete=models.CASCADE)
    grupo_etario = models.ForeignKey(GrupoEtario, related_name='expediente_grupo_etario', on_delete=models.CASCADE)
    tipo_patrocinio = models.ForeignKey(TipoPatrocinio, on_delete=models.CASCADE, null=True, blank=True)
    resumen_intervencion = models.ForeignKey(ResumenIntervencion, on_delete=models.CASCADE, blank=True, null=True)

    edad_persona = models.PositiveIntegerField(blank=True, null=True)
    situacion_habitacional = models.CharField(max_length=255, blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)

    estado = models.BooleanField("Estado", default=True)

    class Meta:
        unique_together = ('numero', 'anio', 'abreviatura')
        ordering = ['-anio', '-numero']

    def save(self, *args, **kwargs):
        if not self.pk:
            today = timezone.now().date()
            self.anio = today.year
            # Tomar la abreviatura desde la sede si no está cargada
            if not self.abreviatura and self.sede:
                self.abreviatura = self.sede.abreviatura.upper()
            # Obtener el último número para esa sede y año
            ultimo = Expediente.objects.filter(
                sede=self.sede,
                anio=self.anio
            ).order_by('-numero').first()
            self.numero = (ultimo.numero + 1) if ultimo else 1
            # Crear identificador
            self.identificador = f"{self.abreviatura}-{str(self.numero).zfill(5)}-{self.anio}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.identificador


class ExpedientePersona(models.Model):
    expediente = models.ForeignKey(Expediente, on_delete=models.CASCADE, related_name='expedientepersona_expediente')
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE, related_name='expedientepersona_persona')
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE, related_name='expedientepersona_rol')


class ExpedienteInstitucion(models.Model):
    expediente = models.ForeignKey(Expediente, on_delete=models.CASCADE, related_name='expedienteinstitucion_expediente')
    institucion = models.ForeignKey(Institucion, on_delete=models.CASCADE, related_name='expedienteinstitucion_institucion')
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE, related_name='expedienteinstitucion_rol')
