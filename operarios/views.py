from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from operarios.forms import OperarioForm
from .models import Operario 
from .decorators import allowed_users

# VISTA: Lista de Operarios
@login_required
def operario_list(request):
    """ Muestra la lista de operarios activos. Accesible por cualquier usuario autenticado. """
    # Lógica de negocio segura (usando ORM)
    operarios = Operario.objects.all().order_by('disponible', 'nombre')

    context = {
        'operario_list': operarios,
        'titulo': "Personal Activo de Bodega"
    }
    
    return render(request, 'Operario/operarios.html', context)

# NUEVA VISTA: Crear Operario (Solo para Jefe de Bodega)
@login_required(login_url='login')
@allowed_users(allowed_roles=['jefe_bodega']) # <-- SOLO Jefe de Bodega
def operario_create(request):
    """ Permite al Jefe de Bodega crear un nuevo Operario. """
    
    form = OperarioForm()

    if request.method == 'POST':
        form = OperarioForm(request.POST)
        if form.is_valid():
            form.save()
            # Redirige a la lista de operarios después de la creación exitosa
            return redirect('operario_list') 
    
    context = {
        'form': form,
        'titulo': "Crear Nuevo Operario"
    }
    
    # Renderiza la nueva plantilla 'Operario/operarioCreate.html'
    return render(request, 'Operario/operarioCreate.html', context)