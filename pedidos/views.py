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
        
        # Nota: La base de datos sigue sin tener las tablas de Operario y Pedido, 
        # pero esto solo afecta el contenido, no el cargador de templates.
        try:
            pedidos = get_pedidos()
            operarios_disponibles = Operario.objects.filter(disponible=True)
        except Exception as e:
            # Si hay un error de DB (como la tabla no existe), renderiza un error amigable.
            if "no such table" in str(e):
                return HttpResponse(f"Error de Base de Datos: Las tablas de Pedidos y Operarios no existen. Ejecuta 'python manage.py migrate'. Detalles: {e}", status=500)
            raise e

        context = {
            'pedido_list': pedidos,
            'operarios_disponibles': operarios_disponibles,
            'role': role
        }
        
        # 🎯 CORRECCIÓN APLICADA AQUÍ: Cambiado 'Pedido/pedidos.html' a 'pedidos/pedidos.html'
        return render(request, 'pedidos/pedidos.html', context)
    
    else:
        # Denegación de Acceso: Confidencialidad Asegurada
        return HttpResponse("Unauthorized User: Solo el Jefe de Bodega puede gestionar pedidos", status=403)


@login_required
def single_pedido(request, id=0):
    """ Muestra el detalle de un pedido. """
    role = getRole(request)
    
    if role != "Jefe de Bodega":
        # Denegación de Acceso: Si Operario intenta acceder al detalle
        return HttpResponse("Unauthorized User: Solo el Jefe de Bodega puede ver el detalle de pedidos", status=403)

    try:
        pedido = get_pedido(id)
    except Exception:
        return HttpResponse("Pedido no encontrado", status=404)

    context = {
        'pedido': pedido
    }
    
    # 🎯 CORRECCIÓN APLICADA AQUÍ: Cambiado 'Pedido/pedido.html' a 'pedidos/pedido.html'
    return render(request, 'pedidos/pedido.html', context)


@login_required
def pedido_create(request):
    """ Permite la creación de un nuevo pedido. SOLO para Jefe de Bodega. """
    role = getRole(request)
    
    if role == "Jefe de Bodega":
        if request.method == 'POST':
            form = PedidoForm(request.POST)
            if form.is_valid():
                create_pedido(form)
                messages.add_message(request, messages.SUCCESS, 'Pedido creado exitosamente')
                # Redirige a la lista de pedidos después de guardar.
                return HttpResponseRedirect(reverse('pedido_list')) 
            else:
                print(form.errors)
        else:
            form = PedidoForm()

        context = {
            'form': form,
        }
        
        # 🎯 CORRECCIÓN APLICADA AQUÍ: Cambiado 'Pedido/pedidoCreate.html' a 'pedidos/pedidoCreate.html'
        return render(request, 'pedidos/pedidoCreate.html', context)
        
    else:
        return HttpResponse("Unauthorized User: Solo el Jefe de Bodega puede crear pedidos", status=403)
    

# pedidos/views.py

@login_required
def pedido_assign(request, pedido_id):
    role = getRole(request)
    
    if role != "Jefe de Bodega":
        return HttpResponse("Acceso denegado.", status=403)

    if request.method == 'POST':
        pedido = get_object_or_404(Pedido, pk=pedido_id)
        operario_id = request.POST.get('operario_id')

        if operario_id:
            try:
                operario = Operario.objects.get(pk=operario_id, disponible=True)
                
                pedido.operario_asignado = operario
                pedido.estado = 'ASIGNADO' # O el estado que corresponda
                pedido.save()

                operario.disponible = False
                operario.save()

                messages.success(request, f'Pedido {pedido_id} asignado a {operario.nombre}.')
            except Operario.DoesNotExist:
                messages.error(request, 'El operario no existe o ya no está disponible.')
            
        return redirect('pedido_list')
    
    return HttpResponse("Método no permitido.", status=405)
    