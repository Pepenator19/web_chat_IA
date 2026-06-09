import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_DIR = os.path.join(BASE_DIR, "data")
PROMPTS_DIR = os.path.join(BASE_DIR, "prompts")

PERSONALITY_FILE = os.path.join(PROMPTS_DIR, "personalidad.txt")
CHAT_MEMORY_FILE = os.path.join(DATA_DIR, "memoria.json")
USER_MEMORIES_FILE = os.path.join(DATA_DIR, "recuerdos.json")

OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5-coder:7b").strip()
AGENT_WORKSPACE = os.getenv("AGENT_WORKSPACE", BASE_DIR)

MAX_HISTORY_MESSAGES = 8
MAX_MESSAGE_CHARS = 2500
MAX_SAVED_HISTORY_MESSAGES = 60
MAX_RESPONSE_TOKENS = 2048
OLLAMA_KEEP_ALIVE = "15m"
OLLAMA_CONTEXT_SIZE = 8192
SHOW_RESPONSE_TIMES = True

APP_TITLE = "Code IA Local"
APP_SUBTITLE = "Chat, programacion y agente autonomo con Ollama"