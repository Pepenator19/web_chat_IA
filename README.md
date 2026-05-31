# web_chat_IA

A small local AI chat project built with Flask and Ollama.

The goal is to build a simple local-first assistant that is easy to inspect, modify, and understand. It runs on your own machine, uses a local Ollama model, and stores memory in local JSON files.

## Features

- Local Ollama model support
- Flask backend
- Backend split into `app.py`, `config.py`, and `memory.py`
- Separate HTML, CSS, and JavaScript frontend
- Personality prompt loaded from `prompts/personalidad.txt`
- Persistent chat history stored in JSON
- Separate user memories stored in JSON
- Memory inspection command: `Que recuerdas de mi?`
- Memory inspection button: `Ver memoria`
- Memory inspection endpoint: `/memories`
- Quick replies for simple greetings
- Optimized context sent to Ollama for faster responses
- Private memory files ignored by Git
- Example JSON memory files included for reference
- No external APIs required

## Recent Update

This update makes the project more organized and closer to a real local assistant:

- Added `config.py` for settings and paths
- Added `memory.py` for memory loading, saving, formatting, and cleanup
- Moved real memory files into `data/`
- Added public example memory files
- Added a `Ver memoria` button in the frontend
- Added `/memories` JSON endpoint
- Added quick replies for simple messages like `hola`, `buenos dias`, and `gracias`
- Reduced the amount of chat history sent to Ollama
- Trimmed long previous messages before sending context to the model
- Added `keep_alive` so Ollama keeps the model loaded longer
- Cleaned model artifacts like `[Celebratory response]`
- Updated the assistant personality
- Reworked the README

## Project Structure

```plaintext
web_chat_IA/
+-- app.py
+-- config.py
+-- memory.py
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
ollama pull phi3
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

## Speed Optimizations

The app includes a few simple optimizations to make local responses faster:

- Sends only a small number of recent messages to Ollama
- Trims long old messages before sending them as context
- Uses `keep_alive` to keep the Ollama model loaded for a while
- Uses quick replies for simple greetings without calling Ollama
- Prints response timing in the terminal

Example terminal messages:

```plaintext
Quick reply used: 0.00s
Ollama response time: 2.34s
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

Proyecto pequeno de chat con IA local construido con Flask y Ollama.

La idea es crear un asistente local simple, facil de revisar, modificar y entender. Todo corre en tu computadora, usa un modelo local de Ollama y guarda la memoria en archivos JSON locales.

## Caracteristicas

- Soporte para modelos locales de Ollama
- Backend con Flask
- Backend dividido en `app.py`, `config.py` y `memory.py`
- Frontend separado con HTML, CSS y JavaScript
- Personalidad cargada desde `prompts/personalidad.txt`
- Historial persistente guardado en JSON
- Recuerdos del usuario guardados por separado en JSON
- Comando para revisar memoria: `Que recuerdas de mi?`
- Boton para revisar memoria: `Ver memoria`
- Endpoint para revisar memoria: `/memories`
- Respuestas rapidas para saludos simples
- Contexto optimizado para responder mas rapido
- Archivos privados de memoria ignorados por Git
- Archivos JSON de ejemplo incluidos como referencia
- No requiere APIs externas

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

Este proyecto esta en desarrollo. La memoria actual usa JSON porque es simple, transparente y facil de modificar. La estructura ya esta separada para poder crecer despues hacia SQLite, busqueda semantica, RAG o una interfaz mas completa.
