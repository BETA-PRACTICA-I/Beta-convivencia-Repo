from django.urls import path
from . import views

app_name = 'protocolos' 

urlpatterns = [
    path('iniciar/<int:tipo_id>/', views.iniciar_protocolo, name='iniciar_protocolo'),
        
        # ¡LA NUEVA URL ESTRELLA!
        # Manejará todos los pasos de todos los protocolos.
    path('<int:protocolo_id>/paso/<int:step>/', views.protocolo_step, name='protocolo_step'),

    # Complementar opciones
    path('<int:protocolo_id>/complementar/', views.complementar_protocolo, name='complementar_protocolo'),
    path('<int:protocolo_id>/complementar/apelacion/', views.complementar_apelacion, name='complementar_apelacion'),
    path('<int:protocolo_id>/complementar/evidencia/', views.complementar_evidencia, name='complementar_evidencia'),

        # Estas vistas ya las teníamos y están perfectas
    path('<int:protocolo_id>/exito/', views.formulario_exito, name='formulario_exito'),
    path('protocolo/descargar/<int:protocolo_id>/', views.descargar_protocolo_pdf, name='descargar_protocolo_pdf'),
    path('actualizar-estado/', views.actualizar_estado_protocolo, name='actualizar_estado_protocolo'),
    path('protocolo/ver/<int:protocolo_id>/', views.ver_protocolo, name='ver_protocolo'),
    path('editar/paso1/<int:protocolo_id>/', views.editar_paso1, name='editar_paso1'),
    path('editar/paso2/<int:protocolo_id>/', views.editar_paso2, name='editar_paso2'),
    path('editar/paso3/<int:protocolo_id>/', views.editar_paso3, name='editar_paso3'),
    path('editar/paso4/<int:protocolo_id>/', views.editar_paso4, name='editar_paso4'),
    path('editar/paso5/<int:protocolo_id>/', views.editar_paso5, name='editar_paso5'),
    path('editar/paso6/<int:protocolo_id>/', views.editar_paso6, name='editar_paso6'),
    path('editar/paso7/<int:protocolo_id>/', views.editar_paso7, name='editar_paso7'),
    ]
    