from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from .forms import VariableForm
from .logic.variable_logic import get_variables, get_variable, create_variable
from django.contrib.auth.decorators import login_required
# Descomentar cuando se cree el archivo monitoring/auth0backend.py
#from monitoring.auth0backend import getRole

@login_required
def variable_list(request):
    role = getRole(request)
    if role == "Gerencia Campus":
        variables = get_variables()
        context = {
            'variable_list': variables
        }
        return render(request, 'Variable/variables.html', context)
    else:
        return HttpResponse("Unauthorized User")

@login_required
def single_variable(request, id=0):
    variable = get_variable(id)
    context = {
        'variable': variable
    }
    return render(request, 'Variable/variable.html', context)

@login_required
def variable_create(request):
    role = getRole(request)
    if role == "Gerencia Campus":
        if request.method == 'POST':
            form = VariableForm(request.POST)
            if form.is_valid():
                create_variable(form)
                messages.add_message(request, messages.SUCCESS, 'Successfully created variable')
                return HttpResponseRedirect(reverse('variableCreate'))
            else:
                print(form.errors)
        else:
            form = VariableForm()

        context = {
            'form': form,
        }
        return render(request, 'Variable/variableCreate.html', context)
    else:
        return HttpResponse("Unauthorized User")
