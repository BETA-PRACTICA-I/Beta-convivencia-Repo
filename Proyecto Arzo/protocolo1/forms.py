from django import forms
from .models import (FormularioDenuncia, FichaEntrevista, Derivacion,
    InformeConcluyente, Apelacion, ResolucionApelacion, EncuestaBullying)

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