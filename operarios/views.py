from django.contrib import messages  
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

# Lógica de Seguridad
from monitoring.auth0backend import getRole

# Modelos y Formularios
from operarios.forms import OperarioForm
from .models import Operario 

# --- VISTA: Lista de Operarios ---

@login_required
def operario_list(request):
    """ Muestra la lista de operarios activos. Accesible por cualquier usuario autenticado. """
    
    operarios = Operario.objects.all().order_by('disponible', 'nombre')

    context = {
        'operario_list': operarios,
        'titulo': "Personal Activo de Bodega"
    }
    
    return render(request, 'operarios/operarios.html', context)

# --- VISTA: Crear Operario ---

@login_required
def operario_create(request):
    """ Permite la creación de un nuevo operario. SOLO para Jefe de Bodega (RBAC). """
    
    role = getRole(request)

    # 🔑 Chequeo de Autorización (RBAC)
    if role == "Jefe de Bodega":
        if request.method == 'POST':
            form = OperarioForm(request.POST)
            if form.is_valid():
                form.save()
                # La función messages.success ahora funciona correctamente
                messages.success(request, 'Operario creado exitosamente') 
                return redirect('operario_list')
            
        else:
            form = OperarioForm()

        context = {
            'form': form,
        }
        return render(request, 'operarios/operarioCreate.html', context)
        
    else:
        return HttpResponse("Unauthorized User: Solo el Jefe de Bodega puede crear operarios", status=403)