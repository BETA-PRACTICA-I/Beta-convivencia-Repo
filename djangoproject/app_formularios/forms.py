from django import forms
from .models import FormularioDenuncia
from .models import FichaEntrevista

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
            'fecha': forms.DateInput(attrs={'type': 'date'}),
            'hora': forms.TimeInput(attrs={'type': 'time'}),
            'contenido_entrevista': forms.Textarea(attrs={'rows': 5}),
        }
