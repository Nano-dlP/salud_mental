from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views

from .views import ExpedienteListView, ExpedienteCreateView
from . import views

app_name = 'expediente'

urlpatterns = [
    path('expediente/', ExpedienteListView.as_view(), name='expediente_list'),
    path('expediente/nuevo/', ExpedienteCreateView.as_view(), name='expediente_create'),
    
    
]
