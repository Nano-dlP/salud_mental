from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views

from .views import ProfesionalCreateView, ProfesionalListView, ProfesionalUpdateView, ProfesionalDeleteView
from . import views

app_name = 'profesional'

urlpatterns = [
    path('profesional/', ProfesionalListView.as_view(), name='profesional_list'),
    path('profesional/nuevo/', ProfesionalCreateView.as_view(), name='profesional_create'),
    path("profesionales/<int:pk>/editar/", ProfesionalUpdateView.as_view(), name="profesional_update"),
    path("profesionales/<int:pk>/eliminar/", ProfesionalDeleteView.as_view(), name="profesional_delete"),

]
