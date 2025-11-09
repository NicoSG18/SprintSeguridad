# operarios/logic/operario_logic.py
from ..models import Operario
from django.shortcuts import get_object_or_404

def get_operarios():
    """Retorna todos los operarios, ordenados por disponibilidad."""
    queryset = Operario.objects.all().order_by('-disponible', 'nombre')
    return queryset

def get_operario(id):
    """Retorna un operario específico usando el ORM."""
    operario = get_object_or_404(Operario, pk=id)
    return operario

def create_operario(form):
    """Guarda un nuevo operario creado a través del formulario."""
    operario = form.save()
    return operario