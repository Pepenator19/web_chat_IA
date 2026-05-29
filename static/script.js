async function enviarMensaje() {

    let mensaje = document.getElementById("mensaje").value;

    let respuesta = await fetch("/chat", {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded"
        },
        body: "mensaje=" + encodeURIComponent(mensaje)
    });

    let texto = await respuesta.text();

    document.getElementById("respuesta").innerText = texto;
}