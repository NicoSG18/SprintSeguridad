from django.contrib import messages  
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from monitoring.auth0backend import getRole
from operarios.forms import OperarioForm
from .models import Operario 


@login_required
def operario_list(request):    
    operarios = Operario.objects.all().order_by('disponible', 'nombre')

    context = {
        'operario_list': operarios,
        'titulo': "Personal Activo de Bodega"
    }
    
    return render(request, 'operarios/operarios.html', context)


@login_required
def operario_create(request):
    role = getRole(request)
    #  Chequeo de Autorización RBAC
    if role == "Jefe de Bodega":
        if request.method == 'POST':
            form = OperarioForm(request.POST)
            if form.is_valid():
                form.save()
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