from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views

from .views import InstitucionCreate, InstitucionListView

app_name = 'institucion'

urlpatterns = [
    path('institucion/', InstitucionListView.as_view(), name='institucion_list'),
    path('institucion_nuevo/', InstitucionCreate.as_view(), name='institucion_create'),
    
]
