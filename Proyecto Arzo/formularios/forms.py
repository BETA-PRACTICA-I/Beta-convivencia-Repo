from django import forms
from .models import (
    ArmasAnexo1, AutolesionAnexo1, EstudianteMadrePadreFicha0, EstudianteMadrePadreFicha1, EstudianteMadrePadreFicha2, FormularioDenuncia, FichaEntrevista, Derivacion,
    InformeConcluyente, Apelacion, ResolucionApelacion,
    EncuestaBullying,   #Protocolos 1-6
    
    RiesgoSuicidaAnexo1, RiesgoSuicidaAnexo2, RiesgoSuicidaAnexo3,
    RiesgoSuicidaAnexo4, RiesgoSuicidaAnexo5,   #Protocolo 7
    ReconocimientoIdentidad, #Protocolo 12
    ActaReunionIdentidad, #Protocolo 12
    FichaAccidenteEscolar,  #Protocolo 8
    SalidaPedagogicaAnexo1, #Protocolo 13
    DesregulacionEmocional, #Protocolo 14
    MediacionInformacion, MediacionActaFinal, MediacionSolicitud, # Protocolo 15
    EvidenciaExtra,
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


class EvidenciaExtraForm(forms.ModelForm):
    class Meta:
        model = EvidenciaExtra
        exclude = ('protocolo', 'creado_en')
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),
            'descripcion': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Descripción opcional'}),
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

class EstudianteMadrePadreFicha0Form(forms.ModelForm):
    """
    Formulario para el Protocolo 11 (Paso 1: Ficha 0).
    Combina la Citación y la Constancia de concurrencia en un solo formulario.
    """
    class Meta:
        model = EstudianteMadrePadreFicha0
        
        # Excluimos 'protocolo' porque se asignará en la vista
        exclude = ('protocolo',)
        
        # Widgets para que los campos de fecha usen el calendario HTML
        widgets = {
            'fecha_citacion': forms.DateInput(attrs={'type': 'date'}),
            'fecha_concurrencia_citada': forms.DateInput(attrs={'type': 'date'}),
        }
        
        # Etiquetas personalizadas para que coincidan EXACTAMENTE con las imágenes
        labels = {
            'nombre_estudiante': 'Nombre Alumna/o',
            'curso': 'Curso',
            'fecha_citacion': 'Con fecha...',
            'nombre_apoderado_citado': 'Se cita al apoderado...',
            'medio_citacion': 'A través de... (teléfono, indicar número/agenda escolar)',
            'fecha_concurrencia_citada': 'A fin de que concurra al Establecimiento el día...de...del...',
            'funcionario_que_cita': 'Nombre y firma del funcionario que cita',
            'nombre_apoderado_concurre': 'Yo... (Nombre Apoderado)',
            'rut_apoderado_concurre': '...cédula nacional de identidad número...',
        }

class EstudianteMadrePadreFicha1Form(forms.ModelForm):
    """
    Formulario para la Ficha 1: REGISTRO DE ENTREVISTA CON APODERADO
    """
    class Meta:
        model = EstudianteMadrePadreFicha1
        exclude = ('protocolo',) # Excluimos el protocolo, se asignará en la vista
        
        widgets = {
            'fecha_entrevista': forms.DateInput(
                attrs={'type': 'date'},
                format='%Y-%m-%d' # Asegura que el widget HTML5 funcione
            ),
            'individualizacion_apoderado': forms.TextInput(
                attrs={'placeholder': 'Nombre completo, RUT, parentesco...'}
            ),
            'motivo_entrevista': forms.Textarea(
                attrs={'rows': 4, 'placeholder': 'Motivo por el cual se cita al apoderado'}
            ),
            'aspectos_relevantes': forms.Textarea(
                attrs={'rows': 10, 'placeholder': 'Resumen de la conversación, acuerdos, observaciones...'}
            ),
            'nombre_firma_funcionario': forms.TextInput(
                attrs={'placeholder': 'Nombre completo del funcionario'}
            ),
            'nombre_firma_apoderado': forms.TextInput(
                attrs={'placeholder': 'Nombre completo del apoderado'}
            ),
        }

class EstudianteMadrePadreFicha2Form(forms.ModelForm):
    """
    Formulario para la Ficha 2: Cierre de Protocolo
    """
    class Meta:
        model = EstudianteMadrePadreFicha2
        exclude = ('protocolo',) # Excluimos la FK al protocolo
        
        # Widgets para que los campos de fecha usen el selector de calendario
        widgets = {
            'fecha_informe_final': forms.DateInput(
                attrs={'type': 'date'},
                format='%Y-%m-%d'
            ),
            'fecha_cierre_protocolo': forms.DateInput(
                attrs={'type': 'date'},
                format='%Y-%m-%d'
            ),
            # Aseguramos que los campos de texto no sean gigantes
            'nombre_estudiante': forms.TextInput(attrs={'placeholder': 'Nombre completo del estudiante'}),
            'curso': forms.TextInput(attrs={'placeholder': 'Ej: 3° Medio B'}),
            'quien_elabora_informe': forms.TextInput(attrs={'placeholder': 'Nombre y cargo'}),
            'funcionario_recibe_informe': forms.TextInput(attrs={'placeholder': 'Nombre y cargo'}),
            'firma_funcionario_elabora': forms.TextInput(attrs={'placeholder': 'Nombre completo del funcionario'}),
            'firma_rector': forms.TextInput(attrs={'placeholder': 'Nombre completo del Rector/a'}),
        }

class SalidaPedagogicaAnexo1Form(forms.ModelForm):
    class Meta:
        model = SalidaPedagogicaAnexo1
        exclude = ['protocolo']
        widgets = {
            'actividad_fecha_hora': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'actividad_niveles_cursos_participantes': forms.TextInput(attrs={'placeholder': 'Ej: 8vo Básico A, 30 estudiantes'}),
            'listado_estudiantes': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Un estudiante por línea: Nombre, Curso, Fono Apoderado'}),
            'listado_docentes': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Un docente por línea: Nombre, Asignatura, Fono'}),
            'listado_apoderados': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Un apoderado por línea: Nombre, Curso, Fono'}),
            'cursos_sin_profesor': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Un curso por línea: Curso, Día, Hora, Reemplaza'}),
            'profesores_con_clases': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Listar profesores afectados'}),
            'observaciones': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if 'class' not in field.widget.attrs:
                field.widget.attrs['class'] = 'form-control'

class DesregulacionEmocionalForm(forms.ModelForm):
    class Meta:
        model = DesregulacionEmocional
        exclude = ['protocolo']
        widgets = {
            'fecha_hora': forms.DateTimeInput(
                attrs={'type': 'datetime-local'},
                format='%Y-%m-%dT%H:%M'
            ),
            'descripcion_situacion': forms.Textarea(attrs={'rows': 10}),
            
            # --- Widgets Etapa 1 ---
            'etapa1_otros_descripcion': forms.TextInput(
                attrs={'placeholder': 'Especifique qué "Otros"...'}
            ),
            'etapa1_responsables_generales': forms.Textarea(
                attrs={
                    'rows': 4, 
                    'placeholder': 'Anote aquí a todos los responsables de las estrategias marcadas en Etapa 1...'
                }
            ),
            
            # --- Widgets Etapa 2 ---
            'etapa2_otros_descripcion': forms.TextInput(
                attrs={'placeholder': 'Especifique qué "Otros"...'}
            ),
            'etapa2_responsables_generales': forms.Textarea(
                attrs={
                    'rows': 4, 
                    'placeholder': 'Anote aquí a todos los responsables de las estrategias marcadas en Etapa 2...'
                }
            ),

            # --- Widgets Etapa 3 ---
            'etapa3_otros_descripcion': forms.TextInput(
                attrs={'placeholder': 'Especifique qué "Otros"...'}
            ),
            'etapa3_responsables_generales': forms.Textarea(
                attrs={
                    'rows': 4, 
                    'placeholder': 'Anote aquí a todos los responsables de las estrategias marcadas en Etapa 3...'
                }
            ),
        }
        help_texts = {
            'nombre_firma_2': '',
        }
        labels = {
            # Ocultamos todas las etiquetas "Otros"
            'etapa1_otros_descripcion': '', 
            'etapa2_otros_descripcion': '',
            'etapa3_otros_descripcion': '',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Aceptamos el formato que genera el input "datetime-local" del navegador
        self.fields['fecha_hora'].input_formats = ['%Y-%m-%dT%H:%M', '%Y-%m-%d %H:%M:%S']

class MediacionSolicitudForm(forms.ModelForm):
    class Meta:
        model = MediacionSolicitud
        exclude = ('protocolo',)
        widgets = {
            'motivo_solicitud': forms.Textarea(attrs={'rows': 4}),
            'antecedentes': forms.Textarea(attrs={'rows': 4}),
        }

class MediacionInformacionForm(forms.ModelForm):
    # Opciones para los BooleanFields
    CHOICES_SI_NO_NS = [(True, 'Sí'), (False, 'No'), (None, 'No Aplica/No Informado')]

    info_nombre_solicitante = forms.TypedChoiceField(
        choices=CHOICES_SI_NO_NS, widget=forms.RadioSelect, coerce=lambda x: x == 'True' if x != 'None' else None,
        label="Se informó Nombre Solicitante"
    )
    info_motivo = forms.TypedChoiceField(
        choices=CHOICES_SI_NO_NS, widget=forms.RadioSelect, coerce=lambda x: x == 'True' if x != 'None' else None,
        label="Se informó Motivo de Mediación"
    )
    info_fecha_hora = forms.TypedChoiceField(
        choices=CHOICES_SI_NO_NS, widget=forms.RadioSelect, coerce=lambda x: x == 'True' if x != 'None' else None,
        label="Se informó Fecha y Hora"
    )
    info_voluntario = forms.TypedChoiceField(
        choices=CHOICES_SI_NO_NS, widget=forms.RadioSelect, coerce=lambda x: x == 'True' if x != 'None' else None,
        label="Se señaló que el proceso es voluntario"
    )

    class Meta:
        model = MediacionInformacion
        exclude = ('protocolo',)
        widgets = {
            'verificacion_detalle': forms.Textarea(attrs={'rows': 3}),
            'respuesta_solicitado': forms.RadioSelect,
            'medio_informado': forms.RadioSelect,
        }

class MediacionActaFinalForm(forms.ModelForm):
    acuerdo_logrado = forms.TypedChoiceField(
        choices=[(True, 'Sí, se logró un acuerdo (Acta de Conciliación)'), (False, 'No, no se logró acuerdo (Acta Frustrada)')],
        widget=forms.RadioSelect,
        coerce=lambda x: x == 'True',
        label="Resultado del Proceso"
    )
    
    class Meta:
        model = MediacionActaFinal
        exclude = ('protocolo',)
        widgets = {
            'fecha_acta': forms.DateInput(attrs={'type': 'date'}),
            'partes_individualizadas': forms.Textarea(attrs={'rows': 3}),
            
            'acuerdo_1_actividades': forms.Textarea(attrs={'rows': 3}),
            'acuerdo_2_actividades': forms.Textarea(attrs={'rows': 3}),
            'acuerdo_3_actividades': forms.Textarea(attrs={'rows': 3}),
            
            'motivo_frustrado': forms.Textarea(attrs={'rows': 4}),
        }