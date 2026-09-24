# Lab NN: [Attack Technique Name]

One-sentence summary of the attack and what makes it interesting.

Model class: **Model-independent** or **Model-dependent**. A model-dependent
lab ships a `cassettes/` directory with a `--record` / `--replay` path, so the
run is reproducible without a live model.

Status: **Complete** / **Partial** / **Planned**, stated honestly. Nothing is
presented as working unless it runs.

---

## Overview

Explain the core mechanism in one paragraph, plainly. What does the attacker
control? What does the victim observe? What happens under the hood?

```
[Optional: ASCII diagram of the attack flow]

Attacker  ->  [malicious component]  ->  victim action
                                 <-  stolen data
```

If the lab covers more than one vector, name the primary one here (it carries
the flag) and list the secondary ones.

---

## The story

One paragraph tying the lab to a named public incident, so the scene is
memorable and quotable. Cite, do not embellish. For example: the Invariant
Labs MCP tool-poisoning notification, the Supabase/Cursor tool-poisoning case,
the EchoLeak mass-notification issue, the Amazon Q extension incident, the
September 2026 OpenAI/Hugging Face agentic breach, or the Unit 42 A2A
session-smuggling write-up.

---

## Goal

The named flag to capture is `AGENTICGOAT{NN_short-slug}`.

State in one line what capturing it proves, and which observable side effect
reveals it (a synthetic secret reaching the localhost listener, a specific file
reached, a rogue registration that persists, a row written). The flag value
itself is never printed here, and it is never pasteable from the walkthrough
below without performing the attack. It is defined in exactly one place in this
lab's code, and it is revealed only when the attack's side effect happens.

---

## Framework mapping

- OWASP Agentic Top 10: ASI0x <name>
- OWASP MCP Top 10: MCP0x <name>   (omit this line if not applicable)
- MITRE ATLAS: <technique id and name, if one applies>

---

## Hints

Two or three progressive nudges, gentle to explicit. They point at the
reasoning, not the payload. The last one may name the technique. None pastes
the working input.

<details><summary>Hint 1</summary>

Where does the agent read instructions it should not trust?

</details>

<details><summary>Hint 2</summary>

Which component decides what the agent is allowed to do, and who configures it?

</details>

<details><summary>Hint 3</summary>

The technique is <name the technique>. The vulnerable assumption is <state it>.

</details>

---

## Solution and walkthrough

The working attack, step by step. Prerequisites, setup, and the commands with
the expected terminal output. Move the existing lab steps here; do not expand
the attack.

**Terminal 1: [role, e.g. the attacker's receiver]**

```bash
[command]
```

**Terminal 2: [role, e.g. the vulnerable agent]**

```bash
[command]
```

Expected output: [describe what success looks like, including where the flag
appears].

For model-dependent labs, document the replay path here:

```bash
python3 agent.py --replay cassettes/attack1.json   # no model, deterministic
```

The cassette is a recording of a real susceptible model run. See the lab's
`cassettes/README.md` for how it was captured and how to refresh it.

---

## Defense

The control that stops the attack, including any existing `--defended` path.
Preserve every existing defense. Show where the attack breaks when the control
is on, and one or two lines on why it holds.

---

## Files

| File | Description |
|------|-------------|
| `canary.py` | Flag definition and canary check (one place only) |
| `[filename]` | [what it does] |
