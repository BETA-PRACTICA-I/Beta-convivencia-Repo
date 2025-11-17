document.addEventListener("DOMContentLoaded", function() {

    // --- 1. Seleccionamos todos los elementos que necesitamos ---

    // El contenedor principal que se anima
    const loginContainer = document.getElementById('login-container');
    
    // Obtenemos TODOS los botones de rol (será una lista)
    const botonesRol = document.querySelectorAll('.btn-rol');
    
    // El botón para "Volver" a la selección de rol
    const btnVolver = document.getElementById('btn-volver');
    
    // El campo <input type="hidden"> donde guardaremos el rol
    const campoRolOculto = document.getElementById('role-input');
    
    // El título <h2> que dice "¡Bienvenido!"
    const campoSaludo = document.getElementById('saludo-rol');

    
    // --- 2. Lógica para los botones de Rol ---

    // Recorremos la lista de botones de rol (Encargado, Abogado, Director)
    botonesRol.forEach(boton => {
        
        // A cada botón, le agregamos un "escuchador" de clics
        boton.addEventListener('click', () => {
            
            // Cuando se hace clic, leemos los datos del botón
            const rol = boton.dataset.role;     // Ej: "director"
            const saludo = boton.dataset.saludo; // Ej: "¡Hola, señor Director!"
            
            // 1. Actualizamos el valor del campo oculto del formulario
            campoRolOculto.value = rol;
            
            // 2. Actualizamos el texto del saludo
            campoSaludo.innerText = saludo;
            
            // 3. ¡LA MAGIA! Agregamos la clase que activa la animación CSS
            loginContainer.classList.add('modo-login');
        });
    });

    
    // --- 3. Lógica para el botón "Volver" ---
    
    // Agregamos un "escuchador" de clic al botón de volver
    btnVolver.addEventListener('click', () => {
        
        // 1. ¡LA MAGIA INVERSA! Quitamos la clase para volver al inicio
        loginContainer.classList.remove('modo-login');

        // 2. Opcional: Limpiamos el campo de rol por si acaso
        campoRolOculto.value = "";
    });

});