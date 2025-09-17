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

    const loginForm = document.getElementById("loginForm");



    
loginForm.addEventListener("submit", function(e) {
    e.preventDefault();

    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value;

    const emailValido = email.endsWith("@uandresbello.edu");
    const passwordValida = password === "abc123";

    if (emailValido && passwordValida) {
        window.location.href = "../EncargadoConvivencia/Homepage.html";
    } else {
        alert("Error de autenticación. Por favor, verifica tu correo y contraseña.");
    }
});


});