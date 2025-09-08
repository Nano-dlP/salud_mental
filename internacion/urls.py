from django.urls import path
from . import views

urlpatterns = [
    path('listado/', views.InternacionListView.as_view(), name='internacion_list'),
    path('crear/', views.InternacionCreateView.as_view(), name='internacion_create'),
]