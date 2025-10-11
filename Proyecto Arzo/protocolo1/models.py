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
    curso_denunciado = models.CharField(max_length=50, blank=True)

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
    lugar = models.CharField(max_length=200)

    # Testigos
    testigos = models.TextField(blank=True)

    # Descripción
    descripcion = models.TextField()

class FichaEntrevista(models.Model):
    numero_entrevista = models.CharField(max_length=20)
    fecha = models.DateField()
    hora = models.TimeField()

    nombre_entrevistado = models.CharField(max_length=100)
    run_entrevistado = models.CharField(max_length=12)
    telefono_entrevistado = models.CharField(max_length=20)
    domicilio_entrevistado = models.CharField(max_length=200)
    correo_entrevistado = models.EmailField()

    contenido_entrevista = models.TextField()

    firma_entrevistado = models.CharField(max_length=100)
    firma_entrevistador = models.CharField(max_length=100)


# ============ FORMULARIO 3: Cierre/Acta de Investigación ============
DERIVACION_CHOICES = [
    ('constatar_lesiones', 'Derivación a constatar lesiones'),
    ('denuncia_delito', 'Denuncia (Si es constitutivo de delito)'),
    ('tribunal_familia', 'Derivación a tribunal de familia'),
    ('otras', 'Otras'),
]

class Derivacion(models.Model):
    derivaciones = models.CharField(
        max_length=100,
        help_text="Separar con coma si hay más de una. Ejemplo: constatar_lesiones,denuncia_delito"
    )

    # Datos para las 3 primeras opciones
    fecha_lesiones = models.DateField(null=True, blank=True)
    institucion_lesiones = models.CharField(max_length=100, blank=True)
    funcionario_lesiones = models.CharField(max_length=100, blank=True)
    firma_lesiones = models.CharField(max_length=100, blank=True)
    respaldo_lesiones = models.FileField(upload_to='derivaciones/', null=True, blank=True)

    fecha_delito = models.DateField(null=True, blank=True)
    institucion_delito = models.CharField(max_length=100, blank=True)
    funcionario_delito = models.CharField(max_length=100, blank=True)
    firma_delito = models.CharField(max_length=100, blank=True)
    respaldo_delito = models.FileField(upload_to='derivaciones/', null=True, blank=True)

    fecha_tribunal = models.DateField(null=True, blank=True)
    institucion_tribunal = models.CharField(max_length=100, blank=True)
    funcionario_tribunal = models.CharField(max_length=100, blank=True)
    firma_tribunal = models.CharField(max_length=100, blank=True)
    respaldo_tribunal = models.FileField(upload_to='derivaciones/', null=True, blank=True)

    # Datos para "Otras"
    tipo_medida_otras = models.CharField(max_length=100, blank=True)
    descripcion_otras = models.TextField(blank=True)
    funcionario_otras = models.CharField(max_length=100, blank=True)
    firma_otras = models.CharField(max_length=100, blank=True)
    respaldo_otras = models.FileField(upload_to='derivaciones/', null=True, blank=True)

    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Derivaciones: {self.derivaciones} ({self.fecha_creacion.date()})"
    
# ============ FORMULARIO 4: Informe Concluyente ============
class InformeConcluyente(models.Model):
    protocolo = models.CharField(max_length=100, blank=True, default='PENDIENTE')
    fecha_informe = models.DateField(default=timezone.now)
    nombre_encargado = models.CharField(max_length=100, blank=True, default='')
    run_encargado = models.CharField(max_length=12, blank=True, default='')
    cargo_encargado = models.CharField(max_length=100, blank=True, default='')
    correo_encargado = models.EmailField(blank=True, default='')

    iniciales = models.CharField(max_length=10, blank=True, default='')
    curso_involucrado = models.CharField(max_length=50, blank=True, default='')
    tipo_involucrado = models.CharField(max_length=20, blank=True, default='')

    tipo_accion = models.CharField(max_length=100, blank=True, default='')
    fecha_accion = models.DateField(default=timezone.now)
    descripcion_accion = models.TextField(blank=True, default='')
    conclusiones = models.TextField(blank=True, default='')

    sancion = models.CharField(max_length=100, blank=True, default='')
    fecha_inicio_sancion = models.DateField(null=True, blank=True)
    fecha_termino_sancion = models.DateField(null=True, blank=True)
    descripcion_sancion = models.TextField(blank=True, default='')

    medida = models.CharField(max_length=100, blank=True, default='')
    fecha_inicio_medida = models.DateField(null=True, blank=True)
    fecha_termino_medida = models.DateField(null=True, blank=True)
    descripcion_medida = models.TextField(blank=True, default='')

    medio_citacion_afectado = models.CharField(max_length=100, blank=True, default='')
    fecha_citacion_afectado = models.DateField(null=True, blank=True)
    lugar_entrevista_afectado = models.CharField(max_length=200, blank=True, default='')
    hora_entrevista_afectado = models.TimeField(null=True, blank=True)
    firma_reclamante = models.CharField(max_length=100, blank=True, default='')

    fecha_envio = models.DateField(null=True, blank=True)
    hora_envio = models.TimeField(null=True, blank=True)
    empresa_correos = models.CharField(max_length=100, blank=True, default='')
    nombre_firma_remitente = models.CharField(max_length=100, blank=True, default='')

    medio_citacion_denunciado = models.CharField(max_length=100, blank=True, default='')
    fecha_citacion_denunciado = models.DateField(null=True, blank=True)
    lugar_entrevista_denunciado = models.CharField(max_length=200, blank=True, default='')
    hora_entrevista_denunciado = models.TimeField(null=True, blank=True)
    firma_denunciado = models.CharField(max_length=100, blank=True, default='')

    nombre_firma_encargado = models.CharField(max_length=100, blank=True, default='')

# ============ FORMULARIO 5: Apelación ============
class Apelacion(models.Model):
    protocolo = models.CharField(max_length=100, blank=True, default='PENDIENTE')
    fecha_recepcion = models.DateField(default=timezone.now)
    nombre_apelante = models.CharField(max_length=100, blank=True, default='')
    run_apelante = models.CharField(max_length=12, blank=True, default='')
    curso_o_cargo = models.CharField(max_length=100, blank=True, default='')
    domicilio = models.CharField(max_length=200, blank=True, default='')
    correo = models.EmailField(blank=True, default='')
    texto_apelacion = models.TextField(blank=True, default='')

# ============ FORMULARIO 6: Resolución de Apelación ============
class ResolucionApelacion(models.Model):
    protocolo = models.CharField(max_length=100, blank=True, default='PENDIENTE')
    fecha_recepcion = models.DateField(default=timezone.now)
    medio_envio = models.CharField(max_length=100, blank=True, default='')
    resolucion = models.TextField(blank=True, default='')
    fundamentos = models.TextField(blank=True, default='')
    rector_o_sostenedor = models.CharField(max_length=100, blank=True, default='')

# ============ FORMULARIO 7: Encuesta ============
FRECUENCIAS = [
    ('4', 'Todos los días'),
    ('3', '2-3 veces por semana'),
    ('2', '2-3 veces por mes'),
    ('1', 'Una vez al mes'),
    ('0', 'Nunca'),
]
class EncuestaBullying(models.Model):
    estudiante_iniciales = models.CharField(max_length=10, blank=True, default='')
    curso = models.CharField(max_length=50, blank=True, default='')
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
    comentario_adicional = models.TextField(blank=True, default='')
