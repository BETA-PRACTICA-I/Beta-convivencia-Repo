from django import forms

class LoginForm(forms.Form): #Clase base de Django para crear formulario
    username = forms.CharField(label="Usuario", max_length=150,  
            widget=forms.TextInput(attrs={
            "placeholder": "Usuario",
            "class": "input",
        }),
        error_messages={
            "required": "Ingresa tu usuario.",
            "max_length": "El usuario no puede superar 150 caracteres.",},)
    
    
    password = forms.CharField(label="Contraseña",max_length=128, 
        widget=forms.PasswordInput(attrs={
            "placeholder": "Contraseña",
            "class": "input",}),
        error_messages={
            "required": "Ingresa tu contraseña.",},)