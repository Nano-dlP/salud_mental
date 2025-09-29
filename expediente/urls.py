from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views

from .views import DemandaEspontaneaCreateView, ExpedienteListView, MedioIngresoSelectView, OficioCreateView, SecretariaCreateView, DemandaEspontaneaUpdateView, ExpedienteUpdateDispatcherView, OficioUpdateView, SecretariaUpdateView, expediente_list
from . import views

app_name = 'expediente'

urlpatterns = [
    path('expediente/', ExpedienteListView.as_view(), name='expediente_list'),
    path('expediente/seleccionar-medio/', MedioIngresoSelectView.as_view(), name='medio_ingreso_select'),
    path('expediente/crear/<int:medio_id>/', DemandaEspontaneaCreateView.as_view(), name='expediente_create_with_medio'),
    
    path('expediente/crear_oficio/<int:medio_id>/', OficioCreateView.as_view(), name='expediente_create_oficio'),
    
    path('expediente/crear_oficio_sec/<int:medio_id>/', SecretariaCreateView.as_view(), name='expediente_create'),
    path('expediente/demanda_editar/<int:pk>/', DemandaEspontaneaUpdateView.as_view(), name='demanda_espontanea_update'),
    path('expediente/oficio_editar/<int:pk>/', OficioUpdateView.as_view(), name='oficio_update'),
    path('expediente/secretaria_editar/<int:pk>/', SecretariaUpdateView.as_view(), name='secretaria_update'),
    path('expediente/editar/<int:pk>/', ExpedienteUpdateDispatcherView.as_view(), name='expediente_update'),

    path('expediente/buscar/', expediente_list, name='expediente_buscar')


    
    
]
