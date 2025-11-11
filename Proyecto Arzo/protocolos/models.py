from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from datetime import timedelta

class TipoProtocolo(models.Model):
    nombre = models.CharField(max_length=200, unique=True)
    #orden = models.PositiveIntegerField(default=0, help_text="Para ordenar la lista de protocolos")
    
    def __str__(self):
        return self.nombre
    
    class Meta:
        db_table = 'protocolo1_tipoprotocolo' # <-- LÍNEA MÁGICA 1

class Protocolo(models.Model):
    tipo = models.ForeignKey(TipoProtocolo, on_delete=models.PROTECT, related_name="protocolos")
    creador = models.ForeignKey(User, on_delete=models.PROTECT, related_name="protocolos_creados")
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=50, default='En Creacion', help_text="Ej: En Creacion, Pendiente, Resuelto, Vencido")
    
    @property
    def fecha_limite(self):
        if self.fecha_creacion:
            return self.fecha_creacion + timedelta(days=15)
        return None

    def _collect_related_strings(self, related_attr, field_names):
        """Utility to pull trimmed string values from optional one-to-one relations."""
        try:
            related_obj = getattr(self, related_attr)
        except (AttributeError, ObjectDoesNotExist):
            return []

        values = []
        for field in field_names:
            raw_value = getattr(related_obj, field, None)
            if not raw_value:
                continue

            text = str(raw_value).strip()
            if text:
                values.append(text)

        return values

    @staticmethod
    def _unique_preserve_order(strings):
        seen = set()
        ordered = []
        for item in strings:
            key = item.lower()
            if key in seen:
                continue
            seen.add(key)
            ordered.append(item)
        return ordered

    @property
    def resumen_involucrados(self):
        if hasattr(self, "_resumen_involucrados_cache"):
            return self._resumen_involucrados_cache

        related_fields = {
            'ficha_denuncia': ['nombre_estudiante', 'nombre_denunciado', 'nombre_denunciante'],
            'fichaentrevista': ['nombre_entrevistado'],
            'informeconcluyente': ['nombre_encargado', 'firma_reclamante', 'firma_denunciado', 'nombre_firma_encargado'],
            'apelacion': ['nombre_apelante'],
            'resolucionapelacion': ['rector_o_sostenedor'],
            'riesgo_suicida_anexo1': ['nombre_afectado', 'apoderado', 'profesor_jefe'],
            'riesgo_suicida_anexo2': ['estudiante_nombre', 'adulto_responsable_nombre'],
            'riesgo_suicida_anexo3': ['estudiante_nombre', 'apoderado_nombre'],
            'riesgo_suicida_anexo4': ['estudiante_nombre', 'profesor_jefe'],
            'riesgo_suicida_anexo5': ['estudiante_nombre', 'responsable_nombre'],
            'reconocimiento_identidad': ['estudiante_nombre_social', 'estudiante_nombre_legal', 'apoderado_nombres'],
            'acta_reunion_identidad': ['firma_apoderado', 'firma_estudiante'],
            'ficha_accidente_escolar': ['estudiante_nombre', 'aviso_apoderado_nombre'],
            'encuestabullying': ['estudiante_iniciales'],
            'anexo_armas': ['nombre_estudiante'],
            'anexo_autolesion': ['nombre_estudiante'],
            'ficha0_madre_padre': ['nombre_estudiante', 'nombre_apoderado_citado', 'nombre_apoderado_concurre'],
            'ficha1_madre_padre': ['individualizacion_apoderado'],
            'ficha2_madre_padre': ['nombre_estudiante'],
        }

        names = []
        for attr, fields in related_fields.items():
            names.extend(self._collect_related_strings(attr, fields))

        unique_names = self._unique_preserve_order(names)
        if not unique_names:
            self._resumen_involucrados_cache = None
            return None

        self._resumen_involucrados_list = unique_names
        display = ', '.join(unique_names)
        self._resumen_involucrados_cache = display
        return display

    @property
    def resumen_cursos(self):
        if hasattr(self, "_resumen_cursos_cache"):
            return self._resumen_cursos_cache

        related_fields = {
            'ficha_denuncia': ['curso_estudiante', 'curso_denunciado', 'curso_denunciado_extra'],
            'riesgo_suicida_anexo1': ['curso'],
            'riesgo_suicida_anexo2': ['estudiante_curso'],
            'riesgo_suicida_anexo3': ['estudiante_curso'],
            'riesgo_suicida_anexo4': ['estudiante_curso'],
            'riesgo_suicida_anexo5': ['estudiante_curso'],
            'reconocimiento_identidad': ['estudiante_curso'],
            'ficha_accidente_escolar': ['estudiante_curso'],
            'encuestabullying': ['curso'],
            'anexo_armas': ['curso'],
            'anexo_autolesion': ['curso'],
            'ficha0_madre_padre': ['curso'],
            'ficha2_madre_padre': ['curso'],
        }

        cursos = []
        for attr, fields in related_fields.items():
            cursos.extend(self._collect_related_strings(attr, fields))

        unique_cursos = self._unique_preserve_order(cursos)
        if not unique_cursos:
            self._resumen_cursos_cache = None
            return None

        self._resumen_cursos_list = unique_cursos
        display = ', '.join(unique_cursos)
        self._resumen_cursos_cache = display
        return display

    @property
    def primer_involucrado(self):
        nombres = getattr(self, '_resumen_involucrados_list', None)
        if nombres is None:
            self.resumen_involucrados
            nombres = getattr(self, '_resumen_involucrados_list', [])
        return nombres[0] if nombres else None

    @property
    def primer_curso(self):
        cursos = getattr(self, '_resumen_cursos_list', None)
        if cursos is None:
            self.resumen_cursos
            cursos = getattr(self, '_resumen_cursos_list', [])
        return cursos[0] if cursos else None
    def __str__(self):
        tipo_nombre = getattr(self.tipo, 'nombre', None)
        return f"Protocolo {self.id}" + (f" - {tipo_nombre}" if tipo_nombre else "")

    class Meta:
        db_table = 'protocolo1_protocolo' # <-- LÍNEA MÁGICA 2