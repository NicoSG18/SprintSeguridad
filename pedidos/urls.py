from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from . import views

urlpatterns = [
    # Lista de Pedidos (Protegida)
    path('', views.pedido_list, name='pedido_list'), 
    
    # Detalle de Pedido
    path('<int:id>/', views.single_pedido, name='single_pedido'), 
    
    # Crear Pedido (Protegida)
    path('crear/', csrf_exempt(views.pedido_create), name='pedido_create'), 
]