from django.contrib import admin
# Modelos de ESTA app (protocolos)
from .models import TipoProtocolo, Protocolo

# Modelos de la app 'formularios' que se usarán como Inlines
from formularios.models import (
    FormularioDenuncia,
    FichaEntrevista,
    Derivacion,
    InformeConcluyente,
    Apelacion,
    ResolucionApelacion,
    EncuestaBullying,

    RiesgoSuicidaAnexo1,
    RiesgoSuicidaAnexo2,
    RiesgoSuicidaAnexo3,
    RiesgoSuicidaAnexo4,
    RiesgoSuicidaAnexo5,
)

# --- Define las clases Inline para CADA formulario ---
# (Estas ya las tenías bien definidas en admin1.py)

class FormularioDenunciaInline(admin.StackedInline):
    model = FormularioDenuncia
    can_delete = False # Evita que se borre el formulario desde el protocolo
    extra = 0 # No muestra formularios vacíos extra para añadir

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

# --- Inlines para Riesgo Suicida ---

class RiesgoSuicidaAnexo1Inline(admin.StackedInline):
    model = RiesgoSuicidaAnexo1
    can_delete = False
    extra = 0

class RiesgoSuicidaAnexo2Inline(admin.StackedInline):
    model = RiesgoSuicidaAnexo2
    can_delete = False
    extra = 0

class RiesgoSuicidaAnexo3Inline(admin.StackedInline):
    model = RiesgoSuicidaAnexo3
    can_delete = False
    extra = 0

class RiesgoSuicidaAnexo4Inline(admin.StackedInline):
    model = RiesgoSuicidaAnexo4
    can_delete = False
    extra = 0

class RiesgoSuicidaAnexo5Inline(admin.StackedInline):
    model = RiesgoSuicidaAnexo5
    can_delete = False
    extra = 0

# --- Configuración del Admin para el modelo Protocolo ---

@admin.register(Protocolo)
class ProtocoloAdmin(admin.ModelAdmin):
    # Campos a mostrar en la lista de protocolos
    list_display = ('id', 'tipo', 'creador', 'estado', 'fecha_creacion')
    # Filtros disponibles en la barra lateral
    list_filter = ('tipo', 'creador', 'estado')
    # Campos por los que se puede buscar
    search_fields = ('id', 'creador__username', 'tipo__nombre')

    # --- MÉTODO CLAVE para mostrar los inlines correctos ---
    def get_inlines(self, request, obj=None):
        """
        Devuelve la lista de clases Inline apropiada según el tipo
        del objeto Protocolo (obj) que se está viendo.
        """
        # Nombres de los protocolos que usan el flujo original de 7 pasos
        protocolos_tipo_1 = [
            "Acoso Escolar", "Drogas y Alcohol", "Agresión o Connotación Sexual",
            "Vulneración de derechos", "Discriminación arbitraria", "Violencia física o psicológica"
        ]

        if obj: # Si estamos viendo/editando un protocolo existente
            if obj.tipo.nombre == "Riesgo suicida":
                # Mostrar solo los inlines de Riesgo Suicida
                return [
                    RiesgoSuicidaAnexo1Inline,
                    RiesgoSuicidaAnexo2Inline,
                    RiesgoSuicidaAnexo3Inline,
                    RiesgoSuicidaAnexo4Inline,
                    RiesgoSuicidaAnexo5Inline,
                    ]
            
            elif obj.tipo.nombre in protocolos_tipo_1:
                # Mostrar los inlines del flujo original
                 return [
                    FormularioDenunciaInline,
                    FichaEntrevistaInline,
                    DerivacionInline,
                    InformeConcluyenteInline,
                    ApelacionInline,
                    ResolucionApelacionInline,
                    EncuestaBullyingInline
                    ]
            # Puedes añadir más elif obj.tipo.nombre == "Otro Tipo": return [OtrosInlines] aquí

        # Si es un protocolo nuevo (obj=None) o el tipo no coincide con ninguno,
        # no mostramos ningún inline por defecto.
        return []

# --- Configuración del Admin para TipoProtocolo (sin cambios) ---
@admin.register(TipoProtocolo)
class TipoProtocoloAdmin(admin.ModelAdmin):
    list_display = ('nombre',) # Muestra el nombre en la lista