/* =========================================================
    ENVIAR MENSAJE
    SEND MESSAGE
========================================================= */

async function enviarMensaje(){

    // INPUT
    // USER INPUT
    const input = document.getElementById("mensaje");

    // TEXTO
    // TEXT
    const mensaje = input.value.trim();

    // EVITAR MENSAJES VACÍOS
    // PREVENT EMPTY MESSAGES
    if(mensaje === "") return;

    // CONTENEDOR CHAT
    // CHAT CONTAINER
    const chatBox = document.getElementById("chatBox");

    /* =====================================================
        MENSAJE USUARIO
        USER MESSAGE
    ===================================================== */

    const userMsg = document.createElement("div");

    userMsg.className = "msg user";

    userMsg.innerText = mensaje;

    chatBox.appendChild(userMsg);

    /* =====================================================
        LIMPIAR INPUT
        CLEAR INPUT
    ===================================================== */

    input.value = "";

    /* =====================================================
        MENSAJE IA
        AI MESSAGE
    ===================================================== */

    const botMsg = document.createElement("div");

    botMsg.className = "msg bot";

    botMsg.innerText = "";

    chatBox.appendChild(botMsg);

    // SCROLL AUTOMÁTICO
    // AUTO SCROLL
    chatBox.scrollTop = chatBox.scrollHeight;

    /* =====================================================
        PETICIÓN AL BACKEND
        BACKEND REQUEST
    ===================================================== */

    try{

        const respuesta = await fetch("/chat", {

            method:"POST",

            headers:{
                "Content-Type":"application/x-www-form-urlencoded"
            },

            body:"mensaje=" + encodeURIComponent(mensaje)
        });

        /* =================================================
            STREAMING
            REAL TIME STREAM
        ================================================= */

        const reader = respuesta.body.getReader();

        const decoder = new TextDecoder();

        while(true){

            // LEER CHUNK
            // READ CHUNK
            const { done, value } = await reader.read();

            // TERMINAR STREAM
            // END STREAM
            if(done) break;

            // DECODIFICAR TEXTO
            // DECODE TEXT
            const texto = decoder.decode(value);

            // AGREGAR RESPUESTA
            // APPEND RESPONSE
            botMsg.innerText += texto;

            // SCROLL ABAJO
            // AUTO SCROLL DOWN
            chatBox.scrollTop = chatBox.scrollHeight;
        }

    }

    catch(error){

        // ERROR
        console.error(error);

        botMsg.innerText =
            "Error conectando con la IA local.";
    }
}

/* =========================================================
    ENTER PARA ENVIAR
    ENTER TO SEND
========================================================= */

document
.getElementById("mensaje")
.addEventListener("keydown", function(event){

    // ENTER SIN SHIFT
    // ENTER WITHOUT SHIFT
    if(event.key === "Enter" && !event.shiftKey){

        event.preventDefault();

        enviarMensaje();
    }
});