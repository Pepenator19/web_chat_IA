from flask import Flask, Response, jsonify, render_template, request
import ollama

from config import MAX_HISTORY_MESSAGES, OLLAMA_MODEL, PERSONALITY_FILE
from memory import (
    add_user_memory,
    build_memory_context,
    format_user_memories,
    load_chat_history,
    load_user_memories,
    save_chat_history,
    should_remember_message,
    should_show_memories,
)

app = Flask(__name__)


def load_personality():
    with open(PERSONALITY_FILE, "r", encoding="utf-8") as file:
        return file.read()


personalidad = load_personality()
historial = load_chat_history(personalidad)
recuerdos = load_user_memories()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/memories", methods=["GET"])
def memories():
    return jsonify(
        {
            "count": len(recuerdos),
            "memories": recuerdos,
            "text": format_user_memories(recuerdos),
        }
    )


@app.route("/chat", methods=["POST"])
def chat():
    global historial
    global recuerdos

    mensaje = request.form["mensaje"].strip()

    if not mensaje:
        return Response("", content_type="text/plain")

    if should_show_memories(mensaje):
        return Response(format_user_memories(recuerdos), content_type="text/plain")

    historial.append(
        {
            "role": "user",
            "content": mensaje,
        }
    )

    if should_remember_message(mensaje):
        add_user_memory(recuerdos, mensaje)

    mensajes_ia = [
        {
            "role": "system",
            "content": personalidad,
        },
        {
            "role": "system",
            "content": build_memory_context(recuerdos),
        },
    ] + historial[-MAX_HISTORY_MESSAGES:]

    def generate_response():
        texto_completo = ""

        respuesta = ollama.chat(
            model=OLLAMA_MODEL,
            messages=mensajes_ia,
            stream=True,
        )

        for chunk in respuesta:
            contenido = chunk["message"]["content"]
            texto_completo += contenido
            yield contenido

        historial.append(
            {
                "role": "assistant",
                "content": texto_completo,
            }
        )

        save_chat_history(historial)

    return Response(generate_response(), content_type="text/plain")


if __name__ == "__main__":
    app.run(debug=True)
