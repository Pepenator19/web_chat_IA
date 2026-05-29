/*
==================================================
SCRIPT PRINCIPAL DEL CHAT IA
==================================================

Este archivo se encarga de:

1. Obtener el mensaje del usuario
2. Enviarlo al servidor Flask
3. Recibir la respuesta de la IA
4. Mostrar la respuesta en la página
*/

async function enviarMensaje() {

    // Obtener el texto escrito por el usuario
    let mensaje = document.getElementById("mensaje").value;

    // Enviar mensaje al servidor Flask usando POST
    let respuesta = await fetch("/chat", {

        // Método HTTP
        method: "POST",

        // Tipo de datos enviados
        headers: {
            "Content-Type": "application/x-www-form-urlencoded"
        },

        // Datos enviados al servidor
        body: "mensaje=" + encodeURIComponent(mensaje)
    });

    // Convertir respuesta del servidor a texto
    let texto = await respuesta.text();

    // Mostrar respuesta de la IA en pantalla
    document.getElementById("respuesta").innerText = texto;
}