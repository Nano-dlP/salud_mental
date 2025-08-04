from django.urls import path
from django.contrib.auth import views as auth_views

from .views import PersonaCreateView, PersonaListView
from . import views

app_name = 'persona'

urlpatterns = [
    path('institucion/', PersonaListView.as_view(), name='persona_list'),
    path('persona/nueva/', PersonaCreateView.as_view(), name='persona_create'),
    #path('isntitucion/editar/<int:pk>/', InstitucionUpdateView.as_view(), name='institucion_edit'),
    #path('institucion/detalle/<int:pk>/', InstitucionDetailView.as_view(), name='institucion_detail'),
    
]
