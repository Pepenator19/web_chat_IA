import json
import re


def _parse_json_object(text: str):
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return None


def _normalize_tool_call(name: str, arguments):
    if isinstance(arguments, str):
        parsed = _parse_json_object(arguments)
        arguments = parsed if parsed is not None else {}
    if not isinstance(arguments, dict):
        arguments = {}
    return {"name": name, "arguments": arguments}


def extract_tool_calls(content: str) -> list:
    if not content:
        return []

    calls = []

    for match in re.finditer(
        r"<tool_call>\s*(\{.*?\})\s*</tool_call>",
        content,
        flags=re.DOTALL,
    ):
        payload = _parse_json_object(match.group(1))
        if payload and "name" in payload:
            calls.append(_normalize_tool_call(payload["name"], payload.get("arguments", {})))

    for match in re.finditer(r"```(?:json|tool)?\s*(\{.*?\})\s*```", content, flags=re.DOTALL):
        payload = _parse_json_object(match.group(1))
        if payload and "name" in payload:
            calls.append(_normalize_tool_call(payload["name"], payload.get("arguments", {})))

    stripped = content.strip()
    if stripped.startswith("{") and stripped.endswith("}"):
        payload = _parse_json_object(stripped)
        if payload and "name" in payload:
            calls.append(_normalize_tool_call(payload["name"], payload.get("arguments", {})))

    for match in re.finditer(
        r'\{\s*"name"\s*:\s*"([A-Za-z]+)"\s*,\s*"arguments"\s*:\s*(\{[\s\S]*?\})\s*\}',
        content,
    ):
        payload = {
            "name": match.group(1),
            "arguments": _parse_json_object(match.group(2)) or {},
        }
        calls.append(_normalize_tool_call(payload["name"], payload.get("arguments", {})))

    deduped = []
    seen = set()
    for call in calls:
        key = (call["name"], json.dumps(call["arguments"], sort_keys=True))
        if key not in seen:
            seen.add(key)
            deduped.append(call)
    return deduped


def extract_final_text(content: str, tool_calls: list) -> str:
    if not content:
        return ""

    cleaned = content
    cleaned = re.sub(r"<tool_call>.*?</tool_call>", "", cleaned, flags=re.DOTALL)
    cleaned = re.sub(r"```(?:json|tool)?\s*\{.*?\}\s*```", "", cleaned, flags=re.DOTALL)

    stripped = cleaned.strip()
    if tool_calls and stripped.startswith("{") and stripped.endswith("}"):
        payload = _parse_json_object(stripped)
        if payload and "name" in payload:
            return ""

    return cleaned.strip()


def message_tool_calls(message) -> list:
    calls = []
    raw_calls = None

    if isinstance(message, dict):
        raw_calls = message.get("tool_calls")
        content = message.get("content", "")
    else:
        raw_calls = getattr(message, "tool_calls", None)
        content = getattr(message, "content", "") or ""

    if raw_calls:
        for item in raw_calls:
            if isinstance(item, dict):
                fn = item.get("function", {})
                calls.append(_normalize_tool_call(fn.get("name", ""), fn.get("arguments", {})))
            else:
                fn = getattr(item, "function", None)
                if fn:
                    calls.append(
                        _normalize_tool_call(
                            getattr(fn, "name", ""),
                            getattr(fn, "arguments", {}),
                        )
                    )

    calls.extend(extract_tool_calls(content))
    return calls