from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta

class TipoProtocolo(models.Model):
    nombre = models.CharField(max_length=200, unique=True)
    #orden = models.PositiveIntegerField(default=0, help_text="Para ordenar la lista de protocolos")
    
    def __str__(self):
        return self.nombre
    
    class Meta:
        db_table = 'protocolo1_tipoprotocolo' # <-- LÍNEA MÁGICA 1

class Protocolo(models.Model):
    tipo = models.ForeignKey(TipoProtocolo, on_delete=models.PROTECT, related_name="protocolos")
    creador = models.ForeignKey(User, on_delete=models.PROTECT, related_name="protocolos_creados")
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=50, default='En Creacion', help_text="Ej: En Creacion, Pendiente, Resuelto, Vencido")
    
    @property
    def fecha_limite(self):
        if self.fecha_creacion:
            return self.fecha_creacion + timedelta(days=15)
        return None
    def __str__(self):
        tipo_nombre = getattr(self.tipo, 'nombre', None)
        return f"Protocolo {self.id}" + (f" - {tipo_nombre}" if tipo_nombre else "")

    class Meta:
        db_table = 'protocolo1_protocolo' # <-- LÍNEA MÁGICA 2