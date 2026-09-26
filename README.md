# AgenticGoat

The vulnerable-by-design toolkit for learning agentic AI security by breaking and
defending it. Each lab stages a real attack technique against a purpose-built
vulnerable target, shows it working end to end, and pairs it with the control
that stops it. Self-hostable anywhere, runs on a local model with no API keys,
and mapped scenario-for-scenario to the
[OWASP Top 10 for Agentic Applications](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications/)
and the [OWASP MCP Top 10](https://owasp.org/www-project-mcp-top-10/). From a
single poisoned tool description to a five-stage multi-agent kill chain, every
attack is paired with the defense that stops it.

The labs run on your own machine against a local model. **No cloud APIs, no
API keys, and in a local run no data leaves your laptop.** The Killercoda and
Codespaces tiers run the same code in a sandboxed environment instead.

> **Not an OWASP project.** AgenticGoat is mapped to the OWASP Top 10 for
> Agentic Applications, the OWASP MCP Top 10, and [MITRE ATLAS](https://atlas.mitre.org/)
> so the labs line up with the frameworks people already cite. It is an
> independent, vendor-neutral project and is not sponsored, endorsed, or
> affiliated with OWASP or MITRE.

---

## Agentic and MCP Top 10 crosswalk

The table below is the map. It links every covered risk to the lab that teaches
it, and it states the status of each row honestly. `Planned` rows are the
backlog, marked so the map stays truthful. This table is the shareable artifact:
it is the "when I read ASI03, there is a Goat scenario waiting" crosswalk.

| ASI / MCP | Risk | Lab | Status |
|---|---|---|---|
| ASI01 | Agent Goal Hijack | Indirect prompt injection via tool output and RAG ([Lab 04](./labs/04-rag-security/)) | Complete |
| ASI02 / MCP03 | Tool Misuse and Exploitation, Tool Poisoning | Poisoned tool description to silent file read and exfil ([Lab 01](./labs/01-mcp-tool-poisoning/)); cross-server poisoning ([Lab 06](./labs/06-ASI02-cross-server-mcp-poisoning/)) | Complete |
| ASI02 / MCP03 | Cross-server shadowing | One server's tool result hijacks another server's tool ([Lab 01b](./labs/01b-cross-server-shadowing/)) | Partial |
| ASI03 / MCP01, MCP02, MCP07 | Identity and Privilege Abuse | Over-broad capability, token theft from context, scope creep | Planned |
| ASI04 / MCP04 | Agentic Supply Chain | Container-metadata injection ([Lab 02](./labs/02-docker-dash/)); MCP-registry angle | Partial |
| ASI05 / MCP05 | Unexpected Code Execution | Agent-generated code, command injection through a tool | Planned |
| ASI06 | Memory and Context Poisoning | Persistent memory poisoning, cross-session persistence ([Lab 05](./labs/05-agentic-memory-attacks/)) | Complete |
| ASI07 / MCP10 | Insecure Inter-Agent Communication | Forged A2A message and agent-card spoofing (part of [Lab 07](./labs/07-mcp-to-a2a-kill-chain/)) | Complete |
| ASI08 | Cascading Failures | Blast-radius propagation across an orchestration chain | Planned |
| ASI09 | Human-Agent Trust Exploitation | Agent recommends a harmful action a human approves | Planned |
| ASI10 | Rogue Agents | Persistence after server removal (tail of [Lab 07](./labs/07-mcp-to-a2a-kill-chain/)) | Complete |
| MCP08 | Lack of Audit and Telemetry | Defensive: the kill chain with tool-call logging | Planned |
| MCP09 | Shadow MCP Servers | Unsanctioned server joins, governance control stops it | Planned |
| The chain | Full MCP-to-A2A kill chain | Five stages, one control breaks it ([Lab 07](./labs/07-mcp-to-a2a-kill-chain/), flagship) | Complete |

[Lab 03](./labs/03-red-team-assessment/) is a methodology lab (automated red
teaming with PyRIT-style orchestrators and Promptfoo) rather than a single
mapped scenario. It
exercises several rows of this map against one target and is listed in the lab
table below.

---

## ⚠️ Responsible use — read first

This repository contains **intentionally vulnerable code and working attack
tooling**, published for **education, defensive research, and authorized security
testing only**.

- **Run it in isolation.** Use a local VM or a disposable dev machine. Do **not**
  deploy any component to a shared, staging, or internet-facing host.
- **The targets are deliberately insecure.** They exist to be exploited. Never
  reuse this code, or patterns from it, in production.
- **The "attacker" servers stay local.** Exfil receivers bind to `localhost` and
  the payloads/credentials in the labs are **synthetic** — no real secrets, no
  real people, no real systems.
- **Only attack systems you own or are explicitly authorized to test.** You are
  responsible for how you use these techniques. Using them against systems
  without permission is illegal.

By using this repository you agree to use it lawfully and ethically. See
[LICENSE](./LICENSE) and [CONTRIBUTING.md](./CONTRIBUTING.md).

---

## Who this is for

Security engineers, red/blue teamers, MCP and agent developers, and researchers
who want to *see* how agentic attacks actually work, not just read about them,
and understand the controls that defeat them. Vendor-neutral by design: no lab
routes you to a product, and the scenario that matters most ([Lab 07])
demonstrates the control that breaks the chain, not a tool that sells it.

New to agentic AI security? Read [BEGINNERS.md](./BEGINNERS.md) first: the
terms, the lab pattern, and your first run in plain words.

---

## Labs

| # | Lab | What it demonstrates | Model class | Status |
|---|-----|----------------------|-------------|--------|
| 01 | [MCP Tool Poisoning](./labs/01-mcp-tool-poisoning/) | Hidden instructions in an MCP tool description, silent file read and exfiltration | Model-dependent (replay available) | Complete |
| 01b | [Cross-Server Shadowing](./labs/01b-cross-server-shadowing/) | One MCP server's tool result "shadows" another server's tool to hijack it | Model-dependent | Partial |
| 02 | [DockerDash](./labs/02-docker-dash/) | Prompt injection via Docker image labels, container destruction and inventory exfil | Model-dependent (replay available) | Complete |
| 03 | [Red Team Assessment](./labs/03-red-team-assessment/) | Automated agentic red-teaming with PyRIT-style orchestrators and Promptfoo (crescendo exfil, TAP tool abuse) | Model-dependent (methodology) | Complete |
| 04 | [RAG Security](./labs/04-rag-security/) | Knowledge-base poisoning, indirect prompt injection, cross-tenant data leakage | Model-dependent (replay available) | Complete |
| 05 | [Agentic Memory Attacks](./labs/05-agentic-memory-attacks/) | Persistent memory poisoning, cross-agent trust abuse, context-window overflow | Model-dependent (replay available) | Complete |
| 06 | [Cross-Server MCP Poisoning](./labs/06-ASI02-cross-server-mcp-poisoning/) | One malicious MCP server steers the agent into abusing a second, trusted server | Model-dependent (replay available) | Complete |
| 07 | [MCP to A2A Kill Chain](./labs/07-mcp-to-a2a-kill-chain/) | **Flagship.** Five-stage chain across the MCP to A2A trust boundary: tool poisoning, rogue A2A registration, routing hijack, lateral movement, persistence after server removal. Each of three controls provably breaks it at a specific stage. | Model-independent | Complete |

---

## How a lab works

Every lab has the same four-part shape, so one lab teaches you to read them all:

1. **A canary is planted.** A synthetic secret, a flag such as `AGENTICGOAT{...}`, lives inside the vulnerable target: a note, an env var, a memory entry.
2. **The attack runs.** A poisoned tool description, document, memory entry or message tricks the agent into reading the canary and sending it to an attacker listener on `localhost`.
3. **Success is observable.** The attack succeeded if and only if the canary reaches the listener. A benign run never delivers it.
4. **A control stops it.** The lab's defense is switched on and the same attack is rerun, and it fails.

Two run modes cover the rest. **Live** points the agent at your own local model (Ollama or LM Studio). **Replay** plays back a cassette of the model's recorded tool calls, so the side effects run without a model. The cassettes shipped today are labelled `"status": "placeholder"`: replay exercises the live plumbing, but the flag is not delivered until a real capture is recorded. Lab 07 is model-independent and needs neither.

## Try it in your browser

Zero install. No GPU. No API keys. Three tiers, from "watch in 30 seconds" to
"run it yourself."

| Tier | What | How |
|---|---|---|
| **F0, Watch** | Side-by-side attack and defended traces from Lab 07, annotated with why each step happened. | [**Static trace viewer**](./docs/index.html) -- no sign-in, no sandbox |
| **F1, Do** | Hands-on Killercoda scenarios: the kill chain (live deterministic) and tool poisoning (replay against live plumbing). | [**Lab 07: MCP to A2A Kill Chain**](https://killercoda.com/aminrj-labs/course/agentic-goat/07-kill-chain) -- five stages, HR data exfiltrated, then broken by controls |
| | | [**Lab 01: MCP Tool Poisoning**](https://killercoda.com/aminrj-labs/course/agentic-goat/01-tool-poisoning) -- poisoned tool description, silent file read, exfiltration |
| **F2, Prove** | Point your own MCP client or local LLM at the real vulnerable servers. | "Open in Codespaces" badge below, then `cd labs/... && make attack` |

> **Relevance guarantee.** The vulnerable components (MCP servers, exfil receivers,
> canaries) are the real, unmodified lab code. For model-dependent labs, only the
> model's inference is pre-recorded in a cassette, and the exploit's side effects are
> produced live. The cassettes shipped today are labelled `"status": "placeholder"`:
> replay exercises the live plumbing, but it is not a capture, so the canary flag is
> not delivered until a real capture is recorded. F2 lets anyone reproduce the whole
> thing against their own real model.

[![Open in Codespaces](https://img.shields.io/badge/Open_in_Codespaces-0078D6?style=flat&logo=visualstudiocode&logoColor=white)](https://codespaces.new/aminrj-labs/agentic-goat?devcontainer=.devcontainer/devcontainer.json)

---

## Attack surface coverage

```
User  →  Agent  →  MCP Tools  →  Memory / Context  →  Other Agents (A2A)  →  External Systems

Lab 01  ─────────── MCP tool descriptions (protocol layer)
Lab 01b ─────────── Cross-server tool shadowing
Lab 02  ─────────────────────── Container metadata (supply chain)
Lab 03  ──── Agent pipeline (automated assessment)
Lab 04  ─────────────────────────────────── RAG / vector store
Lab 05  ─────────────────────── Agent memory + multi-agent trust
Lab 06  ─────────── Shared tool context across trusted MCP servers
Lab 07  ─────────── MCP → A2A trust boundary (multi-stage kill chain)
```

---

## Prerequisites

Common to every lab:

- **Python 3.11+**
- A **local OpenAI-compatible LLM endpoint** with tool/function calling. Either:
  - **[Ollama](https://ollama.com/)** (default): serves on `http://localhost:11434/v1`
  - **[LM Studio](https://lmstudio.ai/)**: serves on `http://localhost:1234/v1`
- **Node.js 18+** (labs that use npm-based MCP servers or Promptfoo)

A capable instruction model with reliable function calling. `qwen2.5-7b-instruct`
is the baseline; some attacks only comply with a stronger model. Larger models
generally reproduce the attacks more reliably.

Model-independent labs (Lab 07 today) need none of this. They run live and
deterministic on the Python standard library, with no model and no download.

### Selecting your backend

Every agent reads its endpoint from environment variables, so you can point a lab
at either backend without editing code:

```bash
# Ollama (default: nothing to set)
# LM Studio:
export LLM_BASE_URL="http://localhost:1234/v1"
export MODEL="qwen2.5-7b-instruct"   # or the model id your backend exposes
```

---

## Quick start (fastest working attack)

Lab 06 has the smoothest end-to-end run, two terminals and a Makefile.

```bash
cd labs/06-ASI02-cross-server-mcp-poisoning
make setup            # create venv + install deps
source venv/bin/activate
make verify           # check your local LLM + function calling
make seed             # plant synthetic "sensitive" notes in the victim server

# Terminal 1: attacker's receiver
make exfil

# Terminal 2: vulnerable agent
make attack
```

You'll watch the agent answer a harmless weather question while silently leaking
the victim server's notes to the attacker's listener in Terminal 1.

New to the topic? **Lab 01** is the gentlest introduction to the core primitive
(a poisoned tool description), start there for the "why," then come back here for
the "how far it goes."

Want to run the flagship with zero setup, no model, and no GPU? **Lab 07** runs
end to end on the standard library alone.

```bash
cd labs/07-mcp-to-a2a-kill-chain
make run        # undefended: five stages, HR data exfiltrated (exit 1)
make defended   # all controls on: chain breaks at stage 2 (exit 0)
make test       # proves the above
```

---

## Repository layout

```
README.md              # paragraph + crosswalk + "Try it in your browser"
BEGINNERS.md           # plain-words intro: terms, the lab pattern, first run
LINEAGE.md             # seeded from mcp-attack-labs, divergence policy
CONTRIBUTING.md        # requires the scenario contract, a model class, honest status
INVENTORY.md           # v1 baseline (entry points, deps, success signals)
LICENSE
labs/
  00-template/         # the scenario contract as a fill-in scaffold
  01-.../              # each lab: README + runnable code + defenses + write-up
  ...                  # model-dependent labs also carry cassettes/ for replay
killercoda/            # zero-install front door (Lab 07, Lab 01)
.devcontainer/         # "Open in Codespaces"
docs/                  # GitHub Pages: the static trace viewer
```

---

## Adding a lab

Copy `labs/00-template/`, fill in the README against the scenario contract in
`CONTRIBUTING.md`, add your code and its defense, declare the model class, and
append a row to the crosswalk and the table above with an honest status.

---

## License

[MIT](./LICENSE): for educational and authorized-testing use. The responsible-use
expectations above are part of using this project.
