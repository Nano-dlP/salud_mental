# usuario/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser

    # Campos que se ven en el panel de lista (listado de usuarios)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'telefono')
    search_fields = ('username', 'email', 'first_name', 'last_name')

    # Secciones del formulario de edición
    fieldsets = UserAdmin.fieldsets + (
        (_('Información adicional'), {
            'fields': ('sede', 'telefono', 'direccion', 'localidad', 'dni', 'foto_perfil'),
        }),
    )

    # Campos extra al crear un usuario
    add_fieldsets = UserAdmin.add_fieldsets + (
        (_('Información adicional'), {
            'fields': ('sede', 'telefono', 'direccion', 'localidad', 'dni', 'foto_perfil'),
        }),
    )

admin.site.register(CustomUser, CustomUserAdmin)
