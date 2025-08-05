from django.contrib import admin
from .models import TipoSolicitud, GrupoEtario,  ResumenIntervencion, TipoPatrocinio, MedioIngreso

admin.site.register(TipoSolicitud)
admin.site.register(GrupoEtario)
admin.site.register(ResumenIntervencion)
admin.site.register(TipoPatrocinio)
admin.site.register(MedioIngreso)


# Register your models here.

