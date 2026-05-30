from flask import Flask, render_template, request, Response
import ollama
import json
import os

app = Flask(__name__)

DATA_DIR = "data"
MEMORY_FILE = os.path.join(DATA_DIR, "memoria.json")
USER_MEMORIES_FILE = os.path.join(DATA_DIR, "recuerdos.json")

os.makedirs(DATA_DIR, exist_ok=True)

# =========================================================
# LOAD AI PERSONALITY
# CARGAR PERSONALIDAD DE LA IA
# =========================================================
#
# English:
# Reads the AI personality from a text file.
#
# Español:
# Lee la personalidad de la IA desde un archivo de texto.
#

with open("prompts/personalidad.txt", "r", encoding="utf-8") as archivo:
    personalidad = archivo.read()


# =========================================================
# LOAD CHAT MEMORY
# CARGAR MEMORIA DEL CHAT
# =========================================================
#
# English:
# Loads previous conversation history if it exists.
#
# Español:
# Carga el historial anterior si existe.
#

if os.path.exists(MEMORY_FILE):

    with open(MEMORY_FILE, "r", encoding="utf-8") as archivo:
        historial = json.load(archivo)

else:

    historial = [
        {
            "role": "system",
            "content": personalidad
        }
    ]


# =========================================================
# LOAD USER MEMORIES
# CARGAR RECUERDOS DEL USUARIO
# =========================================================
#
# English:
# Loads important remembered user information.
#
# Español:
# Carga recuerdos importantes del usuario.
#

if os.path.exists(USER_MEMORIES_FILE):

    with open(USER_MEMORIES_FILE, "r", encoding="utf-8") as archivo:
        recuerdos = json.load(archivo)

else:

    recuerdos = []


# =========================================================
# MAIN PAGE
# PÁGINA PRINCIPAL
# =========================================================

@app.route("/")
def index():

    return render_template("index.html")


# =========================================================
# AI CHAT ROUTE
# RUTA PRINCIPAL DEL CHAT
# =========================================================

@app.route("/chat", methods=["POST"])
def chat():

    global historial
    global recuerdos

    # =====================================================
    # GET USER MESSAGE
    # OBTENER MENSAJE DEL USUARIO
    # =====================================================

    mensaje = request.form["mensaje"]

    # Save user message
    # Guardar mensaje del usuario

    historial.append({
        "role": "user",
        "content": mensaje
    })

    # =====================================================
    # CREATE MEMORY CONTEXT
    # CREAR CONTEXTO DE RECUERDOS
    # =====================================================

    contexto_recuerdos = ""

    if len(recuerdos) > 0:

        contexto_recuerdos = (
            "Important user memories:\n"
            + "\n".join(recuerdos)
        )

    # =====================================================
    # CREATE AI MESSAGE CONTEXT
    # CREAR CONTEXTO PARA LA IA
    # =====================================================

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

    # =====================================================
    # STREAM RESPONSE FUNCTION
    # FUNCIÓN DE RESPUESTA EN STREAMING
    # =====================================================

    def generar_respuesta():

        texto_completo = ""

        # ================================================
        # OLLAMA STREAMING
        # STREAMING CON OLLAMA
        # ================================================

        respuesta = ollama.chat(

            model="phi3",

            messages=mensajes_ia,

            stream=True
        )

        # ================================================
        # RECEIVE TOKENS IN REAL TIME
        # RECIBIR TOKENS EN TIEMPO REAL
        # ================================================

        for chunk in respuesta:

            contenido = chunk["message"]["content"]

            texto_completo += contenido

            # Send chunk to frontend
            # Enviar fragmento al frontend

            yield contenido

        # ================================================
        # SAVE AI RESPONSE
        # GUARDAR RESPUESTA DE LA IA
        # ================================================

        historial.append({
            "role": "assistant",
            "content": texto_completo
        })

        # ================================================
        # SAVE CHAT MEMORY
        # GUARDAR MEMORIA DEL CHAT
        # ================================================

        with open(
            MEMORY_FILE,
            "w",
            encoding="utf-8"
        ) as archivo:

            json.dump(
                historial,
                archivo,
                ensure_ascii=False,
                indent=4
            )

    # =====================================================
    # SIMPLE MEMORY DETECTOR
    # DETECTOR SIMPLE DE RECUERDOS
    # =====================================================

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
                USER_MEMORIES_FILE,
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

    # =====================================================
    # RETURN STREAM RESPONSE
    # DEVOLVER RESPUESTA EN STREAMING
    # =====================================================

    return Response(
        generar_respuesta(),
        content_type="text/plain"
    )


# =========================================================
# START SERVER
# INICIAR SERVIDOR
# =========================================================

if __name__ == "__main__":

    app.run(debug=True)
