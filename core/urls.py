from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views

from .views import ProvinciaListView, IndexView, ProvinciaCreate

app_name = 'core'

urlpatterns = [
    path('provincia/', ProvinciaListView.as_view(), name='provincia_list'),
    path('', IndexView.as_view(), name='index'),
    path('provincia_nuevo/', ProvinciaCreate.as_view(), name='provincia_create'),
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
]
