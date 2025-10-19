from django.contrib import admin
from .models import (
    TipoProtocolo,
    Protocolo,
    FormularioDenuncia,
    FichaEntrevista,
    Derivacion,
    InformeConcluyente,
    Apelacion,
    ResolucionApelacion,
    EncuestaBullying,
)

# Inlines para mostrar los formularios dentro de Protocolo
class FormularioDenunciaInline(admin.StackedInline):
    model = FormularioDenuncia
    can_delete = False
    extra = 0

class FichaEntrevistaInline(admin.StackedInline):
    model = FichaEntrevista
    can_delete = False
    extra = 0

class DerivacionInline(admin.StackedInline):
    model = Derivacion
    can_delete = False
    extra = 0

class InformeConcluyenteInline(admin.StackedInline):
    model = InformeConcluyente
    can_delete = False
    extra = 0

class ApelacionInline(admin.StackedInline):
    model = Apelacion
    can_delete = False
    extra = 0

class ResolucionApelacionInline(admin.StackedInline):
    model = ResolucionApelacion
    can_delete = False
    extra = 0

class EncuestaBullyingInline(admin.StackedInline):
    model = EncuestaBullying
    can_delete = False
    extra = 0

@admin.register(Protocolo)
class ProtocoloAdmin(admin.ModelAdmin):
    # Ajustado: eliminar 'created_at' que no existe.
    list_display = ('id', 'tipo', 'creador')
    list_filter = ('tipo', 'creador')
    search_fields = ('id',)
    inlines = [
        FormularioDenunciaInline,
        FichaEntrevistaInline,
        DerivacionInline,
        InformeConcluyenteInline,
        ApelacionInline,
        ResolucionApelacionInline,
        EncuestaBullyingInline,
    ]

# Registrar modelos individuales para acceso rápido
admin.site.register(TipoProtocolo)
admin.site.register(FormularioDenuncia)
admin.site.register(FichaEntrevista)
admin.site.register(Derivacion)
admin.site.register(InformeConcluyente)
admin.site.register(Apelacion)
admin.site.register(ResolucionApelacion)
admin.site.register(EncuestaBullying)