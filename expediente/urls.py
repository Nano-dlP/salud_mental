from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views

from .views import DemandaEspontaneaCreateView, ExpedienteListView, MedioIngresoSelectView, OficioCreateView
from . import views

app_name = 'expediente'

urlpatterns = [
    path('expediente/', ExpedienteListView.as_view(), name='expediente_list'),
    path('expediente/seleccionar-medio/', MedioIngresoSelectView.as_view(), name='medio_ingreso_select'),
    path('expediente/crear/<int:medio_id>/', DemandaEspontaneaCreateView.as_view(), name='expediente_create_with_medio'),
    path('expediente/crear_oficio/<int:medio_id>/', OficioCreateView.as_view(), name='expediente_create_oficio'),
    
    
]
