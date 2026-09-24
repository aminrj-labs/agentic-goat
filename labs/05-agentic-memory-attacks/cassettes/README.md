# Cassettes (record/replay)

A cassette records the lab's LLM answers (in call order) as plain JSON so the
attack can be replayed with **no model, no endpoint and no API key**.
Everything else stays live: the memory store on disk, the sandbox files, the
tools and the exfil listener on port 9999. See the module docstring of
`cassette.py` for the file format.

Cassette support is wired into the AssistantOS orchestrator
(`assistantos/orchestrator.py`, via `set_cassette`), so every
`chat.completions.create` call made by the orchestrator and by the
researcher/executor sub-agents (which share the client) is recorded or
replayed. The shipped cassette covers the **Attack 1** flow
(`attack1_external_memory_poison.py`), which is the lab's Goal scenario: an
out-of-band memory write followed by one victim-session query.

The cassette `external-poison.json` shipped with this repo is a **placeholder**
(`"status": "placeholder"`). It is not a capture: its two assistant turns are
illustrative, and replaying it prints a loud warning. Replay still exercises
the real side effects: the malicious entry is really written to
`memory/memory.json`, really injected into the system prompt, the
`web_tool_fetch` call really hits the exfil listener, and `file_tool_list`
really reads the sandbox. Because the listener reveals the flag on its first
capture, a replay against a running `exfil_server.py` will print the
`FLAG CAPTURED` line even with this placeholder (the captured `data` value is
illustrative, not a real conversation). Record a real capture as below to get
the model's genuine behavior.

The `--record`/`--replay` flags are wired into `attack1_external_memory_poison.py`
(the Goal scenario). The orchestrator hook is shared, so the other scripts
(`attack2_*`, `attack3_*`, `attack_chain.py`, which drive the same
orchestrator client) can use the same `Cassette` + `set_cassette` pattern;
`attack4_context_overflow.py` uses a separate ad-hoc client and is out of
scope for the shipped cassette.

## Replay (no model needed)

```
python3 exfil_server.py                                  # terminal 1
python3 attack1_external_memory_poison.py \
  --replay cassettes/external-poison.json                # terminal 2
```

Expected: the malicious memory entry is injected and shown in the system
prompt, the agent's (replayed) turns trigger a live GET to
`localhost:9999/exfil` and a live sandbox listing, and the exfil listener
prints the capture (with the flag line on a fresh listener).

## Record a real capture

Prerequisites: an OpenAI-compatible chat endpoint (for example `ollama serve`
with `qwen2.5-7b-instruct` or a comparable instruct model pulled), the exfil
listener running.

```
export LLM_BASE_URL=http://localhost:11434/v1

python3 exfil_server.py                                  # terminal 1
python3 attack1_external_memory_poison.py \
  --record cassettes/external-poison.json                # terminal 2
```

The run overwrites `cassettes/external-poison.json` with
`"status": "recorded"` (turns = the model's actual tool-call sequence, so a
recorded cassette usually holds more than the two placeholder turns). Commit
the capture (it contains only the synthetic session content). The model must
follow the poisoned memory entry on the recorded run; if it does not, retry or
note the failure in the cassette commit message. A recorded capture is
verified by replaying it (as above) and confirming the exfil listener receives
the self-initiated request.
