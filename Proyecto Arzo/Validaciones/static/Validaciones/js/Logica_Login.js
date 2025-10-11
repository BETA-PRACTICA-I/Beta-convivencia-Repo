// Selecciona el botón de Convivencia y el contenedor de botones
const botonConvivencia = document.getElementById("btn-convivencia");
const botonesContainer = document.querySelector(".botones");
const formularioContainer = document.getElementById("formularioContainer");
const logo = document.querySelector(".logo");

// Animación al hacer click
botonConvivencia.addEventListener("click", () => {
    // Oculta los botones instantáneamente
    botonesContainer.classList.add("oculto");

    // Animación para ocultar el logo
    logo.classList.add("fade-out");
    setTimeout(() => {
        logo.style.display = "none";
    }, 700);

    // Animación para mostrar el formulario
    formularioContainer.classList.remove("oculto");
    formularioContainer.classList.add("fade-in", "visible");

    // Baja la opacidad del fondo
    document.body.classList.add("fondo-opaco");    
// Logica_Login.js

const loginForm = document.getElementById("loginForm");

if (loginForm) {
    loginForm.addEventListener("submit", function (e) {
    const rut = document.getElementById("Rut")?.value.trim() || "";
    const password = document.getElementById("password")?.value || "";

    // Validación mínima en el cliente
    if (!rut || !password) {
      e.preventDefault(); // solo bloquea si faltan datos
        alert("Ingresa tu RUT y contraseña.");
    }
    // si ambos existen, NO hacemos preventDefault:
    // Django recibe el POST y hace authenticate + login + redirect.
    });
}

});