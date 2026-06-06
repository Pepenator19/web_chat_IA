CODING_MODES = {
    "programar": {
        "label": "Programar",
        "description": "Genera codigo limpio y funcional",
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
        "prompt": (
            "Modo REVISAR activo.\n"
            "Haz una revision tipo code review.\n"
            "Marca problemas por severidad: critico, advertencia, sugerencia.\n"
            "Sugiere mejoras concretas y justificadas."
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
        "quick_prompts": QUICK_PROMPTS.get(mode_id, []),
    }


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

    if mode_id in {"programar", "refactor"}:
        return {"temperature": 0.2, "top_p": 0.9}

    if mode_id == "debug":
        return {"temperature": 0.1, "top_p": 0.85}

    if mode_id == "revisar":
        return {"temperature": 0.15, "top_p": 0.9}

    return {"temperature": 0.35, "top_p": 0.95}