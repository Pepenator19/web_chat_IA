# web_chat_IA

A small local AI chat project built with Flask and Ollama.

The goal is to build a simple local-first assistant that is easy to inspect, modify, and understand. It runs on your own machine, uses a local Ollama model, and stores memory in local JSON files.

## Features

- Local Ollama model support
- Flask backend
- Separate HTML, CSS, and JavaScript frontend
- Personality prompt loaded from a text file
- Persistent chat history stored in JSON
- Separate user memories stored in JSON
- Private memory files ignored by Git
- Example JSON memory files included for reference
- No external APIs required

## Project Structure

```plaintext
web_chat_IA/
+-- app.py
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

```bash
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

Activate the virtual environment:

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

```bash
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

## Español

Proyecto pequeño de chat con IA local construido con Flask y Ollama.

La idea es crear un asistente local simple, fácil de revisar, modificar y entender. Todo corre en tu propia computadora, usa un modelo local de Ollama y guarda la memoria en archivos JSON locales.

## Características

- Soporte para modelos locales de Ollama
- Backend con Flask
- Frontend separado con HTML, CSS y JavaScript
- Personalidad cargada desde un archivo de texto
- Historial persistente guardado en JSON
- Recuerdos del usuario guardados por separado en JSON
- Archivos privados de memoria ignorados por Git
- Archivos JSON de ejemplo incluidos como referencia
- No requiere APIs externas

## Requisitos

Antes de ejecutar el proyecto necesitas:

- Python 3.10 o superior
- Git
- Ollama

Descarga Ollama:

```bash
https://ollama.com
```

Instala un modelo local, por ejemplo:

```bash
ollama pull phi3
```

## Instalación

Clona el repositorio:

```bash
git clone https://github.com/Pepenator19/web_chat_IA.git
```

Entra a la carpeta:

```bash
cd web_chat_IA
```

Crea un entorno virtual:

```bash
python -m venv venv
```

Activa el entorno virtual:

Windows:

```bash
venv\Scripts\activate
```

Linux / macOS:

```bash
source venv/bin/activate
```

Instala las dependencias:

```bash
pip install -r requirements.txt
```

## Ejecutar El Proyecto

Asegúrate de que Ollama esté abierto y funcionando. Después ejecuta:

```bash
python app.py
```

Abre la dirección local que aparece en la terminal, normalmente:

```bash
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

También hay archivos de ejemplo para mostrar el formato sin subir datos personales reales:

```plaintext
data/example_memory.json
data/example_recuerdos.json
```

## Privacidad

Este proyecto:

- Funciona localmente con Ollama
- No usa APIs externas
- No envía conversaciones a servicios en la nube
- Guarda la memoria en tu propia computadora
- Mantiene los archivos reales de memoria fuera de Git

## Estado Del Proyecto

Este proyecto está en desarrollo. La memoria actual usa JSON porque es simple, transparente y fácil de modificar. Más adelante se podrían agregar mejoras como mejor organización de recuerdos, búsqueda semántica, RAG o una interfaz más completa.
