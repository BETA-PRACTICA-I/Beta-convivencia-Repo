from django.shortcuts import render, redirect
from .forms import (FormularioDenunciaForm, FichaEntrevistaForm, DerivacionForm,
    InformeConcluyenteForm, ApelacionForm, ResolucionApelacionForm, EncuestaBullyingForm)
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required(login_url='Validaciones:login') 
def formulario_paso1(request):
    if request.method == 'POST':
        form = FormularioDenunciaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('protocolo1:formulario_paso2')  # o siguiente paso
    else:
        form = FormularioDenunciaForm()
    return render(request, 'protocolo1/formulario_paso1.html', {'form': form})

@login_required(login_url='Validaciones:login')
def formulario_paso2(request):
    if request.method == 'POST':
        form = FichaEntrevistaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('protocolo1:formulario_paso3')  # o siguiente paso
    else:
        form = FichaEntrevistaForm()
    return render(request, 'protocolo1/formulario_paso2.html', {'form': form})


@login_required(login_url='Validaciones:login') 
def formulario_paso3(request):
    form = DerivacionForm(request.POST or None, request.FILES or None) 
    
    if request.method == 'POST' and form.is_valid():
        data = form.cleaned_data
        try:
            from .models import Derivacion

            # Mapeo de campos del formulario a campos del modelo
            derivaciones = ", ".join(data['tipo_derivacion'])

            # Inicializa todos los campos en None/'' por defecto
            kwargs = {
                'derivaciones': derivaciones,
                'fecha_lesiones': None,
                'institucion_lesiones': '',
                'funcionario_lesiones': '',
                'firma_lesiones': '',
                'respaldo_lesiones': None,
                'fecha_delito': None,
                'institucion_delito': '',
                'funcionario_delito': '',
                'firma_delito': '',
                'respaldo_delito': None,
                'fecha_tribunal': None,
                'institucion_tribunal': '',
                'funcionario_tribunal': '',
                'firma_tribunal': '',
                'respaldo_tribunal': None,
                'tipo_medida_otras': '',
                'descripcion_otras': '',
                'funcionario_otras': '',
                'firma_otras': '',
                'respaldo_otras': None,
            }

            # Asigna los datos según las opciones seleccionadas
            if 'constatar_lesiones' in data['tipo_derivacion']:
                kwargs['fecha_lesiones'] = data['fecha']
                kwargs['institucion_lesiones'] = data['institucion']
                kwargs['funcionario_lesiones'] = data['funcionario_responsable']
                kwargs['firma_lesiones'] = data['firma_funcionario']
                kwargs['respaldo_lesiones'] = data['respaldo']
            if 'denuncia_delito' in data['tipo_derivacion']:
                kwargs['fecha_delito'] = data['fecha']
                kwargs['institucion_delito'] = data['institucion']
                kwargs['funcionario_delito'] = data['funcionario_responsable']
                kwargs['firma_delito'] = data['firma_funcionario']
                kwargs['respaldo_delito'] = data['respaldo']
            if 'tribunal_familia' in data['tipo_derivacion']:
                kwargs['fecha_tribunal'] = data['fecha']
                kwargs['institucion_tribunal'] = data['institucion']
                kwargs['funcionario_tribunal'] = data['funcionario_responsable']
                kwargs['firma_tribunal'] = data['firma_funcionario']
                kwargs['respaldo_tribunal'] = data['respaldo']
            if 'otras' in data['tipo_derivacion']:
                kwargs['tipo_medida_otras'] = data['tipo_medida']
                kwargs['descripcion_otras'] = data['descripcion']
                kwargs['funcionario_otras'] = data['funcionario_responsable_otras']
                kwargs['firma_otras'] = data['firma_funcionario_otras']
                kwargs['respaldo_otras'] = data['respaldo_otras']

            Derivacion.objects.create(**kwargs)

        except Exception as e:
            print(f"ERROR AL GUARDAR EL MODELO DERIVACION: {e}")

        return redirect('protocolo1:formulario_paso4')
    return render(request, 'protocolo1/formulario_paso3.html', {'form': form})


@login_required(login_url='Validaciones:login') 
def formulario_paso4(request):
    form = InformeConcluyenteForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('protocolo1:formulario_paso5')
    return render(request, 'protocolo1/formulario_paso4.html', {'form': form})

@login_required(login_url='Validaciones:login') 
def formulario_paso5(request):
    form = ApelacionForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('protocolo1:formulario_paso6')
    return render(request, 'protocolo1/formulario_paso5.html', {'form': form})

@login_required(login_url='Validaciones:login') 
def formulario_paso6(request):
    form = ResolucionApelacionForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('protocolo1:formulario_paso7')
    return render(request, 'protocolo1/formulario_paso6.html', {'form': form})

@login_required(login_url='Validaciones:login') 
def formulario_paso7(request):
    form = EncuestaBullyingForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('formulario_exito')
    return render(request, 'protocolo1/formulario_paso7.html', {'form': form})

# (Opcional) vista de Ã©xito simple
def formulario_exito(request):
    return render(request, 'protocolo1/exito.html')

# views.py
@login_required(login_url='Validaciones:login') 
def formulario_paso1(request):
    if request.method == 'POST':
        form = FormularioDenunciaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('protocolo1:formulario_paso2')  # o siguiente paso
        else:
            # Línea de depuración clave:
            print("ERRORES DEL FORMULARIO:", form.errors) 
            # -----------------------------------
    else:
        form = FormularioDenunciaForm()
    return render(request, 'protocolo1/formulario_paso1.html', {'form': form})

