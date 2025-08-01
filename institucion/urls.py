from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views

from .views import InstitucionCreateView, InstitucionListView, InstitucionUpdateView

app_name = 'institucion'

urlpatterns = [
    path('institucion/', InstitucionListView.as_view(), name='institucion_list'),
    path('institucion/nuevo/', InstitucionCreateView.as_view(), name='institucion_create'),
    path('isntitucion/editar/<int:pk>/', InstitucionUpdateView.as_view(), name='institucion_edit'),
    
]
