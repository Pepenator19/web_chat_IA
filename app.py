from flask import Flask, render_template, request
import ollama
import json
import os

app = Flask(__name__)

# =========================================
# CARGAR PERSONALIDAD
# =========================================

with open("prompts/personalidad.txt", "r", encoding="utf-8") as archivo:
    personalidad = archivo.read()

# =========================================
# CARGAR MEMORIA
# =========================================

if os.path.exists("memoria.json"):

    with open("memoria.json", "r", encoding="utf-8") as archivo:
        historial = json.load(archivo)

else:

    historial = [
        {
            "role": "system",
            "content": personalidad
        }
    ]

# =========================================
# CARGAR RECUERDOS
# =========================================

if os.path.exists("recuerdos.json"):

    with open("recuerdos.json", "r", encoding="utf-8") as archivo:
        recuerdos = json.load(archivo)

else:

    recuerdos = []

# =========================================
# PÁGINA PRINCIPAL
# =========================================

@app.route("/")
def index():

    return render_template("index.html")


# =========================================
# CHAT IA
# =========================================

@app.route("/chat", methods=["POST"])
def chat():

    global historial
    global recuerdos

    # Obtener mensaje
    mensaje = request.form["mensaje"]

    # =====================================
    # GUARDAR MENSAJE USUARIO
    # =====================================

    historial.append({
        "role": "user",
        "content": mensaje
    })

    # =====================================
    # CREAR CONTEXTO DE RECUERDOS
    # =====================================

    contexto_recuerdos = ""

    if len(recuerdos) > 0:

        contexto_recuerdos = (
            "Recuerdos importantes del usuario:\n"
            + "\n".join(recuerdos)
        )

    # =====================================
    # MENSAJES PARA OLLAMA
    # =====================================

    mensajes_ia = [

        {
            "role": "system",
            "content": personalidad
        },

        {
            "role": "system",
            "content": contexto_recuerdos
        }

    ] + historial[-15:]

    # =====================================
    # RESPUESTA IA
    # =====================================

    respuesta = ollama.chat(
        model="phi3",
        messages=mensajes_ia
    )

    texto = respuesta["message"]["content"]

    # =====================================
    # GUARDAR RESPUESTA IA
    # =====================================

    historial.append({
        "role": "assistant",
        "content": texto
    })

    # =====================================
    # GUARDAR MEMORIA
    # =====================================

    with open("memoria.json", "w", encoding="utf-8") as archivo:

        json.dump(
            historial,
            archivo,
            ensure_ascii=False,
            indent=4
        )

    # =====================================
    # DETECTOR SIMPLE DE RECUERDOS
    # =====================================

    claves = [
        "me llamo",
        "tengo",
        "me gusta",
        "mi laptop",
        "uso",
        "soy"
    ]

    for clave in claves:

        if clave in mensaje.lower():

            recuerdos.append(mensaje)

            with open(
                "recuerdos.json",
                "w",
                encoding="utf-8"
            ) as archivo:

                json.dump(
                    recuerdos,
                    archivo,
                    ensure_ascii=False,
                    indent=4
                )

            break

    # =====================================
    # DEVOLVER RESPUESTA
    # =====================================

    return texto


# =========================================
# INICIAR SERVIDOR
# =========================================

if __name__ == "__main__":

    app.run(debug=True)