from django.db import models
from operarios.models import Operario # Importar para la FK

class Pedido(models.Model):
    descripcion = models.CharField(max_length=255)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(
        max_length=50,
        choices=[('PENDIENTE', 'Pendiente'), ('ASIGNADO', 'Asignado'), ('COMPLETO', 'Completo')],
        default='PENDIENTE'
    )
    operario_asignado = models.ForeignKey(
        Operario,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='pedidos_asignados'
    )

    def __str__(self):
        return f"Pedido #{self.id}: {self.descripcion} - {self.estado}"