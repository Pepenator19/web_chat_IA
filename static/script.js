const input = document.getElementById("mensaje");
const chatBox = document.getElementById("chatBox");


function agregarMensaje(texto, tipo) {
    const mensaje = document.createElement("div");

    mensaje.className = `message ${tipo}-message`;
    mensaje.innerText = texto;

    chatBox.appendChild(mensaje);
    chatBox.scrollTop = chatBox.scrollHeight;

    return mensaje;
}


async function enviarMensaje() {
    const texto = input.value.trim();

    if (texto === "") {
        return;
    }

    agregarMensaje(texto, "user");
    input.value = "";

    const respuestaIA = agregarMensaje("", "ai");

    try {
        const respuesta = await fetch("/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
            },
            body: `mensaje=${encodeURIComponent(texto)}`,
        });

        const reader = respuesta.body.getReader();
        const decoder = new TextDecoder();

        while (true) {
            const { done, value } = await reader.read();

            if (done) {
                break;
            }

            respuestaIA.innerText += decoder.decode(value);
            chatBox.scrollTop = chatBox.scrollHeight;
        }
    } catch (error) {
        console.error(error);
        respuestaIA.innerText = "Error conectando con la IA local.";
    }
}


async function mostrarMemoria() {
    agregarMensaje("¿Qué recuerdas de mí?", "user");

    const respuestaIA = agregarMensaje("", "ai");

    try {
        const respuesta = await fetch("/memories");
        const data = await respuesta.json();

        respuestaIA.innerText = data.text;
    } catch (error) {
        console.error(error);
        respuestaIA.innerText = "No pude leer la memoria local.";
    }
}


input.addEventListener("keydown", function (event) {
    if (event.key === "Enter" && !event.shiftKey) {
        event.preventDefault();
        enviarMensaje();
    }
});
