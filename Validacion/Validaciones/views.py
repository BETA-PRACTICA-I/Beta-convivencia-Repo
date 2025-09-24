from django.shortcuts import render,redirect #Para devolver pagina HTML y redirigir a otra url
from django.contrib.auth import authenticate, login #verifica con bd y crea sesion
from django.contrib import messages #para mensajes de ingresó correctamente o las credenciales son invalidas
from django.contrib.auth.decorators import login_required #obliga que el usuario este logeado para avanzar
from .forms import LoginForm #importamos el formulario

# Create your views here.

def Login_view(request):
    if request.method == 'POST': #verificamos si la informacion esta entrando al formulario
        form = LoginForm(request.POST) #le pasamos a form los datos ingresados
        if form.is_valid(): 
            username = form.cleaned_data["username"]#"sanitiza" los datos #ejemplo "hola que tal" a "holaquetal"
            password = form.cleaned_data["password"]# extrae y "asigna los datos limpios"

            #aqui es donde se autentica el usuario 
            user = authenticate(request, username=username, password=password)

            #si el usuario coincide 
            if user is not None:
                    #lo logeamos 
                    login(request,user) #crea la sesion con el usuario autenticado

                    messages.success(request,f"¡Hola, bienvenido!")
                    return redirect("homepage") #redirecciona a la homepage
            else:
                messages.error(request,f"Las credenciales son incorrectas")
        else:
            messages.warning(request,f"Favor revisar nuevamente datos ingresados.")
    else:
        form = LoginForm() #caso formulario vacio, lo devuelve al login   
    
    return render(request, "Validaciones/Login.html", {"form": form}) #renvia al login en todos los casos fallidos 

def Home_view(request): #vista de la hompage
    return render(request, "Validaciones/homepage.html") #renderiza la plantilla hompage


