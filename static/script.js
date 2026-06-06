const input = document.getElementById("mensaje");
const chatBox = document.getElementById("chatBox");
const modeList = document.getElementById("modeList");
const quickPrompts = document.getElementById("quickPrompts");
const languageSelect = document.getElementById("languageSelect");
const statusPill = document.getElementById("statusPill");
const sendButton = document.getElementById("sendButton");
const activeModeLabel = document.getElementById("activeModeLabel");
const activeModeDescription = document.getElementById("activeModeDescription");
const composerMode = document.getElementById("composerMode");
const composerLanguage = document.getElementById("composerLanguage");

let modes = [];
let activeMode = "programar";
let isSending = false;

const LANGUAGE_LABELS = {
    auto: "Auto",
    python: "Python",
    javascript: "JavaScript",
    typescript: "TypeScript",
    html: "HTML",
    css: "CSS",
    java: "Java",
    csharp: "C#",
    cpp: "C++",
    sql: "SQL",
    bash: "Bash",
    php: "PHP",
    go: "Go",
    rust: "Rust",
};


function setStatus(text, type = "ready") {
    statusPill.textContent = text;
    statusPill.classList.remove("loading", "error");

    if (type === "loading") {
        statusPill.classList.add("loading");
    }

    if (type === "error") {
        statusPill.classList.add("error");
    }
}


function updateComposerMeta() {
    const mode = modes.find((item) => item.id === activeMode);
    const language = LANGUAGE_LABELS[languageSelect.value] || "Auto";

    composerMode.textContent = `Modo: ${mode ? mode.label : "Programar"}`;
    composerLanguage.textContent = `Lenguaje: ${language}`;
}


function renderModes() {
    modeList.innerHTML = "";

    modes.forEach((mode) => {
        const button = document.createElement("button");
        button.type = "button";
        button.className = `mode-button${mode.id === activeMode ? " active" : ""}`;
        button.innerHTML = `<strong>${mode.label}</strong><span>${mode.description}</span>`;
        button.addEventListener("click", () => selectMode(mode.id));
        modeList.appendChild(button);
    });
}


function renderQuickPrompts() {
    const mode = modes.find((item) => item.id === activeMode);
    quickPrompts.innerHTML = "";

    if (!mode || !mode.quick_prompts) {
        return;
    }

    mode.quick_prompts.forEach((prompt) => {
        const chip = document.createElement("button");
        chip.type = "button";
        chip.className = "prompt-chip";
        chip.textContent = prompt.replace(/\n/g, " ").trim();
        chip.title = prompt;
        chip.addEventListener("click", () => {
            input.value = prompt;
            input.focus();
        });
        quickPrompts.appendChild(chip);
    });
}


function selectMode(modeId) {
    activeMode = modeId;
    const mode = modes.find((item) => item.id === modeId);

    if (mode) {
        activeModeLabel.textContent = mode.label;
        activeModeDescription.textContent = mode.description;
    }

    renderModes();
    renderQuickPrompts();
    updateComposerMeta();
}


function escaparHtml(texto) {
    return texto
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}


function limpiarRespuestaModelo(texto) {
    return texto.replace(/\n?\[[^\]]{1,80}\]\s*/g, "").trim();
}


function crearBloqueCodigo(lenguaje, codigo) {
    const wrapper = document.createElement("div");
    wrapper.className = "code-block-wrapper";

    const header = document.createElement("div");
    header.className = "code-block-header";

    const label = document.createElement("span");
    label.className = "code-language";
    label.textContent = lenguaje || "code";

    const copyButton = document.createElement("button");
    copyButton.type = "button";
    copyButton.className = "copy-button";
    copyButton.textContent = "Copiar";
    copyButton.addEventListener("click", async () => {
        try {
            await navigator.clipboard.writeText(codigo);
            copyButton.textContent = "Copiado";
            copyButton.classList.add("copied");
            setTimeout(() => {
                copyButton.textContent = "Copiar";
                copyButton.classList.remove("copied");
            }, 1600);
        } catch (error) {
            copyButton.textContent = "Error";
        }
    });

    const pre = document.createElement("pre");
    pre.className = "code-block";

    const code = document.createElement("code");
    code.className = lenguaje ? `language-${lenguaje}` : "";
    code.textContent = codigo;

    header.appendChild(label);
    header.appendChild(copyButton);
    pre.appendChild(code);
    wrapper.appendChild(header);
    wrapper.appendChild(pre);

    if (window.hljs) {
        window.hljs.highlightElement(code);
    }

    return wrapper;
}


function renderizarRespuesta(texto, target) {
    target.innerHTML = "";

    const bloqueCodigo = /```([a-zA-Z0-9_+#-]*)\n?([\s\S]*?)```/g;
    let posicion = 0;
    let coincidencia;

    while ((coincidencia = bloqueCodigo.exec(texto)) !== null) {
        const antes = texto.slice(posicion, coincidencia.index);
        const lenguaje = coincidencia[1] || "text";
        const codigo = coincidencia[2].replace(/\n$/, "");

        if (antes.trim() !== "") {
            const paragraph = document.createElement("p");
            paragraph.innerHTML = escaparHtml(antes.trim()).replace(/\n/g, "<br>");
            target.appendChild(paragraph);
        }

        target.appendChild(crearBloqueCodigo(lenguaje, codigo));
        posicion = bloqueCodigo.lastIndex;
    }

    const despues = texto.slice(posicion);

    if (despues.trim() !== "") {
        const paragraph = document.createElement("p");
        paragraph.innerHTML = escaparHtml(despues.trim()).replace(/\n/g, "<br>");
        target.appendChild(paragraph);
    }

    if (!target.children.length) {
        target.textContent = texto;
    }
}


function agregarMensaje(texto, tipo) {
    const mensaje = document.createElement("div");
    mensaje.className = `message ${tipo}-message`;

    if (tipo === "ai" || tipo === "user") {
        renderizarRespuesta(texto, mensaje);
    } else {
        mensaje.textContent = texto;
    }

    chatBox.appendChild(mensaje);
    chatBox.scrollTop = chatBox.scrollHeight;

    return mensaje;
}


async function cargarModos() {
    try {
        const respuesta = await fetch("/modes");
        const data = await respuesta.json();
        modes = data.modes || [];
        renderModes();
        renderQuickPrompts();
        updateComposerMeta();
    } catch (error) {
        console.error(error);
        setStatus("Sin modos", "error");
    }
}


async function enviarMensaje() {
    const texto = input.value.trim();

    if (texto === "" || isSending) {
        return;
    }

    isSending = true;
    sendButton.disabled = true;
    setStatus("Generando...", "loading");

    agregarMensaje(texto, "user");
    input.value = "";

    const respuestaIA = agregarMensaje("", "ai");
    let textoCompleto = "";

    try {
        const body = new URLSearchParams({
            mensaje: texto,
            modo: activeMode,
            lenguaje: languageSelect.value,
        });

        const respuesta = await fetch("/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
            },
            body: body.toString(),
        });

        const reader = respuesta.body.getReader();
        const decoder = new TextDecoder();

        while (true) {
            const { done, value } = await reader.read();

            if (done) {
                break;
            }

            textoCompleto += decoder.decode(value, { stream: true });
            respuestaIA.textContent = limpiarRespuestaModelo(textoCompleto);
            chatBox.scrollTop = chatBox.scrollHeight;
        }

        renderizarRespuesta(limpiarRespuestaModelo(textoCompleto), respuestaIA);
        chatBox.scrollTop = chatBox.scrollHeight;
        setStatus("Listo");
    } catch (error) {
        console.error(error);
        respuestaIA.textContent = "Error conectando con la IA local. Verifica que Ollama este corriendo.";
        setStatus("Error", "error");
    } finally {
        isSending = false;
        sendButton.disabled = false;
    }
}


async function mostrarMemoria() {
    agregarMensaje("Que recuerdas de mi?", "user");

    const respuestaIA = agregarMensaje("", "ai");
    setStatus("Leyendo memoria...", "loading");

    try {
        const respuesta = await fetch("/memories");
        const data = await respuesta.json();
        respuestaIA.textContent = data.text;
        setStatus("Listo");
    } catch (error) {
        console.error(error);
        respuestaIA.textContent = "No pude leer la memoria local.";
        setStatus("Error", "error");
    }
}


async function limpiarChat() {
    const confirmar = window.confirm("Quieres limpiar el historial visible y guardado del chat?");

    if (!confirmar) {
        return;
    }

    try {
        await fetch("/clear", { method: "POST" });
        chatBox.innerHTML = `
            <div class="message ai-message welcome-message">
                <p>Chat limpiado. Empezamos desde cero.</p>
                <p>Elige un modo y dime que quieres programar.</p>
            </div>
        `;
        setStatus("Listo");
    } catch (error) {
        console.error(error);
        setStatus("Error", "error");
    }
}


function insertarPlantillaCodigo() {
    const lenguaje = languageSelect.value === "auto" ? "python" : languageSelect.value;
    const plantilla = `\n\`\`\`${lenguaje}\n\n\`\`\``;
    const inicio = input.selectionStart ?? input.value.length;
    const fin = input.selectionEnd ?? input.value.length;

    input.value = input.value.slice(0, inicio) + plantilla + input.value.slice(fin);
    input.focus();
    input.selectionStart = inicio + lenguaje.length + 5;
    input.selectionEnd = input.selectionStart;
}


input.addEventListener("keydown", function (event) {
    if (event.key === "Enter" && event.ctrlKey) {
        event.preventDefault();
        enviarMensaje();
    }
});

document.addEventListener("keydown", function (event) {
    if (event.ctrlKey && event.key.toLowerCase() === "k") {
        event.preventDefault();
        limpiarChat();
    }
});

languageSelect.addEventListener("change", updateComposerMeta);

cargarModos();