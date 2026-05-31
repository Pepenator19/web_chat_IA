from flask import Flask, Response, jsonify, render_template, request
import ollama
from time import perf_counter

from config import (
    MAX_HISTORY_MESSAGES,
    MAX_RESPONSE_TOKENS,
    OLLAMA_CONTEXT_SIZE,
    OLLAMA_KEEP_ALIVE,
    OLLAMA_MODEL,
    PERSONALITY_FILE,
    SHOW_RESPONSE_TIMES,
)
from memory import (
    add_user_memory,
    build_chat_context,
    build_memory_context,
    clean_model_output,
    format_user_memories,
    get_quick_reply,
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

    quick_reply = get_quick_reply(mensaje)

    if quick_reply:
        historial.append({"role": "user", "content": mensaje})
        historial.append({"role": "assistant", "content": quick_reply})
        save_chat_history(historial)
        historial = load_chat_history(personalidad)

        if SHOW_RESPONSE_TIMES:
            print("Quick reply used: 0.00s")

        return Response(quick_reply, content_type="text/plain")

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
    ] + build_chat_context(historial, MAX_HISTORY_MESSAGES)

    def generate_response():
        global historial

        texto_completo = ""
        start_time = perf_counter()

        respuesta = ollama.chat(
            model=OLLAMA_MODEL,
            messages=mensajes_ia,
            options={
                "num_ctx": OLLAMA_CONTEXT_SIZE,
                "num_predict": MAX_RESPONSE_TOKENS,
            },
            keep_alive=OLLAMA_KEEP_ALIVE,
            stream=True,
        )

        for chunk in respuesta:
            contenido = chunk["message"]["content"]
            texto_completo += contenido
            yield contenido

        texto_completo = clean_model_output(texto_completo)

        historial.append(
            {
                "role": "assistant",
                "content": texto_completo,
            }
        )

        save_chat_history(historial)
        historial = load_chat_history(personalidad)

        if SHOW_RESPONSE_TIMES:
            elapsed = perf_counter() - start_time
            print(f"Ollama response time: {elapsed:.2f}s")

    return Response(generate_response(), content_type="text/plain")


if __name__ == "__main__":
    app.run(debug=True)
