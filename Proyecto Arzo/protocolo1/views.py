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
            return redirect('protocolo1:formulario_paso4')  # o siguiente paso
    else:
        form = FichaEntrevistaForm()
    return render(request, 'protocolo1/formulario_paso2.html', {'form': form})

@login_required(login_url='Validaciones:login') 
def formulario_paso3(request):
    form = DerivacionForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
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

