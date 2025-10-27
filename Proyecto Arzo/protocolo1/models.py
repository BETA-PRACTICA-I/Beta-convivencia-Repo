from django.db import models
from django.utils import timezone
from datetime import timedelta

# Importamos el modelo User de Django para saber quién crea cada protocolo
from django.contrib.auth.models import User

class TipoProtocolo(models.Model):
    nombre = models.CharField(max_length=200, unique=True)
    def __str__(self):
        return self.nombre

class Protocolo(models.Model):
    tipo = models.ForeignKey(TipoProtocolo, on_delete=models.PROTECT, related_name="protocolos")
    creador = models.ForeignKey(User, on_delete=models.PROTECT, related_name="protocolos_creados")
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=50, default='En Creacion', help_text="Ej: En Creacion, Pendiente, Resuelto, Vencido")
    
    @property
    def fecha_limite(self): #aqui definimos otro parametro pasandole fecha de creacion + 15 dias
        if self.fecha_creacion:
            return self.fecha_creacion + timedelta(days=15)
        return None
    def __str__(self):
        # muestra "Protocolo 12 - Acoso Escolar" si existe tipo.nombre
        tipo_nombre = getattr(self.tipo, 'nombre', None)
        return f"Protocolo {self.id}" + (f" - {tipo_nombre}" if tipo_nombre else "")



# ============ FORMULARIO 1: FormularioDenuncia ============

class FormularioDenuncia(models.Model):
    # LA LÍNEA MÁGICA: Conecta este formulario a un único Protocolo.
    # Si se borra el Protocolo, este formulario se borra en cascada.
    # permitir NULL temporalmente para migraciones; no usar primary_key aquí
    protocolo = models.OneToOneField(Protocolo, on_delete=models.CASCADE, related_name='ficha_denuncia')

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

    def __str__(self):
        return f"FormularioDenuncia (Protocolo {getattr(self.protocolo, 'id', '—')})"


# ============ FORMULARIO 2: FichaEntrevista ============

class FichaEntrevista(models.Model):
    # LA LÍNEA MÁGICA: Conecta este formulario a un único Protocolo, ya no te voy a explicar esto denuevo po.
    protocolo = models.OneToOneField(Protocolo, on_delete=models.CASCADE)

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

    def __str__(self):
        return f"FichaEntrevista (Protocolo {getattr(self.protocolo, 'id', '—')})"


# ============ FORMULARIO 3: Derivaciones ============
class Derivacion(models.Model):

    protocolo = models.OneToOneField(Protocolo, on_delete=models.CASCADE)

    derivaciones = models.CharField(max_length=100,)
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
        return f"Derivacion (Protocolo {getattr(self.protocolo, 'id', '—')})"


# ============ FORMULARIO 4: Informe Concluyente ============
class InformeConcluyente(models.Model):
    protocolo = models.OneToOneField(Protocolo, on_delete=models.CASCADE)

    estado_informe = models.CharField(max_length=100, default='PENDIENTE')
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

    def __str__(self):
        return f"InformeConcluyente (Protocolo {getattr(self.protocolo, 'id', '—')})"


# ============ FORMULARIO 5: Apelación ============
class Apelacion(models.Model):
    protocolo = models.OneToOneField(Protocolo, on_delete=models.CASCADE)

    estado_informe = models.CharField(max_length=100, default='PENDIENTE')
    fecha_recepcion = models.DateField(default=timezone.now)
    nombre_apelante = models.CharField(max_length=100, default='')
    run_apelante = models.CharField(max_length=12, default='')
    curso_o_cargo = models.CharField(max_length=100, default='')
    domicilio = models.CharField(max_length=200, default='')
    correo = models.EmailField(default='')
    texto_apelacion = models.TextField(default='')

    def __str__(self):
        return f"Apelacion (Protocolo {getattr(self.protocolo, 'id', '—')})"


# ============ FORMULARIO 6: Resolución de Apelación ============
class ResolucionApelacion(models.Model):
    protocolo = models.OneToOneField(Protocolo, on_delete=models.CASCADE)

    estado_informe = models.CharField(max_length=100, default='PENDIENTE')
    fecha_recepcion = models.DateField(default=timezone.now)
    medio_envio = models.CharField(max_length=100, default='')
    resolucion = models.TextField(default='')
    fundamentos = models.TextField(default='')
    rector_o_sostenedor = models.CharField(max_length=100, default='')

    def __str__(self):
        return f"ResolucionApelacion (Protocolo {getattr(self.protocolo, 'id', '—')})"


# ============ FORMULARIO 7: Encuesta ============
FRECUENCIAS = [
    ('4', 'Todos los días'),
    ('3', '2-3 veces por semana'),
    ('2', '2-3 veces por mes'),
    ('1', 'Una vez al mes'),
    ('0', 'Nunca'),
]
class EncuestaBullying(models.Model):
    protocolo = models.OneToOneField(Protocolo, on_delete=models.CASCADE)

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

    def __str__(self):
        return f"EncuestaBullying (Protocolo {getattr(self.protocolo, 'id', '—')})"
