from django.shortcuts import render, redirect
from .forms import FormularioDenunciaForm
from .forms import FichaEntrevistaForm

def formulario_paso1(request):
    if request.method == 'POST':
        form = FormularioDenunciaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('formulario_exito')  # o siguiente paso
    else:
        form = FormularioDenunciaForm()
    return render(request, 'app_formularios/formulario_paso1.html', {'form': form})

def formulario_paso2(request):
    if request.method == 'POST':
        form = FichaEntrevistaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('formulario_exito')  # o siguiente paso
    else:
        form = FichaEntrevistaForm()
    return render(request, 'app_formularios/formulario_paso2.html', {'form': form})

