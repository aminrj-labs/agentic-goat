"""Record/replay cassette for the lab's OpenAI-compatible chat client.

Spec: agentic-goat v1, section 6.3.

The driver routes every chat.completions.create call through one choke
point:

    response = _complete(**kwargs)

and _complete delegates to a Cassette when --record or --replay was given:

    --record PATH   the live model answers; every response is appended
                    to PATH in call order
    --replay PATH   the stored responses are served in order; no model,
                    no endpoint and no API key are required

Only the LLM call is intercepted. MCP servers, tools, the canary file and
the exfil listener run live in both modes, so replay reproduces the real
side effects of the attack.

Cassettes are plain JSON:

    {"schema": 1,
     "status": "recorded" | "placeholder",
     "lab": "...", "model": "...", "endpoint": "...",
     "recorded_at": "2026-09-24T...Z" | null,
     "turns": [
        {"content": "..." | null,
         "tool_calls": [{"id": "...",
                          "function": {"name": "...",
                                       "arguments": "<json string>"}}],
         "finish_reason": "tool_calls" | "stop"},
        ...
     ]}

A "placeholder" cassette is shipped when no model endpoint was available
at authoring time. Replaying one prints a loud warning and serves
illustrative assistant turns; follow cassettes/README.md to record a real
capture with any OpenAI-compatible model.
"""

import json
import os
from datetime import datetime, timezone

SCHEMA_VERSION = 1


class _Args:
    def __init__(self, name, arguments):
        self.name = name
        self.arguments = arguments


class _ToolCall:
    def __init__(self, id, name, arguments):
        self.id = id
        self.type = "function"
        self.function = _Args(name, arguments)


class _Message:
    def __init__(self, content, tool_calls):
        self.role = "assistant"
        self.content = content
        self.tool_calls = tool_calls
        self.name = None
        self.refusal = None

    def model_dump(self):
        out = {"role": "assistant", "content": self.content}
        if self.tool_calls:
            out["tool_calls"] = [
                {
                    "id": tc.id,
                    "type": "function",
                    "function": {
                        "name": tc.function.name,
                        "arguments": tc.function.arguments,
                    },
                }
                for tc in self.tool_calls
            ]
        return out


class _Choice:
    def __init__(self, message, finish_reason):
        self.message = message
        self.index = 0
        self.finish_reason = finish_reason


class _Response:
    def __init__(self, message, finish_reason):
        self.choices = [_Choice(message, finish_reason)]


def _serialize(response):
    choice = response.choices[0]
    msg = choice.message
    tool_calls = []
    for tc in (msg.tool_calls or []):
        tool_calls.append(
            {
                "id": tc.id,
                "function": {
                    "name": tc.function.name,
                    "arguments": tc.function.arguments,
                },
            }
        )
    return {
        "content": msg.content,
        "tool_calls": tool_calls,
        "finish_reason": choice.finish_reason or "stop",
    }


def _build(turn):
    tool_calls = [
        _ToolCall(
            tc["id"],
            tc["function"]["name"],
            tc["function"]["arguments"],
        )
        for tc in (turn.get("tool_calls") or [])
    ]
    message = _Message(turn.get("content"), tool_calls)
    return _Response(message, turn.get("finish_reason", "stop"))


class Cassette:
    def __init__(self, path, mode, model=None, endpoint=None, lab=None):
        if mode not in ("record", "replay"):
            raise ValueError(f"mode must be 'record' or 'replay', got {mode!r}")
        self.path = path
        self.mode = mode
        self.model = model
        self.endpoint = endpoint
        self.lab = lab
        self.turns = []
        self._cursor = 0
        if mode == "replay":
            self._load()
        elif os.path.exists(path):
            print(f"[Cassette] {path} exists; recording will overwrite it")

    def _load(self):
        try:
            with open(self.path, encoding="utf-8") as f:
                data = json.load(f)
        except (OSError, json.JSONDecodeError) as e:
            raise SystemExit(f"[Cassette] cannot read {self.path}: {e}")
        if data.get("schema") != SCHEMA_VERSION:
            raise SystemExit(
                f"[Cassette] unsupported schema in {self.path} "
                f"(got {data.get('schema')!r}, want {SCHEMA_VERSION})"
            )
        self.note = data.get("note")
        if data.get("status") == "placeholder":
            lines = [
                "",
                "=" * 72,
                "  [Cassette] PLAYING A PLACEHOLDER CASSETTE (not a capture)",
                f"  {self.path}",
                "",
                "  The assistant text and tool arguments are illustrative.",
                "  Every side effect (MCP servers, canary file, exfil",
                "  listener) still runs live. To record a real capture with",
                "  any OpenAI-compatible model, see cassettes/README.md",
            ]
            if self.note:
                lines.append("")
                lines.append(f"  {self.note}")
            lines.append("=" * 72)
            print("\n".join(lines) + "\n")
        self.turns = data.get("turns") or []
        if not self.turns:
            raise SystemExit(f"[Cassette] {self.path} contains no turns")
        if data.get("model") and not self.model:
            self.model = data["model"]

    def complete(self, create, **kwargs):
        if self.mode == "record":
            response = create(**kwargs)
            self.turns.append(_serialize(response))
            return response
        if self._cursor >= len(self.turns):
            raise SystemExit(
                f"\n[Cassette] exhausted: the agent asked for turn "
                f"{self._cursor + 1} but {self.path} stores {len(self.turns)}. "
                "Re-record with --record using the same servers and prompt."
            )
        turn = self.turns[self._cursor]
        self._cursor += 1
        return _build(turn)

    def finalize(self):
        parent = os.path.dirname(self.path)
        if parent:
            os.makedirs(parent, exist_ok=True)
        data = {
            "schema": SCHEMA_VERSION,
            "status": "recorded",
            "lab": self.lab,
            "model": self.model,
            "endpoint": self.endpoint,
            "recorded_at": datetime.now(timezone.utc).isoformat(),
            "turns": self.turns,
        }
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
            f.write("\n")
        print(f"[Cassette] recorded {len(self.turns)} turn(s) to {self.path}")


def placeholder(path, lab, model, endpoint, note, turns):
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    data = {
        "schema": SCHEMA_VERSION,
        "status": "placeholder",
        "lab": lab,
        "model": model,
        "endpoint": endpoint,
        "recorded_at": None,
        "note": note,
        "turns": turns,
    }
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
        f.write("\n")
