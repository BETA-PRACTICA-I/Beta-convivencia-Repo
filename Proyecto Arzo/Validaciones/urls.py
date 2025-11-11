from django.urls import path
from . import views

# El app_name es crucial para que {% url 'Validaciones:login' %} funcione
app_name = 'Validaciones'

urlpatterns = [
    path('', views.Login_view, name='login'),
    
    path('homepage/', views.Home_view, name='homepage'),

    path('homepage/Almacen', views.Almacen_view, name='Almacen'),

    path('abogado/homepage/', views.abogado_homepage_view, name='abogado_homepage'),

    path('director/homepage/', views.director_homepage_view, name='director_homepage'),
    
]