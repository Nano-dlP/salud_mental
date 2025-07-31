from django.contrib import admin

# Register your models here.

from .models import Usuario

# Register the Profesional model with the admin site
admin.site.register(Usuario)