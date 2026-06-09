HELP_CONTENT = """# Ayuda global de Code IA Local

## Que es esta app
Asistente local con Flask + Ollama. Todo corre en tu PC: chat, programacion y agente autonomo.

## Modos disponibles

### Agente (autonomo)
Ejecuta acciones reales en tu carpeta de trabajo:
- Leer, escribir y editar archivos
- Buscar en el proyecto (Grep, Glob)
- Ejecutar comandos de terminal (Shell)
Configura la **carpeta de trabajo** en el panel lateral antes de usarlo.

### Programar
Genera codigo limpio y funcional.

### Debug
Analiza errores y propone correcciones.

### Explicar
Explica codigo o conceptos con claridad.

### Refactor
Mejora estructura y legibilidad sin cambiar comportamiento.

### Revisar
Code review con severidad: critico, advertencia, sugerencia.

### Charla
Conversacion libre sin enfocarse solo en codigo.

### Ayuda
Responde dudas sobre como usar la app, modos, atajos y memoria.

## Atajos
- Ctrl + Enter: enviar mensaje
- Ctrl + K: limpiar chat
- Shift + Enter: nueva linea en el textarea

## Memoria
- Historial del chat: data/memoria.json
- Recuerdos del usuario: data/recuerdos.json
- Comando: "Que recuerdas de mi?"
- Boton: Ver memoria

## Endpoints API
- POST /chat — enviar mensaje (modo, lenguaje, workspace)
- GET /modes — listar modos
- GET /help — ayuda global
- GET /memories — ver recuerdos
- POST /clear — limpiar chat

## Variables de entorno
- OLLAMA_MODEL — cambiar modelo
- AGENT_WORKSPACE — carpeta por defecto del agente

## Requisitos
Python 3.10+, Ollama corriendo, modelo instalado (ej: qwen2.5-coder:7b)
"""

CODING_MODES = {
    "agente": {
        "label": "Agente",
        "description": "Autonomo: lee, edita y ejecuta en tu PC",
        "group": "principal",
        "uses_language": False,
        "uses_workspace": True,
        "stream_type": "agent",
        "prompt": (
            "Modo AGENTE activo.\n"
            "Tienes herramientas reales para actuar en la carpeta de trabajo del usuario.\n"
            "No des instrucciones manuales: ejecuta tu mismo con las herramientas.\n"
            "Investiga, actua, verifica y resume lo hecho."
        ),
    },
    "programar": {
        "label": "Programar",
        "description": "Genera codigo limpio y funcional",
        "group": "codigo",
        "uses_language": True,
        "uses_workspace": False,
        "stream_type": "text",
        "prompt": (
            "Modo PROGRAMAR activo.\n"
            "El usuario quiere codigo util y ejecutable.\n"
            "Prioriza soluciones simples, correctas y listas para copiar.\n"
            "Si falta contexto, asume lo minimo razonable y dilo en una frase.\n"
            "Entrega bloques Markdown con lenguaje indicado."
        ),
    },
    "debug": {
        "label": "Debug",
        "description": "Encuentra y corrige errores",
        "group": "codigo",
        "uses_language": True,
        "uses_workspace": False,
        "stream_type": "text",
        "prompt": (
            "Modo DEBUG activo.\n"
            "Analiza el codigo o error del usuario paso a paso.\n"
            "Identifica la causa probable, muestra la correccion y explica por que fallaba.\n"
            "Si hay varias causas, ordenalas por probabilidad."
        ),
    },
    "explicar": {
        "label": "Explicar",
        "description": "Explica codigo o conceptos",
        "group": "codigo",
        "uses_language": True,
        "uses_workspace": False,
        "stream_type": "text",
        "prompt": (
            "Modo EXPLICAR activo.\n"
            "Explica con claridad, sin asumir que el usuario es experto.\n"
            "Usa ejemplos cortos cuando ayuden.\n"
            "Evita respuestas enormes salvo que el usuario lo pida."
        ),
    },
    "refactor": {
        "label": "Refactor",
        "description": "Mejora estructura y legibilidad",
        "group": "codigo",
        "uses_language": True,
        "uses_workspace": False,
        "stream_type": "text",
        "prompt": (
            "Modo REFACTOR activo.\n"
            "Mejora legibilidad, nombres, estructura y mantenibilidad.\n"
            "No cambies el comportamiento salvo que el usuario lo pida.\n"
            "Resume los cambios clave al final."
        ),
    },
    "revisar": {
        "label": "Revisar",
        "description": "Revision de codigo tipo code review",
        "group": "codigo",
        "uses_language": True,
        "uses_workspace": False,
        "stream_type": "text",
        "prompt": (
            "Modo REVISAR activo.\n"
            "Haz una revision tipo code review.\n"
            "Marca problemas por severidad: critico, advertencia, sugerencia.\n"
            "Sugiere mejoras concretas y justificadas."
        ),
    },
    "charla": {
        "label": "Charla",
        "description": "Conversacion libre y natural",
        "group": "general",
        "uses_language": False,
        "uses_workspace": False,
        "stream_type": "text",
        "prompt": (
            "Modo CHARLA activo.\n"
            "Conversa de forma natural, amigable y util.\n"
            "No estas limitada solo a programacion: puedes hablar de cualquier tema.\n"
            "Se breve y calida. Si el usuario pide codigo, ayudale, pero no fuerces temas tecnicos."
        ),
    },
    "ayuda": {
        "label": "Ayuda",
        "description": "Guia de uso de la aplicacion",
        "group": "general",
        "uses_language": False,
        "uses_workspace": False,
        "stream_type": "text",
        "prompt": (
            "Modo AYUDA activo.\n"
            "Respondes preguntas sobre como usar Code IA Local.\n"
            "Explica modos, atajos, memoria, agente autonomo, requisitos y endpoints.\n"
            "Se clara, estructurada y practica. Usa listas cuando ayude.\n"
            "Si no sabes algo concreto del entorno del usuario, dilo sin inventar."
        ),
    },
}

DEFAULT_MODE = "programar"

LANGUAGE_HINTS = {
    "auto": "Detecta el lenguaje mas probable segun el contexto.",
    "python": "Responde pensando en Python 3.10+ salvo que el usuario indique otra version.",
    "javascript": "Responde pensando en JavaScript moderno (ES6+).",
    "typescript": "Responde pensando en TypeScript con tipos claros.",
    "html": "Responde pensando en HTML5 semantico.",
    "css": "Responde pensando en CSS moderno.",
    "java": "Responde pensando en Java reciente.",
    "csharp": "Responde pensando en C# moderno.",
    "cpp": "Responde pensando en C++.",
    "sql": "Responde pensando en SQL estandar.",
    "bash": "Responde pensando en scripts Bash.",
    "php": "Responde pensando en PHP moderno.",
    "go": "Responde pensando en Go idiomatico.",
    "rust": "Responde pensando en Rust seguro y claro.",
}

QUICK_PROMPTS = {
    "agente": [
        "Lista los archivos del proyecto y resume la estructura",
        "Lee app.py y explicame que hace",
        "Crea un archivo test_agent.py con un hello world",
        "Busca todos los archivos .py y dime cuantos hay",
    ],
    "programar": [
        "Crea una funcion que ",
        "Haz un script en Python que ",
        "Genera una API REST simple con Flask que ",
        "Escribe tests unitarios para ",
    ],
    "debug": [
        "Este codigo da error, ayudame a corregirlo:\n```\n\n```",
        "Por que falla este traceback?",
        "Revisa este bug y dime la causa:",
    ],
    "explicar": [
        "Explica este codigo linea por linea:\n```\n\n```",
        "Que hace esta funcion?",
        "Explicame este concepto como si fuera principiante:",
    ],
    "refactor": [
        "Refactoriza este codigo para que sea mas legible:\n```\n\n```",
        "Como simplificarias esta funcion?",
        "Mejora nombres y estructura de este codigo:",
    ],
    "revisar": [
        "Haz code review de este codigo:\n```\n\n```",
        "Que problemas de seguridad ves aqui?",
        "Que mejoras harías antes de produccion?",
    ],
    "charla": [
        "Como estas hoy?",
        "Cuentame algo interesante",
        "Que puedes hacer ademas de programar?",
        "Recomiendame algo para aprender esta semana",
    ],
    "ayuda": [
        "Que modos tiene la app?",
        "Como funciona el modo agente?",
        "Que atajos de teclado hay?",
        "Como funciona la memoria local?",
    ],
}


def normalize_mode(mode):
    normalized = (mode or DEFAULT_MODE).strip().lower()
    return normalized if normalized in CODING_MODES else DEFAULT_MODE


def get_mode_info(mode):
    mode_id = normalize_mode(mode)
    data = CODING_MODES[mode_id]
    return {
        "id": mode_id,
        "label": data["label"],
        "description": data["description"],
        "group": data.get("group", "codigo"),
        "uses_language": data.get("uses_language", True),
        "uses_workspace": data.get("uses_workspace", False),
        "stream_type": data.get("stream_type", "text"),
        "quick_prompts": QUICK_PROMPTS.get(mode_id, []),
    }


def get_help_content():
    return HELP_CONTENT


def is_agent_mode(mode):
    return normalize_mode(mode) == "agente"


def get_mode_stream_type(mode):
    return CODING_MODES[normalize_mode(mode)].get("stream_type", "text")


def list_modes():
    return [get_mode_info(mode_id) for mode_id in CODING_MODES]


def normalize_language(language):
    normalized = (language or "auto").strip().lower()
    return normalized if normalized in LANGUAGE_HINTS else "auto"


def build_mode_context(mode, language):
    mode_id = normalize_mode(mode)
    language_id = normalize_language(language)
    mode_data = CODING_MODES[mode_id]

    parts = [
        mode_data["prompt"],
        LANGUAGE_HINTS[language_id],
    ]

    return "\n".join(parts)


def get_model_options(mode):
    mode_id = normalize_mode(mode)

    if mode_id == "agente":
        return {"temperature": 0.2, "top_p": 0.9}

    if mode_id in {"programar", "refactor"}:
        return {"temperature": 0.2, "top_p": 0.9}

    if mode_id == "debug":
        return {"temperature": 0.1, "top_p": 0.85}

    if mode_id == "revisar":
        return {"temperature": 0.15, "top_p": 0.9}

    if mode_id == "charla":
        return {"temperature": 0.75, "top_p": 0.95}

    if mode_id == "ayuda":
        return {"temperature": 0.25, "top_p": 0.9}

    return {"temperature": 0.35, "top_p": 0.95}


def build_help_context():
    return f"Documentacion interna de la app:\n\n{HELP_CONTENT}"