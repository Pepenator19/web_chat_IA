const input = document.getElementById("mensaje");
const chatBox = document.getElementById("chatBox");
const modeList = document.getElementById("modeList");
const agentProSlot = document.getElementById("agentProSlot");
const quickPrompts = document.getElementById("quickPrompts");
const languageSelect = document.getElementById("languageSelect");
const workspaceInput = document.getElementById("workspaceInput");
const workspacePanel = document.getElementById("workspacePanel");
const languagePanel = document.getElementById("languagePanel");
const statusPill = document.getElementById("statusPill");
const sendButton = document.getElementById("sendButton");
const sendButtonLabel = document.getElementById("sendButtonLabel");
const insertCodeButton = document.getElementById("insertCodeButton");
const activeModeLabel = document.getElementById("activeModeLabel");
const activeModeDescription = document.getElementById("activeModeDescription");
const workspaceEyebrow = document.getElementById("workspaceEyebrow");
const workspaceHeader = document.getElementById("workspaceHeader");
const workspaceArea = document.getElementById("workspaceArea");
const composer = document.querySelector(".composer");
const composerMode = document.getElementById("composerMode");
const composerLanguage = document.getElementById("composerLanguage");
const composerWorkspace = document.getElementById("composerWorkspace");
const themeSwatches = document.getElementById("themeSwatches");
const accentColorPicker = document.getElementById("accentColorPicker");
const accent2ColorPicker = document.getElementById("accent2ColorPicker");
const bgColorPicker = document.getElementById("bgColorPicker");
const resetThemeButton = document.getElementById("resetThemeButton");
const themeCollapsible = document.getElementById("themeCollapsible");

let modes = [];
let activeMode = "programar";
let isSending = false;

const THEME_STORAGE_KEY = "codeia-theme-v1";

const THEME_PRESETS = {
    midnight: {
        label: "Midnight",
        bg: "#0b1020",
        panel: "#111827",
        panel2: "#1a2235",
        accent: "#3b82f6",
        accent2: "#22c55e",
        agent1: "#06b6d4",
        agent2: "#8b5cf6",
        agent3: "#f59e0b",
    },
    cyberpunk: {
        label: "Cyber",
        bg: "#0a0014",
        panel: "#14001f",
        panel2: "#1f0030",
        accent: "#ff2d95",
        accent2: "#00f5ff",
        agent1: "#ff2d95",
        agent2: "#00f5ff",
        agent3: "#facc15",
    },
    matrix: {
        label: "Matrix",
        bg: "#020a04",
        panel: "#041208",
        panel2: "#071a0c",
        accent: "#22c55e",
        accent2: "#4ade80",
        agent1: "#22c55e",
        agent2: "#a3e635",
        agent3: "#fbbf24",
    },
    sunset: {
        label: "Sunset",
        bg: "#140a0a",
        panel: "#1c1010",
        panel2: "#261616",
        accent: "#f97316",
        accent2: "#fb7185",
        agent1: "#f97316",
        agent2: "#e11d48",
        agent3: "#facc15",
    },
    violet: {
        label: "Violet",
        bg: "#0c0618",
        panel: "#130b22",
        panel2: "#1a1030",
        accent: "#8b5cf6",
        accent2: "#c084fc",
        agent1: "#8b5cf6",
        agent2: "#ec4899",
        agent3: "#38bdf8",
    },
    ocean: {
        label: "Ocean",
        bg: "#03121f",
        panel: "#061a2a",
        panel2: "#0a2438",
        accent: "#0ea5e9",
        accent2: "#2dd4bf",
        agent1: "#0ea5e9",
        agent2: "#6366f1",
        agent3: "#2dd4bf",
    },
};

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

const MODE_PLACEHOLDERS = {
    agente: "Ej: Lista los archivos del proyecto, crea un script, o arregla un bug...",
    programar: "Describe lo que quieres programar o pega tu codigo aqui...",
    debug: "Pega el error o el codigo que falla...",
    explicar: "Pega el codigo o concepto que quieres entender...",
    refactor: "Pega el codigo que quieres mejorar...",
    revisar: "Pega el codigo para hacer code review...",
    charla: "Conversa libremente sobre lo que quieras...",
    ayuda: "Pregunta como usar la app, modos, atajos o el agente...",
};


function getActiveModeData() {
    return modes.find((item) => item.id === activeMode) || null;
}


function hexToRgb(hex) {
    const clean = hex.replace("#", "");
    const full = clean.length === 3
        ? clean.split("").map((c) => c + c).join("")
        : clean;
    const num = parseInt(full, 16);
    return {
        r: (num >> 16) & 255,
        g: (num >> 8) & 255,
        b: num & 255,
    };
}


function rgbString(hex) {
    const { r, g, b } = hexToRgb(hex);
    return `${r}, ${g}, ${b}`;
}


function darkenHex(hex, amount = 0.2) {
    const { r, g, b } = hexToRgb(hex);
    const mix = (value) => Math.max(0, Math.round(value * (1 - amount)));
    const toHex = (value) => value.toString(16).padStart(2, "0");
    return `#${toHex(mix(r))}${toHex(mix(g))}${toHex(mix(b))}`;
}


function applyThemeVariables(theme) {
    const root = document.documentElement;
    root.style.setProperty("--bg", theme.bg);
    root.style.setProperty("--panel", theme.panel);
    root.style.setProperty("--panel-2", theme.panel2);
    root.style.setProperty("--accent", theme.accent);
    root.style.setProperty("--accent-2", theme.accent2);
    root.style.setProperty("--glow-1", rgbString(theme.accent));
    root.style.setProperty("--glow-2", rgbString(theme.accent2));
    root.style.setProperty("--user-start", theme.accent);
    root.style.setProperty("--user-end", darkenHex(theme.accent, 0.25));
    root.style.setProperty("--eyebrow", theme.accent2);
    root.style.setProperty("--agent-1", theme.agent1 || theme.accent);
    root.style.setProperty("--agent-2", theme.agent2 || theme.accent2);
    root.style.setProperty("--agent-3", theme.agent3 || "#f59e0b");
    root.style.setProperty("--code-bg", darkenHex(theme.bg, 0.15));
    root.style.setProperty("--composer-bg", `${theme.panel}eb`);
    root.style.setProperty("--header-bg", `${theme.panel}b8`);

    accentColorPicker.value = theme.accent;
    accent2ColorPicker.value = theme.accent2;
    bgColorPicker.value = theme.bg;
}


function saveThemeState(state) {
    localStorage.setItem(THEME_STORAGE_KEY, JSON.stringify(state));
}


function loadThemeState() {
    try {
        const raw = localStorage.getItem(THEME_STORAGE_KEY);
        return raw ? JSON.parse(raw) : { preset: "midnight", custom: null };
    } catch (error) {
        return { preset: "midnight", custom: null };
    }
}


function renderThemeSwatches(activePreset) {
    themeSwatches.innerHTML = "";

    Object.entries(THEME_PRESETS).forEach(([id, preset]) => {
        const button = document.createElement("button");
        button.type = "button";
        button.className = `theme-swatch${id === activePreset ? " active" : ""}`;
        button.title = preset.label;
        button.innerHTML = `
            <div class="theme-swatch-inner">
                <div class="theme-swatch-top" style="background:${preset.bg}"></div>
                <div class="theme-swatch-bottom">
                    <div class="theme-swatch-accent" style="background:${preset.accent}"></div>
                    <div class="theme-swatch-accent2" style="background:${preset.accent2}"></div>
                </div>
            </div>
            <span class="theme-swatch-label">${preset.label}</span>
        `;
        button.addEventListener("click", () => selectThemePreset(id));
        themeSwatches.appendChild(button);
    });
}


function selectThemePreset(presetId) {
    const preset = THEME_PRESETS[presetId];
    if (!preset) {
        return;
    }

    document.documentElement.setAttribute("data-theme", presetId === "midnight" ? "" : presetId);
    if (presetId === "midnight") {
        document.documentElement.removeAttribute("data-theme");
    }

    applyThemeVariables(preset);
    renderThemeSwatches(presetId);
    saveThemeState({ preset: presetId, custom: null });
}


function applyCustomTheme() {
    const custom = {
        label: "Custom",
        bg: bgColorPicker.value,
        panel: darkenHex(bgColorPicker.value, 0.08),
        panel2: darkenHex(bgColorPicker.value, 0.16),
        accent: accentColorPicker.value,
        accent2: accent2ColorPicker.value,
        agent1: accentColorPicker.value,
        agent2: accent2ColorPicker.value,
        agent3: "#f59e0b",
    };

    document.documentElement.removeAttribute("data-theme");
    applyThemeVariables(custom);
    renderThemeSwatches("");
    saveThemeState({ preset: "custom", custom });
}


function initThemeSystem() {
    const state = loadThemeState();

    if (state.preset === "custom" && state.custom) {
        document.documentElement.removeAttribute("data-theme");
        applyThemeVariables(state.custom);
        renderThemeSwatches("");
        return;
    }

    selectThemePreset(state.preset || "midnight");
}


function resetTheme() {
    selectThemePreset("midnight");
}


function setStatus(text, type = "ready") {
    const isAgent = activeMode === "agente";
    statusPill.textContent = text;
    statusPill.classList.remove("loading", "error", "agent-pill");

    if (isAgent) {
        statusPill.classList.add("agent-pill");
    }

    if (type === "loading") {
        statusPill.classList.add("loading");
    }

    if (type === "error") {
        statusPill.classList.add("error");
    }
}


function updateComposerMeta() {
    const mode = getActiveModeData();
    const language = LANGUAGE_LABELS[languageSelect.value] || "Auto";

    composerMode.textContent = `Modo: ${mode ? mode.label : "Programar"}`;
    composerLanguage.textContent = `Lenguaje: ${language}`;

    if (mode && mode.uses_workspace) {
        composerWorkspace.textContent = `Carpeta: ${workspaceInput.value || "-"}`;
        composerWorkspace.classList.remove("hidden");
    } else {
        composerWorkspace.classList.add("hidden");
    }

    if (mode) {
        workspacePanel.classList.toggle("hidden", !mode.uses_workspace);
        languagePanel.classList.toggle("hidden", !mode.uses_language);
        insertCodeButton.classList.toggle("hidden", mode.id === "charla" || mode.id === "ayuda");
        input.placeholder = MODE_PLACEHOLDERS[mode.id] || MODE_PLACEHOLDERS.programar;
    }

    updateAgentChrome();
}


function updateAgentChrome() {
    const isAgent = activeMode === "agente";

    workspaceHeader.classList.toggle("agent-active", isAgent);
    workspaceArea.classList.toggle("agent-active", isAgent);
    composer.classList.toggle("agent-composer", isAgent);
    quickPrompts.classList.toggle("agent-prompts", isAgent);
    sendButton.classList.toggle("agent-send", isAgent);

    if (isAgent) {
        workspaceEyebrow.textContent = "Modo agente autonomo";
        sendButtonLabel.textContent = "Desplegar agente";
        statusPill.classList.add("agent-pill");
    } else {
        workspaceEyebrow.textContent = "Asistente local";
        sendButtonLabel.textContent = "Enviar";
        statusPill.classList.remove("agent-pill");
    }
}


function renderAgentProButton(mode) {
    agentProSlot.innerHTML = "";

    const button = document.createElement("button");
    button.type = "button";
    button.className = `mode-button-pro${mode.id === activeMode ? " active" : ""}`;
    button.innerHTML = `
        <div class="pro-shimmer"></div>
        <div class="mode-button-pro-inner">
            <div class="pro-icon-wrap" aria-hidden="true">⚡</div>
            <div>
                <div class="pro-title-row">
                    <strong>${mode.label}</strong>
                </div>
                <span class="pro-desc">${mode.description}</span>
            </div>
        </div>
    `;
    button.addEventListener("click", () => selectMode(mode.id));
    agentProSlot.appendChild(button);
}


function renderModes() {
    modeList.innerHTML = "";
    agentProSlot.innerHTML = "";

    modes.forEach((mode) => {
        if (mode.id === "agente") {
            renderAgentProButton(mode);
            return;
        }

        const button = document.createElement("button");
        button.type = "button";
        button.className = `mode-button${mode.id === activeMode ? " active" : ""}`;
        button.dataset.group = mode.group || "codigo";
        button.innerHTML = `<strong>${mode.label}</strong><span>${mode.description}</span>`;
        button.addEventListener("click", () => selectMode(mode.id));
        modeList.appendChild(button);
    });
}


function renderQuickPrompts() {
    const mode = getActiveModeData();
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
    const mode = getActiveModeData();

    if (mode) {
        if (mode.id === "agente") {
            activeModeLabel.textContent = mode.label;
            activeModeDescription.textContent = "Autonomo · Archivos · Terminal · Busqueda";
        } else {
            activeModeLabel.textContent = mode.label;
            activeModeDescription.textContent = mode.description;
        }
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


function crearTarjetaHerramienta(name, args, content, kind) {
    const card = document.createElement("div");
    card.className = `tool-card tool-card-${kind}`;

    const title = document.createElement("div");
    title.className = "tool-card-title";
    title.textContent = kind === "tool" ? `Herramienta: ${name}` : `Resultado: ${name}`;

    const body = document.createElement("pre");
    body.className = "tool-card-body";
    body.textContent = kind === "tool"
        ? JSON.stringify(args, null, 2)
        : content;

    card.appendChild(title);
    card.appendChild(body);
    return card;
}


function crearContenedorAgente() {
    const container = document.createElement("div");
    container.className = "message ai-message agent-message";
    container.innerHTML = '<p class="agent-status">Iniciando agente...</p>';
    chatBox.appendChild(container);
    chatBox.scrollTop = chatBox.scrollHeight;
    return container;
}


function actualizarAgente(container, event) {
    let status = container.querySelector(".agent-status");
    if (!status) {
        status = document.createElement("p");
        status.className = "agent-status";
        container.prepend(status);
    }

    if (event.event === "step") {
        status.textContent = `Paso ${event.iteration} del agente...`;
    }

    if (event.event === "tool") {
        container.appendChild(crearTarjetaHerramienta(event.name, event.arguments, "", "tool"));
    }

    if (event.event === "result") {
        container.appendChild(crearTarjetaHerramienta(event.name, {}, event.content, "result"));
    }

    if (event.event === "error") {
        status.textContent = "Error del agente";
        const error = document.createElement("p");
        error.textContent = event.content;
        container.appendChild(error);
    }

    if (event.event === "done") {
        status.textContent = "Tarea completada";
        const answer = document.createElement("div");
        answer.className = "agent-final";
        renderizarRespuesta(limpiarRespuestaModelo(event.content || ""), answer);
        container.appendChild(answer);
    }

    chatBox.scrollTop = chatBox.scrollHeight;
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

    const mode = getActiveModeData();
    const isAgent = mode && mode.stream_type === "agent";

    setStatus(isAgent ? "Agente activo..." : "Generando...", "loading");

    agregarMensaje(texto, "user");
    input.value = "";

    const respuestaIA = isAgent ? crearContenedorAgente() : agregarMensaje("", "ai");
    let textoCompleto = "";

    try {
        const body = new URLSearchParams({
            mensaje: texto,
            modo: activeMode,
            lenguaje: languageSelect.value,
            workspace: workspaceInput.value,
        });

        const respuesta = await fetch("/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
            },
            body: body.toString(),
        });

        if (!respuesta.ok) {
            const errorText = await respuesta.text();
            throw new Error(errorText || "Error en la peticion");
        }

        const contentType = respuesta.headers.get("content-type") || "";

        if (contentType.includes("application/x-ndjson")) {
            const raw = await respuesta.text();
            const lines = raw.split("\n").filter((line) => line.trim() !== "");

            for (const line of lines) {
                try {
                    const event = JSON.parse(line);
                    actualizarAgente(respuestaIA, event);
                    if (event.event === "done") {
                        textoCompleto = event.content || "";
                    }
                    if (event.event === "error") {
                        setStatus("Error", "error");
                    }
                } catch (parseError) {
                    console.error(parseError, line);
                }
            }

            if (textoCompleto) {
                setStatus("Listo");
            }
        } else {
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
        }
    } catch (error) {
        console.error(error);
        if (isAgent) {
            actualizarAgente(respuestaIA, {
                event: "error",
                content: error.message || "Error conectando con el agente local.",
            });
        } else {
            respuestaIA.textContent = "Error conectando con la IA local. Verifica que Ollama este corriendo.";
        }
        setStatus("Error", "error");
    } finally {
        isSending = false;
        sendButton.disabled = false;
    }
}


async function mostrarAyudaGlobal() {
    agregarMensaje("Quiero ver la ayuda global de la aplicacion", "user");

    const respuestaIA = agregarMensaje("", "ai");
    setStatus("Cargando ayuda...", "loading");

    try {
        const respuesta = await fetch("/help");
        const data = await respuesta.json();
        renderizarRespuesta(data.content || "Sin contenido de ayuda.", respuestaIA);
        setStatus("Listo");
    } catch (error) {
        console.error(error);
        respuestaIA.textContent = "No pude cargar la ayuda global.";
        setStatus("Error", "error");
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
                <p>Prueba el modo <strong>Agente</strong>, <strong>Charla</strong> o <strong>Ayuda</strong>.</p>
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
workspaceInput.addEventListener("input", updateComposerMeta);
accentColorPicker.addEventListener("input", applyCustomTheme);
accent2ColorPicker.addEventListener("input", applyCustomTheme);
bgColorPicker.addEventListener("input", applyCustomTheme);
resetThemeButton.addEventListener("click", resetTheme);

function initThemeCollapsible() {
    if (!themeCollapsible) {
        return;
    }

    themeCollapsible.open = localStorage.getItem("codeia-theme-open") === "true";
    themeCollapsible.addEventListener("toggle", () => {
        localStorage.setItem("codeia-theme-open", themeCollapsible.open ? "true" : "false");
    });
}

initThemeSystem();
initThemeCollapsible();
cargarModos();