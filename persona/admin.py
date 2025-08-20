# persona/admin.py
from django.contrib import admin
from django.contrib.postgres.search import TrigramSimilarity
from .models import Persona

class PersonaAdmin(admin.ModelAdmin):
    search_fields = ['apellido']  # Esto solo activa búsqueda exacta

    def get_search_results(self, request, queryset, search_term):
        """Sobrescribimos para usar TrigramSimilarity"""
        if search_term:
            queryset = queryset.annotate(
                similarity=TrigramSimilarity('apellido', search_term)
            ).filter(similarity__gt=0.3).order_by('-similarity')
            return queryset, False
        return super().get_search_results(request, queryset, search_term)

admin.site.register(Persona, PersonaAdmin)
