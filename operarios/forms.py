# operarios/forms.py

from django import forms
from .models import Operario

class OperarioForm(forms.ModelForm):

    class Meta:
        model = Operario
        fields = [
            'nombre',
            'identificador_interno',
            'disponible',
        ]
        labels = {
            'nombre': 'Nombre Completo',
            'identificador_interno': 'ID de Empleado',
            'disponible': '¿Está Disponible para Asignación?',
        }