import json
import os
import re
import string
import unicodedata

from config import (
    CHAT_MEMORY_FILE,
    DATA_DIR,
    MAX_MESSAGE_CHARS,
    MAX_SAVED_HISTORY_MESSAGES,
    USER_MEMORIES_FILE,
)


MEMORY_TRIGGERS = [
    "me llamo",
    "tengo",
    "me gusta",
    "mi laptop",
    "uso",
    "soy",
]

MEMORY_QUESTIONS = [
    "que recuerdas de mi",
    "que sabes de mi",
    "what do you remember about me",
    "what do you know about me",
]

QUICK_REPLIES = {
    "hola": "Hola. Estoy lista para ayudarte a programar.",
    "buenos dias": "Buenos dias. Lista para revisar, corregir o construir codigo contigo.",
    "buen dia": "Buen dia. Que codigo mejoramos hoy?",
    "buenas": "Buenas. Ya estoy despierta, mas o menos como cualquier IA local con cafe imaginario.",
    "gracias": "De nada. La humanidad sobrevive otro commit.",
}

def ensure_data_folder():
    os.makedirs(DATA_DIR, exist_ok=True)


def load_json_file(path, default_value):
    ensure_data_folder()

    if not os.path.exists(path):
        return default_value

    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def save_json_file(path, value):
    ensure_data_folder()

    with open(path, "w", encoding="utf-8") as file:
        json.dump(value, file, ensure_ascii=False, indent=4)


def load_chat_history(personality):
    default_history = [
        {
            "role": "system",
            "content": personality,
        }
    ]

    history = load_json_file(CHAT_MEMORY_FILE, default_history)
    return trim_saved_history(remove_system_messages(history))


def save_chat_history(history):
    save_json_file(CHAT_MEMORY_FILE, trim_saved_history(history))


def build_chat_context(history, max_messages):
    recent_history = remove_system_messages(history)[-max_messages:]
    return [truncate_message(message) for message in recent_history]


def remove_system_messages(history):
    return [
        message
        for message in history
        if message.get("role") in ["user", "assistant"]
    ]


def trim_saved_history(history):
    return remove_system_messages(history)[-MAX_SAVED_HISTORY_MESSAGES:]


def truncate_message(message):
    content = message.get("content", "")

    if len(content) <= MAX_MESSAGE_CHARS:
        return message

    return {
        "role": message.get("role", "user"),
        "content": content[:MAX_MESSAGE_CHARS] + "\n[Message shortened for speed]",
    }


def load_user_memories():
    return load_json_file(USER_MEMORIES_FILE, [])


def save_user_memories(memories):
    save_json_file(USER_MEMORIES_FILE, memories)


def should_show_memories(message):
    normalized_message = normalize_message(message)
    return normalized_message in MEMORY_QUESTIONS


def get_quick_reply(message):
    normalized_message = normalize_message(message)
    return QUICK_REPLIES.get(normalized_message)


def should_remember_message(message):
    normalized_message = normalize_message(message)
    return any(trigger in normalized_message for trigger in MEMORY_TRIGGERS)


def add_user_memory(memories, message):
    clean_message = message.strip()

    if clean_message and clean_message not in memories:
        memories.append(clean_message)
        save_user_memories(memories)
        return True

    return False


def build_memory_context(memories):
    if not memories:
        return "No saved user memories yet."

    formatted_memories = "\n".join(f"- {memory}" for memory in memories)
    return f"Important user memories:\n{formatted_memories}"


def format_user_memories(memories):
    if not memories:
        return "Todavia no tengo recuerdos guardados sobre ti."

    lines = ["Esto es lo que recuerdo de ti:", ""]

    for index, memory in enumerate(memories, start=1):
        lines.append(f"{index}. {memory}")

    return "\n".join(lines)


def normalize_message(message):
    normalized = unicodedata.normalize("NFD", message.lower().strip())
    without_accents = "".join(
        character
        for character in normalized
        if unicodedata.category(character) != "Mn"
    )
    without_punctuation = without_accents.translate(
        str.maketrans("", "", string.punctuation + "¿¡")
    )

    return " ".join(without_punctuation.split())


def clean_model_output(text):
    return re.sub(r"\n?\[[^\]]{1,80}\]\s*", "", text).strip()
