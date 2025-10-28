from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, Http404
from django.template.loader import render_to_string
from django.forms import Form # Importante para chequear tipos de formularios
from django.core.exceptions import ObjectDoesNotExist # Para manejar cuando un form no existe
from django.utils import timezone
from weasyprint import HTML

# --- Importamos los modelos de ESTA app ('protocolos') ---
from .models import Protocolo, TipoProtocolo

# --- ¡Importamos TODOS los formularios y modelos desde la app 'formularios'! ---
from formularios.forms import (
    FormularioDenunciaForm, FichaEntrevistaForm, DerivacionForm,
    InformeConcluyenteForm, ApelacionForm, ResolucionApelacionForm, EncuestaBullyingForm
    # --- ¡Aquí importarás tus NUEVOS formularios para los protocolos 7-15! ---
    # Ej: FormRiesgoSuicidaP1Form, FormRiesgoSuicidaP2Form,
)
from formularios.models import (
    FormularioDenuncia, FichaEntrevista, Derivacion, InformeConcluyente,
    Apelacion, ResolucionApelacion, EncuestaBullying
    # --- ¡Aquí importarás tus NUEVOS modelos para los protocolos 7-15! ---
    # Ej: RiesgoSuicidaP1, RiesgoSuicidaP2,
)

# Definimos los nombres de los protocolos 1-6 en una constante (buena práctica)
PROTOCOLOS_TIPO_1 = [
    "Acoso Escolar", "Drogas y Alcohol", "Agresión o Connotación Sexual",
    "Vulneración de derechos", "Discriminación arbitraria", "Violencia física o psicológica"
]

@login_required(login_url='Validaciones:login')
def iniciar_protocolo(request, tipo_id):
    """
    Crea una nueva instancia de Protocolo y redirige al paso 1.
    """
    tipo = get_object_or_404(TipoProtocolo, id=tipo_id)
    protocolo = Protocolo.objects.create(tipo=tipo, creador=request.user)
    # Redirigimos a la Súper-Vista, al paso 1
    return redirect('protocolos:protocolo_step', protocolo_id=protocolo.id, step=1)

@login_required(login_url='Validaciones:login')
def protocolo_step(request, protocolo_id, step):
    """
    ¡LA SÚPER-VISTA!
    Maneja el renderizado y guardado de CADA paso de CADA protocolo.
    """
    protocolo = get_object_or_404(Protocolo, id=protocolo_id)
    
    # --- Seguridad: Solo el creador puede ver/editar ---
    if protocolo.creador != request.user:
        messages.error(request, "No tienes permiso para ver o editar este protocolo.")
        return redirect('Validaciones:homepage')

    tipo_nombre = protocolo.tipo.nombre
    form_config = None # Aquí guardaremos la config del paso actual
    total_steps = 0 # Para saber cuándo redirigir a "exito"

    # --- Lógica para los protocolos 1-6 ---
    if tipo_nombre in PROTOCOLOS_TIPO_1:
        total_steps = 7
        # Mapeamos cada paso a su Form, Modelo y Template
        step_map = {
            1: {'form': FormularioDenunciaForm, 'model': FormularioDenuncia, 'template': 'protocolo1/formulario_paso1.html'},
            2: {'form': FichaEntrevistaForm, 'model': FichaEntrevista, 'template': 'protocolo1/formulario_paso2.html'},
            3: {'form': DerivacionForm, 'model': Derivacion, 'template': 'protocolo1/formulario_paso3.html'}, # Caso especial
            4: {'form': InformeConcluyenteForm, 'model': InformeConcluyente, 'template': 'protocolo1/formulario_paso4.html'},
            5: {'form': ApelacionForm, 'model': Apelacion, 'template': 'protocolo1/formulario_paso5.html'},
            6: {'form': ResolucionApelacionForm, 'model': ResolucionApelacion, 'template': 'protocolo1/formulario_paso6.html'},
            7: {'form': EncuestaBullyingForm, 'model': EncuestaBullying, 'template': 'protocolo1/formulario_paso7.html'},
        }
        form_config = step_map.get(step)

    # --- Lógica para el PROTOCOLO 7: "Riesgo suicida" ---
    elif tipo_nombre == "Riesgo suicida":
        # ¡Aquí defines los pasos para este protocolo!
        # total_steps = 2 # Por ejemplo
        # step_map = {
        #     1: {'form': FormRiesgoSuicidaP1Form, 'model': RiesgoSuicidaP1, 'template': 'riesgo_suicida/paso1.html'},
        #     2: {'form': FormRiesgoSuicidaP2Form, 'model': RiesgoSuicidaP2, 'template': 'riesgo_suicida/paso2.html'},
        # }
        # form_config = step_map.get(step)
        
        # --- Temporal, mientras no lo implementas ---
        return HttpResponse(f"Vista para Protocolo '{tipo_nombre}' - Paso {step} - AÚN NO IMPLEMENTADA")

    # --- Lógica para el PROTOCOLO 8: "Casos de salud" ---
    elif tipo_nombre == "Casos de salud":
        # ...
        return HttpResponse(f"Vista para Protocolo '{tipo_nombre}' - Paso {step} - AÚN NO IMPLEMENTADA")

    # ... y así con los 15 protocolos ...
    
    # --- Si el paso o protocolo no está configurado ---
    if not form_config:
        messages.error(request, f"El paso {step} no está definido para el protocolo '{tipo_nombre}'.")
        return redirect('Validaciones:homepage')

    # --- Obtenemos las clases y el template ---
    form_class = form_config['form']
    model_class = form_config['model']
    template_name = form_config['template']

    # --- Lógica clave: Buscar si ya existe una instancia (para editar) ---
    instance = None
    try:
        instance = model_class.objects.get(protocolo=protocolo)
    except ObjectDoesNotExist:
        instance = None # No pasa nada, es un formulario nuevo

    # --- Lógica de Procesamiento del Formulario ---
    if request.method == 'POST':
        # --- CASO ESPECIAL: DerivacionForm (no es ModelForm) ---
        if form_class == DerivacionForm:
            form = DerivacionForm(request.POST, request.FILES)
            if form.is_valid():
                data = form.cleaned_data
                # Mapeamos los campos del form a los del modelo (¡tienen nombres distintos!)
                defaults_data = {
                    'derivaciones': ", ".join(data.get('tipo_derivacion', [])),
                    'fecha_lesiones': data.get('fecha_lesiones'),
                    'institucion_lesiones': data.get('institucion_lesiones'),
                    'funcionario_lesiones': data.get('funcionario_responsable_lesiones'), # Mapeo
                    'firma_lesiones': data.get('firma_funcionario_lesiones'), # Mapeo
                    'respaldo_lesiones': data.get('respaldo_lesiones'),
                    
                    'fecha_delito': data.get('fecha_delito'),
                    'institucion_delito': data.get('institucion_delito'),
                    'funcionario_delito': data.get('funcionario_responsable_delito'), # Mapeo
                    'firma_delito': data.get('firma_funcionario_delito'), # Mapeo
                    'respaldo_delito': data.get('respaldo_delito'),
                    
                    'fecha_tribunal': data.get('fecha_tribunal'),
                    'institucion_tribunal': data.get('institucion_tribunal'),
                    'funcionario_tribunal': data.get('funcionario_responsable_tribunal'), # Mapeo
                    'firma_tribunal': data.get('firma_funcionario_tribunal'), # Mapeo
                    'respaldo_tribunal': data.get('respaldo_tribunal'),
                    
                    'tipo_medida_otras': data.get('tipo_medida_otras'),
                    'descripcion_otras': data.get('descripcion_otras'),
                    'funcionario_otras': data.get('funcionario_responsable_otras'), # Mapeo
                    'firma_otras': data.get('firma_funcionario_otras'), # Mapeo
                    'respaldo_otras': data.get('respaldo_otras'),
                }
                # Usamos update_or_create para guardar o actualizar
                obj, created = Derivacion.objects.update_or_create(
                    protocolo=protocolo,
                    defaults=defaults_data
                )
                form_valid = True
            else:
                form_valid = False
        
        # --- CASO NORMAL: Es un ModelForm ---
        else:
            form = form_class(request.POST, request.FILES, instance=instance)
            if form.is_valid():
                obj = form.save(commit=False)
                obj.protocolo = protocolo
                obj.save()
                form_valid = True
            else:
                form_valid = False

        # --- Redirección después de POST ---
        if form_valid:
            messages.success(request, f"Paso {step} guardado correctamente. ✔️")
            if step < total_steps:
                return redirect('protocolos:protocolo_step', protocolo_id=protocolo.id, step=step + 1)
            else:
                return redirect('protocolos:formulario_exito', protocolo_id=protocolo.id)
        else:
            messages.error(request, "Por favor, corrige los errores en el formulario.")

    # --- Lógica para GET (Mostrar el formulario) ---
    else:
        # --- CASO ESPECIAL: DerivacionForm (no es ModelForm) ---
        if form_class == DerivacionForm:
            initial_data = {}
            if instance:
                # Si ya existe, pre-poblamos el formulario
                initial_data = {
                    'tipo_derivacion': instance.derivaciones.split(', ') if instance.derivaciones else [],
                    'fecha_lesiones': instance.fecha_lesiones,
                    'institucion_lesiones': instance.institucion_lesiones,
                    'funcionario_responsable_lesiones': instance.funcionario_lesiones, # Mapeo
                    'firma_funcionario_lesiones': instance.firma_lesiones, # Mapeo
                    'respaldo_lesiones': instance.respaldo_lesiones,
                    # ... (y así con todos los demás campos) ...
                    'fecha_delito': instance.fecha_delito,
                    'institucion_delito': instance.institucion_delito,
                    'funcionario_responsable_delito': instance.funcionario_delito,
                    'firma_funcionario_delito': instance.firma_delito,
                    'respaldo_delito': instance.respaldo_delito,
                    'fecha_tribunal': instance.fecha_tribunal,
                    'institucion_tribunal': instance.institucion_tribunal,
                    'funcionario_responsable_tribunal': instance.funcionario_tribunal,
                    'firma_funcionario_tribunal': instance.firma_tribunal,
                    'respaldo_tribunal': instance.respaldo_tribunal,
                    'tipo_medida_otras': instance.tipo_medida_otras,
                    'descripcion_otras': instance.descripcion_otras,
                    'funcionario_responsable_otras': instance.funcionario_otras,
                    'firma_funcionario_otras': instance.firma_otras,
                    'respaldo_otras': instance.respaldo_otras,
                }
            form = DerivacionForm(initial=initial_data)
        
        # --- CASO NORMAL: Es un ModelForm ---
        else:
            form = form_class(instance=instance)

    # --- Contexto y Renderizado Final ---
    context = {
        'form': form,
        'protocolo': protocolo,
        'step': step,
        'tipo_nombre': tipo_nombre,
    }
    return render(request, template_name, context)

# --- VISTAS ADICIONALES (Éxito, PDF, Ver) ---

@login_required(login_url='Validaciones:login')
def formulario_exito(request, protocolo_id=None):
    """
    Página de éxito al finalizar un protocolo. Cambia el estado.
    """
    if protocolo_id:
        try:
            protocolo = Protocolo.objects.get(id=protocolo_id, creador=request.user)
            if protocolo.estado == 'En Creacion':
                protocolo.estado = 'Pendiente'
                protocolo.save() 
        except Protocolo.DoesNotExist:
            messages.error(request, "Error: No se pudo encontrar el protocolo para finalizarlo.")
            return redirect('Validaciones:homepage')
    
    return render(request, 'protocolo1/exito.html', {'protocolo_id': protocolo_id})

@login_required(login_url='Validaciones:login')
def descargar_protocolo_pdf(request, protocolo_id):
    """
    Genera y descarga un PDF con toda la información del protocolo.
    """
    protocolo = get_object_or_404(
        Protocolo.objects.select_related(
            'tipo',
            'ficha_denuncia', 
            'fichaentrevista', # Django usa el related_name o el nombre_modelo_en_minuscula
            'derivacion', 
            'informeconcluyente', 
            'apelacion', 
            'resolucionapelacion', 
            'encuestabullying',
            # --- ¡Aquí añadirás los related_name de los NUEVOS formularios! ---
            # 'riesgo_suicida_p1',
            # 'riesgo_suicida_p2',
        ), 
        id=protocolo_id,
        creador=request.user # Seguridad
    )

    context = {
        'protocolo': protocolo,
        'fecha_actual': timezone.now(),
        'request': request,
        'protocolos_tipo_1': PROTOCOLOS_TIPO_1 # Pasamos la lista al template
    }
    
    # --- Lógica del Template PDF ---
    # Tu template 'protocolo_pdf.html' ahora debe tener ifs:
    # {% if protocolo.tipo.nombre in protocolos_tipo_1 %}
    #    ... (mostrar los 7 formularios de siempre) ...
    # {% elif protocolo.tipo.nombre == "Riesgo suicida" %}
    #    ... (mostrar los formularios de riesgo suicida) ...
    # {% endif %}

    html_string = render_to_string('protocolo1/protocolo_pdf.html', context)
    pdf_file = HTML(string=html_string, base_url=request.build_absolute_uri('/')).write_pdf()
    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="protocolo_{protocolo.id}_{protocolo.tipo.nombre}.pdf"'
    return response

@login_required(login_url='Validaciones:login')
def ver_protocolo(request, protocolo_id):
    """
    Muestra una vista de solo lectura de un protocolo completado.
    """
    protocolo = get_object_or_404(
        Protocolo.objects.select_related(
            'tipo',
            'ficha_denuncia', 
            'fichaentrevista', 
            'derivacion', 
            'informeconcluyente', 
            'apelacion', 
            'resolucionapelacion', 
            'encuestabullying',
            # --- ¡Aquí añadirás los related_name de los NUEVOS formularios! ---
            # 'riesgo_suicida_p1',
            # 'riesgo_suicida_p2',
        ), 
        id=protocolo_id
        # Permitimos ver a otros usuarios (o solo al creador? si es solo creador, añade:)
        # creador=request.user
    )

    context = {
        'protocolo': protocolo,
        'protocolos_tipo_1': PROTOCOLOS_TIPO_1 # Pasamos la lista al template
    }
    
    # --- Lógica del Template VER ---
    # Tu template 'ver_protocolo.html' ahora debe tener ifs:
    # {% if protocolo.tipo.nombre in protocolos_tipo_1 %}
    #    ... (mostrar los 7 formularios de siempre) ...
    # {% elif protocolo.tipo.nombre == "Riesgo suicida" %}
    #    ... (mostrar los formularios de riesgo suicida) ...
    # {% endif %}

    return render(request, 'protocolo1/ver_protocolo.html', context)

