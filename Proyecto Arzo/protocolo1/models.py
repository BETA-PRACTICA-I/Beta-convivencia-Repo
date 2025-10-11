from django.db import models
from django.utils import timezone


class FormularioDenuncia(models.Model):
    # Datos del denunciante
    nombre_denunciante = models.CharField(max_length=100)
    run_denunciante = models.CharField(max_length=12)
    telefono_denunciante = models.CharField(max_length=20)
    domicilio_denunciante = models.CharField(max_length=200)
    correo_denunciante = models.EmailField()

    # Datos del estudiante
    nombre_estudiante = models.CharField(max_length=100)
    curso_estudiante = models.CharField(max_length=50)
    run_estudiante = models.CharField(max_length=12)
    domicilio_estudiante = models.CharField(max_length=200)

    # Datos del denunciado
    nombre_denunciado = models.CharField(max_length=100)
    curso_denunciado = models.CharField(max_length=50, )

    # Rol del denunciado (solo uno)
    ROL_CHOICES = [
        ('Estudiante', 'Estudiante'),
        ('Apoderado', 'Apoderado'),
        ('Profesor Jefe', 'Profesor Jefe'),
        ('Profesor de Asignatura', 'Profesor de Asignatura'),
        ('Asistente', 'Asistente'),
        ('Otro', 'Otro'),
    ]
    rol = models.CharField(max_length=30, choices=ROL_CHOICES)

    # Campos adicionales según el rol
    curso_denunciado_extra = models.CharField(max_length=50, blank=True)
    asignatura = models.CharField(max_length=100, blank=True)
    otro_rol = models.CharField(max_length=100, blank=True)

    # Antecedentes
    fecha_hora = models.CharField(max_length=100)
    lugar = models.CharField(max_length=100)

    # Testigos
    testigos = models.CharField(max_length=500)

    # Descripción
    descripcion = models.CharField(max_length=1000)

class FichaEntrevista(models.Model):
    numero_entrevista = models.CharField(max_length=20)
    fecha_hora = models.CharField(max_length=100)

    nombre_entrevistado = models.CharField(max_length=100)
    run_entrevistado = models.CharField(max_length=12)
    telefono_entrevistado = models.CharField(max_length=20)
    domicilio_entrevistado = models.CharField(max_length=200)
    correo_entrevistado = models.EmailField()

    contenido_entrevista = models.TextField()

    firma_entrevistado = models.CharField(max_length=100)
    firma_entrevistador = models.CharField(max_length=100)


# ============ FORMULARIO 3: Cierre/Acta de Investigación ============
class DerivacionForm(forms.Form):
    tipo_derivacion = forms.MultipleChoiceField(
        choices=DERIVACION_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        label="Seleccione las derivaciones"
    )

    # Campos para las 3 primeras opciones
    fecha = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'}),
        label="Fecha"
    )
    institucion = forms.CharField(
        required=False,
        widget=forms.TextInput(),
        label="Institución"
    )
    funcionario_responsable = forms.CharField(
        required=False,
        widget=forms.TextInput(),
        label="Funcionario Responsable"
    )
    firma_funcionario = forms.CharField(
        required=False,
        widget=forms.TextInput(),
        label="Firma del Funcionario Responsable"
    )
    respaldo = forms.FileField(
        required=False,
        widget=forms.ClearableFileInput(attrs={'accept': '.pdf,.doc,.docx,image/*'}),
        label="Adjuntar documentación de respaldo"
    )

    # Campos para "Otras"
    tipo_medida = forms.CharField(
        required=False,
        widget=forms.TextInput(),
        label="Tipo de medida"
    )
    descripcion = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'rows': 3}),
        label="Descripción"
    )
    funcionario_responsable_otras = forms.CharField(
        required=False,
        widget=forms.TextInput(),
        label="Funcionario Responsable (Otras)"
    )
    firma_funcionario_otras = forms.CharField(
        required=False,
        widget=forms.TextInput(),
        label="Firma del Funcionario Responsable (Otras)"
    )
    respaldo_otras = forms.FileField(
        required=False,
        widget=forms.ClearableFileInput(attrs={'accept': '.pdf,.doc,.docx,image/*'}),
        label="Adjuntar documentación de respaldo (Otras)"
    )

# ============ FORMULARIO 4: Informe Concluyente ============
class InformeConcluyente(models.Model):
    protocolo = models.CharField(max_length=100, default='PENDIENTE')
    fecha_informe = models.DateField(default=timezone.now)
    nombre_encargado = models.CharField(max_length=100, default='')
    run_encargado = models.CharField(max_length=12, default='')
    cargo_encargado = models.CharField(max_length=100, default='')
    correo_encargado = models.EmailField(default='')

    iniciales = models.CharField(max_length=10, default='')
    curso_involucrado = models.CharField(max_length=50, default='')
    tipo_involucrado = models.CharField(max_length=20, default='')

    tipo_accion = models.CharField(max_length=100, default='')
    fecha_accion = models.DateField(default=timezone.now)
    descripcion_accion = models.TextField(default='')
    conclusiones = models.TextField(default='')

    sancion = models.CharField(max_length=100, default='')
    fecha_inicio_sancion = models.DateField(null=True, )
    fecha_termino_sancion = models.DateField(null=True, )
    descripcion_sancion = models.TextField(default='')

    medida = models.CharField(max_length=100, default='', blank=True)
    fecha_inicio_medida = models.DateField(blank=True, )
    fecha_termino_medida = models.DateField(blank=True, )
    descripcion_medida = models.TextField(default='', blank=True)

    medio_citacion_afectado = models.CharField(max_length=100, default='')
    fecha_citacion_afectado = models.DateField(null=True, )
    lugar_entrevista_afectado = models.CharField(max_length=200, default='')
    hora_entrevista_afectado = models.TimeField(null=True, )
    firma_reclamante = models.CharField(max_length=100, default='')

    fecha_envio = models.DateField(null=True, )
    hora_envio = models.TimeField(null=True, )
    empresa_correos = models.CharField(max_length=100, default='')
    nombre_firma_remitente = models.CharField(max_length=100, default='')

    medio_citacion_denunciado = models.CharField(max_length=100, default='')
    fecha_citacion_denunciado = models.DateField(null=True, )
    lugar_entrevista_denunciado = models.CharField(max_length=200, default='')
    hora_entrevista_denunciado = models.TimeField(null=True, )
    firma_denunciado = models.CharField(max_length=100, default='')

    nombre_firma_encargado = models.CharField(max_length=100, default='')

# ============ FORMULARIO 5: Apelación ============
class Apelacion(models.Model):
    protocolo = models.CharField(max_length=100, default='PENDIENTE')
    fecha_recepcion = models.DateField(default=timezone.now)
    nombre_apelante = models.CharField(max_length=100, default='')
    run_apelante = models.CharField(max_length=12, default='')
    curso_o_cargo = models.CharField(max_length=100, default='')
    domicilio = models.CharField(max_length=200, default='')
    correo = models.EmailField(default='')
    texto_apelacion = models.TextField(default='')

# ============ FORMULARIO 6: Resolución de Apelación ============
class ResolucionApelacion(models.Model):
    protocolo = models.CharField(max_length=100, default='PENDIENTE')
    fecha_recepcion = models.DateField(default=timezone.now)
    medio_envio = models.CharField(max_length=100, default='')
    resolucion = models.TextField(default='')
    fundamentos = models.TextField(default='')
    rector_o_sostenedor = models.CharField(max_length=100, default='')

# ============ FORMULARIO 7: Encuesta ============
FRECUENCIAS = [
    ('4', 'Todos los días'),
    ('3', '2-3 veces por semana'),
    ('2', '2-3 veces por mes'),
    ('1', 'Una vez al mes'),
    ('0', 'Nunca'),
]
class EncuestaBullying(models.Model):
    estudiante_iniciales = models.CharField(max_length=10, default='')
    curso = models.CharField(max_length=50, default='')
    sobrenombres = models.CharField(max_length=1, choices=FRECUENCIAS, default='0')
    burlas = models.CharField(max_length=1, choices=FRECUENCIAS, default='0')
    agresion_fisica = models.CharField(max_length=1, choices=FRECUENCIAS, default='0')
    amenazas = models.CharField(max_length=1, choices=FRECUENCIAS, default='0')
    presion_dinero = models.CharField(max_length=1, choices=FRECUENCIAS, default='0')
    presion_hacer_cosas = models.CharField(max_length=1, choices=FRECUENCIAS, default='0')
    garabatos = models.CharField(max_length=1, choices=FRECUENCIAS, default='0')
    esconden_cosas = models.CharField(max_length=1, choices=FRECUENCIAS, default='0')
    danan_cosas = models.CharField(max_length=1, choices=FRECUENCIAS, default='0')
    mentiras = models.CharField(max_length=1, choices=FRECUENCIAS, default='0')
    no_me_dejan_jugar = models.CharField(max_length=1, choices=FRECUENCIAS, default='0')
    no_me_dejan_estudiar = models.CharField(max_length=1, choices=FRECUENCIAS, default='0')
    no_me_dejan_opinar = models.CharField(max_length=1, choices=FRECUENCIAS, default='0')
    miedo_venir = models.CharField(max_length=1, choices=FRECUENCIAS, default='0')
    tristeza = models.CharField(max_length=1, choices=FRECUENCIAS, default='0')
    soledad = models.CharField(max_length=1, choices=FRECUENCIAS, default='0')
    molestia_sexual = models.CharField(max_length=1, choices=FRECUENCIAS, default='0')
    comentario_adicional = models.TextField(default='')
