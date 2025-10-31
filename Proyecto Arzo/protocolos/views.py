from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, Http404
from django.template.loader import render_to_string
from django.forms import Form 
from django.core.exceptions import ObjectDoesNotExist 
from django.utils import timezone
from weasyprint import HTML

from .models import Protocolo, TipoProtocolo

from formularios.forms import (
    FormularioDenunciaForm, FichaEntrevistaForm, DerivacionForm,
    InformeConcluyenteForm, ApelacionForm, ResolucionApelacionForm, EncuestaBullyingForm,

    RiesgoSuicidaAnexo1Form, RiesgoSuicidaAnexo2Form, RiesgoSuicidaAnexo3Form,
    RiesgoSuicidaAnexo4Form, RiesgoSuicidaAnexo5Form
    )
from formularios.models import (
    FormularioDenuncia, FichaEntrevista, Derivacion, InformeConcluyente,
    Apelacion, ResolucionApelacion, EncuestaBullying,

    RiesgoSuicidaAnexo1, RiesgoSuicidaAnexo2, RiesgoSuicidaAnexo3,
    RiesgoSuicidaAnexo4, RiesgoSuicidaAnexo5
    )

PROTOCOLOS_TIPO_1 = [
    "Acoso Escolar", "Drogas y Alcohol", "Agresión o Connotación Sexual",
    "Vulneración de derechos", "Discriminación arbitraria", "Violencia física o psicológica"
]

@login_required(login_url='Validaciones:login')
def iniciar_protocolo(request, tipo_id):
    tipo = get_object_or_404(TipoProtocolo, id=tipo_id)
    protocolo = Protocolo.objects.create(tipo=tipo, creador=request.user)
    return redirect('protocolos:protocolo_step', protocolo_id=protocolo.id, step=1)

@login_required(login_url='Validaciones:login')
def protocolo_step(request, protocolo_id, step):
    protocolo = get_object_or_404(Protocolo, id=protocolo_id)
    
    if protocolo.creador != request.user:
        messages.error(request, "No tienes permiso para ver o editar este protocolo.")
        return redirect('Validaciones:homepage')

    tipo_nombre = protocolo.tipo.nombre
    form_config = None 
    total_steps = 0 

    if tipo_nombre in PROTOCOLOS_TIPO_1:
        total_steps = 7
        step_map = {
            1: {'form': FormularioDenunciaForm, 'model': FormularioDenuncia, 'template': 'protocolo1/formulario_paso1.html'},
            2: {'form': FichaEntrevistaForm, 'model': FichaEntrevista, 'template': 'protocolo1/formulario_paso2.html'},
            3: {'form': DerivacionForm, 'model': Derivacion, 'template': 'protocolo1/formulario_paso3.html'},
            4: {'form': InformeConcluyenteForm, 'model': InformeConcluyente, 'template': 'protocolo1/formulario_paso4.html'},
            5: {'form': ApelacionForm, 'model': Apelacion, 'template': 'protocolo1/formulario_paso5.html'},
            6: {'form': ResolucionApelacionForm, 'model': ResolucionApelacion, 'template': 'protocolo1/formulario_paso6.html'},
            7: {'form': EncuestaBullyingForm, 'model': EncuestaBullying, 'template': 'protocolo1/formulario_paso7.html'},
        }
        form_config = step_map.get(step)

    # --- 3. ¡AQUÍ ESTÁ LA NUEVA LÓGICA! ---
    elif tipo_nombre == "Riesgo suicida":
        # Cantidad de pasos, debe ser = a la cantidad de anexos.
        total_steps = 5
        step_map = {
            1: {'form': RiesgoSuicidaAnexo1Form, 'model': RiesgoSuicidaAnexo1, 'template': 'riesgo_suicida/paso1.html'},
            2: {'form': RiesgoSuicidaAnexo2Form, 'model': RiesgoSuicidaAnexo2, 'template': 'riesgo_suicida/paso2.html'},
            3: {'form': RiesgoSuicidaAnexo3Form, 'model': RiesgoSuicidaAnexo3, 'template': 'riesgo_suicida/paso3.html'},
            4: {'form': RiesgoSuicidaAnexo4Form, 'model': RiesgoSuicidaAnexo4, 'template': 'riesgo_suicida/paso4.html'},
            5: {'form': RiesgoSuicidaAnexo5Form, 'model': RiesgoSuicidaAnexo5, 'template': 'riesgo_suicida/paso5.html'}
            }
        form_config = step_map.get(step)
    
    elif tipo_nombre == "Casos de salud":
        return HttpResponse(f"Vista para Protocolo '{tipo_nombre}' - Paso {step} - AÚN NO IMPLEMENTADA")

    
    if not form_config:
        messages.error(request, f"El paso {step} no está definido para el protocolo '{tipo_nombre}'.")
        return redirect('Validaciones:homepage')

    form_class = form_config['form']
    model_class = form_config['model']
    template_name = form_config['template']

    instance = None
    try:
        instance = model_class.objects.get(protocolo=protocolo)
    except ObjectDoesNotExist:
        instance = None 

    if request.method == 'POST':
        if form_class == DerivacionForm:
            form = DerivacionForm(request.POST, request.FILES)
            if form.is_valid():
                data = form.cleaned_data
                defaults_data = {
                    'derivaciones': ", ".join(data.get('tipo_derivacion', [])),
                    'fecha_lesiones': data.get('fecha_lesiones'),
                    'institucion_lesiones': data.get('institucion_lesiones'),
                    'funcionario_lesiones': data.get('funcionario_responsable_lesiones'),
                    'firma_lesiones': data.get('firma_funcionario_lesiones'),
                    'respaldo_lesiones': data.get('respaldo_lesiones'),
                    'fecha_delito': data.get('fecha_delito'),
                    'institucion_delito': data.get('institucion_delito'),
                    'funcionario_delito': data.get('funcionario_responsable_delito'),
                    'firma_delito': data.get('firma_funcionario_delito'),
                    'respaldo_delito': data.get('respaldo_delito'),
                    'fecha_tribunal': data.get('fecha_tribunal'),
                    'institucion_tribunal': data.get('institucion_tribunal'),
                    'funcionario_tribunal': data.get('funcionario_responsable_tribunal'),
                    'firma_tribunal': data.get('firma_funcionario_tribunal'),
                    'respaldo_tribunal': data.get('respaldo_tribunal'),
                    'tipo_medida_otras': data.get('tipo_medida_otras'),
                    'descripcion_otras': data.get('descripcion_otras'),
                    'funcionario_otras': data.get('funcionario_responsable_otras'),
                    'firma_otras': data.get('firma_funcionario_otras'),
                    'respaldo_otras': data.get('respaldo_otras'),
                }
                obj, created = Derivacion.objects.update_or_create(
                    protocolo=protocolo,
                    defaults=defaults_data
                )
                form_valid = True
            else:
                form_valid = False
        
        else:
            form = form_class(request.POST, request.FILES, instance=instance)
            if form.is_valid():
                obj = form.save(commit=False)
                obj.protocolo = protocolo
                obj.save()
                form_valid = True
            else:
                form_valid = False

        if form_valid:
            messages.success(request, f"Paso {step} guardado correctamente. ✔️")
            if step < total_steps:
                return redirect('protocolos:protocolo_step', protocolo_id=protocolo.id, step=step + 1)
            else:
                return redirect('protocolos:formulario_exito', protocolo_id=protocolo.id)
        else:
            messages.error(request, "Por favor, corrige los errores en el formulario.")

    else:
        if form_class == DerivacionForm:
            initial_data = {}
            if instance:
                initial_data = {
                    'tipo_derivacion': instance.derivaciones.split(', ') if instance.derivaciones else [],
                    'fecha_lesiones': instance.fecha_lesiones,
                    'institucion_lesiones': instance.institucion_lesiones,
                    'funcionario_responsable_lesiones': instance.funcionario_lesiones,
                    'firma_funcionario_lesiones': instance.firma_lesiones,
                    'respaldo_lesiones': instance.respaldo_lesiones,
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
        
        else:
            form = form_class(instance=instance)

    context = {
        'form': form,
        'protocolo': protocolo,
        'step': step,
        'tipo_nombre': tipo_nombre,
    }
    return render(request, template_name, context)


# --- VISTAS ADICIONALES (Éxito, PDF, Ver) ---
# (Estas vistas no necesitan cambios, pero las incluyo para que el archivo esté completo)

@login_required(login_url='Validaciones:login')
def formulario_exito(request, protocolo_id=None):
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

            'riesgo_suicida_anexo1',
            'riesgo_suicida_anexo2',
            'riesgo_suicida_anexo3',
            'riesgo_suicida_anexo4',
            'riesgo_suicida_anexo5'
            ),
        id=protocolo_id,
        creador=request.user
    )

    context = {
        'protocolo': protocolo,
        'fecha_actual': timezone.now(),
        'request': request,
        'protocolos_tipo_1': PROTOCOLOS_TIPO_1
    }
    
    # IMPORTANTE: Ahora tendrás que editar 'protocolo_pdf.html'
    # para que muestre los campos de 'riesgo_suicida_anexo1'
    # si el tipo de protocolo es "Riesgo suicida"

    html_string = render_to_string('protocolo1/protocolo_pdf.html', context)
    pdf_file = HTML(string=html_string, base_url=request.build_absolute_uri('/')).write_pdf()
    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="protocolo_{protocolo.id}_{protocolo.tipo.nombre}.pdf"'
    return response

@login_required(login_url='Validaciones:login')
def ver_protocolo(request, protocolo_id):
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

            'riesgo_suicida_anexo1',
            'riesgo_suicida_anexo2',
            'riesgo_suicida_anexo3',
            'riesgo_suicida_anexo4',
            'riesgo_suicida_anexo5'
            ), 
        id=protocolo_id
    )

    context = {
        'protocolo': protocolo,
        'protocolos_tipo_1': PROTOCOLOS_TIPO_1
    }
    
    # IMPORTANTE: También tendrás que editar 'ver_protocolo.html'
    # para que muestre los campos de 'riesgo_suicida_anexo1'

    return render(request, 'protocolo1/ver_protocolo.html', context)

def get_instance_or_none(model, **kwargs):
    """Función de ayuda para obtener una instancia o devolver None si no existe."""
    try:
        return model.objects.get(**kwargs)
    except model.DoesNotExist:
        return None

@login_required(login_url='Validaciones:login')
def editar_paso1(request, protocolo_id):
    protocolo = get_object_or_404(Protocolo, id=protocolo_id)
    instancia = get_instance_or_none(FormularioDenuncia, protocolo=protocolo)
    
    if request.method == 'POST':
        form = FormularioDenunciaForm(request.POST, request.FILES, instance=instancia)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.protocolo = protocolo
            obj.save()
            return redirect('protocolos:editar_paso2', protocolo_id=protocolo.id)
    else:
        form = FormularioDenunciaForm(instance=instancia)
        
    return render(request, 'protocolo1/formulario_paso1.html', {'form': form, 'protocolo': protocolo})

@login_required(login_url='Validaciones:login')
def editar_paso2(request, protocolo_id):
    protocolo = get_object_or_404(Protocolo, id=protocolo_id)
    instancia = get_instance_or_none(FichaEntrevista, protocolo=protocolo)
    
    if request.method == 'POST':
        form = FichaEntrevistaForm(request.POST, request.FILES, instance=instancia)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.protocolo = protocolo
            obj.save()
            return redirect('protocolos:editar_paso3', protocolo_id=protocolo.id)
    else:
        form = FichaEntrevistaForm(instance=instancia)
        
    return render(request, 'protocolo1/formulario_paso2.html', {'form': form, 'protocolo': protocolo})

@login_required(login_url='Validaciones:login')
def editar_paso3(request, protocolo_id):
    protocolo = get_object_or_404(Protocolo, id=protocolo_id)
    instancia = get_instance_or_none(Derivacion, protocolo=protocolo) # <-- CORREGIDO

    if request.method == 'POST':
        form = DerivacionForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data
            # Replicamos la lógica de la vista de creación
            defaults_data = {
                'derivaciones': ", ".join(data.get('tipo_derivacion', [])),
                'fecha_lesiones': data.get('fecha_lesiones'),
                'institucion_lesiones': data.get('institucion_lesiones'),
                'funcionario_lesiones': data.get('funcionario_responsable_lesiones'),
                'firma_lesiones': data.get('firma_funcionario_lesiones'),
                'respaldo_lesiones': data.get('respaldo_lesiones'),
                'fecha_delito': data.get('fecha_delito'),
                'institucion_delito': data.get('institucion_delito'),
                'funcionario_delito': data.get('funcionario_responsable_delito'),
                'firma_delito': data.get('firma_funcionario_delito'),
                'respaldo_delito': data.get('respaldo_delito'),
                'fecha_tribunal': data.get('fecha_tribunal'),
                'institucion_tribunal': data.get('institucion_tribunal'),
                'funcionario_tribunal': data.get('funcionario_responsable_tribunal'),
                'firma_tribunal': data.get('firma_funcionario_tribunal'),
                'respaldo_tribunal': data.get('respaldo_tribunal'),
                'tipo_medida_otras': data.get('tipo_medida_otras'),
                'descripcion_otras': data.get('descripcion_otras'),
                'funcionario_otras': data.get('funcionario_responsable_otras'),
                'firma_otras': data.get('firma_funcionario_otras'),
                'respaldo_otras': data.get('respaldo_otras'),
            }
            # Usamos update_or_create para manejar tanto la creación como la edición
            obj, created = Derivacion.objects.update_or_create( # <-- CORREGIDO
                protocolo=protocolo,
                defaults=defaults_data
            )
            return redirect('protocolos:editar_paso4', protocolo_id=protocolo.id)
    else:
        # Replicamos la lógica para pre-rellenar el formulario
        initial_data = {}
        if instancia:
            initial_data = {
                'tipo_derivacion': instancia.derivaciones.split(', ') if instancia.derivaciones else [],
                'fecha_lesiones': instancia.fecha_lesiones,
                'institucion_lesiones': instancia.institucion_lesiones,
                'funcionario_responsable_lesiones': instancia.funcionario_lesiones,
                'firma_funcionario_lesiones': instancia.firma_lesiones,
                'respaldo_lesiones': instancia.respaldo_lesiones,
                'fecha_delito': instancia.fecha_delito,
                'institucion_delito': instancia.institucion_delito,
                'funcionario_responsable_delito': instancia.funcionario_delito,
                'firma_funcionario_delito': instancia.firma_delito,
                'respaldo_delito': instancia.respaldo_delito,
                'fecha_tribunal': instancia.fecha_tribunal,
                'institucion_tribunal': instancia.institucion_tribunal,
                'funcionario_responsable_tribunal': instancia.funcionario_tribunal,
                'firma_funcionario_tribunal': instancia.firma_tribunal,
                'respaldo_tribunal': instancia.respaldo_tribunal,
                'tipo_medida_otras': instancia.tipo_medida_otras,
                'descripcion_otras': instancia.descripcion_otras,
                'funcionario_otras': instancia.funcionario_otras,
                'firma_funcionario_otras': instancia.firma_otras,
                'respaldo_otras': instancia.respaldo_otras,
            }
        form = DerivacionForm(initial=initial_data)
        
    return render(request, 'protocolo1/formulario_paso3.html', {'form': form, 'protocolo': protocolo})

@login_required(login_url='Validaciones:login')
def editar_paso4(request, protocolo_id):
    protocolo = get_object_or_404(Protocolo, id=protocolo_id)
    instancia = get_instance_or_none(InformeConcluyente, protocolo=protocolo)
    
    if request.method == 'POST':
        form = InformeConcluyenteForm(request.POST, request.FILES, instance=instancia)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.protocolo = protocolo
            obj.save()
            return redirect('protocolos:editar_paso5', protocolo_id=protocolo.id)
    else:
        form = InformeConcluyenteForm(instance=instancia)
        
    return render(request, 'protocolo1/formulario_paso4.html', {'form': form, 'protocolo': protocolo})

@login_required(login_url='Validaciones:login')
def editar_paso5(request, protocolo_id):
    protocolo = get_object_or_404(Protocolo, id=protocolo_id)
    instancia = get_instance_or_none(Apelacion, protocolo=protocolo)
    
    if request.method == 'POST':
        form = ApelacionForm(request.POST, request.FILES, instance=instancia)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.protocolo = protocolo
            obj.save()
            return redirect('protocolos:editar_paso6', protocolo_id=protocolo.id)
    else:
        form = ApelacionForm(instance=instancia)
        
    return render(request, 'protocolo1/formulario_paso5.html', {'form': form, 'protocolo': protocolo})

@login_required(login_url='Validaciones:login')
def editar_paso6(request, protocolo_id):
    protocolo = get_object_or_404(Protocolo, id=protocolo_id)
    instancia = get_instance_or_none(ResolucionApelacion, protocolo=protocolo)
    
    if request.method == 'POST':
        form = ResolucionApelacionForm(request.POST, request.FILES, instance=instancia)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.protocolo = protocolo
            obj.save()
            return redirect('protocolos:editar_paso7', protocolo_id=protocolo.id)
    else:
        form = ResolucionApelacionForm(instance=instancia)
        
    return render(request, 'protocolo1/formulario_paso6.html', {'form': form, 'protocolo': protocolo})

@login_required(login_url='Validaciones:login')
def editar_paso7(request, protocolo_id):
    protocolo = get_object_or_404(Protocolo, id=protocolo_id)
    instancia = get_instance_or_none(EncuestaBullying, protocolo=protocolo)
    
    if request.method == 'POST':
        form = EncuestaBullyingForm(request.POST, request.FILES, instance=instancia)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.protocolo = protocolo
            obj.save()
            messages.success(request, '¡Protocolo actualizado con éxito!')
            return redirect('protocolos:ver_protocolo', protocolo_id=protocolo.id)
    else:
        form = EncuestaBullyingForm(instance=instancia)
        
    return render(request, 'protocolo1/formulario_paso7.html', {'form': form, 'protocolo': protocolo})
