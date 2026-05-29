"""
==================================================
CHAT IA LOCAL CON FLASK + OLLAMA
==================================================

Este programa:

1. Crea un servidor web usando Flask
2. Muestra la página HTML
3. Recibe mensajes del usuario
4. Envía mensajes al modelo IA local
5. Devuelve respuestas al navegador

Modelo usado:
- phi3

Tecnologías:
- Python
- Flask
- Ollama
- HTML
- CSS
- JavaScript
"""

# Importar Flask
from flask import Flask, render_template, request

# Importar Ollama
import ollama


# Crear aplicación Flask
app = Flask(__name__)


# Ruta principal
@app.route("/")
def index():

    """
    Mostrar la página principal.
    """

    return render_template("index.html")


# Ruta del chat
@app.route("/chat", methods=["POST"])
def chat():

    """
    Recibe mensaje del usuario,
    lo envía a la IA y devuelve la respuesta.
    """

    # Obtener mensaje enviado desde JavaScript
    mensaje = request.form["mensaje"]


    # Enviar conversación al modelo IA
    respuesta = ollama.chat(

        # Modelo utilizado
        model="phi3",

        # Mensajes enviados al modelo
        messages=[

            # Personalidad de la IA
            {
                "role": "system",
                "content": "Eres una IA útil, breve y algo sarcástica."
            },

            # Mensaje del usuario
            {
                "role": "user",
                "content": mensaje
            }
        ]
    )


    # Extraer texto de respuesta
    texto = respuesta["message"]["content"]


    # Devolver texto al navegador
    return texto


# Ejecutar servidor Flask
if __name__ == "__main__":

    # Activar modo debug
    app.run(debug=True)