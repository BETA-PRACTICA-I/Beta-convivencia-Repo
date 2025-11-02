from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import LoginForm
from django.utils.http import url_has_allowed_host_and_scheme

# Importar modelos para las vistas de homepage
from protocolos.models import TipoProtocolo, Protocolo
# Importante para chequear grupos
from django.contrib.auth.models import Group 

# Create your views here.

def Login_view(request):
    next_url = request.GET.get('next') or request.POST.get('next')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        
        # --- ¡PASO 1: LEEMOS QUÉ BOTÓN SE APRETÓ! ---
        # Esto viene del input <input type="hidden" name="role_type" ...>
        role_clicked = request.POST.get("role_type") 
        
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            
            user = authenticate(request, username=username, password=password)

            if user is not None:
                # El usuario y contraseña son correctos.
                login(request, user)
                messages.success(request, f"¡Hola, bienvenido!")

                # --- ¡PASO 2: LÓGICA DE REDIRECCIÓN BASADA EN EL BOTÓN! ---
                
                # Revisamos los permisos REALES del usuario
                is_abogado = user.groups.filter(name='Abogados').exists()
                is_encargado = user.groups.filter(name='Encargados').exists()
                # is_director = user.groups.filter(name='Directores').exists()

                # --- REVISAMOS EL BOTÓN APRETADO PRIMERO ---

                # Opción 1: El usuario apretó "Encargado"
                if role_clicked == 'encargado':
                    if is_encargado:
                        # Apretó "Encargado" y SÍ es Encargado. ¡Adelante!
                        return redirect("Validaciones:homepage")
                    else:
                        # Apretó "Encargado" pero NO es Encargado.
                        messages.error(request, "Credenciales correctas, pero no tienes permisos de Encargado.")
                        return redirect("Validaciones:login")

                # Opción 2: El usuario apretó "Abogado"
                elif role_clicked == 'abogado':
                    if is_abogado:
                        # Apretó "Abogado" y SÍ es Abogado. ¡Adelante!
                        return redirect("Validaciones:abogado_homepage")
                    else:
                        # Apretó "Abogado" pero NO es Abogado.
                        messages.error(request, "Credenciales correctas, pero no tienes permisos de Abogado.")
                        return redirect("Validaciones:login")
                
                # Opción 3: El usuario apretó "Director" (para el futuro)
                # elif role_clicked == 'director':
                #    if is_director:
                #        return redirect("Validaciones:director_homepage")
                #    else:
                #        messages.error(request, "Credenciales correctas, pero no tienes permisos de Director.")
                #        return redirect("Validaciones:login")

                # Fallback: Si el rol no se reconoce (o el JS falló)
                else:
                    messages.error(request, "No se pudo determinar el rol seleccionado.")
                    return redirect("Validaciones:login")

            else:
                # El usuario o contraseña eran incorrectos
                messages.error(request, f"Las credenciales son incorrectas")
        else:
            # El formulario no fue válido (ej. campos vacíos)
            messages.warning(request, f"Favor revisar nuevamente datos ingresados.")
    else:
        form = LoginForm()
    
    # Si es GET, o si el form/auth falló, mostramos el login de nuevo
    return render(request, "Validaciones/Login.html", {"form": form})


# =========================================================================
# VISTAS DE HOMEPAGE (CON SEGURIDAD MEJORADA)
# =========================================================================

@login_required(login_url='Validaciones:login') 
def Home_view(request):
    # --- Vista para Encargados de Convivencia ---
    
    # Seguridad: Si no eres Encargado (y no eres superadmin), no puedes estar aquí.
    if not request.user.groups.filter(name='Encargados').exists() and not request.user.is_superuser:
        messages.error(request, "Acceso no autorizado.")
        # Si es abogado, lo mandamos a su panel por si acaso
        if request.user.groups.filter(name='Abogados').exists():
            return redirect('Validaciones:abogado_homepage')
        return redirect('Validaciones:login') # Si no, al login

    protocolos_filtrados = (Protocolo.objects
                .exclude(estado='En Creacion')
                .select_related('tipo', 'creador')
                .order_by('-fecha_creacion'))
    
    tipos = TipoProtocolo.objects.all()

    return render(request, "Validaciones/homepage.html", {
        "tipos": tipos,
        "protocolos": protocolos_filtrados,
    })


@login_required(login_url='Validaciones:login')
def abogado_homepage_view(request):
    # --- Vista "Solo Lectura" para Abogados ---

    # Seguridad: Si no eres Abogado (y no eres superadmin), no puedes estar aquí.
    if not request.user.groups.filter(name='Abogados').exists() and not request.user.is_superuser:
        messages.error(request, "Acceso no autorizado.")
        # Si es encargado, lo mandamos a su panel por si acaso
        if request.user.groups.filter(name='Encargados').exists():
            return redirect('Validaciones:homepage')
        return redirect('Validaciones:login') # Si no, al login

    protocolos_filtrados = (Protocolo.objects
                .exclude(estado='En Creacion')
                .select_related('tipo', 'creador')
                .order_by('-fecha_creacion'))

    return render(request, "Validaciones/abogadohomepage.html", {
        "protocolos": protocolos_filtrados,
    })

