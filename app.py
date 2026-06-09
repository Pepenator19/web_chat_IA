import json
import os

from flask import Flask, Response, jsonify, render_template, request
import ollama
from time import perf_counter

from agent_core import stream_agent_events
from coding import (
    build_help_context,
    build_mode_context,
    get_help_content,
    get_mode_stream_type,
    get_model_options,
    is_agent_mode,
    list_modes,
    normalize_language,
    normalize_mode,
)
from config import (
    AGENT_WORKSPACE,
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
    remove_system_messages,
    save_chat_history,
    should_remember_message,
    should_show_memories,
)

app = Flask(__name__)


def load_personality():
    with open(PERSONALITY_FILE, "r", encoding="utf-8") as file:
        return file.read()


def resolve_workspace(raw_workspace: str) -> str:
    workspace = (raw_workspace or AGENT_WORKSPACE).strip().strip('"')
    if not workspace:
        workspace = AGENT_WORKSPACE
    workspace = os.path.abspath(workspace)
    if not os.path.isdir(workspace):
        raise ValueError(f"La carpeta de trabajo no existe: {workspace}")
    return workspace


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
        default_workspace=AGENT_WORKSPACE,
    )


@app.route("/modes", methods=["GET"])
def modes():
    return jsonify({"modes": list_modes()})


@app.route("/help", methods=["GET"])
def help_page():
    return jsonify(
        {
            "title": "Ayuda global",
            "content": get_help_content(),
        }
    )


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
    workspace_raw = request.form.get("workspace", AGENT_WORKSPACE)

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

    historial.append({"role": "user", "content": mensaje})

    if should_remember_message(mensaje):
        add_user_memory(recuerdos, mensaje)

    if is_agent_mode(modo):
        try:
            workspace = resolve_workspace(workspace_raw)
        except ValueError as exc:
            return Response(str(exc), content_type="text/plain", status=400)

        def generate_agent():
            global historial
            start_time = perf_counter()
            final_text = ""

            try:
                recent_history = remove_system_messages(historial)[-MAX_HISTORY_MESSAGES:]

                for line in stream_agent_events(
                    workspace=workspace,
                    model=OLLAMA_MODEL,
                    user_input=mensaje,
                    history=recent_history[:-1],
                ):
                    yield line
                    try:
                        event = json.loads(line)
                        if event.get("event") == "done":
                            final_text = event.get("content", "")
                    except json.JSONDecodeError:
                        pass

                if final_text:
                    historial.append({"role": "assistant", "content": final_text})
                    save_chat_history(historial)
                    historial = load_chat_history(personalidad)

                if SHOW_RESPONSE_TIMES:
                    elapsed = perf_counter() - start_time
                    print(f"Agent response time: {elapsed:.2f}s")
            except Exception as exc:
                error_line = (
                    '{"event":"error","content":"Error del agente: '
                    + str(exc).replace('"', "'")
                    + '"}\n'
                )
                yield error_line

        return Response(generate_agent(), content_type="application/x-ndjson")

    system_messages = [
        {"role": "system", "content": personalidad},
        {"role": "system", "content": build_mode_context(modo, lenguaje)},
        {"role": "system", "content": build_memory_context(recuerdos)},
    ]

    if modo == "ayuda":
        system_messages.append({"role": "system", "content": build_help_context()})

    mensajes_ia = system_messages + build_chat_context(historial, MAX_HISTORY_MESSAGES)
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

        historial.append({"role": "assistant", "content": texto_completo})
        save_chat_history(historial)
        historial = load_chat_history(personalidad)

        if SHOW_RESPONSE_TIMES:
            elapsed = perf_counter() - start_time
            print(f"Ollama response time ({modo}): {elapsed:.2f}s")

    content_type = "text/plain"
    if get_mode_stream_type(modo) == "agent":
        content_type = "application/x-ndjson"

    return Response(generate_response(), content_type=content_type)


if __name__ == "__main__":
    app.run(debug=True)