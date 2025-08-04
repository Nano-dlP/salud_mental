from django.contrib import admin
from .models import TipoSolicitud, GrupoEtario,  ResumenIntervencion, TipoPatrocinio, MediosIngreso

admin.site.register(TipoSolicitud)
admin.site.register(GrupoEtario)
admin.site.register(ResumenIntervencion)
admin.site.register(TipoPatrocinio)
admin.site.register(MediosIngreso)


# Register your models here.

