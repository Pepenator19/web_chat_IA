from flask import Flask, render_template, request
import ollama

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():

    mensaje = request.form["mensaje"]

    respuesta = ollama.chat(
        model="phi3",
        messages=[
            {
                "role": "system",
                "content": "Eres una IA útil, breve y algo sarcástica."
            },
            {
                "role": "user",
                "content": mensaje
            }
        ]
    )

    texto = respuesta["message"]["content"]

    return texto


if __name__ == "__main__":
    app.run(debug=True)