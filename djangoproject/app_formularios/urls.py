from django.urls import path
from . import views

urlpatterns = [
    path('formulario/', views.formulario_paso1, name='formulario_paso1'),
    path('formulario2/', views.formulario_paso2, name='formulario_paso2'),
]
