# Contributing

Thanks for helping improve AgenticGoat. This is a teaching project, so the bar
is not just "does the attack work": it is "can a reader understand it,
reproduce it, and learn the defense."

## Ground rules

- **Educational and authorized use only.** Contributions must fit the
  responsible-use notice in the [README](./README.md) and [LICENSE](./LICENSE).
  No tooling aimed at attacking real third-party systems, no real credentials,
  no real personal data.
- **Everything runs locally.** Labs must work against a local LLM endpoint
  (Ollama or LM Studio) with no cloud API and no paid keys. Attacker receivers
  bind to `localhost` only. The optional `--llm` path and the bring-your-own
  client path reach a user-supplied endpoint, and only when the user opts in.
- **Synthetic data only.** Bait documents, secrets, tokens, and identities must
  be obviously fake. Every flag in the project is a synthetic canary.
- **Be honest about status.** Never present design notes or partial work as
  complete. Label work in progress as such, in the lab README and in the
  crosswalk, using the literal words `Complete`, `Partial`, or `Planned`.
- **No new offensive capability.** A contribution is packaging of an existing
  mechanism: docs, a defense, a replay cassette, a new lab that follows the
  contract. If a change would broaden what a lab can reach, stop and open an
  issue first.

## The scenario contract (required)

Every lab README uses these seven sections, in this order, with these exact
headings. Start from [labs/00-template/](./labs/00-template/).

1. `## Overview` : one paragraph, the mechanism, plainly.
2. `## The story` : one paragraph tying the lab to a named public incident.
   Cite, do not embellish.
3. `## Goal` : the named flag and one line on what capturing it proves.
4. `## Framework mapping` : the fixed block with the OWASP Agentic Top 10 and
   OWASP MCP Top 10 IDs (omit the MCP line if not applicable) and MITRE ATLAS
   where one applies.
5. `## Hints` : two or three progressive nudges, each in a collapsed
   `<details>` block. Gentle to explicit. They point at the reasoning, not the
   payload; the last may name the technique; none pastes the working input.
6. `## Solution and walkthrough` : the working steps, as they already exist.
   Do not expand the attack.
7. `## Defense` : the control that stops it, including any existing
   `--defended` path. Preserve every existing defense.

## The flag convention (required)

Each lab captures one flag of the form:

```
AGENTICGOAT{NN_short-slug}
```

`NN` is the lab number, `short-slug` names the mechanism (for example
`AGENTICGOAT{01_tool-desc-poisoning}`). The rules:

- The flag is a synthetic canary defined in one place per lab (see
  `labs/00-template/canary.py` for the stub).
- It is revealed only by the observable side effect that means the attack
  worked: a synthetic secret reaching a localhost listener, a specific file
  read, a rogue registration that persists, a database row written. Never by
  parsing what a model said.
- It is never printed on a benign run, and never pasteable from a walkthrough
  step without performing the attack. `Goal` states the flag's name and how it
  is captured, not its value.
- Do not change the attack to make a flag easier to capture or a replay
  smoother. If a success signal is ambiguous, report it.

If a lab genuinely cannot capture a flag this way (a methodology lab), it must
document the deviation in `Goal` and state which deterministic signal verifies
the run instead.

## Model classification (required)

Each lab declares exactly one class in its README, right under the title:

- **Model-independent.** Runs live and deterministic with no model. The lab's
  failure lives in the wiring, not in a model's choice.
- **Model-dependent.** The trigger requires a capable model. These labs must
  also ship `--record` and `--replay` (a cassette of one real susceptible
  model run, under `cassettes/`, with a `README.md` explaining how to capture
  and refresh it). A hand-written cassette presented as a real capture is not
  acceptable: leave a clearly-labelled placeholder and the documented capture
  step.

Read the endpoint from environment variables (`LLM_BASE_URL`, `MODEL`,
`API_KEY`) so the lab works on either backend. Do not hardcode a base URL.

## Adding a lab

1. Copy `labs/00-template/` as your starting point.
2. Fill in the README against the seven sections above.
3. Add your code, its canary (`canary.py`), and its defense.
4. Declare the model class and, if model-dependent, the record-and-replay
   path.
5. Add a row to the crosswalk table and to the lab table in the top-level
   `README.md`, with the literal status word.
6. Do not commit runtime artifacts (logs, generated stores, `venv/`, cassettes
   captured from a machine with real data). Add them to `.gitignore` if
   needed.
7. Keep the documentation voice plain and factual, practitioner tone, no
   marketing adjectives, no em dashes.

## Status labels

| Label | Meaning |
|-------|---------|
| `Complete` | Runs end to end; has a defense, a flag, and a full README |
| `Partial` | Partial: code runs but docs, defenses, or the run are incomplete |
| `Planned` | Design only; explicitly not yet implemented |

## Commits and branches

- Work on a feature branch; open a PR against `main`.
- Keep history intact: no force-pushes or history rewrites on shared branches.
- Write clear commit messages describing what changed and why.
