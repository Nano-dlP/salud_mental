from django.contrib import admin
from .models import TipoSolicitud, GrupoEtario,  ResumenIntervencion, TipoPatrocinio, MedioIngreso, EstadoArchivo

admin.site.register(TipoSolicitud)
admin.site.register(GrupoEtario)
admin.site.register(ResumenIntervencion)
admin.site.register(TipoPatrocinio)
admin.site.register(MedioIngreso)
admin.site.register(EstadoArchivo)

# Register your models here.

