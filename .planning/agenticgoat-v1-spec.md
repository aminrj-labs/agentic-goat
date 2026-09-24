# AgenticGoat v1: build spec for a coding agent

Create AgenticGoat as a new repository seeded from `aminrj-labs/mcp-attack-labs`, then ship its first public version. `mcp-attack-labs` is left untouched and continues as the upstream lab bench; AgenticGoat diverges from here.

Date: 23 September 2026 (revised)
Owner: Amine (Molntek)
Audience: a coding agent executing this milestone. This document is directive, not advisory. Where it says "must," treat it as a gate. Where a decision is left open, stop and ask rather than guessing.

Revision note: this version changes the repo model from an in-place rename to a clone-and-diverge, and replaces the front-door section with a researched design. Sections 2, 5, 6, and 7 are the ones that changed most.

---

## 0. Mission and boundaries

`mcp-attack-labs` is a set of seven locally-reproducible, MIT-licensed, defense-paired security labs for MCP and agentic AI, mapped to the OWASP Agentic and MCP Top 10s. It works, and it stays exactly as it is. AgenticGoat is a **new, separate repository**, seeded from a clone of it, that becomes the packaged, framework-mapped, browser-runnable distribution. This milestone does three things, in this order:

1. Publish the ASI/MCP crosswalk table as the README and as a per-lab header block.
2. Rewrite the seven labs to one fixed scenario contract, adding a named capture flag and progressive hints to each.
3. Build a zero-install browser front door (the priority piece for adoption).

Everything here is packaging, documentation, and deterministic reproduction of behavior that already exists in the labs. No new offensive capability is in scope. Do not author new exploit payloads, do not broaden what any lab can reach, and do not change the observable behavior of any existing attack. Adding a record-and-replay affordance (Section 6) is permitted because it reproduces an existing attack deterministically for demonstration; it does not create new capability.

This is educational, defensive security tooling in the established "goat" genre (WebGoat, Kubernetes Goat, Juice Shop). Every lab pairs an attack with the control that stops it, and that pairing is preserved everywhere.

---

## 1. Binding scope

### 1.1 Ship in v1

- A new `agentic-goat` repository, seeded from a pinned clone of `mcp-attack-labs`, with lineage recorded (Section 2).
- A README whose centrepiece is the ASI/MCP crosswalk table (Section 3).
- All seven labs conformed to the scenario contract (Section 4), each with a named flag and collapsed progressive hints.
- A reusable `labs/00-template/` encoding the contract for contributors.
- A per-lab model classification and, for model-dependent labs, a deterministic record-and-replay path (Section 6).
- The front door (Section 5): the two flagship labs runnable in a browser with no local install and no GPU, plus a static read-only trace viewer.
- Responsible-use notice, license, and synthetic-only guarantees carried forward unchanged (Section 8).

### 1.2 Do NOT build in v1

Later milestones. Building any of them now is a scope violation, even if it seems cheap. If you finish early, stop and report.

- Any new attack lab (ASI03 identity, ASI08 cascading failures, ASI09 human-trust, MCP08/MCP09 defensive). The crosswalk lists them as planned; you do not implement them.
- The Kubernetes / Helm tier.
- A `--ctf` flag-export mode or CTFd integration.
- Generalizing `--defended` into an L0/L1/L2 ladder across all labs. Lab 07 keeps its existing flags as-is.
- Book cross-references, newsletter, or site content.
- Any always-on service that Amine has to operate and pay for. The front door uses hosts the learner supplies (Killercoda, Codespaces) and static pages; you do not stand up a model proxy or a backend Amine must run (Section 5.4 explains why).
- A bespoke web UI or dashboard. The README, the docs, and the static trace viewer are the surface.

If a change is not clearly one of the three moves in 1.1, it is out of scope.

---

## 2. Pre-flight and repo creation (clone-and-diverge)

Do this first. Stop if step 1 is unconfirmed.

1. Confirm the target name and homes are reserved and intended by Amine:
   - GitHub repo for the new project (proposed `aminrj-labs/agentic-goat`).
   - Any domain the static viewer will use (for example `agenticgoat.dev`), if used.
   If unconfirmed, stop and ask. Do not create against an unverified name.
2. Seed the new repo from `mcp-attack-labs`:
   - Clone `mcp-attack-labs` and record the exact source commit SHA.
   - Create the new `agentic-goat` repo and push the clone to it, **carrying git history** so authorship and timeline are preserved.
   - Add `LINEAGE.md` at the root: "AgenticGoat was seeded from aminrj-labs/mcp-attack-labs at commit `<SHA>` on `<date>`. The two projects diverge from here. mcp-attack-labs remains the upstream raw lab bench; AgenticGoat is the packaged, framework-mapped, browser-runnable distribution. Cross-pollination between them is manual."
3. Leave `mcp-attack-labs` untouched in this milestone. Do not rename it, do not open PRs against it, do not add redirects. A one-line pointer may be added to its README **only if Amine asks**, and it must not imply the bench is deprecated.
4. Take an inventory commit in the new repo: record each lab's directory name, entry-point commands, dependencies, and current success signal, so the contract migration in Section 4 can be diffed against a known baseline. You already have the baseline for the two flagship labs:
   - **Lab 07** runs on the Python standard library alone: `make run` (undefended, exits 1, "HR data exfiltrated"), `make defended` (controls on, chain breaks at stage 2, exits 0), `make test`. No model, no download, no credentials. Optional `python3 run_chain.py --llm` drives Stage 1 against a real endpoint; Stages 2 to 5 are deterministic control-plane logic either way.
   - **Lab 01** requires a live, capable model with function calling. Its own note: "gpt-oss-20b works well; small 7B models like qwen2.5-7b often are not susceptible." It uses a real MCP filesystem server (`@modelcontextprotocol/server-filesystem`), `agent.py`, `exfil_server.py` on `localhost:9999`, and a synthetic SSH-key canary file. It cannot run without a model.

This split (one flagship needs no model, the other needs a strong one) drives the entire front-door design.

---

## 3. Move 1: the ASI/MCP crosswalk

### 3.1 What to produce

A single Markdown table mapping the two OWASP frameworks to the labs, with an honest status per row. It becomes the top of the README under a one-paragraph "what this is," and it must stand on its own as a shareable artifact.

Statuses use three literal words: `Complete`, `Partial`, `Planned`. No emoji glyphs in table cells; they render inconsistently on Killercoda and in feed readers.

### 3.2 The mapping (author the table from this)

| ASI / MCP | Risk | Lab | Status |
|---|---|---|---|
| ASI01 | Agent Goal Hijack | Indirect prompt injection via tool output and RAG (Lab 04) | Complete |
| ASI02 / MCP03 | Tool Misuse and Exploitation, Tool Poisoning | Poisoned tool description to silent file read and exfil (Lab 01); cross-server poisoning (Lab 06) | Complete |
| ASI02 / MCP03 | Cross-server shadowing | One server's description hijacks another's tool (Lab 01b) | Partial |
| ASI03 / MCP01, MCP02, MCP07 | Identity and Privilege Abuse | Over-broad capability, token theft from context, scope creep | Planned |
| ASI04 / MCP04 | Agentic Supply Chain | Container-metadata injection (Lab 02); MCP-registry angle | Partial |
| ASI05 / MCP05 | Unexpected Code Execution | Agent-generated code, command injection through a tool | Planned |
| ASI06 | Memory and Context Poisoning | Persistent memory poisoning, cross-session persistence (Lab 05) | Complete |
| ASI07 / MCP10 | Insecure Inter-Agent Communication | Forged A2A message, agent-card spoofing (part of Lab 07) | Complete |
| ASI08 | Cascading Failures | Blast-radius propagation across an orchestration chain | Planned |
| ASI09 | Human-Agent Trust Exploitation | Agent recommends a harmful action a human approves | Planned |
| ASI10 | Rogue Agents | Persistence after server removal (tail of Lab 07) | Complete |
| MCP08 | Lack of Audit and Telemetry | Defensive: the kill chain with tool-call logging | Planned |
| MCP09 | Shadow MCP Servers | Unsanctioned server joins, governance control stops it | Planned |
| The chain | Full MCP-to-A2A kill chain | Five stages, one control breaks it (Lab 07, flagship) | Complete |

Rows marked `Planned` make the map honest; do not implement them here.

### 3.3 Per-lab framework header

Every lab README gains a fixed header block before the contract sections:

```
Framework mapping
- OWASP Agentic Top 10: ASI0x <name>
- OWASP MCP Top 10: MCP0x <name>   (omit if not applicable)
- MITRE ATLAS: <technique id and name, if one applies>
```

### 3.4 Acceptance

- README opens with the paragraph and the crosswalk table.
- Every `Complete` and `Partial` row links to its lab directory.
- Every lab README carries the header block; IDs match the table.
- Framework names link out once, in the README, to the OWASP Top 10 for Agentic Applications, the OWASP MCP Top 10, and MITRE ATLAS, with the non-endorsement line: this project is mapped to those frameworks and is not an OWASP project.

---

## 4. Move 2: the scenario contract

### 4.1 The fixed shape

Rewrite each lab's README to these seven sections, in this order, with these exact headings. Documentation change plus a small verification addition, not a rewrite of the attack code.

1. `## Overview`. One paragraph: the mechanism, plainly.
2. `## The story`. One paragraph tying the lab to a named public incident, so it is memorable and quotable (for example EchoLeak, the Supabase/Cursor tool-poisoning case, the Amazon Q extension, the September 2026 OpenAI/Hugging Face agentic breach, the Unit 42 A2A session-smuggling write-up). Cite, do not embellish.
3. `## Goal`. The named flag to capture and one line on what capturing it proves. See 4.2.
4. `## Framework mapping`. The header block from 3.3.
5. `## Hints`. Two or three progressive nudges, each in a collapsed `<details>` block. See 4.3.
6. `## Solution and walkthrough`. The working steps, as they already exist. Move existing content here; do not expand the attack.
7. `## Defense`. The control that stops it, including any existing `--defended` path. Preserve every existing defense.

### 4.2 The flag convention

Each lab captures one flag of the form:

```
AGENTICGOAT{NN_short-slug}
```

`NN` is the lab number, `short-slug` names the mechanism (for example `AGENTICGOAT{01_tool-desc-poisoning}`). The flag is a synthetic canary defined in one place per lab, revealed only by the observable side effect that means the attack worked (Section 6). It is never printed on a benign run and never pasteable from a walkthrough step without performing the attack. `Goal` states the flag's name and how it is captured, not its value.

### 4.3 The hints

Two or three per lab, gentle to explicit, each like:

```
<details><summary>Hint 1</summary>
Where does the agent read instructions it should not trust?
</details>
```

Hints point at the reasoning, not the payload. The last may name the technique; none pastes the working input.

### 4.4 The seven labs to conform

Preserve behavior; only restructure docs and wire the flag to the existing success signal.

| Lab | Flag slug | Model need | Migration note |
|---|---|---|---|
| 01 MCP Tool Poisoning | `01_tool-desc-poisoning` | Model-dependent | Reference case for `The story`. Needs the record-and-replay path (Section 6) for the front door. |
| 01b Cross-Server Shadowing | `01b_cross-server-shadowing` | Model-dependent | Status stays `Partial`. Mark incomplete parts honestly in `Overview`; do not finish the attack here. |
| 02 DockerDash | `02_image-label-injection` | Model-dependent | Container-metadata injection. Keep the localhost-only exfil receiver. |
| 03 Red Team Assessment | `03_automated-assessment` | Tooling | Methodology lab (PyRIT, Promptfoo), not a single flag. `Goal` is a passing assessment run that detects the seeded issue, verified deterministically. Document the deviation. |
| 04 RAG Security | `04_rag-poisoning` | Model-dependent | Covers ASI01 and ASI06. One primary flag; note secondary vectors in `Overview`. |
| 05 Agentic Memory Attacks | `05_memory-poisoning` | Model-dependent | Persistence across sessions is the capture signal. |
| 06 Cross-Server MCP Poisoning | `06_cross-server-abuse` | Model-dependent | Smoothest end-to-end run today; make it the second-gentlest after Lab 01. |
| 07 MCP to A2A Kill Chain | `07_kill-chain` | Model-independent | Flagship. Stdlib-only, deterministic. Keep `make run` / `make defended` / `make test`. The flag is captured only at the end of the chain. Verify this still holds after restructuring. |

### 4.5 The template

Create `labs/00-template/`: a README pre-filled with the seven headings and placeholder guidance, a stub flag definition, a stub canary check, and a note on which model class the lab is (Section 6). Update `CONTRIBUTING.md` to require the contract, a model classification, and an honest status.

### 4.6 Acceptance

- All labs use the seven headings verbatim, in order.
- Each defines one flag per 4.2 (Lab 03's deviation documented).
- Each has two or three collapsed, non-spoiling hints.
- No attack's observable behavior changed. Diff entry-point runs against the Section 2 baseline.
- `labs/00-template/` exists and `CONTRIBUTING.md` points to it.

---

## 5. Move 3: the zero-install front door (priority)

This is the piece that decides adoption, so it gets the most care. The goal is the Kubernetes Goat effect: a curious person reaches a working, honest demonstration in under a minute, with nothing installed, no GPU, and no API key. The design below achieves that without weakening what the labs actually prove.

### 5.1 The problem, stated exactly

The labs split into two kinds:

- **Model-independent labs** (Lab 07 today, and any lab whose failure lives in the control plane or the wiring). The vulnerability is in how registration, routing, and authorization are handled, not in a model's choice. These run live and deterministic with no model. They are the strongest possible browser demos because nothing is simulated: the real components produce the real outcome.
- **Model-dependent labs** (Lab 01 and most others). The vulnerability is real and lives in the wiring too (a poisoned tool description, a poisoned RAG store), but the *trigger* is a capable model choosing to follow the injected instruction. Lab 01's own note is decisive: a strong model such as gpt-oss-20b complies; small 7B models often do not. No free browser sandbox has the GPU to run a model that reliably complies.

So the front door cannot depend on running a capable model in the sandbox, and it must not fake the outcome. Section 6 resolves this with record-and-replay against live plumbing.

### 5.2 Options considered, and the decision

- **Run a model in the sandbox with Ollama.** Rejected. Killercoda and Codespaces have no GPU; a 4GB+ model download does not fit a 1-hour session; CPU inference is too slow for a smooth demo; and for Lab 01 a small model that would fit is exactly the model that is "often not susceptible," so the attack would not even reproduce. This path fails on speed and on relevance at once.
- **Call a frontier model from the sandbox with an embedded shared key.** Rejected. Publishing a key invites abuse and cost, and it leaks. It also makes the "zero-setup" front door depend on a paid external service.
- **Host a model proxy that holds the key and rate-limits.** Rejected for v1. It is an always-on service Amine must run and pay for, which 1.2 forbids, and it is the wrong thing to operate before there is demand.
- **Bring your own model or MCP client.** Kept, but as an upgrade path, not the default (5.3, tier F2). It is the most realistic and costs Amine nothing to host, but it requires the learner to set up a client and a key, so it is not the zero-install front door.
- **Model-independent-live plus record-and-replay against live plumbing.** Chosen as the default. Model-independent labs run for real. Model-dependent labs replay a real captured model run while the real MCP servers, RAG store, A2A registry, exfil receiver, and canary all execute live (Section 6). No GPU, no key, deterministic, and defensible because the transcript is a real model's run, not a hand-written script.

### 5.3 The three-tier front door

Ship a ladder, cheapest and most frictionless first. The same scenario body feeds all tiers; the hosts are thin wrappers, so the content is maintained once.

- **F0, Watch (static, zero sign-in).** A read-only trace viewer on GitHub Pages that shows the real captured attack and the defended run side by side, annotated with why each step happened. Repurpose the existing `agentdojo-live` post-solve trace panel for this. This is the 30-second payoff link for a talk, a post, or the newsletter. No account, no sandbox, no cost.
- **F1, Do (hands-on, zero-install).** The interactive path, on hosts the learner supplies:
  - **Killercoda scenarios** for Lab 07 and Lab 01. Guided steps, one action per step, an explicit "you should now see" line each. Lab 07 runs live and deterministic as-is. Lab 01 runs in replay mode against live plumbing. This is the discovery path for the security-training audience and is where a VWAD listing points.
  - **An "Open in Codespaces" badge**, backed by a `.devcontainer/` that boots the whole repo with Python 3.11, Node 18, and dependencies preinstalled. This is for the MCP and agent developer audience who wants the full bench in their own editor, not just two guided scenarios. Same replay and deterministic modes; no GPU needed. The free tier (120 core-hours per month on a 2-core machine) is ample for lab runs.
- **F2, Prove (bring your own agent).** Documented in the repo, not hosted: point your own MCP client (Claude Desktop, Cursor) or a local Ollama or LM Studio at the real vulnerable servers and watch a real model get exploited. This is the answer to "is the replay legitimate?" and the bridge to the full local labs. It carries a clear warning: connect only a client you control, in an isolated context, and only against the synthetic targets; never point a client holding real credentials or data at these servers.

### 5.4 Killercoda scenario structure

Author two scenarios:

```
killercoda/07-kill-chain/     # ship first; nearly free
killercoda/01-tool-poisoning/ # replay mode
```

Each follows the Killercoda layout, defined from the git repo (Killercoda updates on push):

```
killercoda/<slug>/
  index.json     # title, description, ordered steps, environment/image, intro and finish refs
  intro.md       # what the learner will do and see; the no-GPU / deterministic note
  step1.md ...   # one action per step, each with a "you should now see" line
  finish.md      # flag captured, the defense, links back to the repo lab and to F2
  assets/        # idempotent background setup scripts run on start
```

Constraints, from the research:

- Free sessions last one hour and are ephemeral. Keep each scenario completable well inside that, and make setup idempotent.
- No GPU. Neither scenario runs a model. Lab 07 needs none; Lab 01 uses replay.
- Do not depend on large downloads at start. Lab 01 needs the npm MCP filesystem server and a few pip packages; pin them, keep them small, and if start time is tight, vendor the artifacts into the scenario rather than installing live.
- Lab 07 scenario steps: `make run` (watch the HR data exfiltrate, exit 1), then `make defended` (chain breaks at stage 2, exit 0), then `make test`. This is a complete, honest, live demonstration with no model.
- Lab 01 scenario steps: start `exfil_server.py`, then run the agent in replay mode against the real MCP filesystem server, then watch the synthetic SSH key arrive at `localhost:9999`, then run the defended variant and watch it blocked. Use tmux or a backgrounded receiver for the two-process shape.

### 5.5 The Codespaces devcontainer

- `.devcontainer/devcontainer.json` plus a Dockerfile or feature set that installs Python 3.11, Node 18, and each lab's dependencies, and runs the repo's setup so `make`-level targets work on first boot.
- Add an "Open in Codespaces" badge to the README next to the Killercoda links.
- Do not add a GPU assumption. `--llm` against a user-supplied key is available for those who want it, but the default paths are replay and deterministic.

### 5.6 The relevance guarantee (state this in the docs)

The front door does not weaken the tests, and the docs must say why, plainly:

- The vulnerable components (MCP servers, RAG store, A2A registry, exfil receiver, canary) are the real, unmodified lab components and run live in every tier except F0.
- For model-independent labs, nothing is simulated at all.
- For model-dependent labs, only the model's inference is pre-recorded, and it is a recording of a real capable model actually complying, not a script written to look like one. The exploit's side effects are produced live and confirmed by the canary.
- The decision trace shows exactly why compliance happened, which is the teaching payload.
- F2 lets anyone reproduce the whole thing against their own real model, so the claim is falsifiable by the learner.

### 5.7 Acceptance

- F0 viewer is live on GitHub Pages, shows the real captured attack and the defended run side by side, and needs no sign-in.
- Both Killercoda scenarios launch from the repo, complete inside a free session with no local install and no GPU, capture the correct flag, and state the defense.
- Lab 07's scenario runs live and deterministic with no model. Lab 01's runs in replay mode with the synthetic secret genuinely reaching the canary.
- "Open in Codespaces" boots a working environment where any lab runs in replay or deterministic mode without a GPU.
- The README's "Try it in your browser" section links F0, both Killercoda scenarios, and the Codespaces badge, and points to F2.
- The relevance guarantee (5.6) is written into the README and each scenario intro.

---

## 6. Model classification and record-and-replay

A cross-cutting requirement that makes the front door honest and CI stable.

### 6.1 Classify every lab

Each lab declares in its README (and in `00-template`) exactly one class:

- **Model-independent.** Runs live and deterministic with no model. Lab 07 is the reference. Preferred wherever the failure genuinely lives in the wiring.
- **Model-dependent.** The trigger requires a capable model. These get a replay path.

### 6.2 Canary verdicts, never model text

Every flag is captured by an observable side effect: a synthetic secret reaching a localhost listener, a specific file read, a rogue registration that persists, a database row written. Never by parsing what a model said. Where a lab already works this way (Lab 01's exfil receiver, Lab 07's exit code and exfil signal), formalize it into the single flag definition; do not change the attack to make capture easier.

### 6.3 The record-and-replay path (model-dependent labs)

- Add a `--record` mode to the lab's agent driver that runs against a real capable model (via `--llm` with `LLM_BASE_URL` and `LLM_MODEL`) and writes a **cassette**: the exact ordered tool calls and arguments the model produced, plus its visible reasoning, as a committed JSON file under the lab (for example `cassettes/attack1.json`).
- Add a `--replay <cassette>` mode that emits those recorded tool calls in order against the real, live lab components, with no model call. The MCP server, exfil receiver, and canary all run for real, so the side effect and the flag are genuine.
- The cassette must be captured from a real susceptible run, so the replayed calls are exactly what a real model did. If the coding agent has no model endpoint to record with, it builds `--record` and `--replay`, commits a clearly-labelled placeholder cassette, and leaves a documented step for Amine to capture the real cassette against gpt-oss-20b or a frontier endpoint. Do not ship a hand-written cassette presented as a real capture.
- Keep the existing `--llm` live path. It is the F2 realism escape hatch and the way cassettes are refreshed.

### 6.4 Acceptance

- Every lab README states its model class.
- Every model-dependent lab has working `--record` and `--replay`, and a committed cassette (real, or placeholder with a documented capture step).
- Replaying a cassette reproduces the same observable side effect and flag capture as a live susceptible run, verified against the Section 2 baseline.
- CI runs the replay and deterministic paths and asserts flag capture, with no model or GPU.

---

## 7. Repo relationship and mechanics

- AgenticGoat is a new repository, seeded from a pinned clone of `mcp-attack-labs` with history carried (Section 2). It is not a rename and not a fork-for-PRs; the two diverge.
- `mcp-attack-labs` stays the upstream raw lab bench and is not modified in this milestone.
- `LINEAGE.md` records the source commit and the divergence policy (manual cross-pollination).
- Preserve the MIT `LICENSE` and the responsible-use section verbatim in the new repo.
- Directory layout after this milestone:

```
README.md              # paragraph + crosswalk + "Try it in your browser"
LINEAGE.md
CONTRIBUTING.md        # requires the contract, a model class, an honest status
LICENSE
labs/
  00-template/
  01-mcp-tool-poisoning/       # + cassettes/
  01b-cross-server-shadowing/
  02-docker-dash/
  03-red-team-assessment/
  04-rag-security/
  05-agentic-memory-attacks/
  06-cross-server-mcp-poisoning/
  07-mcp-to-a2a-kill-chain/
killercoda/
  07-kill-chain/
  01-tool-poisoning/
.devcontainer/
  devcontainer.json
docs/                  # GitHub Pages: the F0 static trace viewer
```

Keep existing lab directory names unless a rename is required for the flag-slug scheme; if you rename, fix internal links.

---

## 8. Constraints and conventions

- No real secrets. Every credential, token, and payload is synthetic. Confirm this holds after the migration and in every cassette.
- Exfil receivers bind to localhost only. Introduce no outbound call to any host other than a local listener (the optional `--llm` and F2 paths reach a user-supplied model endpoint only, and only when the user opts in).
- No new runtime dependencies beyond what the labs already use (Python 3.11+, Node 18+ where a lab needs it, a user-supplied model endpoint for `--llm`). Deterministic and replay paths run without a model and, where a lab already does, on the standard library.
- Preserve every existing defense and every `--defended` path.
- Documentation voice: plain, first-person where natural, practitioner tone, no self-congratulation, no marketing adjectives. Markdown only. No em dashes.
- Do not change attack behavior to make a flag easier to capture or a replay smoother. If a success signal is ambiguous, report it; do not strengthen the attack to fix it.
- Commit in logical units per move, with messages naming the move. Apply the session's configured commit attribution lines if any are set; otherwise use plain messages.

---

## 9. Sequencing

1. Pre-flight and repo creation (Section 2). Stop if the name is unconfirmed.
2. Move 1: crosswalk and per-lab headers (Section 3).
3. Move 2: the template, then the seven labs to the contract, then the model classification per lab (Sections 4 and 6.1).
4. Front door, in ROI order:
   a. Lab 07 Killercoda scenario first (model-independent, nearly free, and it is the flagship).
   b. The `--record` / `--replay` path and cassette for Lab 01 (Section 6.3).
   c. Lab 01 Killercoda scenario on replay.
   d. The `.devcontainer/` and Codespaces badge.
   e. The F0 static trace viewer on GitHub Pages.
5. Run the Definition of Done and report.

Do not begin a step until the previous one passes its acceptance list.

---

## 10. Definition of Done

- [ ] New `agentic-goat` repo exists, seeded from `mcp-attack-labs` at a recorded commit, history carried, `LINEAGE.md` present. `mcp-attack-labs` untouched.
- [ ] README opens with the paragraph, the crosswalk table (words `Complete` / `Partial` / `Planned`, no emoji), and a "Try it in your browser" section linking F0, both Killercoda scenarios, and the Codespaces badge.
- [ ] Framework links and the non-endorsement note present and correct.
- [ ] All labs use the seven contract headings verbatim and in order.
- [ ] Each lab defines one named flag per convention (Lab 03's deviation documented), captured only by a canary side effect, and declares its model class.
- [ ] Each lab has two or three collapsed, non-spoiling progressive hints.
- [ ] `labs/00-template/` exists; `CONTRIBUTING.md` requires the contract, a model class, and an honest status.
- [ ] Every model-dependent lab has `--record` and `--replay` and a committed cassette (real or clearly-labelled placeholder with a capture step).
- [ ] Lab 07 Killercoda scenario runs live and deterministic, no model, inside a free session; flag captured; defense shown.
- [ ] Lab 01 Killercoda scenario runs on replay against live plumbing; synthetic secret reaches the canary; defended variant blocks it.
- [ ] "Open in Codespaces" boots a working environment where labs run in replay or deterministic mode without a GPU.
- [ ] F0 static trace viewer live on GitHub Pages, real capture and defended run side by side, no sign-in.
- [ ] The relevance guarantee (5.6) is written into the README and each scenario intro.
- [ ] Diffed against the Section 2 baseline, no attack's observable behavior changed.
- [ ] MIT license, responsible-use notice, synthetic-only secrets, localhost-only exfil all intact.
- [ ] Nothing from the 1.2 do-not-build list was implemented.

Report against this list item by item. For anything you cannot complete, stop and say why rather than working around it.

---

### Reference links

- Killercoda creators docs: <https://killercoda.com/creators> and the FAQ (one-hour free sessions, git-repo scenarios): <https://killercoda.com/faq>
- GitHub Codespaces (free tier, devcontainers): <https://github.com/features/codespaces> and billing detail <https://docs.github.com/en/billing/concepts/product-billing/github-codespaces>
- devcontainer spec: <https://containers.dev>
- Kubernetes Goat, the structural model to imitate: <https://github.com/madhuakula/kubernetes-goat>
- OWASP Top 10 for Agentic Applications: <https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications/>
- OWASP MCP Top 10: <https://owasp.org/www-project-mcp-top-10/>
- MITRE ATLAS: <https://atlas.mitre.org/>
- Upstream bench (unchanged): <https://github.com/aminrj-labs/mcp-attack-labs>
