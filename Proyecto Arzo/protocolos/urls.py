from django.urls import path
from . import views

app_name = 'protocolos' 

urlpatterns = [
        # Esta URL la tenías en 'Validaciones' quizás, pero es para iniciar
    path('iniciar/<int:tipo_id>/', views.iniciar_protocolo, name='iniciar_protocolo'),
        
        # ¡LA NUEVA URL ESTRELLA!
        # Manejará todos los pasos de todos los protocolos.
    path('<int:protocolo_id>/paso/<int:step>/', views.protocolo_step, name='protocolo_step'),

        # Estas vistas ya las teníamos y están perfectas
    path('<int:protocolo_id>/exito/', views.formulario_exito, name='formulario_exito'),
    path('protocolo/descargar/<int:protocolo_id>/', views.descargar_protocolo_pdf, name='descargar_protocolo_pdf'),
    path('protocolo/ver/<int:protocolo_id>/', views.ver_protocolo, name='ver_protocolo'),
    ]
    