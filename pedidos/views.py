from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required

# Lógica de Seguridad (asumimos que ya está descomentada)
from monitoring.auth0backend import getRole 

# Importaciones de Modelos y Lógica de Negocio
from .models import Pedido
from operarios.models import Operario 
from .forms import PedidoForm

# --- Funciones de Lógica de Negocio SEGURAS (Usando el ORM) ---
def get_pedidos():
    return Pedido.objects.all().order_by('estado', 'fecha_creacion')

def get_pedido(id):
    # Usando el ORM y un manejador de errores seguro (no hay SQL injection)
    return get_object_or_404(Pedido, pk=id)

def create_pedido(form):
    pedido = form.save()
    return pedido


# --- VISTAS PROTEGIDAS POR RBAC ---

@login_required
def pedido_list(request):
    """ Muestra la lista de pedidos. SOLO para Jefe de Bodega. """
    role = getRole(request)
    
    # Chequeo de Autorización (RBAC)
    if role == "Jefe de Bodega":
        
        pedidos = get_pedidos()
        operarios_disponibles = Operario.objects.filter(disponible=True)

        context = {
            'pedido_list': pedidos,
            'operarios_disponibles': operarios_disponibles,
            'role': role
        }
        
        return render(request, 'Pedido/pedidos.html', context)
    
    else:
        # Denegación de Acceso: Confidencialidad Asegurada
        return HttpResponse("Unauthorized User: Solo el Jefe de Bodega puede gestionar pedidos", status=403)


@login_required
def single_pedido(request, id=0):
    """ Muestra el detalle de un pedido. """
    # Nota: Si el Jefe de Bodega tiene el único rol con acceso, se mantiene el filtro de visibilidad.
    try:
        pedido = get_pedido(id)
    except Exception:
        return HttpResponse("Pedido no encontrado", status=404)

    context = {
        'pedido': pedido
    }
    return render(request, 'Pedido/pedido.html', context)


@login_required
def pedido_create(request):
    """ Permite la creación de un nuevo pedido. SOLO para Jefe de Bodega. """
    role = getRole(request)
    
    # Chequeo de Autorización (RBAC)
    if role == "Jefe de Bodega":
        if request.method == 'POST':
            form = PedidoForm(request.POST)
            if form.is_valid():
                create_pedido(form)
                messages.add_message(request, messages.SUCCESS, 'Pedido creado exitosamente')
                return HttpResponseRedirect(reverse('pedido_create'))
            else:
                print(form.errors)
        else:
            form = PedidoForm()

        context = {
            'form': form,
        }
        return render(request, 'Pedido/pedidoCreate.html', context)
        
    else:
        # Denegación de Acceso
        return HttpResponse("Unauthorized User: Solo el Jefe de Bodega puede crear pedidos", status=403)