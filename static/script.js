/*
==================================================
    CHAT IA - SCRIPT PRINCIPAL
    MAIN CHAT SCRIPT
==================================================

ES:
Este archivo:
1. Obtiene el mensaje del usuario
2. Lo envía al servidor Flask
3. Recibe la respuesta de la IA
4. Muestra la respuesta en pantalla

EN:
This file:
1. Gets the user's message
2. Sends it to the Flask server
3. Receives the AI response
4. Displays the response on screen

Porque aparentemente los humanos disfrutan
hacer que JavaScript hable con Python 🫠
==================================================
*/

/* ==================================================
    FUNCIÓN PRINCIPAL DEL CHAT
    MAIN CHAT FUNCTION
================================================== */

async function enviarMensaje() {

    // ==========================================
    // OBTENER INPUT
    // GET INPUT ELEMENT
    // ==========================================

    let input = document.getElementById("mensaje");

    // ==========================================
    // OBTENER TEXTO
    // GET USER MESSAGE
    // ==========================================

    let mensaje = input.value.trim();

    // ==========================================
    // EVITAR MENSAJES VACÍOS
    // PREVENT EMPTY MESSAGES
    // ==========================================

    if (mensaje === "") return;

    // ==========================================
    // ENVIAR MENSAJE AL SERVIDOR
    // SEND MESSAGE TO SERVER
    // ==========================================

    let respuesta = await fetch("/chat", {

        // Método HTTP
        // HTTP method
        method: "POST",

        // Tipo de contenido enviado
        // Sent content type
        headers: {
            "Content-Type": "application/x-www-form-urlencoded"
        },

        // Datos enviados al backend
        // Data sent to backend
        body: "mensaje=" + encodeURIComponent(mensaje)
    });

    // ==========================================
    // OBTENER RESPUESTA DE LA IA
    // GET AI RESPONSE
    // ==========================================

    let texto = await respuesta.text();

    // ==========================================
    // MOSTRAR RESPUESTA EN HTML
    // DISPLAY RESPONSE IN HTML
    // ==========================================

    document.getElementById("respuesta").innerText = texto;

    // ==========================================
    // LIMPIAR INPUT
    // CLEAR INPUT
    // ==========================================

    input.value = "";
}

/* ==================================================
    ENVIAR CON ENTER
    SEND MESSAGE WITH ENTER KEY
================================================== */

document
.getElementById("mensaje")
.addEventListener("keypress", function(event) {

    // Si el usuario presiona ENTER
    // If user presses ENTER
    if (event.key === "Enter") {

        enviarMensaje();
    }
});