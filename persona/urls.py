from django.urls import path
from django.contrib.auth import views as auth_views

from .views import PersonaCreateView, PersonaListView, PersonaDetailView, PersonaUpdateView
from . import views

app_name = 'persona'

urlpatterns = [
    path('persona/', PersonaListView.as_view(), name='persona_list'),
    path('persona/nueva/', PersonaCreateView.as_view(), name='persona_create'),
    path('persona/editar/<int:pk>/', PersonaUpdateView.as_view(), name='persona_edit'),
    path('persona/detalle/<int:pk>/', PersonaDetailView.as_view(), name='persona_detail'),
    
]
