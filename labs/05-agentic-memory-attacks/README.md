# Lab 05: Agentic Memory Attacks

Four attacks against **AssistantOS**, a purpose-built minimal agentic
framework with persistent memory, sub-agents, and long conversations:
external memory poisoning, conversational memory poisoning, cross-agent
trust exploitation, and context-window overflow. No cloud APIs, no internet
required.

Model class: **Model-dependent.** Every attack asks a local LLM to do
something it should not; the expected success rates below are measured on
instruction-tuned 7B-class models and vary by model.

Status: **Complete.**

Difficulty: Advanced. Labs 01 to 04 recommended (not required); 45 to 90
minutes.

---

## Overview

The target is `assistantos/`: an orchestrator that loads a persistent JSON
memory store into its system prompt at every session start, a researcher
sub-agent that fetches documents, a web tool that makes real HTTP requests
for non-fixture URLs, and a sandbox file tool. Memory entries are injected
verbatim into the system prompt, which is the keystone: anything that gets
written into the store is read back as instructions.

The four attacks exploit the three properties that make agents useful:

| Attack | Property abused | Real-world analogue | Expected success |
|---|---|---|---|
| 1, External memory poisoning | Memory persists across sessions | Persistent XSS stored in a database | 85 to 95 % |
| 2, Conversational memory poisoning | Agents write to their own memory | Stored XSS via a form submission | 55 to 75 % |
| 3, Cross-agent trust | Sub-agent results are trusted | Server-side request forgery | 60 to 80 % |
| 4, Context window overflow | Safety rules decay at context depth | Drowning a contract clause in fine print | near 0 % at shallow fill, 40 to 70 % at 75 to 85 % fill |

```
Attack 1: attacker writes memory.json  ->  next session loads it into the
         system prompt  ->  model calls web_tool_fetch to the exfil
         endpoint before every response  ->  one write, infinite persistence

Attack 2: 6-turn conversation  ->  agent stores a "compliance preference"
         whose value is an exfil instruction  ->  next session complies

Attack 3: poisoned web fixture  ->  researcher returns it with a
         [SYSTEM NOTE] block  ->  orchestrator executes it as trusted output

Attack 4: 15-20 benign padding turns  ->  system prompt sits deep in
         context  ->  constraints the model enforced at turn 1 no longer hold
```

Per-attack framework mapping (kept from the lab's own assessment):

| Attack | OWASP LLM 2025 | OWASP Agentic Top 10 | MITRE ATLAS |
|---|---|---|---|
| 1 | LLM04: Data/Model Poisoning | ASI06 Memory and Context Poisoning | AML.T0043 |
| 2 | LLM01: Prompt Injection | ASI06 Memory and Context Poisoning | AML.T0051 |
| 3 | LLM01: Prompt Injection | ASI07 Insecure Inter-Agent Communication | AML.T0054 |
| 4 | LLM01: Prompt Injection | ASI01 Agent Goal Hijack | AML.T0051 |

### Files

| File | Description |
|------|-------------|
| `assistantos/orchestrator.py` | Top-level agent loop (the main target) |
| `assistantos/memory_store.py` | Persistent JSON memory (the keystone) |
| `assistantos/session.py` | Session lifecycle, episodic save |
| `assistantos/agents/researcher.py` | Research sub-agent (Attack 3 vector) |
| `tools/web_tool.py` | Web fetch (real HTTP for non-fixture URLs; the exfil channel) |
| `tools/file_tool.py` | Sandbox file access (intentionally permissive) |
| `memory/memory.json` | Persistent memory store (created by `make seed`) |
| `fixtures/api_docs_clean.txt`, `fixtures/api_docs_poisoned.txt` | Legitimate and compromised fixtures for Attack 3 |
| `attack1_external_memory_poison.py` | Attack 1 |
| `attack2_conversational_memory_poison.py` | Attack 2 |
| `attack3_cross_agent_trust.py` | Attack 3 |
| `attack4_context_overflow.py` | Attack 4 |
| `attack_chain.py` | Multi-stage chain: all four in sequence |
| `hardened_orchestrator.py` | Orchestrator with all five defense layers enabled |
| `defenses/` | One file per layer: `memory_integrity.py` (HMAC), `memory_source_guard.py` (value blocklist), `agent_message_sandbox.py` (sub-agent fencing), `context_freshness.py` (prompt re-injection), `audit_log.py` (append-only log) |
| `seed.py` | Seeds `memory.json` with clean baseline entries |
| `exfil_server.py` | Attacker receiver at `localhost:9999`; also the single definition of the lab flag |
| `verify_setup.py`, `measure.py`, `Makefile` | Pre-flight checks, n-iteration measurement, all targets |

---

## The story

Persistent memory is what separates a product agent from a chatbot, and it
is also what this lab attacks. The architecture comes from the generative
agents line of work (Park et al., 2023), where agents maintain long-lived
memory stores that are re-read into context each session: the same design
that shipped as user-facing memory in commercial assistants in 2024 and 2025.
The attack side has been known since Perez and Ribeiro's "Ignore Previous
Prompt" workshop paper (NeurIPS 2022), which showed that stored instructions
survive and execute long after the user who planted them is gone, and
Liu et al.'s "Lost in the Middle" (TACL 2024) showed that instructions
buried deep in long contexts are progressively ignored. Memory poisoning
is that result applied to a system that writes for you: the agent's own
"remember this" feature is the injection primitive, and persistence is the
payload.

This lab builds all four variants of that primitive against one shared
target, so you can compare what each persistence property leaks and which
defense layer closes which hole. The full write-up is in
[blog-post.md](blog-post.md).

---

## Goal

Capture the flag `AGENTICGOAT{05_memory-poisoning}`.

The flag is defined in `exfil_server.py`. The capture signal is
cross-session persistence: after the attacker performs an out-of-band write
to the memory store (Attack 1) or gets the agent itself to store a poisoned
entry (Attack 2), a fresh victim session that the user did not poison makes
the agent call the exfil endpoint on its own before answering. When the
receiver gets that first self-initiated request, it prints the
`FLAG CAPTURED` line.

Capturing it proves the dangerous property of agent memory: one write to the
store becomes an instruction that survives across sessions, fires on
every user interaction, and stays invisible to the user, who sees only
normal answers.

---

## Framework mapping

- OWASP Agentic Top 10: ASI06 Memory and Context Poisoning
- OWASP LLM Top 10: LLM04 Data and Model Poisoning, LLM01 Prompt Injection
- MITRE ATLAS: AML.T0043 Craft Adversarial Data, AML.T0051 Indirect Prompt Injection

---

## Hints

<details><summary>Hint 1</summary>

At session start, the orchestrator builds its system prompt from something
the user never reviews and that anyone with write access to one file can
extend. Find where `memory.json` becomes prompt text in
`assistantos/orchestrator.py`.

</details>

<details><summary>Hint 2</summary>

Only one agent tool can leave the machine, and two of the four attacks need
it while one needs nothing outside the conversation at all. Which tool is
it, and which attack is the one that does not need it?

</details>

<details><summary>Hint 3</summary>

The vulnerable assumption: a memory entry is system-prompt text, and the
writer of the entry is the only trust decision. Layer 1 (HMAC signing of
entries at write time) is the control that makes external poisoning require
the key, not just a path.

</details>

---

## Solution and walkthrough

**Prerequisites:** Python 3.11+, `make`, a local LLM endpoint (Ollama is the
default; LM Studio via `LLM_BASE_URL`) serving `qwen2.5-7b-instruct` or a
comparable instruct model, 8 GB RAM minimum. See [common
prerequisites](../../README.md#prerequisites).

```bash
cd labs/05-agentic-memory-attacks
make setup
source venv/bin/activate
make verify
make seed
```

**Terminal 1: the attacker's receiver** (needed for Attacks 1, 2, and the
chain)

```bash
make exfil
```

**Terminal 2: the attacks**

Attack 1 (the flag run):

```bash
make attack1
```

The script injects a memory entry that mimics a legitimate output-format
preference, then starts a fresh session and asks a benign question. Watch
Terminal 1: when the attack succeeds, the agent calls the web tool with the
exfil URL before answering, Terminal 1 prints the captured query string
(session ID plus a brief conversation summary), and the `FLAG CAPTURED` line
appears. The user-facing response looks completely normal.

Attack 2:

```bash
make reset
make attack2
```

A six-turn conversation in which the user apparently asks the agent to
remember a "compliance preference." The agent writes the entry itself; the
next session loads it and complies.

Attack 3:

```bash
make reset
make attack3
```

The researcher sub-agent is pointed at the poisoned API-docs fixture and
returns it with an embedded `[SYSTEM NOTE]` block. The orchestrator treats
sub-agent output as trusted and executes the injected action.

Attack 4 (no exfil server needed):

```bash
make attack4
```

The script pads the context to several fill ratios (0 %, 75 %, 85 %) with
benign turns and re-asks a constrained question. Success is measured as the
fraction of fills where the model drops the constraint the system prompt set
at turn 1. Expect a degradation curve, not a binary result.

The multi-stage chain:

```bash
make reset
make attack-chain
```

Runs all four in sequence and reports which stages fired.

Optional: `make measure attack=1 n=20` for per-attack success rates,
`make measure-all-stats` for all four, and `make compare attack=1` (or
`attack=3`) for a vulnerable versus hardened side-by-side.

---

## Defense

`hardened_orchestrator.py` enables all five layers, one file each in
`defenses/`:

| Layer | File | Stops |
|---|---|---|
| 1, Memory integrity | `memory_integrity.py` | Attack 1 (completely: unsigned entries are rejected) |
| 2, Source guard | `memory_source_guard.py` | Attack 2 (significantly: values with URLs and imperative framing are blocked) |
| 3, Agent sandbox | `agent_message_sandbox.py` | Attack 3 (significantly: sub-agent results are fenced and instruction patterns stripped) |
| 4, Context freshness | `context_freshness.py` | Attack 4 (largely: the system prompt is re-injected every N turns) |
| 5, Audit log | `audit_log.py` | All attacks (detection: append-only log of every tool call with anomaly flags) |

Run each hardened variant:

```bash
make hardened-attack1   # Layer 1 rejects the unsigned entry; no exfil
make hardened-attack2   # Layer 2 blocks the poisoned write
make hardened-attack3   # Layer 3 fences the sub-agent output
make hardened-attack4   # Layer 4 keeps the constraints recent
```

Expected: Attack 1 dies completely; Attacks 2 and 3 drop from their
vulnerable success rates to low single digits (the fenced output is
reported, not executed); Attack 4's constraint-following stays flat across
fill ratios.

Why the architecture holds: Layer 1 converts "who can write the file" into
"who holds the signing key," which is the only durable fix for external
poisoning because the store itself is appendable by design. Layers 2 and 3
treat memory values and sub-agent output as untrusted input, which is the
rule the vulnerable pipeline never enforced. Layer 4 does not fix attention,
it just keeps the relevant instruction recent. Layer 5 changes nothing
offensively; it makes every attempt observable and forensically replayable.

The five defensive rules, in one line each:

1. Sign memory entries at write time (HMAC, server-side key).
2. Treat memory values as untrusted input and scan every write.
3. Fence every sub-agent result before the orchestrator reads it.
4. Re-inject safety constraints every N turns.
5. Log every tool call, append-only, and alert on anomalies.
