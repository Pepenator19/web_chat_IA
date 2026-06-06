# web_chat_IA

A local-first coding assistant built with Flask and Ollama.

The goal is to offer a simple, private, and hackable programming assistant that runs on your own machine. It uses a local Ollama model, keeps memory in JSON files, and includes an IDE-style web UI for writing, debugging, explaining, refactoring, and reviewing code.

Default model:

```plaintext
qwen2.5-coder:3b-instruct
```

## Features

- Local Ollama model support
- Coding-focused assistant personality
- 5 work modes: Program, Debug, Explain, Refactor, Review
- Language selector: Python, JavaScript, TypeScript, HTML, CSS, SQL, and more
- IDE-style dark UI with syntax highlighting
- Copy button on every code block
- Quick prompt chips per mode
- Flask backend split into `app.py`, `config.py`, `memory.py`, and `coding.py`
- Separate HTML, CSS, and JavaScript frontend
- Personality prompt loaded from `prompts/personalidad.txt`
- Persistent chat history stored in JSON
- Separate user memories stored in JSON
- Memory inspection command: `Que recuerdas de mi?`
- Memory inspection button: `Ver memoria`
- Memory inspection endpoint: `/memories`
- Chat reset endpoint: `/clear`
- Coding modes endpoint: `/modes`
- Quick replies for simple greetings and help
- Streaming responses from Ollama
- Private memory files ignored by Git
- Example JSON memory files included for reference
- No external APIs required

## Recent Update

This release turns the project into a real local coding assistant:

- Added `coding.py` with programming modes and mode-specific prompts
- Added 5 coding modes: Program, Debug, Explain, Refactor, Review
- Added language selector with auto-detect and common languages
- Redesigned the frontend into an IDE-style workspace
- Added syntax highlighting with Highlight.js
- Added copy buttons for code blocks
- Added quick prompt chips for each mode
- Added clear chat button and `/clear` endpoint
- Added `/modes` endpoint for frontend mode loading
- Increased coding context limits for better code answers
- Expanded memory triggers for technical preferences
- Improved code-aware message truncation
- Updated personality prompt for programming tasks
- Tuned temperature per mode for more precise coding answers

## Project Structure

```plaintext
web_chat_IA/
+-- app.py
+-- config.py
+-- memory.py
+-- coding.py
+-- prompts/
|   +-- personalidad.txt
+-- static/
|   +-- script.js
|   +-- style.css
+-- templates/
|   +-- index.html
+-- data/
|   +-- memoria.json
|   +-- recuerdos.json
|   +-- example_memory.json
|   +-- example_recuerdos.json
+-- requirements.txt
+-- requirements_full.txt
+-- .gitignore
+-- README.md
```

## Requirements

Before running the project, install:

- Python 3.10 or higher
- Git
- Ollama

Download Ollama:

```plaintext
https://ollama.com
```

Install a local model, for example:

```bash
ollama pull qwen2.5-coder:3b-instruct
```

## Installation

Clone the repository:

```bash
git clone https://github.com/Pepenator19/web_chat_IA.git
```

Enter the project folder:

```bash
cd web_chat_IA
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate the virtual environment.

Windows:

```bash
venv\Scripts\activate
```

Linux / macOS:

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run The Project

Make sure Ollama is running, then start the app:

```bash
python app.py
```

Open the local address shown in your terminal, usually:

```plaintext
http://127.0.0.1:5000
```

## Coding Modes

The assistant supports 5 programming modes:

| Mode | Purpose |
|------|---------|
| Program | Generate clean and functional code |
| Debug | Find and fix bugs |
| Explain | Explain code or concepts |
| Refactor | Improve structure and readability |
| Review | Do a code review with severity levels |

Each mode changes the system prompt and model temperature for better results.

## UI Shortcuts

- `Ctrl + Enter` send message
- `Ctrl + K` clear chat
- `Shift + Enter` new line in the textarea

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Main chat UI |
| `/chat` | POST | Send a message to the assistant |
| `/modes` | GET | List available coding modes |
| `/memories` | GET | Return saved user memories |
| `/clear` | POST | Clear saved chat history |

`/chat` accepts these form fields:

- `mensaje` required message text
- `modo` optional mode: `programar`, `debug`, `explicar`, `refactor`, `revisar`
- `lenguaje` optional language hint: `auto`, `python`, `javascript`, etc.

## Local Memory

The project stores memory locally using JSON files:

```plaintext
data/memoria.json
data/recuerdos.json
```

- `memoria.json` stores the chat history.
- `recuerdos.json` stores important user memories.

These files are private and are ignored by Git.

Example files are included so other people can understand the format without exposing real personal data:

```plaintext
data/example_memory.json
data/example_recuerdos.json
```

You can inspect saved user memories from the chat by typing:

```plaintext
Que recuerdas de mi?
```

The frontend also includes a `Ver memoria` button, and the backend exposes a JSON endpoint:

```plaintext
/memories
```

Memory logic is separated in `memory.py`, so the storage system can later move from JSON to SQLite, embeddings, or a vector database without rewriting the whole Flask app.

## Model Settings

Current defaults in `config.py`:

- `MAX_HISTORY_MESSAGES = 8`
- `MAX_MESSAGE_CHARS = 2500`
- `MAX_RESPONSE_TOKENS = 2048`
- `OLLAMA_CONTEXT_SIZE = 8192`
- `OLLAMA_KEEP_ALIVE = 15m`

You can change the model with the `OLLAMA_MODEL` environment variable without editing the code.

Example:

```bash
set OLLAMA_MODEL=qwen2.5-coder:3b-instruct
python app.py
```

Example terminal messages:

```plaintext
Quick reply used: 0.00s
Ollama response time (debug): 2.34s
```

## Privacy

This project:

- Runs locally with Ollama
- Does not use external APIs
- Does not send chat data to cloud services
- Stores memory on your own machine
- Keeps real memory files out of Git

## Git Ignored Files

The `.gitignore` file ignores local environments, Python cache files, and private memory files:

```gitignore
__pycache__/
*.pyc
venv/
.env
data/*.json
!data/example_memory.json
!data/example_recuerdos.json
```

## Espanol

Proyecto de asistente de programacion local construido con Flask y Ollama.

La idea es crear un asistente local simple, privado y facil de modificar. Todo corre en tu computadora, usa un modelo local de Ollama y guarda la memoria en archivos JSON.

## Caracteristicas

- Soporte para modelos locales de Ollama
- Asistente enfocado en programacion
- 5 modos de trabajo: Programar, Debug, Explicar, Refactor, Revisar
- Selector de lenguaje: Python, JavaScript, TypeScript, HTML, CSS, SQL y mas
- Interfaz oscura estilo IDE con resaltado de sintaxis
- Boton para copiar bloques de codigo
- Chips de prompts rapidos por modo
- Backend dividido en `app.py`, `config.py`, `memory.py` y `coding.py`
- Frontend separado con HTML, CSS y JavaScript
- Personalidad cargada desde `prompts/personalidad.txt`
- Historial persistente guardado en JSON
- Recuerdos del usuario guardados por separado en JSON
- Comando para revisar memoria: `Que recuerdas de mi?`
- Boton para revisar memoria: `Ver memoria`
- Endpoint para revisar memoria: `/memories`
- Endpoint para limpiar chat: `/clear`
- Endpoint de modos: `/modes`
- Respuestas en streaming desde Ollama
- Archivos privados de memoria ignorados por Git
- Archivos JSON de ejemplo incluidos como referencia
- No requiere APIs externas

## Modos De Programacion

| Modo | Uso |
|------|-----|
| Programar | Generar codigo limpio y funcional |
| Debug | Encontrar y corregir errores |
| Explicar | Explicar codigo o conceptos |
| Refactor | Mejorar estructura y legibilidad |
| Revisar | Hacer code review con severidad |

## Atajos De La Interfaz

- `Ctrl + Enter` enviar mensaje
- `Ctrl + K` limpiar chat
- `Shift + Enter` nueva linea

## Ejecutar El Proyecto

Asegurate de que Ollama este abierto y funcionando. Despues ejecuta:

```bash
python app.py
```

Abre la direccion local que aparece en la terminal, normalmente:

```plaintext
http://127.0.0.1:5000
```

## Memoria Local

El proyecto guarda la memoria localmente usando archivos JSON:

```plaintext
data/memoria.json
data/recuerdos.json
```

- `memoria.json` guarda el historial del chat.
- `recuerdos.json` guarda recuerdos importantes del usuario.

Estos archivos son privados y Git los ignora.

Tambien hay archivos de ejemplo para mostrar el formato sin subir datos personales reales:

```plaintext
data/example_memory.json
data/example_recuerdos.json
```

Puedes revisar los recuerdos guardados desde el chat escribiendo:

```plaintext
Que recuerdas de mi?
```

La interfaz tambien tiene un boton `Ver memoria`, y el backend incluye un endpoint en JSON:

```plaintext
/memories
```

## Estado Del Proyecto

Este proyecto esta en desarrollo activo. La memoria actual usa JSON porque es simple, transparente y facil de modificar. La estructura ya esta separada para poder crecer despues hacia subida de archivos, snippets guardados, SQLite, busqueda semantica o RAG.