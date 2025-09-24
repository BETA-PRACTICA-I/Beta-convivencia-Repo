from django.db import models

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



