import json
from typing import Callable

import ollama

from agent_parser import extract_final_text, message_tool_calls
from agent_tools import TOOL_DEFINITIONS, ToolRegistry

MAX_AGENT_ITERATIONS = 25


def build_agent_system_prompt(workspace: str) -> str:
    return f"""Eres un agente de programacion autonomo integrado en Code IA Local.

## Entorno
- Sistema operativo: Windows
- Carpeta de trabajo: {workspace}
- Tienes acceso REAL a terminal, archivos y busqueda.

## Reglas
1. EJECUTA tu mismo las acciones. Nunca pidas al usuario que corra comandos manualmente.
2. Investiga antes de editar: Read, Grep, Glob, ListDir.
3. Cambios minimos y enfocados.
4. Si algo falla, diagnostica y reintenta.
5. Responde en espanol.

## Herramientas
Shell, Read, Write, StrReplace, Grep, Glob, Delete, ListDir

## Formato de herramientas
Responde SOLO con:

<tool_call>
{{"name": "NombreHerramienta", "arguments": {{"param": "valor"}}}}
</tool_call>

Cuando termines, responde en lenguaje natural con un resumen."""


class WebAgent:
    def __init__(self, workspace: str, model: str, history: list | None = None):
        self.workspace = workspace
        self.model = model
        self.tools = ToolRegistry(workspace)
        self.messages = [{"role": "system", "content": build_agent_system_prompt(workspace)}]

        if history:
            for item in history:
                role = item.get("role")
                if role in {"user", "assistant"}:
                    self.messages.append({"role": role, "content": item.get("content", "")})

    def _looks_like_instruction_not_action(self, text: str) -> bool:
        lowered = text.lower()
        hints = [
            "puedes usar",
            "puedes ejecutar",
            "debes ejecutar",
            "usa el siguiente comando",
            "ejecuta el siguiente",
            "corre el comando",
            "usa este comando",
            "```shell",
            "```bash",
        ]
        return any(hint in lowered for hint in hints)

    def _chat(self) -> dict:
        response = ollama.chat(
            model=self.model,
            messages=self.messages,
            tools=TOOL_DEFINITIONS,
            options={
                "temperature": 0.2,
                "num_ctx": 16384,
                "num_predict": 4096,
            },
        )
        if hasattr(response, "message"):
            message = response.message
            return {
                "role": message.role,
                "content": message.content or "",
                "tool_calls": message.tool_calls,
            }
        return response["message"]

    def run_turn(self, user_input: str, emit: Callable[[dict], None] | None = None) -> str:
        self.messages.append({"role": "user", "content": user_input})

        for iteration in range(1, MAX_AGENT_ITERATIONS + 1):
            if emit:
                emit({"event": "step", "iteration": iteration})

            message = self._chat()
            content = message.get("content", "") or ""
            tool_calls = message_tool_calls(message)

            if tool_calls:
                self.messages.append(
                    {
                        "role": "assistant",
                        "content": content,
                        "tool_calls": [
                            {
                                "function": {
                                    "name": call["name"],
                                    "arguments": call["arguments"],
                                }
                            }
                            for call in tool_calls
                        ],
                    }
                )

                for call in tool_calls:
                    if emit:
                        emit(
                            {
                                "event": "tool",
                                "name": call["name"],
                                "arguments": call["arguments"],
                            }
                        )

                    result = self.tools.execute(call["name"], call["arguments"])

                    if emit:
                        emit({"event": "result", "name": call["name"], "content": result})

                    self.messages.append(
                        {
                            "role": "user",
                            "content": (
                                f'<tool_result tool="{call["name"]}">\n'
                                f"{result}\n"
                                f"</tool_result>\n"
                                "Continua con la siguiente accion o responde al usuario si terminaste."
                            ),
                        }
                    )
                continue

            final_text = extract_final_text(content, tool_calls)
            if not final_text:
                self.messages.append({"role": "assistant", "content": content})
                continue

            if self._looks_like_instruction_not_action(final_text) and iteration < MAX_AGENT_ITERATIONS:
                self.messages.append({"role": "assistant", "content": content})
                self.messages.append(
                    {
                        "role": "user",
                        "content": (
                            "No des instrucciones al usuario. "
                            "Ejecuta tu mismo la accion con una herramienta usando el formato <tool_call>."
                        ),
                    }
                )
                continue

            self.messages.append({"role": "assistant", "content": final_text})
            if emit:
                emit({"event": "done", "content": final_text})
            return final_text

        fallback = "Alcance el limite de pasos del agente. Reformula la tarea o divide el trabajo."
        if emit:
            emit({"event": "done", "content": fallback})
        return fallback


def stream_agent_events(workspace: str, model: str, user_input: str, history: list | None = None):
    events = []

    def emit(event: dict):
        events.append(event)

    agent = WebAgent(workspace, model, history=history)
    final = agent.run_turn(user_input, emit=emit)

    for event in events:
        yield json.dumps(event, ensure_ascii=False) + "\n"

    if not events or events[-1].get("event") != "done":
        yield json.dumps({"event": "done", "content": final}, ensure_ascii=False) + "\n"