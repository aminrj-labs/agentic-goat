# Lab 07: MCP to A2A Kill Chain

The flagship. A single poisoned MCP tool description is the entry point to a
five-stage kill chain that crosses from the MCP tool layer into an
agent-to-agent (A2A) trust graph, exfiltrates data the agent was never
authorised to reach, and survives removal of the malicious server that
started it. Each of three controls provably breaks the same chain at a
specific stage. Runs on the Python standard library: `git clone`, then
`make run`. No model, no cloud, no credentials.

Model class: **Model-independent.** Every stage is deterministic
control-plane logic; a model is never required. Stage 1 can optionally be
driven against a real local LLM with `--llm` to show the entry point working
against a live model, but the other four stages are identical either way.

Status: **Complete.**

---

## Overview

The entry point is the tool-description poisoning primitive from
[Lab 01](../01-mcp-tool-poisoning/) and [Lab 06](../06-ASI02-cross-server-mcp-poisoning/):
a poisoned MCP tool description instructs the host agent to register and
prefer a "helper" peer. From there the chain is A2A, and each stage is a real
operation on a minimal, local A2A layer that ships with this lab (Agent Cards
with signing and verification, a discovery registry, and a skill router
carrying the authorization and blast-radius controls), modelled on the A2A
protocol (v1.0, Linux Foundation, April 2026,
<https://a2a-protocol.org>). It is not the real SDK; it is
a deliberately small stand-in that reproduces the parts the attack and its
defences actually turn on (see [`a2a/`](a2a/)).

| Stage | Name | What happens | ASI |
|---|---|---|---|
| 1 | Tool description poisoning | A poisoned MCP tool description instructs the host to register and prefer a "helper" peer | ASI02 / ASI01 |
| 2 | Rogue A2A agent registration | The attacker registers a rogue agent as a discoverable peer | ASI07 |
| 3 | Routing hijack | The rogue advertises overlapping skills; the router sends legitimate tasks to it | ASI01 |
| 4 | Lateral movement + exfiltration | The rogue uses its trusted position to invoke a sensitive skill and exfiltrate | ASI07 / ASI08 |
| 5 | Persistence after server removal | The malicious MCP server is removed; the rogue registration persists and stays routable | ASI06 |

Undefended, all five stages succeed and HR data reaches the exfil sink:

```
Stage 1 — Tool description poisoning      attacker: followed hidden instruction
Stage 2 — Rogue A2A agent registration    attacker: registered 'summariser-helper' (unverified)
Stage 3 — Routing hijack                  attacker: routed 'document.summarise' -> 'summariser-helper'
Stage 4 — Lateral movement + exfiltration attacker: rogue invoked 'hr.read' -> exfiltrated: EMP-4471 ...
Stage 5 — Persistence after server removal attacker: rogue registration persists and remains routable
RESULT: chain completed — HR data exfiltrated.   (exit code 1)
```

The point of the lab is not the attack: it is that the *same* attack code,
run with a control switched on, breaks at a predictable place. That is the
question a defender is actually asking: if I turn this on, what stops?

| Control | CLI | Breaks at | Why |
|---|---|---|---|
| Verify the card, authenticate the channel | `--control card` | Stage 2 | The rogue can mint a well-formed card but cannot sign it against the trust anchor, so registration is refused; an unregistered peer cannot route, so stages 3 to 5 collapse too |
| Authorize the action, not just the caller | `--control authz` | Stage 4 | Registration and routing stay open, but the rogue is in nobody's allow-list, so the sensitive skill is denied. This is the control that survives an agent being genuinely trusted but overreaching, not merely impersonated |
| Contain the blast radius | `--control blast` | Stage 4 | The high-stakes skill pauses for human confirmation instead of executing on the rogue's say-so. The circuit breaker (threshold 3) is a backstop against delegation bursts: this chain makes only two routes, so the breaker never trips here and human-in-the-loop is what breaks the chain |
| All three | `--defended` | Stage 2 | Defence in depth; the earliest control wins, the rest are backstops |

```bash
make card       # RESULT: chain broken at Stage 2
make authz      # RESULT: chain broken at Stage 4
make blast      # RESULT: chain broken at Stage 4
```

Being explicit, because the honesty is the point of a security lab:

- **The A2A trust mechanics are real logic**, not narration. Card signing
  and verification, the registry's accept/reject decision, skill routing, the
  authorization allow-list, the circuit breaker, and on-disk persistence are
  all executable and independently testable
  ([`test_chain.py`](test_chain.py)).
- **Signing uses HMAC, not PKI/JWS.** A stand-in with the one property that
  matters: a signature either chains to a key you hold or it does not.
  Swapping in real asymmetric signatures does not change any stage's
  outcome.
- **Stage 1's injection is deterministic by default.** That a model *will*
  obey an instruction hidden in a tool description is demonstrated against a
  real local LLM in Labs 01 and 06. Lab 07's contribution is what a
  successful injection *leads to*: the A2A propagation, which is
  deterministic control-plane logic.

### Files

| Path | What |
|------|------|
| `a2a/cards.py` | Agent Cards + signing/verification (Control 1) |
| `a2a/registry.py` | Discovery registry + persistence (stages 2, 5) |
| `a2a/router.py` | Skill router + authorization + blast radius (Controls 2, 3) |
| `mcp_entry.py` | Poisoned tool description + agent brain (stage 1) |
| `killchain.py` | The five stages executed against the A2A layer; also the single definition of the lab flag |
| `defenses.py` | The three controls as one toggleable config |
| `run_chain.py` | CLI transcript runner |
| `test_chain.py` | Executable proof of every claim above |
| `state/` | Runtime artifacts: `registry.json`, `exfil.json` (the exfil sink; created on first run, removed by `make clean`) |

---

## The story

Agent-to-agent communication is the new perimeter, and the attack surface
arrived with the protocol. The A2A specification (version 1.0, Linux
Foundation, April 2026, <https://a2a-protocol.org>) is built on Agent Cards:
a peer publishes a card, another peer discovers it through a registry, and a
router sends work to whichever peer advertises the right skill. Unit 42's
A2A session-smuggling write-up showed what that architecture means in
practice: the edge between agents is where trust breaks first, because a peer
you did not vet becomes a route you did not choose.

This lab takes that edge and drives a full kill chain across it, starting
from the only entry point you already know: a poisoned tool description. It
is the executable form of Chapter 9 of the author's *Agentic AI Security*
manuscript ("Inter-Agent Communication and the A2A Kill Chain"): the same
chain, the same controls, each control verified against the stage it is
supposed to hold. Stage 5 builds on the persistent-state poisoning theme from
[Lab 05](../05-agentic-memory-attacks/).

---

## Goal

Capture the flag `AGENTICGOAT{07_kill-chain}`.

The flag is defined in `killchain.py`. It is captured only at the end of the
chain: it is written to the exfil sink (`state/exfil.json`) in the same event
that ships the HR record out, during stage 4 lateral movement, and only in
the undefended run. After `make run`,

```bash
cat state/exfil.json
```

shows the HR record and the flag side by side; the chain is compromised and
`make run` exits 1. In every configured run with a control on (`make
defended`, `make card`, `make authz`, `make blast`), the sink stays empty
and the flag is never revealed; the chain breaks and the exit code is 0.

Capturing it proves the full distance: from one poisoned tool description to
data the host agent was never authorised to read, moved by a peer that
survives the removal of the server that introduced it.

---

## Framework mapping

| Concern | OWASP Agentic | OWASP MCP | MITRE ATLAS |
|---|---|---|---|
| Tool description poisoning (entry) | ASI02 Tool Misuse and Exploitation | MCP03 Tool Poisoning | AML.T0051 Indirect Prompt Injection |
| Rogue agent registration | ASI07 Insecure Inter-Agent Communication | n/a | n/a |
| Routing hijack | ASI01 Agent Goal Hijack | n/a | n/a |
| Lateral movement + exfiltration | ASI07 Insecure Inter-Agent Communication, ASI08 Cascading Failures | n/a | n/a |
| Persistence after server removal | ASI06 Memory and Context Poisoning | n/a | AML.T0054 |

---

## Hints

<details><summary>Hint 1</summary>

The chain starts in a tool description (the Lab 01 primitive), but the harm
happens where the agent talks to other agents. Which stage is the first trust
decision that could have been made differently, and what input does it get
that no one checked?

</details>

<details><summary>Hint 2</summary>

Three controls, three different break points. Run each control alone and
note the stage where "chain broken" appears: `card` breaks earlier than
`authz`, and `blast` breaks at the same stage as `authz` for a different
reason. Say which decision each one is actually enforcing.

</details>

<details><summary>Hint 3</summary>

Stage 5 is the trap: removing the malicious MCP server is not incident
response. Reload the registry from `state/registry.json` and ask who is
still registered. Persistence outlives the process that created it.

</details>

---

## Solution and walkthrough

**Prerequisites:** Python 3 (standard library only). `pytest` for `make
test`. No model, no API keys, no network.

```bash
cd labs/07-mcp-to-a2a-kill-chain
```

**The attack (undefended)**

```bash
make run
```

All five stages succeed, the transcript reports `RESULT: chain completed`,
the process exits 1, and `state/exfil.json` now holds the HR record plus the
flag (the capture you verify with the command in Goal).

**The defense, control by control**

```bash
make defended   # all controls: broken at stage 2, exit 0
make card       # broken at stage 2
make authz      # broken at stage 4
make blast      # broken at stage 4
```

After each, `cat state/exfil.json` (or its absence of entries) confirms the
sink never received data. Exit codes carry the verdict for scripting and CI:
0 means the chain broke, 1 means compromise reached.

**The proof**

```bash
make test
```

`test_chain.py` pins the claims: undefended completes all five stages and
exfiltrates; each individual control breaks its own stage; with all controls
the chain breaks at the first trust decision; and stage 1 lands in every
configuration (it is the primitive; the controls act later).

**Optional: a live model at the entry point**

```bash
python3 run_chain.py --llm
```

`--llm` drives stage 1 against a real endpoint (`LLM_BASE_URL`,
`LLM_MODEL`; Ollama default) so you can watch a real model follow the hidden
instruction. Stages 2 to 5 are identical with or without it.

Reading the run, honestly:

- The A2A trust mechanics are real logic, not narration: signing,
  verification, registration, routing, allow-listing, the circuit breaker,
  and persistence are all exercised for real.
- Signing is HMAC, not PKI. The property that matters (signatures chain to a
  key you hold, or they don't) is preserved with zero crypto dependencies.
- Stage 1 is deterministic by default because "a model obeys a hidden
  instruction" is already proven against live models in Labs 01 and 06;
  `--llm` reconnects that proof when you want it.

---

## Defense

The three controls, and why each holds:

- **Verify the card, authenticate the channel (`--control card`).** A rogue
  can mint a well-formed card but cannot sign it against the trust anchor.
  Registration is refused, the rogue never becomes routable, and stages 3 to
  5 collapse with it. This stops impostors.
- **Authorize the action, not just the caller (`--control authz`).** Least
  privilege at the skill level: only `hr-agent` may read HR, only
  `doc-assistant` may summarise. The rogue, even if genuinely registered and
  routed to, is in nobody's allow-list. This is the control that survives an
  agent being trusted-but-overreaching, not merely impersonated.
- **Contain the blast radius (`--control blast`).** High-stakes skills pause
  for human confirmation, and a burst of delegations from one caller trips a
  circuit breaker. Even when registration and routing both succeed, the
  sensitive action does not execute, and a cascade that starts anyway is cut
  off at a threshold instead of propagating. In this five-stage chain the
  breaker never trips (two routes, threshold 3): it is the backstop, and
  human-in-the-loop is what stops this chain.
- **Defence in depth (`--defended`).** Run all three and the chain breaks at
  the earliest trust decision (stage 2) with the others as backstops.

The residual risk, stated flat: card verification stops impostors, action
authorization stops an authenticated agent overreaching, and blast-radius
controls limit a cascade that starts anyway. None of this fixes identity
provenance over time: an agent whose identity was legitimate yesterday and is
subverted today still presents a valid-looking card. Decentralised-identity
and Know-Your-Agent approaches are still early. The honest position in 2026:
you can make the inter-agent edge much harder to abuse and much easier to
see; you cannot yet make agent identity self-proving over its lifetime.
Instrument the edge accordingly.
