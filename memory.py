import json
import os
import string
import unicodedata

from config import CHAT_MEMORY_FILE, DATA_DIR, USER_MEMORIES_FILE


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

    return load_json_file(CHAT_MEMORY_FILE, default_history)


def save_chat_history(history):
    save_json_file(CHAT_MEMORY_FILE, history)


def load_user_memories():
    return load_json_file(USER_MEMORIES_FILE, [])


def save_user_memories(memories):
    save_json_file(USER_MEMORIES_FILE, memories)


def should_show_memories(message):
    normalized_message = normalize_message(message)
    return normalized_message in MEMORY_QUESTIONS


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
