from django.db import models

# El modelo Operario, que representa los recursos humanos de la bodega.
class Operario(models.Model):
    nombre = models.CharField(max_length=100)
    identificador_interno = models.CharField(max_length=20, unique=True)
    disponible = models.BooleanField(default=True) # Clave para el requerimiento de Bodega

    def __str__(self):
        return f"{self.nombre} ({'Disponible' if self.disponible else 'Asignado'})"