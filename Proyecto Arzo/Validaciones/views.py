import json
from django.db.models import Count, Q
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
                is_director = user.groups.filter(name='Director').exists()

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
                
                #Opción 3: El usuario apretó "Director" (para el futuro)
                elif role_clicked == 'director':
                    if is_director:
                        return redirect("Validaciones:director_homepage")
                    else:
                        messages.error(request, "Credenciales correctas, pero no tienes permisos de Director.")
                        return redirect("Validaciones:login")

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
                .filter(estado='Pendiente')
                .select_related('tipo', 'creador')
                .order_by('-fecha_creacion'))
    
    tipos = TipoProtocolo.objects.all()

    return render(request, "Validaciones/homepage.html", {
        "tipos": tipos,
        "protocolos": protocolos_filtrados,
    })


@login_required
def Almacen_view(request):
    # Empezamos con los protocolos resueltos y traemos datos relacionados para optimizar
    protocolos_query = Protocolo.objects.filter(estado='Resuelto').select_related('tipo', 'ficha_denuncia', 'creador')

    # 1. Búsqueda por texto (parámetro 'q')
    query = request.GET.get('q')
    if query:
        # Busca en varios campos a la vez, incluyendo el ID del protocolo
        protocolos_query = protocolos_query.filter(
            Q(ficha_denuncia__nombre_denunciante__icontains=query) |
            Q(ficha_denuncia__curso_denunciado__icontains=query) |
            Q(tipo__nombre__icontains=query) |
            Q(id__icontains=query)
        )

    # 2. Filtro por tipo de protocolo
    tipo_id = request.GET.get('tipo')
    if tipo_id:
        protocolos_query = protocolos_query.filter(tipo__id=tipo_id)

    # 3. Filtro por rango de fechas
    fecha_desde = request.GET.get('fecha_desde')
    if fecha_desde:
        protocolos_query = protocolos_query.filter(fecha_creacion__date__gte=fecha_desde)
    
    fecha_hasta = request.GET.get('fecha_hasta')
    if fecha_hasta:
        protocolos_query = protocolos_query.filter(fecha_creacion__date__lte=fecha_hasta)

    # Obtenemos todos los tipos de protocolo para el dropdown del filtro
    tipos = TipoProtocolo.objects.all()

    context = {
        'protocolos': protocolos_query.order_by('-fecha_creacion'),
        'tipos': tipos,
        'user': request.user
    }
    
    return render(request, 'Validaciones/Almacen.html', context)        

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

@login_required(login_url='Validaciones:login')
def director_homepage_view(request):
    # --- Vista para Directores (Panel de Gráficos) ---
    
    # Seguridad: Si no eres Director (y no eres superadmin), no puedes estar aquí.
    if not request.user.groups.filter(name='Director').exists() and not request.user.is_superuser:
        messages.error(request, "Acceso no autorizado.")
        # Redirecciones de fallback
        if request.user.groups.filter(name='Encargados').exists():
            return redirect('Validaciones:homepage')
        if request.user.groups.filter(name='Abogados').exists():
            return redirect('Validaciones:abogado_homepage')
        return redirect('Validaciones:login') # Si no, al login

    # --- INICIA LA NUEVA LÓGICA ---

    # 1. Obtener la lista de protocolos para la TABLA (igual que abogados)
    #    Filtramos los que están 'En Creacion' porque esos no cuentan.
    protocolos_filtrados = (Protocolo.objects
                .exclude(estado='En Creacion')
                .select_related('tipo', 'creador')
                .order_by('-fecha_creacion'))

    # 2. Datos para Gráfico 1 (Barras - Protocolos por Tipo)
    #    Usamos la magia de Django 🪄 para anotar (contar) los protocolos
    #    (que no estén 'En Creacion') para CADA tipo.
    conteo_tipos_qs = TipoProtocolo.objects.annotate(
        total=Count('protocolos', filter=~Q(protocolos__estado='En Creacion'))
    ).order_by('id') # Usamos 'id' para que el orden sea consistente

    # Creamos las listas que Chart.js necesita
    labels_tipos = [tipo.nombre for tipo in conteo_tipos_qs]
    data_tipos = [tipo.total for tipo in conteo_tipos_qs]

    # 3. Datos para Gráfico 2 (Circular - Protocolos por Estado)
    #    Reutilizamos la consulta de la tabla para contar por estado
    conteo_estados = protocolos_filtrados.values('estado').annotate(total=Count('estado')).order_by()

    # Convertimos el resultado (que es una lista de diccionarios)
    # en un diccionario simple para buscar fácil (Ej: {'Pendiente': 12, 'Resuelto': 8})
    conteo_dict = {item['estado']: item['total'] for item in conteo_estados}

    # Preparamos las listas finales, asegurando el orden
    # y poniendo 0 si un estado no tiene protocolos.
    labels_estados = ['Pendiente', 'Resuelto', 'Vencido']
    data_estados = [
        conteo_dict.get('Pendiente', 0),
        conteo_dict.get('Resuelto', 0),
        conteo_dict.get('Vencido', 0)
    ]

    # 4. Preparar el contexto final
    context = {
        'protocolos': protocolos_filtrados, # Para la tabla
        
        # Usamos json.dumps para pasar las listas de forma segura a JavaScript
        'chart_labels_tipos': json.dumps(labels_tipos),
        'chart_data_tipos': json.dumps(data_tipos),
        'chart_labels_estados': json.dumps(labels_estados),
        'chart_data_estados': json.dumps(data_estados),
    } 
    
    return render(request, "Validaciones/directorhomepage.html", context)

