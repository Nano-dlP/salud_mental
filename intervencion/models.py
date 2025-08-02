from django.db import models

from core.models import Auditoria
from usuario.models import Usuario 
from expediente.models import Expediente

# Create your models here.
class TipoIntervencion(models.Model):
    tipo_intervencion = models.CharField(max_length=50, verbose_name="Tipo de Intervención")
    estado = models.BooleanField(default=True)
    
    def __str__(self):
        return self.tipo_intervencion
    
    
class Intervencion(Auditoria):
    expediente = models.ForeignKey(Expediente, on_delete=models.CASCADE, verbose_name="Expediente")
    tipo_intervencion = models.ForeignKey(TipoIntervencion, on_delete=models.CASCADE, verbose_name="Tipo de Intervención")
    fecha_intervencion = models.DateField(verbose_name="Fecha de Intervención")
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, verbose_name="Usuario")
    descripcion = models.TextField(verbose_name="Descripción de la Intervención")


    def __str__(self):
        return f"Intervención {self.id} - {self.tipo_intervencion.tipo_intervencion} - {self.fecha_intervencion}"
    

    

