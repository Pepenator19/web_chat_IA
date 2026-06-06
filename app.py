from flask import Flask, Response, jsonify, render_template, request
import ollama
from time import perf_counter

from coding import build_mode_context, get_model_options, list_modes, normalize_language, normalize_mode
from config import (
    APP_SUBTITLE,
    APP_TITLE,
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
    return render_template(
        "index.html",
        app_title=APP_TITLE,
        app_subtitle=APP_SUBTITLE,
        model_name=OLLAMA_MODEL,
    )


@app.route("/modes", methods=["GET"])
def modes():
    return jsonify({"modes": list_modes()})


@app.route("/memories", methods=["GET"])
def memories():
    return jsonify(
        {
            "count": len(recuerdos),
            "memories": recuerdos,
            "text": format_user_memories(recuerdos),
        }
    )


@app.route("/clear", methods=["POST"])
def clear_chat():
    global historial

    historial = load_chat_history(personalidad)
    save_chat_history(historial)

    return jsonify({"ok": True, "message": "Historial del chat limpiado."})


@app.route("/chat", methods=["POST"])
def chat():
    global historial
    global recuerdos

    mensaje = request.form.get("mensaje", "").strip()
    modo = normalize_mode(request.form.get("modo"))
    lenguaje = normalize_language(request.form.get("lenguaje"))

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
            "content": build_mode_context(modo, lenguaje),
        },
        {
            "role": "system",
            "content": build_memory_context(recuerdos),
        },
    ] + build_chat_context(historial, MAX_HISTORY_MESSAGES)

    model_options = get_model_options(modo)

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
                "temperature": model_options["temperature"],
                "top_p": model_options["top_p"],
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
            print(f"Ollama response time ({modo}): {elapsed:.2f}s")

    return Response(generate_response(), content_type="text/plain")


if __name__ == "__main__":
    app.run(debug=True)