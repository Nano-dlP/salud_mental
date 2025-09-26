from django.urls import path
from . import views

app_name = 'internacion'

urlpatterns = [
    path('internacion/listar/', views.InternacionListView.as_view(), name='internacion_list'),
    path('internacion/crear/', views.InternacionCreateView.as_view(), name='internacion_create'),
]