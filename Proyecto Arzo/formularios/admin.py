from django.contrib import admin
# ¡Importamos los modelos de ESTA app!
from .models import (
    FormularioDenuncia,
    FichaEntrevista,
    Derivacion,
    InformeConcluyente,
    Apelacion,
    ResolucionApelacion,
    EncuestaBullying,
)

# Registramos cada modelo de formulario para que se pueda ver y editar
# individualmente en el panel de administración.
admin.site.register(FormularioDenuncia)
admin.site.register(FichaEntrevista)
admin.site.register(Derivacion)
admin.site.register(InformeConcluyente)
admin.site.register(Apelacion)
admin.site.register(ResolucionApelacion)
admin.site.register(EncuestaBullying)