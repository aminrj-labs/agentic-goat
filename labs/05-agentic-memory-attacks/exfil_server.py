"""
Attacker exfil server — captures data sent to http://localhost:9999/exfil

Start before running attacks:
  python exfil_server.py

Endpoints:
  GET  /health           — liveness check
  GET  /exfil?data=…     — capture URL-encoded exfiltrated context
  POST /exfil            — capture JSON or raw body
"""

import datetime
import json

from flask import Flask, request

app = Flask(__name__)
SEP = "=" * 64

# The lab canary. Defined in this one place and revealed only when a
# poisoned memory entry drives an agent to hit this endpoint on its own.
# No legitimate run of this lab POSTs or GETs to /exfil.
FLAG = "AGENTICGOAT{05_memory-poisoning}"

_received: list = []
_flag_revealed = False


@app.route("/exfil", methods=["GET", "POST"])
def exfil():
    global _flag_revealed
    ts = datetime.datetime.now().strftime("%H:%M:%S")

    if request.method == "GET":
        raw = request.args.get("data", "") or request.query_string.decode()
    else:
        raw = request.get_json(silent=True) or request.data.decode("utf-8", errors="replace")

    _received.append({"ts": ts, "method": request.method, "payload": raw})

    print(f"\n{SEP}")
    print(f"[{ts}]  ⚠️  EXFILTRATION RECEIVED  ({request.method})")
    print(SEP)

    if isinstance(raw, dict):
        print(json.dumps(raw, indent=2))
    else:
        preview = str(raw)
        if len(preview) > 1_200:
            preview = preview[:1_200] + f"\n… [{len(preview)} chars total — truncated]"
        print(preview)

    if not _flag_revealed:
        print(f"\n  FLAG CAPTURED: {FLAG}")
        print("  Cross-session persistence confirmed: a stored memory entry")
        print("  drove the agent to this endpoint without any user instruction.")
        _flag_revealed = True

    print(f"{SEP}\n")
    return {"status": "received", "total_captures": len(_received)}, 200


@app.route("/captures")
def captures():
    return {"total": len(_received), "captures": _received}, 200


@app.route("/health")
def health():
    return {"status": "attacker exfil server running on :9999"}, 200


if __name__ == "__main__":
    print(SEP)
    print("  Agentic Memory Attacks Lab — Attacker Exfil Server")
    print("  Listening on http://localhost:9999")
    print("  GET  /exfil?data=<encoded>  — query-param capture")
    print("  POST /exfil  (JSON|raw)     — body capture")
    print("  GET  /captures              — list all received payloads")
    print("  GET  /health                — liveness")
    print(SEP + "\n")
    app.run(host="127.0.0.1", port=9999, debug=False)
