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
    if request.method == 'POST':
        form = DerivacionForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data
            try:
                from .models import Derivacion

                # Crea una instancia del modelo Derivacion
                derivacion_obj = Derivacion(
                    derivaciones=", ".join(data['tipo_derivacion'])
                )

                # Asigna los datos directamente si la opción fue seleccionada
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

                # Guarda el objeto en la base de datos
                derivacion_obj.save()

                return redirect('protocolo1:formulario_paso4')
            except Exception as e:
                print(f"ERROR AL GUARDAR EL MODELO DERIVACION: {e}")
    else:
        form = DerivacionForm()
        
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

