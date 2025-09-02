from django.db import models
from django.db.models import Q

class PersonaManagers(models.Manager):
    
    def buscar_persona(self, buscar_persona):
        if not buscar_persona:  # Si viene vacío o None
            return self.none()  # devuelve queryset vacío
        return self.filter(
            Q(apellido__icontains=buscar_persona) |
            Q(nombre__icontains=buscar_persona) |
            Q(numero_documento__icontains=buscar_persona)
        )
