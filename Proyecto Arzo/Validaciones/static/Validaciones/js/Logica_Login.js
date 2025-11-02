// Esperamos a que todo el contenido del DOM esté cargado
document.addEventListener("DOMContentLoaded", () => {
    
    // Contenedores principales
    const botonesContainer = document.querySelector(".botones");
    const formularioContainer = document.getElementById("formularioContainer");
    const logo = document.querySelector(".logo");

    // Formulario y sus campos
    const loginForm = document.getElementById("loginForm");
    const hiddenRoleInput = document.getElementById("role_type"); // El input oculto
    const formTitleElement = document.getElementById("form-title"); // El título del form

    // --- ¡AQUÍ ESTÁ LA MAGIA! ---
    // Seleccionamos TODOS los botones de rol
    const botonConvivencia = document.getElementById("btn-convivencia");
    const botonAbogados = document.getElementById("btn-abogados");
    const botonDirector = document.getElementById("btn-director");

    // --- FUNCIÓN REUTILIZABLE PARA MOSTRAR EL FORMULARIO ---
    function mostrarFormulario(role, title) {
        
        // 1. Guardar el rol seleccionado en el input oculto
        if (hiddenRoleInput) {
            hiddenRoleInput.value = role;
        }

        // 2. Cambiar el título del formulario (usamos 'h2' como fallback si 'form-title' no existe)
        const titleElement = formTitleElement || formularioContainer.querySelector("h2");
        if (titleElement) {
            titleElement.textContent = `Inicio de Sesión - ${title}`;
        }
        
        // 3. Ocultar botones
        if (botonesContainer) {
            botonesContainer.classList.add("oculto");
        }

        // 4. Ocultar logo (con animación)
        if (logo) {
            logo.classList.add("fade-out");
            setTimeout(() => {
                logo.style.display = "none";
            }, 700); // 0.7 segundos
        }

        // 5. Mostrar formulario (con animación)
        if (formularioContainer) {
            formularioContainer.classList.remove("oculto");
            formularioContainer.classList.add("fade-in", "visible");
        }

        // 6. Opacar fondo (si tienes estilos CSS para esto)
        document.body.classList.add("fondo-opaco");
    }

    // --- AÑADIMOS EVENT LISTENERS A *TODOS* LOS BOTONES ---

    if (botonConvivencia) {
        botonConvivencia.addEventListener("click", () => {
            // Usamos el 'data-role' que pusimos en Login.html
            mostrarFormulario(botonConvivencia.dataset.role || 'encargado', "Encargado");
        });
    }

    // --- ¡ESTE BLOQUE FALTABA EN TU ARCHIVO! ---
    if (botonAbogados) {
        botonAbogados.addEventListener("click", () => {
            // Usamos el 'data-role' que pusimos en Login.html
            mostrarFormulario(botonAbogados.dataset.role || 'abogado', "Abogado");
        });
    }
    
    // --- ¡Y ESTE TAMBIÉN! ---
    if (botonDirector) {
        botonDirector.addEventListener("click", () => {
             // Dejamos esto listo para el futuro
            mostrarFormulario(botonDirector.dataset.role || 'director', "Director");
        });
    }

    // --- VALIDACIÓN DEL FORMULARIO (igual que antes) ---
    if (loginForm) {
        loginForm.addEventListener("submit", function (e) {
            const rut = document.getElementById("Rut")?.value.trim() || "";
            const password = document.getElementById("password")?.value || "";

            if (!rut || !password) {
                e.preventDefault(); 
                // Evitaremos el alert() ya que no funciona en el iFrame
                console.error("RUT y contraseña son obligatorios.");
                // Podrías mostrar un mensaje de error en el HTML si quisieras
            }
        });
    }
});

