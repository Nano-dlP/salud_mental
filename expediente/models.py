from django.db import models

from core.models import Localidad
from django.utils import timezone


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


class MedioIngreso(models.Model):
    medio_ingreso = models.CharField(max_length=50, verbose_name="Medio de Ingreso")
    estado = models.BooleanField(default=True)
    
    def __str__(self):
        return self.medio_ingreso
    
    class Meta:
        verbose_name = 'Medio de Ingreso'
        verbose_name_plural = 'Medios de Ingresos'


class EstadoArchivo(models.Model):
    estado_archivo = models.CharField(max_length=50, verbose_name="Estado del Archivo")
    estado = models.BooleanField(default=True)
    
    def __str__(self):
        return self.estado_archivo
    
    class Meta:
        verbose_name = 'Estado del archivo'
        verbose_name_plural = 'Estado de los archivos'


    
class Expediente(models.Model):
    localidad = models.ForeignKey(Localidad, on_delete=models.PROTECT, related_name='expediente_localidad')
    numero = models.PositiveIntegerField("Número de expediente")
    anio = models.PositiveIntegerField("Año del expediente", default=2025)
    identificador = models.CharField("Identificador del expediente", max_length=100, unique=True, editable=False)
    
    fecha_creacion = models.DateField("Fecha de creación", auto_now_add=True)
    fecha_de_juzgado = models.DateTimeField('Fecha del Juzgado', blank=True, null=True )
    fecha_de_recepcion = models.DateTimeField('Fecha de Recepción', blank=True, null=True )
    expediente_fisico = models.BooleanField(default=False)
    cuij = models.CharField(max_length=50, verbose_name='CUIJ', blank=True, null=True)
    clave_sisfe = models.CharField(max_length=50, verbose_name='Clave SISFE', blank=True, null=True)
    medio_ingreso = models.ForeignKey(MedioIngreso, on_delete=models.CASCADE, blank=True, null=True, related_name='expediente_medio_ingreso')
    situacion_habitacional_hist = models.CharField(max_length=100, verbose_name="Situación habitacional histórica", blank=True, null=True)
    tipo_solicitud = models.ForeignKey(TipoSolicitud, on_delete=models.CASCADE, related_name='expediente_tipo_solicitud', blank=True, null=True)
    grupo_etario = models.ForeignKey(GrupoEtario, related_name='expediente_grupo_etario', on_delete=models.CASCADE, blank=True, null=True)
    tipo_patrocinio = models.ForeignKey(TipoPatrocinio, on_delete=models.CASCADE, null=True, blank=True, related_name='expediente_resumen_intervencion')
    resumen_intervencion = models.ForeignKey(ResumenIntervencion, on_delete=models.CASCADE, blank=True, null=True, related_name='expediente_resumen_intervencion')
    
    estado = models.BooleanField("Estado", default=True)

    class Meta:
        unique_together = ('numero', 'anio', 'localidad')

    def save(self, *args, **kwargs):
        if not self.pk:  # Si es un nuevo expediente
            today = timezone.now().date()
            self.anio = today.year

            # Buscamos el último expediente de la misma localidad y año
            ultimo = Expediente.objects.filter(
                localidad=self.localidad,
                anio=self.anio
            ).order_by('-numero').first()

            self.numero = (ultimo.numero + 1) if ultimo else 1

            # Generar identificador tipo "ROS-00001-2025"
            self.identificador = f"{self.localidad.abreviatura.upper()}-{str(self.numero).zfill(5)}-{self.anio}"

        super().save(*args, **kwargs)

    def __str__(self):
        return self.identificador
    localidad = models.ForeignKey(Localidad, on_delete=models.PROTECT)
    numero = models.PositiveIntegerField("Guarda el número de expediente generado")
    anio = models.PositiveIntegerField("Guarda el año obtenido por la función", default=2025)
    abreviatura = models.CharField(max_length=4)
    identificador = models.CharField("Identificador del Expediente",  max_length=100, unique=True, editable=False)
    fecha_creacion = models.DateField("Fecha en que se creó", auto_now_add=True)
    medio_ingreso = models.ForeignKey(MedioIngreso, on_delete=models.CASCADE, blank=True, null=True)
    expediente_fisico = models.BooleanField(default=False)
    tipo_solicitud = models.ForeignKey(TipoSolicitud, on_delete=models.CASCADE)
    grupo_etario = models.ForeignKey(GrupoEtario, related_name='expdiente_grupo_etario', on_delete=models.CASCADE)
    tipo_patrocinio = models.ForeignKey(TipoPatrocinio, on_delete=models.CASCADE, null=True, blank=True)
    resumen_intervencion = models.ForeignKey(ResumenIntervencion, on_delete=models.CASCADE, blank=True, null=True)
    estado = models.BooleanField("Estado", default=True)
    
    
    def __str__(self):
        return  self.identificador

    
    class Meta:
        unique_together = ('numero', 'anio', 'abreviatura')

    def save(self, *args, **kwargs):
        if not self.pk: #Esto comprueba si el expediente es nuevo (es decir, no tiene clave primaria aún, no fue guardado). Solo ejecuta la lógica si es un nuevo expediente.
            today = timezone.now().date() #Obtiene la fecha actual y guarda el año actual en self.anio.
            self.anio = today.year
            #Busca el último expediente creado en esa localidad y en ese año, ordenado de mayor a menor por numero. Si existe un expediente anterior, se lo guarda en ultimo. Si no, ultimo será None.
            ultimo = Expediente.objects.filter(
                localidad=self.localidad,
                anio=self.anio
            ).order_by('-numero').first()

            #Si se encontró un expediente anterior, el nuevo número será uno más.
            #Si no hay ninguno anterior (es el primero del año en esa localidad), el número será 1.
            if ultimo:
                self.numero = ultimo.numero + 1
            else:
                self.numero = 1

            self.identificador = f"{self.localidad.abreviatura.upper()}-{str(self.numero).zfill(5)}-{self.anio}"

        super().save(*args, **kwargs)

    def __str__(self):
        return self.identificador
    pass