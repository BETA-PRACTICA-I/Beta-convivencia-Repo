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
        fields = '__all__'
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 5}),
            'testigos': forms.Textarea(attrs={'rows': 3}),
            'rol': forms.Select(attrs={'id': 'id_rol'}),
            'curso_denunciado_extra': forms.TextInput(attrs={'id': 'id_curso_denunciado'}),
            'asignatura': forms.TextInput(attrs={'id': 'id_asignatura'}),
            'otro_rol': forms.TextInput(attrs={'id': 'id_otro_rol'}),
            'fecha_hora': forms.TextInput(attrs={'type': 'datetime-local'}),
        }

class FichaEntrevistaForm(forms.ModelForm):
    class Meta:
        model = FichaEntrevista
        fields = '__all__'
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
        fields = '__all__'
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

class ApelacionForm(forms.ModelForm):
    class Meta:
        model = Apelacion
        fields = '__all__'
        widgets = {
            'fecha_recepcion': forms.DateInput(attrs={'type': 'date'}),
            'texto_apelacion': forms.Textarea(attrs={'rows': 6}),
        }

class ResolucionApelacionForm(forms.ModelForm):
    class Meta:
        model = ResolucionApelacion
        fields = '__all__'
        widgets = {
            'fecha_recepcion': forms.DateInput(attrs={'type': 'date'}),
            'resolucion': forms.Textarea(attrs={'rows': 5}),
            'fundamentos': forms.Textarea(attrs={'rows': 6}),
        }

class EncuestaBullyingForm(forms.ModelForm):
    class Meta:
        model = EncuestaBullying
        fields = '__all__'
        widgets = {
            'comentario_adicional': forms.Textarea(attrs={'rows': 4}),
        }



