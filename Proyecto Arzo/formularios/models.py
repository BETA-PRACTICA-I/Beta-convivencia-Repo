from django.db import models
from django.utils import timezone
from datetime import timedelta
from protocolos.models import Protocolo

# Importamos el modelo User de Django para saber quién crea cada protocolo
from django.contrib.auth.models import User

"""
██████╗░██████╗░░█████╗░████████╗░█████╗░░█████╗░░█████╗░██╗░░░░░░█████╗░  ░░███╗░░  ░░░░░░  ░█████╗░
██╔══██╗██╔══██╗██╔══██╗╚══██╔══╝██╔══██╗██╔══██╗██╔══██╗██║░░░░░██╔══██╗  ░████║░░  ░░░░░░  ██╔═══╝░
██████╔╝██████╔╝██║░░██║░░░██║░░░██║░░██║██║░░╚═╝██║░░██║██║░░░░░██║░░██║  ██╔██║░░  █████╗  ██████╗░
██╔═══╝░██╔══██╗██║░░██║░░░██║░░░██║░░██║██║░░██╗██║░░██║██║░░░░░██║░░██║  ╚═╝██║░░  ╚════╝  ██╔══██╗
██║░░░░░██║░░██║╚█████╔╝░░░██║░░░╚█████╔╝╚█████╔╝╚█████╔╝███████╗╚█████╔╝  ███████╗  ░░░░░░  ╚█████╔╝
╚═╝░░░░░╚═╝░░╚═╝░╚════╝░░░░╚═╝░░░░╚════╝░░╚════╝░░╚════╝░╚══════╝░╚════╝░  ╚══════╝  ░░░░░░  ░╚════╝░
"""

# ============ FORMULARIO 1: FormularioDenuncia ============

class FormularioDenuncia(models.Model):
    # LA LÍNEA MÁGICA: Conecta este formulario a un único Protocolo.
    # Si se borra el Protocolo, este formulario se borra en cascada.
    # permitir NULL temporalmente para migraciones; no usar primary_key aquí
    protocolo = models.OneToOneField(
        'protocolos.Protocolo', 
        on_delete=models.CASCADE, 
        related_name='ficha_denuncia'
    )

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

    class Meta:
        db_table = 'protocolo1_formulariodenuncia'  # <-- LÍNEA MÁGICA 3

    def __str__(self):
        return f"FormularioDenuncia (Protocolo {getattr(self.protocolo, 'id', '—')})"


# ============ FORMULARIO 2: FichaEntrevista ============

class FichaEntrevista(models.Model):
    # LA LÍNEA MÁGICA: Conecta este formulario a un único Protocolo, ya no te voy a explicar esto denuevo po.
    protocolo = models.OneToOneField(
        'protocolos.Protocolo', 
        on_delete=models.CASCADE, 
    )

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

    class Meta:
        db_table = 'protocolo1_fichaentrevista'  # <-- LÍNEA MÁGICA 4

    def __str__(self):
        return f"FichaEntrevista (Protocolo {getattr(self.protocolo, 'id', '—')})"


# ============ FORMULARIO 3: Derivaciones ============

class Derivacion(models.Model):

    protocolo = models.OneToOneField(
        'protocolos.Protocolo', 
        on_delete=models.CASCADE, 
    )

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

    class Meta:
        db_table = 'protocolo1_derivacion'

    def __str__(self):
        return f"Derivacion (Protocolo {getattr(self.protocolo, 'id', '—')})"


# ============ FORMULARIO 4: Informe Concluyente ============

class InformeConcluyente(models.Model):
    protocolo = models.OneToOneField(
        'protocolos.Protocolo', 
        on_delete=models.CASCADE, 
    )

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

    class Meta:
        db_table = 'protocolo1_informeconcluyente'

    def __str__(self):
        return f"InformeConcluyente (Protocolo {getattr(self.protocolo, 'id', '—')})"


# ============ FORMULARIO 5: Apelación ============

class Apelacion(models.Model):
    protocolo = models.OneToOneField(
        'protocolos.Protocolo', 
        on_delete=models.CASCADE, 
    )

    estado_informe = models.CharField(max_length=100, default='PENDIENTE')
    fecha_recepcion = models.DateField(default=timezone.now)
    nombre_apelante = models.CharField(max_length=100, default='')
    run_apelante = models.CharField(max_length=12, default='')
    curso_o_cargo = models.CharField(max_length=100, default='')
    domicilio = models.CharField(max_length=200, default='')
    correo = models.EmailField(default='')
    texto_apelacion = models.TextField(default='')

    class Meta:
        db_table = 'protocolo1_apelacion'

    def __str__(self):
        return f"Apelacion (Protocolo {getattr(self.protocolo, 'id', '—')})"


# ============ FORMULARIO 6: Resolución de Apelación ============

class ResolucionApelacion(models.Model):
    protocolo = models.OneToOneField(
        'protocolos.Protocolo', 
        on_delete=models.CASCADE, 
    )

    estado_informe = models.CharField(max_length=100, default='PENDIENTE')
    fecha_recepcion = models.DateField(default=timezone.now)
    medio_envio = models.CharField(max_length=100, default='')
    resolucion = models.TextField(default='')
    fundamentos = models.TextField(default='')
    rector_o_sostenedor = models.CharField(max_length=100, default='')

    class Meta:
        db_table = 'protocolo1_resolucionapelacion'

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

GENERO = [
    ('M', 'Masculino'),
    ('F', 'Femenino'),
    ('O', 'Otro/No especifica'),
]

class EncuestaBullying(models.Model):
    protocolo = models.OneToOneField(
        'protocolos.Protocolo', 
        on_delete=models.CASCADE, 
        related_name='encuestabullying',
    )

    # Campos del PDF
    estudiante_iniciales = models.CharField(max_length=10, default='', blank=True) # Blank=True si es opcional
    curso = models.CharField(max_length=50, default='', blank=True) # Blank=True si es opcional
    fecha_encuesta = models.DateField(default=timezone.now) # NUEVO: Fecha de la encuesta
    edad_estudiante = models.PositiveSmallIntegerField(null=True, blank=True) # NUEVO: Edad (opcional)
    genero_estudiante = models.CharField(max_length=1, choices=GENERO, blank=True) # NUEVO: Género (opcional)

    # Campos de frecuencia (igual que antes)
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

    comentario_adicional = models.TextField(default='', blank=True) # Blank=True si es opcional

    class Meta:
        db_table = 'protocolo1_encuestabullying'

    def __str__(self):
        # Ajustar esto si se necesita más información, como las iniciales
        return f"EncuestaBullying (Protocolo {getattr(self.protocolo, 'id', '—')})"


"""
██████╗░██████╗░░█████╗░████████╗░█████╗░░█████╗░░█████╗░██╗░░░░░░█████╗░  ███████╗
██╔══██╗██╔══██╗██╔══██╗╚══██╔══╝██╔══██╗██╔══██╗██╔══██╗██║░░░░░██╔══██╗  ╚════██║
██████╔╝██████╔╝██║░░██║░░░██║░░░██║░░██║██║░░╚═╝██║░░██║██║░░░░░██║░░██║  ░░░░██╔╝
██╔═══╝░██╔══██╗██║░░██║░░░██║░░░██║░░██║██║░░██╗██║░░██║██║░░░░░██║░░██║  ░░░██╔╝░
██║░░░░░██║░░██║╚█████╔╝░░░██║░░░╚█████╔╝╚█████╔╝╚█████╔╝███████╗╚█████╔╝  ░░██╔╝░░
╚═╝░░░░░╚═╝░░╚═╝░╚════╝░░░░╚═╝░░░░╚════╝░░╚════╝░░╚════╝░╚══════╝░╚════╝░  ░░╚═╝░░░
"""

class RiesgoSuicidaAnexo1(models.Model):
    # Enlace UNO A UNO con el protocolo principal
    protocolo = models.OneToOneField(Protocolo, on_delete=models.CASCADE, related_name="riesgo_suicida_anexo1")
    
    # --- Datos del afectado ---
    nombre_afectado = models.CharField(max_length=255)
    curso = models.CharField(max_length=100)
    profesor_jefe = models.CharField(max_length=255)
    apoderado = models.CharField(max_length=255)

    # --- Registro de situación ---
    fecha = models.DateField()
    hora = models.TimeField()
    persona_detecta = models.CharField(max_length=255, verbose_name="Persona que detectó la situación")
    relato_hechos = models.TextField(verbose_name="Relato de los hechos")

    def __str__(self):
        return f"Anexo 1 (Riesgo Suicida) para Protocolo {self.protocolo.id}"
    
class RiesgoSuicidaAnexo2(models.Model):
    # Enlace UNO A UNO con el protocolo principal
    protocolo = models.OneToOneField(Protocolo, on_delete=models.CASCADE, related_name="riesgo_suicida_anexo2")

    # --- 1. Antecedentes del Establecimiento Educacional ---
    fecha_derivacion = models.DateField(default=timezone.now, verbose_name="Fecha de Derivación") # Usamos default timezone.now
    establecimiento_nombre = models.CharField(max_length=255, verbose_name="Establecimiento Educacional", blank=True) # Podríamos autocompletarlo
    profesional_deriva_nombre = models.CharField(max_length=255, verbose_name="Nombre del profesional que deriva")
    profesional_deriva_cargo = models.CharField(max_length=150, verbose_name="Cargo del profesional que deriva")
    profesional_deriva_email = models.EmailField(verbose_name="Correo electrónico del profesional que deriva")
    profesional_deriva_telefono = models.CharField(max_length=50, verbose_name="Teléfono de contacto del profesional que deriva")
    establecimiento_contacto_email = models.EmailField(verbose_name="Correo electrónico de contacto con el Establecimiento", blank=True) # Podríamos autocompletarlo
    establecimiento_contacto_telefono = models.CharField(max_length=50, verbose_name="Teléfono de contacto con el Establecimiento", blank=True) # Podríamos autocompletarlo

    # --- 2. Antecedentes del Estudiante ---
    # (Podríamos intentar autocompletar algunos desde Anexo 1 si es necesario más adelante)
    estudiante_nombre = models.CharField(max_length=255, verbose_name="Nombre del Estudiante")
    estudiante_run = models.CharField(max_length=12, verbose_name="RUN del Estudiante")
    estudiante_fecha_nacimiento = models.DateField(verbose_name="Fecha de nacimiento del Estudiante")
    estudiante_edad = models.PositiveSmallIntegerField(verbose_name="Edad del Estudiante")
    estudiante_curso = models.CharField(max_length=100, verbose_name="Curso del Estudiante")
    adulto_responsable_nombre = models.CharField(max_length=255, verbose_name="Adulto responsable o apoderado")
    adulto_responsable_telefono = models.CharField(max_length=50, verbose_name="Teléfono de contacto del adulto responsable")
    estudiante_direccion = models.CharField(max_length=300, verbose_name="Dirección del Estudiante")

    # --- 3. Motivo de Derivación ---
    motivo_derivacion = models.TextField(verbose_name="Motivos por el cual se deriva (indique el riesgo)")

    # --- 4. Acciones Efectuadas ---
    acciones_efectuadas = models.TextField(verbose_name="Acciones efectuadas por el Establecimiento Educacional")

    def __str__(self):
        return f"Anexo 2 (Riesgo Suicida - Derivación) para Protocolo {self.protocolo.id}"

class RiesgoSuicidaAnexo3(models.Model):

    protocolo = models.OneToOneField(Protocolo, on_delete=models.CASCADE, related_name="riesgo_suicida_anexo3")
    
    # Fecha y hora de la notificación
    fecha = models.DateField(default=timezone.now, verbose_name="Fecha de Notificación")
    hora = models.TimeField(verbose_name="Hora de Notificación")
    
    # Info (esta podría autocompletarse, la dejamos opcional por ahora)
    establecimiento_nombre = models.CharField(max_length=255, verbose_name="Establecimiento Educacional", blank=True)
    estudiante_nombre = models.CharField(max_length=255, verbose_name="Nombre del Estudiante", blank=True)
    estudiante_curso = models.CharField(max_length=100, verbose_name="Curso del Estudiante", blank=True)
    
    # Datos del Apoderado
    apoderado_nombre = models.CharField(max_length=255, verbose_name="Nombre del Adulto (Padre, madre o apoderado)")
    apoderado_run = models.CharField(max_length=12, verbose_name="RUN del Apoderado")
    
    # Acciones y Firmas
    acciones_a_seguir = models.TextField(verbose_name="Acciones a seguir por el apoderado")
    nombre_firma_apoderado = models.CharField(max_length=255, verbose_name="Nombre y Firma del Apoderado")
    nombre_firma_funcionario = models.CharField(max_length=255, verbose_name="Nombre y Firma de Funcionario")
    cargo_funcionario = models.CharField(max_length=150, verbose_name="Cargo de Funcionario")

    def __str__(self):
        return f"Anexo 3 (Notificación Apoderado) para Protocolo {self.protocolo.id}"

class RiesgoSuicidaAnexo4(models.Model):

    protocolo = models.OneToOneField(Protocolo, on_delete=models.CASCADE, related_name="riesgo_suicida_anexo4")
    
    # Datos de la reunión
    fecha = models.DateField(default=timezone.now, verbose_name="Fecha de Reunión")
    hora_inicio = models.TimeField(verbose_name="Hora de Inicio")
    hora_termino = models.TimeField(verbose_name="Hora de Término")
    lugar_reunion = models.CharField(max_length=255, verbose_name="Lugar de Reunión")
    
    # Datos del estudiante (opcionales, se podrían autocompletar)
    estudiante_nombre = models.CharField(max_length=255, verbose_name="Nombre del Estudiante", blank=True)
    estudiante_curso = models.CharField(max_length=100, verbose_name="Curso del Estudiante", blank=True)
    profesor_jefe = models.CharField(max_length=255, verbose_name="Profesor Jefe", blank=True)

    # Asistentes (Usamos un TextField para simplicidad)
    asistentes = models.TextField(verbose_name="Asistentes (Nombre, Cargo/Rol)", help_text="Liste un asistente por línea (Ej: Juan Pérez - Psicólogo)")
    
    # Contenido de la reunión
    puntos_tratados = models.TextField(verbose_name="Puntos Tratados")
    acuerdos = models.TextField(verbose_name="Acuerdos y Compromisos")
    
    # Próxima reunión (opcional)
    proxima_reunion_fecha = models.DateField(verbose_name="Fecha Próxima Reunión", null=True, blank=True)
    proxima_reunion_hora = models.TimeField(verbose_name="Hora Próxima Reunión", null=True, blank=True)
    proxima_reunion_lugar = models.CharField(max_length=255, verbose_name="Lugar Próxima Reunión", blank=True)
    
    # Firmas
    firma_funcionario_establecimiento = models.CharField(max_length=255, verbose_name="Nombre y Firma Funcionario Establecimiento")
    firma_profesional_salud = models.CharField(max_length=255, verbose_name="Nombre y Firma Profesional Equipo de Salud")

    def __str__(self):
        return f"Anexo 4 (Reunión Clínica) para Protocolo {self.protocolo.id}"

class RiesgoSuicidaAnexo5(models.Model):

    protocolo = models.OneToOneField(Protocolo, on_delete=models.CASCADE, related_name="riesgo_suicida_anexo5")
    
    # I. ANTECEDENTES DEL ESTABLECIMIENTO
    fecha_derivacion = models.DateField(default=timezone.now, verbose_name="Fecha de Derivación")
    establecimiento_nombre = models.CharField(max_length=255, verbose_name="Establecimiento Educacional", blank=True, help_text="Se autocompletará")
    establecimiento_direccion = models.CharField(max_length=255, verbose_name="Dirección", blank=True)
    establecimiento_telefono = models.CharField(max_length=20, verbose_name="Teléfono", blank=True)
    
    # II. ANTECEDENTES DEL ESTUDIANTE
    estudiante_nombre = models.CharField(max_length=255, verbose_name="Nombre Completo del Estudiante", blank=True)
    estudiante_run = models.CharField(max_length=12, verbose_name="RUN del Estudiante", blank=True)
    estudiante_fecha_nacimiento = models.DateField(verbose_name="Fecha de Nacimiento", null=True, blank=True)
    estudiante_edad = models.PositiveSmallIntegerField(verbose_name="Edad", null=True, blank=True)
    estudiante_curso = models.CharField(max_length=100, verbose_name="Curso", blank=True)
    
    # III. MOTIVO DE DERIVACIÓN
    motivo_derivacion = models.TextField(verbose_name="Motivo de Derivación")
    
    # IV. ACCIONES REALIZADAS POR EL ESTABLECIMIENTO (Textos simples)
    acciones_entrevista_apoderado = models.TextField(verbose_name="Entrevista con Apoderado (Resumen)", blank=True)
    acciones_coordinacion_salud = models.TextField(verbose_name="Coordinación Equipo de Salud (Resumen)", blank=True)
    acciones_otras = models.TextField(verbose_name="Otras acciones realizadas", blank=True)
    
    # V. RESPONSABLE DE LA DERIVACIÓN
    responsable_nombre = models.CharField(max_length=255, verbose_name="Nombre del Funcionario Responsable")
    responsable_cargo = models.CharField(max_length=150, verbose_name="Cargo del Funcionario")
    responsable_telefono = models.CharField(max_length=20, verbose_name="Teléfono de Contacto")
    responsable_email = models.EmailField(verbose_name="Email de Contacto")

    def __str__(self):
        return f"Anexo 5 (Derivación) para Protocolo {self.protocolo.id}"
    


class ReconocimientoIdentidad(models.Model):
    """
    Modelo para almacenar las solicitudes de reconocimiento de identidad de género.
    """
    ESTADO_CHOICES = [
        ('Pendiente', 'Pendiente'),
        ('Aplicado', 'Aplicado'),
        ('Rechazado', 'Rechazado'),
    ]

    # Vinculamos esta solicitud a un protocolo general
    protocolo = models.OneToOneField(Protocolo, on_delete=models.CASCADE, related_name='reconocimiento_identidad')

    # Datos del formulario
    nombre_legal = models.CharField(max_length=200, help_text="Nombre completo según documento de identidad")
    rut_estudiante = models.CharField(max_length=20, help_text="RUT o N° de identificación del estudiante")
    nombre_identitario = models.CharField(max_length=200, help_text="Nombre social con el que se identifica")
    pronombres = models.CharField(max_length=50, help_text="Pronombres seleccionados o especificados")
    
    # Datos de gestión
    fecha_solicitud = models.DateTimeField(auto_now_add=True)
    estado_solicitud = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='Pendiente')

    def __str__(self):
        return f"Solicitud de {self.nombre_identitario} ({self.protocolo.creador.username})"

    class Meta:
        verbose_name = "Solicitud de Reconocimiento de Identidad"
        verbose_name_plural = "Solicitudes de Reconocimiento de Identidad"

class GestionReconocimiento(models.Model):
    """
    Modelo para la Ficha 2: Gestión interna de la solicitud de identidad de género.
    """
    protocolo = models.OneToOneField(Protocolo, on_delete=models.CASCADE, related_name='gestion_reconocimiento')

    # Acciones realizadas
    sistemas_actualizados = models.CharField(max_length=255, blank=True, help_text="Sistemas actualizados, separados por comas")
    fecha_actualizacion = models.DateField()
    
    # Comunicación y cierre
    comunicacion_estudiante = models.CharField(max_length=2, choices=[('Si', 'Sí'), ('No', 'No')])
    observaciones = models.TextField(blank=True)
    respaldo_gestion = models.FileField(upload_to='reconocimiento_gestion/', blank=True, null=True)

    # Responsable
    funcionario_responsable = models.CharField(max_length=255)

    def __str__(self):
        return f"Gestión de Solicitud para Protocolo {self.protocolo.id}"

    class Meta:
        verbose_name = "Gestión de Reconocimiento de Identidad"
        verbose_name_plural = "Gestiones de Reconocimiento de Identidad"


"""
██████╗░██████╗░░█████╗░████████╗░█████╗░░█████╗░░█████╗░██╗░░░░░░█████╗░  ░█████╗░
██╔══██╗██╔══██╗██╔══██╗╚══██╔══╝██╔══██╗██╔══██╗██╔══██╗██║░░░░░██╔══██╗  ██╔══██╗
██████╔╝██████╔╝██║░░██║░░░██║░░░██║░░██║██║░░╚═╝██║░░██║██║░░░░░██║░░██║  ░█████╔╝
██╔═══╝░██╔══██╗██║░░██║░░░██║░░░██║░░██║██║░░██╗██║░░██║██║░░░░░██║░░██║  ██╔══██╗
██║░░░░░██║░░██║╚█████╔╝░░░██║░░░╚█████╔╝╚█████╔╝╚█████╔╝███████╗╚█████╔╝  ╚█████╔╝
╚═╝░░░░░╚═╝░░╚═╝░╚════╝░░░░╚═╝░░░░╚════╝░░╚════╝░░╚════╝░╚══════╝░╚════╝░  ░╚════╝░
"""

class FichaAccidenteEscolar(models.Model):

    protocolo = models.OneToOneField(Protocolo, on_delete=models.CASCADE, related_name="ficha_accidente_escolar")
    
    # Datos del estudiante
    estudiante_nombre = models.CharField(max_length=255, verbose_name="Nombre Estudiante")
    estudiante_curso = models.CharField(max_length=100, verbose_name="Curso")
    fecha_hora_accidente = models.DateTimeField(verbose_name="Fecha y Hora del Accidente")
    
    # Detalle
    descripcion_accidente = models.TextField(verbose_name="Describa el accidente escolar (Detección)")
    primeros_auxilios = models.TextField(verbose_name="Acciones de Primeros Auxilios Realizadas")
    
    # Aviso a apoderados
    aviso_apoderado_nombre = models.CharField(max_length=255, verbose_name="Nombre apoderado")
    aviso_apoderado_medio = models.CharField(max_length=100, verbose_name="Medio de comunicación utilizado")
    aviso_funcionario = models.CharField(max_length=255, verbose_name="Funcionario encargado de comunicarlo")
    
    # Aislamiento (si aplica)
    aislamiento_motivo = models.TextField(verbose_name="Motivo del aislamiento", blank=True)
    aislamiento_funcionario = models.CharField(max_length=255, verbose_name="Funcionario a cargo", blank=True)
    aislamiento_lugar = models.CharField(max_length=255, verbose_name="Lugar aislado", blank=True)
    
    # Traslado (si aplica)
    traslado_fecha_hora = models.DateTimeField(verbose_name="Día y hora del traslado", null=True, blank=True)
    traslado_centro = models.CharField(max_length=255, verbose_name="Centro al que fue trasladado", blank=True)
    traslado_funcionario = models.CharField(max_length=255, verbose_name="Quién efectúa el traslado", blank=True)

    def __str__(self):
        return f"Ficha Accidente Escolar (Protocolo {self.protocolo.id})"
    

"""
██████╗░██████╗░░█████╗░████████╗░█████╗░░█████╗░░█████╗░██╗░░░░░░█████╗░  ░█████╗░
██╔══██╗██╔══██╗██╔══██╗╚══██╔══╝██╔══██╗██╔══██╗██╔══██╗██║░░░░░██╔══██╗  ██╔══██╗
██████╔╝██████╔╝██║░░██║░░░██║░░░██║░░██║██║░░╚═╝██║░░██║██║░░░░░██║░░██║  ╚██████║
██╔═══╝░██╔══██╗██║░░██║░░░██║░░░██║░░██║██║░░██╗██║░░██║██║░░░░░██║░░██║  ░╚═══██║
██║░░░░░██║░░██║╚█████╔╝░░░██║░░░╚█████╔╝╚█████╔╝╚█████╔╝███████╗╚█████╔╝  ░█████╔╝
╚═╝░░░░░╚═╝░░╚═╝░╚════╝░░░░╚═╝░░░░╚════╝░░╚════╝░░╚════╝░╚══════╝░╚════╝░  ░╚════╝░
"""

# --- NUEVO MODELO PARA PROTOCOLO 9: ARMAS ---
class ArmasAnexo1(models.Model):
    # Enlace UNO A UNO con el protocolo principal
    protocolo = models.OneToOneField(
        Protocolo, 
        on_delete=models.CASCADE, 
        related_name="anexo_armas" # Usaremos este nombre para llamarlo
    )
    
    # --- Datos del Estudiante ---
    nombre_estudiante = models.CharField(max_length=255)
    curso = models.CharField(max_length=100)
    rut = models.CharField(max_length=12)
    descripcion = models.TextField(verbose_name="Descripción de la situación")

    def __str__(self):
        return f"Anexo 1 (Armas) para Protocolo {self.protocolo.id}"
    

"""
██████╗░██████╗░░█████╗░████████╗░█████╗░░█████╗░░█████╗░██╗░░░░░░█████╗░  ░░███╗░░░█████╗░
██╔══██╗██╔══██╗██╔══██╗╚══██╔══╝██╔══██╗██╔══██╗██╔══██╗██║░░░░░██╔══██╗  ░████║░░██╔══██╗
██████╔╝██████╔╝██║░░██║░░░██║░░░██║░░██║██║░░╚═╝██║░░██║██║░░░░░██║░░██║  ██╔██║░░██║░░██║
██╔═══╝░██╔══██╗██║░░██║░░░██║░░░██║░░██║██║░░██╗██║░░██║██║░░░░░██║░░██║  ╚═╝██║░░██║░░██║
██║░░░░░██║░░██║╚█████╔╝░░░██║░░░╚█████╔╝╚█████╔╝╚█████╔╝███████╗╚█████╔╝  ███████╗╚█████╔╝
╚═╝░░░░░╚═╝░░╚═╝░╚════╝░░░░╚═╝░░░░╚════╝░░╚════╝░░╚════╝░╚══════╝░╚════╝░  ╚══════╝░╚════╝░

"""

class AutolesionAnexo1(models.Model):
    protocolo = models.OneToOneField(
        'protocolos.Protocolo', 
        on_delete=models.CASCADE, 
        related_name='anexo_autolesion'  # <-- ¡Clave para la "súper-vista"!
    )
    
    # Campos de entrada idénticos al Protocolo 9
    nombre_estudiante = models.CharField(max_length=255, verbose_name="Nombre del Estudiante")
    curso = models.CharField(max_length=100, verbose_name="Curso")
    rut = models.CharField(max_length=12, verbose_name="RUT") 
    descripcion = models.TextField(verbose_name="Descripción de la situación")

    def __str__(self):
        return f"Anexo Autolesión para Protocolo #{self.protocolo_id}"
    

