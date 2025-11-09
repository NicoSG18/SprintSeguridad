# operarios/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # Ruta para crear un nuevo operario
    path('crear/', views.operario_create, name='operario_create'),
    
    # Ruta base para /operarios/ (Lista de Operarios)
    path('', views.operario_list, name='operario_list'),
]