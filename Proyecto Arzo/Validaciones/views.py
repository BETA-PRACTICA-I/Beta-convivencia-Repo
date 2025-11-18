import json
from django.db.models import Count, Q
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import LoginForm
from django.utils.http import url_has_allowed_host_and_scheme

# Importar modelos para las vistas de homepage
from protocolos.models import TipoProtocolo, Protocolo
# Relaciones que necesitamos tener a mano para los resúmenes mostrados en la home.
SUMMARY_RELATIONS = (
    'tipo', 'creador',
    'ficha_denuncia',
    'fichaentrevista',
    'informeconcluyente',
    'apelacion',
    'resolucionapelacion',
    'encuestabullying',
    'riesgo_suicida_anexo1',
    'riesgo_suicida_anexo2',
    'riesgo_suicida_anexo3',
    'riesgo_suicida_anexo4',
    'riesgo_suicida_anexo5',
    'reconocimiento_identidad',
    'acta_reunion_identidad',
    'ficha_accidente_escolar',
    'anexo_armas',
    'anexo_autolesion',
    'ficha0_madre_padre',
    'ficha1_madre_padre',
    'ficha2_madre_padre',
    'salida_pedagogica_anexo1',
    'desregulacion_emocional',
    'mediacion_informacion',
    'mediacion_acta_final',
)

# -----------------------------------------------------------------
# VISTA DE LOGIN (MODIFICADA)
# -----------------------------------------------------------------
def login_view(request):
    # Si el método es POST, significa que el usuario envió el formulario
    if request.method == 'POST':
        form = LoginForm(request.POST)
        
        # --- ¡NUEVA LÍNEA! ---
        # Capturamos el 'role' (ej: 'director') que enviamos desde 
        # el input oculto en el HTML.
        rol_seleccionado = request.POST.get('role')
        
        # Comprobamos si el formulario es válido (campos llenos, etc.)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            
            # Autenticamos al usuario con su RUT y contraseña
            user = authenticate(request, username=username, password=password)
            
            # Si el usuario es None, RUT o contraseña están incorrectos
            if user is not None:
                
                # --- ¡LÓGICA MODIFICADA! ---
                # Ahora que sabemos que el usuario existe,
                # verificamos que el ROL que seleccionó en la pantalla
                # coincida con los grupos a los que pertenece.
                
                if rol_seleccionado == 'encargado' and user.groups.filter(name='Encargados').exists():
                    login(request, user)
                    return redirect("Validaciones:homepage")
                
                elif rol_seleccionado == 'abogado' and user.groups.filter(name='Abogados').exists():
                    login(request, user)
                    return redirect("Validaciones:abogadohomepage")
                
                elif rol_seleccionado == 'director' and user.groups.filter(name='Director').exists():
                    login(request, user)
                    return redirect("Validaciones:directorhomepage")
                
                else:
                    # Si el usuario es válido, pero el rol que seleccionó
                    # no es el correcto (ej: es 'encargado' e intentó entrar como 'director')
                    messages.error(request, f'Usted no tiene permisos para acceder al rol de "{rol_seleccionado}".')
                    return render(request, 'Validaciones/Login.html', {'form': form})
                
                # --- FIN DE LA LÓGICA MODIFICADA ---

            else:
                # Si user es None (RUT o contraseña incorrectos)
                messages.error(request, 'RUT o contraseña incorrectos.')
                return render(request, 'Validaciones/Login.html', {'form': form})
        else:
            # Si el formulario no es válido (ej: campos vacíos)
            messages.error(request, 'Formulario inválido.')
            return render(request, 'Validaciones/Login.html', {'form': form})
    
    # Si el método es GET (primera vez que carga la página)
    else:
        form = LoginForm()
    
    # Renderizamos la nueva plantilla de Login
    return render(request, 'Validaciones/Login.html', {'form': form})

# -----------------------------------------------------------------
# VISTAS DE HOME (AQUÍ ESTÁ LA CORRECCIÓN)
# -----------------------------------------------------------------

@login_required
def homepage(request):
    
    # --- ¡CAMBIO 1! ---
    # Obtenemos la lista de TODOS los tipos de protocolo para el menú "Crear Nuevo"
    tipos = TipoProtocolo.objects.all().order_by('nombre')
    
    query = request.GET.get('q', '')
    
    # --- ¡CAMBIO 2! ---
    # Excluimos los protocolos 'En Creacion' Y 'Resuelto' de la tabla principal
    protocolos_filtrados = Protocolo.objects.select_related(
        'creador', 'tipo'
    ).prefetch_related(
        *SUMMARY_RELATIONS
    ).exclude(
        Q(estado='En Creacion') | Q(estado='Resuelto')
    ).order_by('-fecha_creacion')
    # --- FIN DEL CAMBIO ---

    if query:
        protocolos_filtrados = protocolos_filtrados.filter(
            Q(creador__first_name__icontains=query) |
            Q(creador__last_name__icontains=query) |
            Q(tipo__nombre__icontains=query) |
            Q(estado__icontains=query)
        ).distinct()

    # Los gráficos seguirán mostrando todos los estados (excepto 'En Creacion')
    # para tener una vista general.
    conteo_base_graficos = Protocolo.objects.exclude(estado='En Creacion')

    conteo_tipos_qs = TipoProtocolo.objects.annotate(
        total=Count('protocolos', filter=Q(protocolos__in=conteo_base_graficos))
    ).order_by('nombre')
    
    labels_tipos = [tipo.nombre for tipo in conteo_tipos_qs]
    data_tipos = [tipo.total for tipo in conteo_tipos_qs]

    conteo_estados = conteo_base_graficos.values('estado').annotate(total=Count('estado')).order_by()
    conteo_dict = {item['estado']: item['total'] for item in conteo_estados}
    labels_estados = ['Pendiente', 'Resuelto', 'Vencido']
    data_estados = [
        conteo_dict.get('Pendiente', 0),
        conteo_dict.get('Resuelto', 0),
        conteo_dict.get('Vencido', 0)
    ]

    context = {
        'protocolos': protocolos_filtrados,
        'search_query': query,
        
        # --- ¡CAMBIO 3! ---
        # Añadimos la lista 'tipos' al contexto para que el HTML la pueda usar
        'tipos': tipos,
        
        'chart_labels_tipos': json.dumps(labels_tipos),
        'chart_data_tipos': json.dumps(data_tipos),
        'chart_labels_estados': json.dumps(labels_estados),
        'chart_data_estados': json.dumps(data_estados),
    }
    return render(request, 'Validaciones/homepage.html', context)

@login_required
def abogadohomepage(request):
    # Aplicamos los mismos cambios para la vista de Abogado
    
    tipos = TipoProtocolo.objects.all().order_by('nombre') # <-- CAMBIO 1
    query = request.GET.get('q', '')
    
    # <-- CAMBIO 2
    protocolos_filtrados = Protocolo.objects.select_related(
        'creador', 'tipo'
    ).prefetch_related(
        *SUMMARY_RELATIONS
    ).exclude(
        Q(estado='En Creacion') | Q(estado='Resuelto')
    ).order_by('-fecha_creacion')

    if query:
        protocolos_filtrados = protocolos_filtrados.filter(
            Q(creador__first_name__icontains=query) |
            Q(creador__last_name__icontains=query) |
            Q(tipo__nombre__icontains=query) |
            Q(estado__icontains=query)
        ).distinct()
    
    conteo_base_graficos = Protocolo.objects.exclude(estado='En Creacion')
    conteo_tipos_qs = TipoProtocolo.objects.annotate(
        total=Count('protocolos', filter=Q(protocolos__in=conteo_base_graficos))
    ).order_by('nombre')
    
    labels_tipos = [tipo.nombre for tipo in conteo_tipos_qs]
    data_tipos = [tipo.total for tipo in conteo_tipos_qs]
    
    conteo_estados = conteo_base_graficos.values('estado').annotate(total=Count('estado')).order_by()
    conteo_dict = {item['estado']: item['total'] for item in conteo_estados}
    labels_estados = ['Pendiente', 'Resuelto', 'Vencido']
    data_estados = [
        conteo_dict.get('Pendiente', 0),
        conteo_dict.get('Resuelto', 0),
        conteo_dict.get('Vencido', 0)
    ]
    
    context = {
        'protocolos': protocolos_filtrados,
        'search_query': query,
        'tipos': tipos, # <-- CAMBIO 3
        'chart_labels_tipos': json.dumps(labels_tipos),
        'chart_data_tipos': json.dumps(data_tipos),
        'chart_labels_estados': json.dumps(labels_estados),
        'chart_data_estados': json.dumps(data_estados),
    }
    return render(request, 'Validaciones/abogadohomepage.html', context)


@login_required
def directorhomepage(request):
    # Aplicamos los mismos cambios para la vista de Director
    
    tipos = TipoProtocolo.objects.all().order_by('nombre') # <-- CAMBIO 1
    query = request.GET.get('q', '')

    # <-- CAMBIO 2
    protocolos_filtrados = Protocolo.objects.select_related(
        'creador', 'tipo'
    ).prefetch_related(
        *SUMMARY_RELATIONS
    ).exclude(
        Q(estado='En Creacion') | Q(estado='Resuelto')
    ).order_by('-fecha_creacion')

    if query:
        protocolos_filtrados = protocolos_filtrados.filter(
            Q(creador__first_name__icontains=query) |
            Q(creador__last_name__icontains=query) |
            Q(tipo__nombre__icontains=query) |
            Q(estado__icontains=query)
        ).distinct()

    conteo_base_graficos = Protocolo.objects.exclude(estado='En Creacion')
    conteo_tipos_qs = TipoProtocolo.objects.annotate(
        total=Count('protocolos', filter=Q(protocolos__in=conteo_base_graficos))
    ).order_by('nombre')
    
    labels_tipos = [tipo.nombre for tipo in conteo_tipos_qs]
    data_tipos = [tipo.total for tipo in conteo_tipos_qs]
    
    conteo_estados = conteo_base_graficos.values('estado').annotate(total=Count('estado')).order_by()
    conteo_dict = {item['estado']: item['total'] for item in conteo_estados}
    labels_estados = ['Pendiente', 'Resuelto', 'Vencido']
    data_estados = [
        conteo_dict.get('Pendiente', 0),
        conteo_dict.get('Resuelto', 0),
        conteo_dict.get('Vencido', 0)
    ]
    
    context = {
        'protocolos': protocolos_filtrados,
        'search_query': query,
        'tipos': tipos, # <-- CAMBIO 3
        'chart_labels_tipos': json.dumps(labels_tipos),
        'chart_data_tipos': json.dumps(data_tipos),
        'chart_labels_estados': json.dumps(labels_estados),
        'chart_data_estados': json.dumps(data_estados),
    }
    return render(request, 'Validaciones/directorhomepage.html', context)


# -----------------------------------------------------------------
# VISTA DE LOGOUT (SIN CAMBIOS)
# -----------------------------------------------------------------
def logout_view(request):
    logout(request)
    messages.success(request, 'Has cerrado sesión exitosamente.')
    return redirect('Validaciones:login')


# -----------------------------------------------------------------
# VISTA DE ALMACEN (¡AQUÍ ESTÁ LA NUEVA LÓGICA!)
# -----------------------------------------------------------------
@login_required
def Almacen(request):
    
    # --- ¡CAMBIO AQUÍ! ---
    # 1. Buscamos solo los protocolos 'Resuelto'
    protocolos_resueltos = Protocolo.objects.filter(
        estado='Resuelto'
    ).select_related(
        'creador', 'tipo'
    ).order_by('-fecha_creacion')

    # 2. Los pasamos al contexto
    context = {
        'protocolos': protocolos_resueltos
    }
    
    # 3. Renderizamos la plantilla (que ahora modificaremos)
    return render(request, 'Validaciones/Almacen.html', context)