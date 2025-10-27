from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import (
    FormularioDenunciaForm, FichaEntrevistaForm, DerivacionForm,
    InformeConcluyenteForm, ApelacionForm, ResolucionApelacionForm, EncuestaBullyingForm
)
from .models import Protocolo, TipoProtocolo, Derivacion as DerivacionModel
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML
from django.utils import timezone

@login_required(login_url='Validaciones:login')
def iniciar_protocolo(request, tipo_id):
    tipo = get_object_or_404(TipoProtocolo, id=tipo_id)
    protocolo = Protocolo.objects.create(tipo=tipo, creador=request.user)
    return redirect('protocolo1:formulario_paso1', protocolo_id=protocolo.id)

@login_required(login_url='Validaciones:login')
def formulario_paso1(request, protocolo_id):
    protocolo = get_object_or_404(Protocolo, id=protocolo_id)
    if request.method == 'POST':
        form = FormularioDenunciaForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.protocolo = protocolo
            obj.save()
            return redirect('protocolo1:formulario_paso2', protocolo_id=protocolo.id)
        else:
            # DEBUG: imprime errores en la consola y muestra mensaje en la plantilla
            print("ERRORES FormularioDenuncia:", form.errors)   # ver en la consola donde corre runserver
            messages.error(request, "Hay errores en el formulario. Revisa los campos marcados.")
    else:
        form = FormularioDenunciaForm()
    return render(request, 'protocolo1/formulario_paso1.html', {'form': form, 'protocolo': protocolo})

@login_required(login_url='Validaciones:login')
def formulario_paso2(request, protocolo_id):
    protocolo = get_object_or_404(Protocolo, id=protocolo_id)
    if request.method == 'POST':
        form = FichaEntrevistaForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.protocolo = protocolo
            obj.save()
            return redirect('protocolo1:formulario_paso3', protocolo_id=protocolo.id)
        else:
            print("ERRORES FichaEntrevista:", form.errors)
            messages.error(request, "Hay errores en el formulario (paso 2). Revisa los campos marcados.")
    else:
        form = FichaEntrevistaForm()
    return render(request, 'protocolo1/formulario_paso2.html', {'form': form, 'protocolo': protocolo})

@login_required(login_url='Validaciones:login')
def formulario_paso3(request, protocolo_id):
    protocolo = get_object_or_404(Protocolo, id=protocolo_id)
    if request.method == 'POST':
        form = DerivacionForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data
            derivacion_obj = DerivacionModel(derivaciones=", ".join(data['tipo_derivacion']))
            # Asignar campos opcionales según selección
            if 'constatar_lesiones' in data['tipo_derivacion']:
                derivacion_obj.fecha_lesiones = data.get('fecha_lesiones')
                derivacion_obj.institucion_lesiones = data.get('institucion_lesiones')
                derivacion_obj.funcionario_lesiones = data.get('funcionario_responsable_lesiones')
                derivacion_obj.firma_lesiones = data.get('firma_funcionario_lesiones')
                derivacion_obj.respaldo_lesiones = data.get('respaldo_lesiones')
            if 'denuncia_delito' in data['tipo_derivacion']:
                derivacion_obj.fecha_delito = data.get('fecha_delito')
                derivacion_obj.institucion_delito = data.get('institucion_delito')
                derivacion_obj.funcionario_delito = data.get('funcionario_responsable_delito')
                derivacion_obj.firma_delito = data.get('firma_funcionario_delito')
                derivacion_obj.respaldo_delito = data.get('respaldo_delito')
            if 'tribunal_familia' in data['tipo_derivacion']:
                derivacion_obj.fecha_tribunal = data.get('fecha_tribunal')
                derivacion_obj.institucion_tribunal = data.get('institucion_tribunal')
                derivacion_obj.funcionario_tribunal = data.get('funcionario_responsable_tribunal')
                derivacion_obj.firma_tribunal = data.get('firma_funcionario_tribunal')
                derivacion_obj.respaldo_tribunal = data.get('respaldo_tribunal')
            if 'otras' in data['tipo_derivacion']:
                derivacion_obj.tipo_medida_otras = data.get('tipo_medida_otras')
                derivacion_obj.descripcion_otras = data.get('descripcion_otras')
                derivacion_obj.funcionario_otras = data.get('funcionario_responsable_otras')
                derivacion_obj.firma_otras = data.get('firma_funcionario_otras')
                derivacion_obj.respaldo_otras = data.get('respaldo_otras')
            derivacion_obj.protocolo = protocolo
            derivacion_obj.save()
            return redirect('protocolo1:formulario_paso4', protocolo_id=protocolo.id)
        else:
            print("ERRORES DERIVACION:", form.errors)
    else:
        form = DerivacionForm()
    return render(request, 'protocolo1/formulario_paso3.html', {'form': form, 'protocolo': protocolo})

@login_required(login_url='Validaciones:login')
def formulario_paso4(request, protocolo_id):
    protocolo = get_object_or_404(Protocolo, id=protocolo_id)
    form = InformeConcluyenteForm(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        if form.is_valid():
            obj = form.save(commit=False)
            obj.protocolo = protocolo
            obj.save()
            return redirect('protocolo1:formulario_paso5', protocolo_id=protocolo.id)
        else:
            # DEBUG: mostrar errores en consola y mensaje al usuario
            print("ERRORES InformeConcluyente:", form.errors)   # revisa la consola donde corre runserver
            messages.error(request, "Hay errores en el formulario (paso 4). Revisa los campos marcados.")
    return render(request, 'protocolo1/formulario_paso4.html', {'form': form, 'protocolo': protocolo})

@login_required(login_url='Validaciones:login')
def formulario_paso5(request, protocolo_id):
    protocolo = get_object_or_404(Protocolo, id=protocolo_id)
    form = ApelacionForm(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        if form.is_valid():
            obj = form.save(commit=False)
            obj.protocolo = protocolo
            obj.save()
            return redirect('protocolo1:formulario_paso6', protocolo_id=protocolo.id)
        else:
            print("ERRORES Apelacion:", form.errors)
            messages.error(request, "Hay errores en el formulario (paso 5). Revisa los campos marcados.")
    return render(request, 'protocolo1/formulario_paso5.html', {'form': form, 'protocolo': protocolo})

@login_required(login_url='Validaciones:login')
def formulario_paso6(request, protocolo_id):
    protocolo = get_object_or_404(Protocolo, id=protocolo_id)
    form = ResolucionApelacionForm(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        if form.is_valid():
            obj = form.save(commit=False)
            obj.protocolo = protocolo
            obj.save()
            return redirect('protocolo1:formulario_paso7', protocolo_id=protocolo.id)
        else:
            print("ERRORES ResolucionApelacion:", form.errors)
            messages.error(request, "Hay errores en el formulario (paso 6). Revisa los campos marcados.")
    return render(request, 'protocolo1/formulario_paso6.html', {'form': form, 'protocolo': protocolo})

@login_required(login_url='Validaciones:login')
def formulario_paso7(request, protocolo_id):
    protocolo = get_object_or_404(Protocolo, id=protocolo_id)
    # Si ya existe una encuesta para este protocolo, editarla; si no, crear nueva
    instancia_existente = None
    try:
        instancia_existente = protocolo.encuestabullying
    except Exception:
        instancia_existente = None

    form = EncuestaBullyingForm(request.POST or None, request.FILES or None, instance=instancia_existente)
    if request.method == 'POST':
        if form.is_valid():
            obj = form.save(commit=False)
            obj.protocolo = protocolo
            obj.save()
            return redirect('protocolo1:formulario_exito', protocolo_id=protocolo.id)
        else:
            print("ERRORES EncuestaBullying:", form.errors)
            messages.error(request, "Hay errores en el formulario (paso 7). Revisa los campos marcados.")
    return render(request, 'protocolo1/formulario_paso7.html', {'form': form, 'protocolo': protocolo})

def formulario_exito(request, protocolo_id=None):
    if protocolo_id:
        try:
            protocolo = Protocolo.objects.get(id=protocolo_id)
            # Cambiamos su estado de 'En Creacion' a 'Pendiente'
            protocolo.estado = 'Pendiente'
            protocolo.save() # Guardamos el cambio en la base de datos
        except Protocolo.DoesNotExist:
            # Si por alguna razón no se encuentra, mostramos un error
            messages.error(request, "Error: No se pudo encontrar el protocolo para finalizarlo.")
            return redirect('Validaciones:homepage')

    return render(request, 'protocolo1/exito.html', {'protocolo_id': protocolo_id})

@login_required(login_url='Validaciones:login')
def descargar_protocolo_pdf(request, protocolo_id):
    # 1. Obtener el protocolo con todos sus datos relacionados para optimizar la consulta.
    protocolo = get_object_or_404(
        Protocolo.objects.select_related(
            'ficha_denuncia', 
            'fichaentrevista', 
            'derivacion', 
            'informeconcluyente', 
            'apelacion', 
            'resolucionapelacion', 
            'encuestabullying'
        ), 
        id=protocolo_id
    )

    # 2. Preparar el contexto para la plantilla del PDF.
    context = {
        'protocolo': protocolo,
        'fecha_actual': timezone.now(),
        'request': request
    }

    # 3. Renderizar la plantilla HTML a una cadena de texto.
    html_string = render_to_string('protocolo1/protocolo_pdf.html', context)

    # 4. Generar el PDF en memoria desde la cadena HTML.
    pdf_file = HTML(string=html_string, base_url=request.build_absolute_uri('/')).write_pdf()

    # 5. Crear la respuesta HTTP con el contenido del PDF.
    response = HttpResponse(pdf_file, content_type='application/pdf')
    
    # 6. Añadir la cabecera 'Content-Disposition' para forzar la descarga del archivo.
    response['Content-Disposition'] = f'attachment; filename="protocolo_{protocolo.id}_{protocolo.tipo.nombre}.pdf"'

    return response

def ver_protocolo(request, protocolo_id):

    # Usamos la misma lógica eficiente para obtener todos los datos
    protocolo = get_object_or_404(
        Protocolo.objects.select_related(
            'tipo',
            'ficha_denuncia', 
            'fichaentrevista', 
            'derivacion', 
            'informeconcluyente', 
            'apelacion', 
            'resolucionapelacion', 
            'encuestabullying'
        ), 
        id=protocolo_id
    )

    context = {
        'protocolo': protocolo
    }

    return render(request, 'protocolo1/ver_protocolo.html', context)