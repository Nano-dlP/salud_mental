from django.contrib import admin

from .models import Pais, Provincia, Genero, Nivel_Educativo, Tipo_Documento, Sede, Localidad
# Register your models here.

admin.site.register(Provincia)
admin.site.register(Pais)
admin.site.register(Genero)
admin.site.register(Nivel_Educativo)
admin.site.register(Tipo_Documento)
admin.site.register(Sede)
admin.site.register(Localidad)
admin.site.site_header = 'Salud Mental Admin'
admin.site.site_title = 'Salud Mental Admin Portal'
admin.site.index_title = 'Bienvenido al portal de administración de Salud Mental'
admin.site.empty_value_display = 'N/A'

