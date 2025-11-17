from django.urls import path
from . import views

app_name = 'Validaciones'  # No cambies esto, es para que funcionen los redirects

urlpatterns = [
    # 1. Corregido: views.Login_view -> views.login_view
    path('', views.login_view, name='login'), 
    
    path('logout/', views.logout_view, name='logout'),
    
    # 2. Corregido: views.Home_view -> views.homepage
    path('homepage/', views.homepage, name='homepage'), # Esta es la homepage del Encargado
    
    # 3. Corregido: views.Abogado_view -> views.abogadohomepage
    path('abogadohomepage/', views.abogadohomepage, name='abogadohomepage'),
    
    # 4. Corregido: views.Director_view -> views.directorhomepage
    path('directorhomepage/', views.directorhomepage, name='directorhomepage'),
    
    path('almacen/', views.Almacen, name='Almacen'),
]