from django.urls import path

from .views import IntervencionCreateView
from . import views

app_name = 'intervencion'

urlpatterns = [
    path('intervencion/', IntervencionCreateView.as_view(), name='intervencion_create'),
    
    
]
