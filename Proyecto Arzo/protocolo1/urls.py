"""formulario URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from . import views

app_name = 'protocolo1'

urlpatterns = [
    path('iniciar/<int:tipo_id>/', views.iniciar_protocolo, name='iniciar_protocolo'),
    path('<int:protocolo_id>/paso1/', views.formulario_paso1, name='formulario_paso1'),
    path('<int:protocolo_id>/paso2/', views.formulario_paso2, name='formulario_paso2'),
    path('<int:protocolo_id>/paso3/', views.formulario_paso3, name='formulario_paso3'),
    path('<int:protocolo_id>/paso4/', views.formulario_paso4, name='formulario_paso4'),
    path('<int:protocolo_id>/paso5/', views.formulario_paso5, name='formulario_paso5'),
    path('<int:protocolo_id>/paso6/', views.formulario_paso6, name='formulario_paso6'),
    path('<int:protocolo_id>/paso7/', views.formulario_paso7, name='formulario_paso7'),
    path('<int:protocolo_id>/exito/', views.formulario_exito, name='formulario_exito'),
]