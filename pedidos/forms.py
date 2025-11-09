from django import forms
from .models import Pedido

class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = [
            'descripcion',
            'estado',
        ]
        labels = {
            'descripcion': 'Descripción del Pedido',
            'estado': 'Estado Inicial',
        }