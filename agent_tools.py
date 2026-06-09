import glob as glob_module
import os
import re
import subprocess
from pathlib import Path

MAX_OUTPUT_CHARS = 30000
DEFAULT_SHELL_TIMEOUT = 120


class ToolRegistry:
    def __init__(self, workspace: str):
        self.workspace = os.path.abspath(workspace)

    def _resolve_path(self, path: str) -> str:
        if not path or path == ".":
            return self.workspace
        if os.path.isabs(path):
            return os.path.normpath(path)
        return os.path.normpath(os.path.join(self.workspace, path))

    def _truncate(self, text: str) -> str:
        if len(text) <= MAX_OUTPUT_CHARS:
            return text
        half = MAX_OUTPUT_CHARS // 2
        return (
            text[:half]
            + f"\n\n... [{len(text) - MAX_OUTPUT_CHARS} caracteres omitidos] ...\n\n"
            + text[-half:]
        )

    def shell(self, command: str, description: str = "", block_until_ms: int = 30000) -> str:
        timeout = max(1, block_until_ms // 1000)
        try:
            result = subprocess.run(
                command,
                shell=True,
                cwd=self.workspace,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=min(timeout, DEFAULT_SHELL_TIMEOUT),
            )
            parts = []
            if description:
                parts.append(f"$ {description}")
            parts.append(f"$ {command}")
            if result.stdout:
                parts.append(result.stdout.rstrip())
            if result.stderr:
                parts.append(f"stderr:\n{result.stderr.rstrip()}")
            parts.append(f"exit_code: {result.returncode}")
            return self._truncate("\n".join(parts))
        except subprocess.TimeoutExpired:
            return f"Error: el comando excedio el tiempo limite de {timeout}s"
        except Exception as exc:
            return f"Error ejecutando comando: {exc}"

    def read(self, path: str, offset: int = 1, limit: int = 0) -> str:
        full_path = self._resolve_path(path)
        try:
            with open(full_path, "r", encoding="utf-8", errors="replace") as handle:
                lines = handle.readlines()
            if offset < 1:
                offset = 1
            start = offset - 1
            end = start + limit if limit > 0 else len(lines)
            selected = lines[start:end]
            numbered = "".join(
                f"{start + index + 1:6}|{line}" for index, line in enumerate(selected)
            )
            return self._truncate(numbered or "(archivo vacio)")
        except FileNotFoundError:
            return f"Error: archivo no encontrado: {path}"
        except Exception as exc:
            return f"Error leyendo archivo: {exc}"

    def write(self, path: str, contents: str) -> str:
        full_path = self._resolve_path(path)
        try:
            parent = os.path.dirname(full_path)
            if parent:
                os.makedirs(parent, exist_ok=True)
            with open(full_path, "w", encoding="utf-8", newline="\n") as handle:
                handle.write(contents)
            return f"Archivo escrito: {path} ({len(contents)} caracteres)"
        except Exception as exc:
            return f"Error escribiendo archivo: {exc}"

    def str_replace(self, path: str, old_string: str, new_string: str, replace_all: bool = False) -> str:
        full_path = self._resolve_path(path)
        try:
            with open(full_path, "r", encoding="utf-8", errors="replace") as handle:
                content = handle.read()
            count = content.count(old_string)
            if count == 0:
                return f"Error: no se encontro el texto a reemplazar en {path}"
            if count > 1 and not replace_all:
                return (
                    f"Error: el texto aparece {count} veces en {path}. "
                    "Usa replace_all=true o proporciona mas contexto."
                )
            if replace_all:
                updated = content.replace(old_string, new_string)
            else:
                updated = content.replace(old_string, new_string, 1)
            with open(full_path, "w", encoding="utf-8", newline="\n") as handle:
                handle.write(updated)
            replaced = count if replace_all else 1
            return f"Reemplazado {replaced} vez/veces en {path}"
        except FileNotFoundError:
            return f"Error: archivo no encontrado: {path}"
        except Exception as exc:
            return f"Error en str_replace: {exc}"

    def grep(
        self,
        pattern: str,
        path: str = ".",
        glob_pattern: str = "",
        glob: str = "",
        output_mode: str = "content",
        head_limit: int = 50,
    ) -> str:
        glob_pattern = glob_pattern or glob
        search_path = self._resolve_path(path)
        results = []
        file_glob = glob_pattern or "*"

        if os.path.isfile(search_path):
            files = [search_path]
        else:
            files = []
            for root, dirs, filenames in os.walk(search_path):
                dirs[:] = [
                    d
                    for d in dirs
                    if not d.startswith(".")
                    and d not in {"node_modules", "__pycache__", "venv", ".git"}
                ]
                for filename in filenames:
                    if glob_module.fnmatch.fnmatch(filename, file_glob):
                        files.append(os.path.join(root, filename))

        regex = re.compile(pattern, re.IGNORECASE)
        for file_path in files:
            try:
                with open(file_path, "r", encoding="utf-8", errors="ignore") as handle:
                    for line_no, line in enumerate(handle, start=1):
                        if regex.search(line):
                            rel = os.path.relpath(file_path, self.workspace)
                            results.append(f"{rel}:{line_no}:{line.rstrip()}")
                            if len(results) >= head_limit:
                                break
            except (OSError, UnicodeError):
                continue
            if len(results) >= head_limit:
                break

        if output_mode == "files_with_matches":
            unique = sorted({item.split(":", 1)[0] for item in results})
            return "\n".join(unique) or "Sin coincidencias"
        if output_mode == "count":
            return str(len(results))
        return self._truncate("\n".join(results) or "Sin coincidencias")

    def glob(self, glob_pattern: str, target_directory: str = ".") -> str:
        base = self._resolve_path(target_directory)
        pattern = glob_pattern if glob_pattern.startswith("**/") else f"**/{glob_pattern}"
        matches = sorted(
            str(Path(p).relative_to(base)) if str(p).startswith(base) else str(p)
            for p in glob_module.glob(os.path.join(base, pattern), recursive=True)
        )
        return self._truncate("\n".join(matches) or "Sin archivos")

    def delete(self, path: str) -> str:
        full_path = self._resolve_path(path)
        try:
            if os.path.isdir(full_path):
                return f"Error: {path} es un directorio, no un archivo"
            os.remove(full_path)
            return f"Archivo eliminado: {path}"
        except FileNotFoundError:
            return f"Error: archivo no encontrado: {path}"
        except Exception as exc:
            return f"Error eliminando archivo: {exc}"

    def list_dir(self, path: str = ".") -> str:
        full_path = self._resolve_path(path)
        try:
            items = sorted(os.listdir(full_path))
            lines = []
            for item in items:
                if item.startswith("."):
                    continue
                full = os.path.join(full_path, item)
                prefix = "DIR " if os.path.isdir(full) else "FILE"
                lines.append(f"{prefix} {item}")
            return "\n".join(lines) or "(carpeta vacia)"
        except Exception as exc:
            return f"Error listando carpeta: {exc}"

    def execute(self, name: str, arguments: dict) -> str:
        dispatch = {
            "Shell": self.shell,
            "Read": self.read,
            "Write": self.write,
            "StrReplace": self.str_replace,
            "Grep": self.grep,
            "Glob": self.glob,
            "Delete": self.delete,
            "ListDir": self.list_dir,
        }
        handler = dispatch.get(name)
        if not handler:
            return f"Error: herramienta desconocida '{name}'"
        try:
            return handler(**arguments)
        except TypeError as exc:
            return f"Error: argumentos invalidos para {name}: {exc}"


TOOL_DEFINITIONS = [
    {
        "type": "function",
        "function": {
            "name": "Shell",
            "description": "Ejecuta un comando en la terminal.",
            "parameters": {
                "type": "object",
                "properties": {
                    "command": {"type": "string"},
                    "description": {"type": "string"},
                    "block_until_ms": {"type": "integer"},
                },
                "required": ["command"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "Read",
            "description": "Lee el contenido de un archivo.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string"},
                    "offset": {"type": "integer"},
                    "limit": {"type": "integer"},
                },
                "required": ["path"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "Write",
            "description": "Crea o sobrescribe un archivo completo.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string"},
                    "contents": {"type": "string"},
                },
                "required": ["path", "contents"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "StrReplace",
            "description": "Reemplaza texto exacto en un archivo existente.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string"},
                    "old_string": {"type": "string"},
                    "new_string": {"type": "string"},
                    "replace_all": {"type": "boolean"},
                },
                "required": ["path", "old_string", "new_string"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "Grep",
            "description": "Busca un patron regex en archivos del proyecto.",
            "parameters": {
                "type": "object",
                "properties": {
                    "pattern": {"type": "string"},
                    "path": {"type": "string"},
                    "glob": {"type": "string"},
                    "output_mode": {"type": "string"},
                    "head_limit": {"type": "integer"},
                },
                "required": ["pattern"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "Glob",
            "description": "Encuentra archivos por patron.",
            "parameters": {
                "type": "object",
                "properties": {
                    "glob_pattern": {"type": "string"},
                    "target_directory": {"type": "string"},
                },
                "required": ["glob_pattern"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "Delete",
            "description": "Elimina un archivo.",
            "parameters": {
                "type": "object",
                "properties": {"path": {"type": "string"}},
                "required": ["path"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "ListDir",
            "description": "Lista archivos y carpetas en un directorio.",
            "parameters": {
                "type": "object",
                "properties": {"path": {"type": "string"}},
            },
        },
    },
]