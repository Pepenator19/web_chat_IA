import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_DIR = os.path.join(BASE_DIR, "data")
PROMPTS_DIR = os.path.join(BASE_DIR, "prompts")

PERSONALITY_FILE = os.path.join(PROMPTS_DIR, "personalidad.txt")
CHAT_MEMORY_FILE = os.path.join(DATA_DIR, "memoria.json")
USER_MEMORIES_FILE = os.path.join(DATA_DIR, "recuerdos.json")

OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "phi3")
MAX_HISTORY_MESSAGES = 4
MAX_MESSAGE_CHARS = 500
MAX_SAVED_HISTORY_MESSAGES = 40
MAX_RESPONSE_TOKENS = 700
OLLAMA_KEEP_ALIVE = "10m"
OLLAMA_CONTEXT_SIZE = 1024
SHOW_RESPONSE_TIMES = True
