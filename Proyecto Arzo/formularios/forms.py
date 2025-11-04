from django import forms
from .models import (
    ArmasAnexo1, AutolesionAnexo1, FormularioDenuncia, FichaEntrevista, Derivacion,
    InformeConcluyente, Apelacion, ResolucionApelacion,
    EncuestaBullying,   #Protocolos 1-6
    
    RiesgoSuicidaAnexo1, RiesgoSuicidaAnexo2, RiesgoSuicidaAnexo3,
    RiesgoSuicidaAnexo4, RiesgoSuicidaAnexo5,   #Protocolo 7
    ReconocimientoIdentidad, #Protocolo 12
    ActaReunionIdentidad, #Protocolo 12
    FichaAccidenteEscolar,  #Protocolo 8
    )


DERIVACION_CHOICES = [
    ('constatar_lesiones', 'Derivación a constatar lesiones'),
    ('denuncia_delito', 'Denuncia (Si es constitutivo de delito)'),
    ('tribunal_familia', 'Derivación a tribunal de familia'),
    ('otras', 'Otras'),
]


class FormularioDenunciaForm(forms.ModelForm):
    class Meta:
        model = FormularioDenuncia
        exclude = ('protocolo',)
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 5}),
            'testigos': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Nombre | Curso o Cargo | Contacto'}),
            'rol': forms.Select(attrs={'id': 'id_rol'}),
            'curso_denunciado_extra': forms.TextInput(attrs={'id': 'id_curso_denunciado'}),
            'asignatura': forms.TextInput(attrs={'id': 'id_asignatura'}),
            'otro_rol': forms.TextInput(attrs={'id': 'id_otro_rol'}),
            'fecha_hora': forms.TextInput(attrs={'type': 'datetime-local'}),
        }

class FichaEntrevistaForm(forms.ModelForm):
    class Meta:
        model = FichaEntrevista
        exclude = ('protocolo',)
        widgets = {
            'fecha_hora': forms.TextInput(attrs={'type': 'datetime-local'}),
            'contenido_entrevista': forms.Textarea(attrs={'rows':5}),
        }

class DerivacionForm(forms.Form):
    tipo_derivacion = forms.MultipleChoiceField(
        choices=DERIVACION_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        label="Seleccione las derivaciones",
        required=True
    )

    # --- Campos para 'Constatar Lesiones' ---
    fecha_lesiones = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    institucion_lesiones = forms.CharField(required=False)
    funcionario_responsable_lesiones = forms.CharField(required=False)
    firma_funcionario_lesiones = forms.CharField(required=False)
    respaldo_lesiones = forms.FileField(required=False)

    # --- Campos para 'Denuncia Delito' ---
    fecha_delito = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    institucion_delito = forms.CharField(required=False)
    funcionario_responsable_delito = forms.CharField(required=False)
    firma_funcionario_delito = forms.CharField(required=False)
    respaldo_delito = forms.FileField(required=False)
    
    # --- Campos para 'Tribunal Familia' ---
    fecha_tribunal = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    institucion_tribunal = forms.CharField(required=False)
    funcionario_responsable_tribunal = forms.CharField(required=False)
    firma_funcionario_tribunal = forms.CharField(required=False)
    respaldo_tribunal = forms.FileField(required=False)

    # --- Campos para 'Otras' ---
    tipo_medida_otras = forms.CharField(required=False, label="Tipo de medida")
    descripcion_otras = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 3}), label="Descripción")
    funcionario_responsable_otras = forms.CharField(required=False, label="Funcionario Responsable (Otras)")
    firma_funcionario_otras = forms.CharField(required=False, label="Firma del Funcionario Responsable (Otras)")
    respaldo_otras = forms.FileField(required=False, label="Adjuntar documentación de respaldo (Otras)")


class InformeConcluyenteForm(forms.ModelForm):
    class Meta:
        model = InformeConcluyente
        exclude = ('protocolo',)
        widgets = {
            'fecha_informe': forms.DateInput(attrs={'type': 'date'}),
            'fecha_accion': forms.DateInput(attrs={'type': 'date'}),
            'fecha_inicio_sancion': forms.DateInput(attrs={'type': 'date'}),
            'fecha_termino_sancion': forms.DateInput(attrs={'type': 'date'}),
            'fecha_inicio_medida': forms.DateInput(attrs={'type': 'date'}),
            'fecha_termino_medida': forms.DateInput(attrs={'type': 'date'}),
            'fecha_citacion_afectado': forms.DateInput(attrs={'type': 'date'}),
            'hora_entrevista_afectado': forms.TimeInput(attrs={'type': 'time'}),
            'fecha_envio': forms.DateInput(attrs={'type': 'date'}),
            'hora_envio': forms.TimeInput(attrs={'type': 'time'}),
            'fecha_citacion_denunciado': forms.DateInput(attrs={'type': 'date'}),
            'hora_entrevista_denunciado': forms.TimeInput(attrs={'type': 'time'}),
            'descripcion_accion': forms.Textarea(attrs={'rows': 4}),
            'conclusiones': forms.Textarea(attrs={'rows': 4}),
            'descripcion_sancion': forms.Textarea(attrs={'rows': 3}),
            'descripcion_medida': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Campos que permitimos estar vacíos en este paso (no requeridos)
        campos_no_obligatorios = [
            'estado_informe', 'fecha_envio', 'hora_envio', 'empresa_correos',
            'nombre_firma_remitente', 'medio_citacion_denunciado',
            'fecha_citacion_denunciado', 'lugar_entrevista_denunciado',
            'hora_entrevista_denunciado', 'firma_denunciado',
            'nombre_firma_encargado'
        ]
        for nombre in campos_no_obligatorios:
            if nombre in self.fields:
                self.fields[nombre].required = False

class ApelacionForm(forms.ModelForm):
    class Meta:
        model = Apelacion
        exclude = ('protocolo',)
        widgets = {
            'fecha_recepcion': forms.DateInput(attrs={'type': 'date'}),
            'texto_apelacion': forms.Textarea(attrs={'rows': 6}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # permitir que este campo esté vacío en este paso
        if 'estado_informe' in self.fields:
            self.fields['estado_informe'].required = False

class ResolucionApelacionForm(forms.ModelForm):
    class Meta:
        model = ResolucionApelacion
        exclude = ('protocolo',)
        widgets = {
            'fecha_recepcion': forms.DateInput(attrs={'type': 'date'}),
            'resolucion': forms.Textarea(attrs={'rows': 5}),
            'fundamentos': forms.Textarea(attrs={'rows': 6}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # permitir que 'estado_informe' esté vacío en este paso
        if 'estado_informe' in self.fields:
            self.fields['estado_informe'].required = False

class EncuestaBullyingForm(forms.ModelForm):
    class Meta:
        model = EncuestaBullying
        # Añade los nuevos campos a exclude si no los quieres en el formulario
        exclude = ('protocolo', 'fecha_encuesta', 'edad_estudiante', 'genero_estudiante')
        widgets = {
            'comentario_adicional': forms.Textarea(attrs={'rows': 4}),
        }

#===============================Para el protocolo 7============================#

class RiesgoSuicidaAnexo1Form(forms.ModelForm):
    class Meta:
        model = RiesgoSuicidaAnexo1
        exclude = ('protocolo',) # El sistema lo maneja, no el usuario
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),
            'hora': forms.TimeInput(attrs={'type': 'time'}),
            'relato_hechos': forms.Textarea(attrs={'rows': 5}),
        }

class RiesgoSuicidaAnexo2Form(forms.ModelForm):
    class Meta:
        model = RiesgoSuicidaAnexo2
        exclude = ('protocolo',) # El sistema lo maneja
        widgets = {
            # --- Widgets para mejorar la entrada de datos ---
            'fecha_derivacion': forms.DateInput(attrs={'type': 'date'}),
            'estudiante_fecha_nacimiento': forms.DateInput(attrs={'type': 'date'}),
            'motivo_derivacion': forms.Textarea(attrs={'rows': 4}),
            'acciones_efectuadas': forms.Textarea(attrs={'rows': 4}),

            # --- Podrías añadir placeholders o clases si usas CSS específico ---
            'establecimiento_nombre': forms.TextInput(attrs={'placeholder': 'Nombre del colegio'}),
            'profesional_deriva_nombre': forms.TextInput(attrs={'placeholder': 'Ej: Juan Pérez'}),
            'profesional_deriva_cargo': forms.TextInput(attrs={'placeholder': 'Ej: Psicólogo Educacional'}),
            'profesional_deriva_email': forms.EmailInput(attrs={'placeholder': 'ejemplo@colegio.cl'}),
            'profesional_deriva_telefono': forms.TextInput(attrs={'placeholder': '+569...'}),
            'establecimiento_contacto_email': forms.EmailInput(attrs={'placeholder': 'contacto@colegio.cl'}),
            'establecimiento_contacto_telefono': forms.TextInput(attrs={'placeholder': '+56...'}),
            'estudiante_nombre': forms.TextInput(attrs={'placeholder': 'Nombre completo'}),
            'estudiante_run': forms.TextInput(attrs={'placeholder': '12345678-9'}),
            'estudiante_edad': forms.NumberInput(attrs={'min': '0'}),
            'estudiante_curso': forms.TextInput(attrs={'placeholder': 'Ej: 8vo Básico A'}),
            'adulto_responsable_nombre': forms.TextInput(attrs={'placeholder': 'Nombre completo apoderado'}),
            'adulto_responsable_telefono': forms.TextInput(attrs={'placeholder': '+569...'}),
            'estudiante_direccion': forms.TextInput(attrs={'placeholder': 'Calle Ejemplo 123, Comuna'}),
        }

class RiesgoSuicidaAnexo3Form(forms.ModelForm):
    class Meta:
        model = RiesgoSuicidaAnexo3
        # Excluimos los campos que no debe llenar el usuario en este paso
        # (o que podríamos autocompletar en el futuro)
        exclude = ('protocolo', 'establecimiento_nombre', 'estudiante_nombre', 'estudiante_curso')

        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),
            'hora': forms.TimeInput(attrs={'type': 'time'}),
            'acciones_a_seguir': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Ej: Asistir a citación en centro de salud, supervisar en domicilio...'}),
            'apoderado_nombre': forms.TextInput(attrs={'placeholder': 'Nombre completo del apoderado'}),
            'apoderado_run': forms.TextInput(attrs={'placeholder': '12345678-9'}),
            'nombre_firma_apoderado': forms.TextInput(attrs={'placeholder': 'Nombre o firma de quien recibe...'}),
            'nombre_firma_funcionario': forms.TextInput(attrs={'placeholder': 'Nombre de quien notifica...'}),
            'cargo_funcionario': forms.TextInput(attrs={'placeholder': 'Ej: Psicólogo, Orientador...'}),
        }

class RiesgoSuicidaAnexo4Form(forms.ModelForm):
    class Meta:
        model = RiesgoSuicidaAnexo4
        # Excluimos los campos del estudiante que podríamos autocompletar
        exclude = ('protocolo', 'estudiante_nombre', 'estudiante_curso', 'profesor_jefe')

        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),
            'hora_inicio': forms.TimeInput(attrs={'type': 'time'}),
            'hora_termino': forms.TimeInput(attrs={'type': 'time'}),
            'lugar_reunion': forms.TextInput(attrs={'placeholder': 'Ej: Oficina de Orientación, Sala de reuniones...'}),

            'asistentes': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Nombre Completo - Cargo/Rol (uno por línea)'}),
            'puntos_tratados': forms.Textarea(attrs={'rows': 6}),
            'acuerdos': forms.Textarea(attrs={'rows': 6}),

            'proxima_reunion_fecha': forms.DateInput(attrs={'type': 'date'}),
            'proxima_reunion_hora': forms.TimeInput(attrs={'type': 'time'}),
            'proxima_reunion_lugar': forms.TextInput(attrs={'placeholder': 'Ej: CESFAM, Oficina Orientación...'}),

            'firma_funcionario_establecimiento': forms.TextInput(attrs={'placeholder': 'Nombre y firma...'}),
            'firma_profesional_salud': forms.TextInput(attrs={'placeholder': 'Nombre y firma...'}),
        }

class RiesgoSuicidaAnexo5Form(forms.ModelForm):
    class Meta:
        model = RiesgoSuicidaAnexo5
        # Excluimos los campos que se llenarán automáticamente
        exclude = ('protocolo', 'establecimiento_nombre', 'establecimiento_direccion', 
                   'establecimiento_telefono', 'estudiante_nombre', 'estudiante_run',
                   'estudiante_fecha_nacimiento', 'estudiante_edad', 'estudiante_curso')

        widgets = {
            'fecha_derivacion': forms.DateInput(attrs={'type': 'date'}),
            'motivo_derivacion': forms.Textarea(attrs={'rows': 6, 'placeholder': 'Describir brevemente el motivo de la derivación...'}),
            'acciones_entrevista_apoderado': forms.Textarea(attrs={'rows': 4}),
            'acciones_coordinacion_salud': forms.Textarea(attrs={'rows': 4}),
            'acciones_otras': forms.Textarea(attrs={'rows': 4}),

            'responsable_nombre': forms.TextInput(attrs={'placeholder': 'Nombre completo...'}),
            'responsable_cargo': forms.TextInput(attrs={'placeholder': 'Ej: Director, Encargado Convivencia...'}),
            'responsable_telefono': forms.TextInput(attrs={'placeholder': '+56 9 ...'}),
            'responsable_email': forms.EmailInput(attrs={'placeholder': 'correo@ejemplo.com'}),
        }

#===============================Para el protocolo 8============================#

class FichaAccidenteEscolarForm(forms.ModelForm):
    class Meta:
        model = FichaAccidenteEscolar
        exclude = ('protocolo',)

        widgets = {
            'fecha_hora_accidente': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'descripcion_accidente': forms.Textarea(attrs={'rows': 4}),
            'primeros_auxilios': forms.Textarea(attrs={'rows': 4}),
            'aislamiento_motivo': forms.Textarea(attrs={'rows': 3}),
            'traslado_fecha_hora': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
    
class SolicitudReconocimientoForm(forms.ModelForm):
    CHOICES_SI_NO = [(True, 'Sí'), (False, 'No')]

    medida_uso_nombre_social = forms.TypedChoiceField(
        label="Uso del nombre social en todos los espacios educativos",
        choices=CHOICES_SI_NO, widget=forms.RadioSelect, coerce=lambda x: x == 'True'
    )
    medida_libro_clases = forms.TypedChoiceField(
        label="Agregar en el libro de clases el nombre social de la niña, niño o adolescente y utilizar éste en cualquier otra documentación afín, como informes de personalidad, comunicaciones al apoderado, informes de especialistas del colegio, diplomas, listados públicos, etc.",
        choices=CHOICES_SI_NO, widget=forms.RadioSelect, coerce=lambda x: x == 'True'
    )
    medida_uniforme = forms.TypedChoiceField(
        label="Utilización de uniforme, ropa deportiva y/o accesorios que considere más adecuado a su identidad de género",
        choices=CHOICES_SI_NO, widget=forms.RadioSelect, coerce=lambda x: x == 'True'
    )
    medida_servicios_higienicos = forms.TypedChoiceField(
        label="Utilización de servicios higiénicos de acuerdo a las necesidades propias del proceso que estén viviendo",
        choices=CHOICES_SI_NO, widget=forms.RadioSelect, coerce=lambda x: x == 'True'
    )

    class Meta:
        model = ReconocimientoIdentidad
        exclude = ['protocolo']
        widgets = {
            'estudiante_fecha_nacimiento': forms.DateInput(attrs={'type': 'date'}),
        }
    
class ActaReunionIdentidadForm(forms.ModelForm):
    CHOICES_SI_NO = [(True, 'Sí'), (False, 'No')]
    declaracion_participa_programas = forms.TypedChoiceField(
        label="Están participando de algunos de los programas del artículo 23 de la Ley 21.120 y reglamentados en el Decreto Supremo N°3, del año 2019, del Ministerio de Desarrollo Social.",
        choices=CHOICES_SI_NO, widget=forms.RadioSelect, coerce=lambda x: x == 'True'
    )
    
    # --- INDENTACIÓN CORREGIDA: Esta clase está ahora al nivel correcto ---
    class Meta:
        model = ActaReunionIdentidad
        exclude = ['protocolo']
        widgets = {
            'fecha_reunion': forms.DateInput(attrs={'type': 'date'}),
            'fecha_impl_nombre_social': forms.DateInput(attrs={'type': 'date'}),
            'fecha_impl_libro_clases': forms.DateInput(attrs={'type': 'date'}),
            'fecha_impl_uniforme': forms.DateInput(attrs={'type': 'date'}),
            'fecha_impl_servicios_higienicos': forms.DateInput(attrs={'type': 'date'}),
            'acuerdo_nombre_social': forms.Textarea(attrs={'rows': 3}),
            'acuerdo_libro_clases': forms.Textarea(attrs={'rows': 3}),
            'acuerdo_uniforme': forms.Textarea(attrs={'rows': 3}),
            'acuerdo_servicios_higienicos': forms.Textarea(attrs={'rows': 3}),
            'declaracion_info_adicional': forms.Textarea(attrs={'rows': 3}),
        }

# --- NUEVO FORMULARIO PARA PROTOCOLO 9 ---
class ArmasAnexo1Form(forms.ModelForm):
    class Meta:
        model = ArmasAnexo1
        exclude = ('protocolo',)
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 6}),
        }

# --- Formulario Protocolo 10 (NUEVO) ---
class AutolesionAnexo1Form(forms.ModelForm):
    class Meta:
        model = AutolesionAnexo1
        fields = ['nombre_estudiante', 'curso', 'rut', 'descripcion']
        
        # Usamos los mismos widgets y placeholders que el P9 para consistencia
        widgets = {
            'nombre_estudiante': forms.TextInput(attrs={'placeholder': 'Nombre completo del estudiante'}),
            'curso': forms.TextInput(attrs={'placeholder': 'Ej: 1° Medio A'}),
            'rut': forms.TextInput(attrs={'placeholder': 'Ej: 12.345.678-9'}),
            'descripcion': forms.Textarea(attrs={'rows': 6, 'placeholder': 'Describa brevemente la situación detectada, indicadores observables, etc.'}),
        }
        
        # Etiquetas claras para el formulario
        labels = {
            'nombre_estudiante': 'Nombre del Estudiante',
            'rut': 'RUT del Estudiante',
            'descripcion': 'Descripción de la situación',
        }
