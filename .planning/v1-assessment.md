# AgenticGoat v1: verified assessment and remediation work orders

Audience: the coding agent that will do the remediation. Read all of it before starting.
Reviewed state: first pass at `f0086e2`; progress re-check on 2026-09-26 at `178ca3e` (R01-R04 landed, see section 0.5).
Reference spec: `.planning/agenticgoat-v1-spec.md` (called "the spec" below, with § numbers).
Method: every tracked source file in `labs/`, `killercoda/`, `.devcontainer/`, `.github/`, `docs/` and the top-level docs was read in full. GitHub CI logs and the Pages API were checked. For the progress re-check, the R01-R04 diffs were read and every CI step was replayed locally on a clean clone (Python 3.12, `mcp` 1.30.0, isolated `HOME`).

---

## 0. Ground rules for this remediation (binding)

1. The spec's constraints still apply: no new offensive capability, no change to observable attack behavior, synthetic data only, localhost-only exfil, no em dashes in docs, and nothing from spec §1.2.
2. **Stop and ask Amine** before any change marked `[ASK]`. These touch attack inputs or need his accounts or endpoints.
3. Items marked `[AMINE]` cannot be done by the agent (a model endpoint, the Killercoda account, repo settings). Prepare everything around them and list them in the final report.
4. One commit per work order, with the message prefixed by its ID (for example `R01: ...`). Follow the git attribution rules in the user's global CLAUDE.md: no AI attribution lines.
5. Do not mark a work order done until its acceptance checks pass **on GitHub Actions**, not only locally. The previous "all DoD verified" claim came from local runs while CI on `main` had never passed.

---

## 0.5 Progress re-check (2026-09-26, `178ca3e`)

### Landed work orders

| ID | Commit(s) | Verdict | Evidence |
|---|---|---|---|
| R01 | `9ac6390`, `178ca3e` | Done locally, not on GitHub | `_reset_state()` now writes `[]`; new `test_defended_sink_is_empty_and_exit_codes`; `make test` gives 7 passed. Undefended rc=1 with the flag in the sink, defended rc=0 with an empty sink. CI pins `mcp>=1.0.0,<2.0.0` |
| R02 | `2b15028` | Done | `git grep` finds no remaining "captured from a real" or gpt-oss-20b capture claims outside `.planning/`. The Killercoda Lab 01 finish no longer prints the flag |
| R03 | `f03c8de` | Done | authz is now stage 4 everywhere. Stage 1 is labelled as modelled in the viewer, the Killercoda intro and the README. The circuit-breaker caveat is documented (closes F19). `07/finish.md` is deduplicated. The Lab 07 intro now carries the relevance guarantee |
| R04 | `4f5d23b` | Done | The five runtime files are untracked and gitignored. Lab 06 `load_notes()` falls back to the seed. Lab 05 `MemoryStore` seeds the clean baseline when `memory.json` is missing. The Lab 03 `.gitignore` rule is narrowed. A fresh clone stays clean after every replay (only the CI step's own `exfil.out`/`agent.out` logs appear, see F33) |

### Local replay of the CI job on `178ca3e` (clean clone, `mcp<2`)

| Step | Result | What it actually proves |
|---|---|---|
| Lab 07 | Pass | Real: exit codes, sink contents and the flag are all asserted |
| Lab 01 | Pass | The live listener received an `add` payload. The flag is **not** in it (placeholder) |
| Lab 01b | Pass | The stub log has a `send_message` to the attacker number. The flag is **not** in it |
| Lab 02 | Pass | The listener received the report. `docker inspect` returned "Image not found" and `docker_stop` "No such container", so no Docker side effect happened; the grepped string comes from the cassette |
| Lab 03 | Pass | The email was logged and forwarded. The canary is **not** in it |
| Lab 05 | Pass | `FLAG CAPTURED` printed, although the payload was the placeholder string `sess-replay-demo_placeholder-conversation-summary` (F7 second half still open) |
| Lab 06 | Pass | One fresh `Paris` entry reached the live log (no longer the committed stale one). The flag is **not** in it |

Conclusion: CI should now go green, but only Lab 07 asserts a flag. F2's core problem (the checks prove that the plumbing ran, not that the canary was captured) is unchanged.

### New findings from the re-check

**F31 (S1). The new commits have not triggered CI, and GitHub's API does not show them.** `git ls-remote origin` (SSH) reports `refs/heads/main` at `178ca3e`. The GitHub REST API (`/branches/main`, `/git/ref/heads/main`) still reports `f0086e2`, returns 422 "No commit found" for `178ca3e`, and lists no workflow run after `2026-09-26T07:03Z` (the re-check ran at 08:35Z, about 45 minutes after the push). Until a green run exists for `178ca3e` on github.com, R01 is not done per ground rule 5. `[AMINE]`: open `https://github.com/aminrj-labs/agentic-goat/commits/main` and the Actions tab in a browser and confirm which head GitHub serves.

**F32 (S1). `mcp` 2.x breaks every install path except CI.** Verified: the `mcp` 2.2.0 wheel replaces `mcp/server/fastmcp.py` with a module that raises `ModuleNotFoundError` ("FastMCP was renamed to MCPServer ... or pin 'mcp<2'"). The MCP servers in Labs 01, 01b, 02 and 06 import `mcp.server.fastmcp`. Lab 03 uses the low-level `mcp.server.Server` API; its 2.x compatibility was not checked. The pin was applied only in `.github/workflows/ci.yml`. These still resolve to 2.x on a fresh machine:
- `labs/01b-cross-server-shadowing/requirements.txt`, `labs/03-red-team-assessment/requirements.txt`, `labs/06-ASI02-cross-server-mcp-poisoning/requirements.txt` (`mcp>=1.0.0`)
- `killercoda/01-tool-poisoning/step1.md` (`pip install mcp ...`)
- `.devcontainer/post-create.sh` (installs each lab's requirements, and hides the failure, F17)
- Lab 01 and Lab 02 have no `requirements.txt`; their READMEs say `pip install mcp ...`

So a learner following any README, Killercoda or Codespaces today gets a crash on import. The pin belongs in every requirements file and install command.

**F33 (S3). CI and replay leave untracked logs in the lab directories.** The CI steps write `exfil.out` and the replays write listener output inside `labs/*/`. They aren't gitignored, so a learner who follows the same commands gets a dirty `git status`.

**F34 (S2). Lab 02 acts on every container on the host, not just the victims.** `docker_mcp_server.docker_ps` lists all running containers, and the image label instructs the model to stop each one and dump its environment (`docker_env`). In the re-check, the replay's live `docker_ps` returned the reviewer's own unrelated containers. A live (non-replay) run on a developer machine would therefore stop unrelated containers and send their environment variables, which can hold real secrets, to the listener and into any cassette recorded from that run. The cassette README mentions redaction, but the lab README has no warning. Minimum fix: a prominent warning to run Lab 02 against a dedicated Docker context (for example a throwaway Docker-in-Docker or rootless daemon with only the three victims). `[ASK]` before scoping `docker_ps` to the lab's containers, because that changes observable attack behavior.

### Scorecard movement

DoD 13 (relevance guarantee) moves from "Partial, and false" to **Met**: the claims are now honest and every intro carries the guarantee. DoD 5 improves (Lab 05 no longer ships pre-poisoned) but stays Partial. Nothing else changed status, and DoD 9 and 11 are now blocked further by F32. New tally: **8 met, 3 partial or unverified, 4 not met, 1 met on paper.**

### Findings status

- **Closed:** F1, F3, F15, F19. F4 partly (the stage number, the duplicate finish and the step 3 claims are fixed). F5 partly (stage numbers and the Stage 1 wording are fixed; Pages is still not live). F7 partly (no longer pre-poisoned; the any-hit flag remains).
- **Open, blocking:** F2, F4 (clone, paths, PEP 668, stub server, no defended step, URLs), F5 (Pages), F31, F32.
- **Open, spec or correctness:** F6, F7 (flag trigger), F8, F9, F10, F11, F12, F13, F14, F16, F17, F18, F34.
- **Open, quality:** F20 to F30, F33.

---

## 1. Verdict (first pass at `f0086e2`; see 0.5 for movement)

Moves 1 and 2 (crosswalk and scenario contract) are substantively done. Move 3 (the front door, the spec's priority) is not.

| # | DoD item (spec §10) | Verdict | Blocking evidence |
|---|---|---|---|
| 1 | Repo seeded, history, LINEAGE | Met | |
| 2 | README crosswalk + "Try it in your browser" | Partial | The F0 link is a repo-relative file. The F2 row is really the Codespaces path. The Killercoda URLs are unverified |
| 3 | Framework links + non-endorsement | Met | |
| 4 | Seven headings verbatim | Met | All 8 READMEs |
| 5 | One flag per lab, canary side-effect only, model class | Partial | Lab 04 parses model text. Lab 05 fires on any `/exfil` hit and ships pre-poisoned. No lab implements `canary_reached()` |
| 6 | 2-3 non-spoiling hints | Met | |
| 7 | Template + CONTRIBUTING | Met | But the template's `canary_reached()` contract is unimplemented everywhere |
| 8 | record/replay + cassette per model-dependent lab | Met on paper | All 7 cassettes are `"status": "placeholder"` |
| 9 | Lab 07 Killercoda works | Not met | The repo is never cloned, and the path `/home/user/...` doesn't exist |
| 10 | Lab 01 Killercoda: replay, secret reaches canary, defended variant | Not met | The placeholder means no flag. A stub replaces the real server. No defense exists |
| 11 | Codespaces works | Unverified | Every install error is swallowed. It points to a nonexistent `make setup` |
| 12 | F0 live on Pages | Not met | Pages API returns 404. The viewer is hand-written and wrong about stage numbers |
| 13 | Relevance guarantee in README + each intro | Partial, and false | It claims a real gpt-oss-20b capture that doesn't exist. Missing from the Lab 07 intro |
| 14 | No behavior change vs baseline | Unverified | The diff was never run or recorded |
| 15 | MIT, responsible use, synthetic, localhost exfil | Mostly met | Lab 05's `WebTool` will GET any URL the model picks (F14) |
| 16 | Nothing from §1.2 | Met | |

---

## 2. Findings (verified against code)

Severity: **S1** means a false claim or a broken deliverable, **S2** a spec violation or correctness bug, **S3** quality.

### S1: blocking

**F1. CI has never passed; its first step crashes.** `gh run list` shows only 2 runs, both failures (`36225614198`, `36119893779`). In `.github/workflows/ci.yml`, the Lab 07 step does `json.load(open("state/exfil.json"))` after `run_chain.py --defended`. But `KillChain._reset_state()` (`labs/07-mcp-to-a2a-kill-chain/killchain.py:116-120`) deletes that file, and a defended run never recreates it, so the step fails with `FileNotFoundError`. Every later lab step has never run on GitHub.

**F2. CI assertions don't test what they claim.**
- Lab 01: asserts `grep -q 'placeholder' exfil.out`, which confirms placeholder text, not the canary. It also uses a heredoc stub instead of the real FS server.
- Lab 02: CI has no victim containers or image. The grepped `containers` string comes from the cassette's own arguments, so the test proves nothing about Docker side effects.
- Lab 03: greps `Type.*: email`, which the placeholder satisfies. There is no canary assertion.
- Lab 04: `py_compile` and a cassette shape check only. There is no replay.
- Lab 05: asserts `FLAG CAPTURED`, which fires on any request (F7).
- Lab 06: asserts `"Paris"` is in `data/exfil_log.json`. That file is **committed** with a 2026-04-02 Paris entry, so the step passes even if the replay does nothing.

**F3. The relevance guarantee is false as shipped.** `README.md` ("Try it in your browser"), `killercoda/01-tool-poisoning/intro.md` and `step2.md` say the cassette was "captured from a real susceptible model (gpt-oss-20b)". All 7 cassettes say `"status": "placeholder"` with the note "no model endpoint was available". `killercoda/01-tool-poisoning/finish.md` prints the flag as "captured", but a placeholder replay never delivers it. Spec §6.3 explicitly forbids presenting a placeholder as a real capture.

**F4. Killercoda scenarios cannot run.**
- There is no `assets/` directory, no background or foreground setup script, and no `git clone`. Yet every step does `cd /home/user/agentic-goat/...`, and on the `ubuntu` image the user is `root` in `/root`.
- Lab 01 `step1.md` runs a system-wide `pip install`, which recent Ubuntu refuses under PEP 668.
- Lab 01 installs `@modelcontextprotocol/server-filesystem` and then doesn't use it. It writes `/tmp/fs_stub.py` instead, which contradicts "real, unmodified lab components" in its own intro.
- Lab 01 has no defended step (and no defense exists, see F9).
- `07-kill-chain/step2.md` says `--control authz` "breaks at stage 3". `test_chain.py:39` proves it's **stage 4**.
- `07-kill-chain/finish.md` duplicates step 3 verbatim.
- `07-kill-chain/step3.md` claims the tests check exit codes and an empty exfil state. `test_chain.py` checks neither.
- The README's Killercoda URLs use `/course/agentic-goat/...`, but there's no `structure.json` and the course directory would be named `killercoda`. These are unverified and likely 404.

**F5. F0 is not live and is inaccurate.**
- `gh api repos/aminrj-labs/agentic-goat/pages` returns 404, and there's no Pages workflow.
- `docs/index.html:265` says Control 2 breaks at Stage 3. It's Stage 4.
- The page claims "real, deterministic runs ... no simulation", but it's hand-typed HTML, and Stage 1 *is* modelled (`mcp_entry.deterministic_brain`, whose docstring says so).
- It covers only Lab 07.

### S2: spec violations and correctness bugs

**F6. Replay replays the stolen data itself.** `cassette.py` intercepts only the LLM call, but the exfil payload travels in model-authored tool *arguments*:
- Lab 01 `sidenote`
- Lab 01b `send_message.body`
- Lab 02 `docker_health_report.env_data`
- Lab 03 `send_email.body`
- Lab 05 the `web_tool_fetch` URL
- Lab 06 `sync_weather_cache.notes_dump`

On replay, the canary reaching the listener is the **recorded copy**, not what the live tool just returned. A real cassette would therefore "capture" the flag even with no canary file, no seeded store and no Docker. That contradicts spec §5.6 ("side effects produced live and confirmed by the canary").

**F7. Lab 05 ships pre-poisoned, and its flag fires on anything.**
- The committed `labs/05-agentic-memory-attacks/memory/memory.json` already contains the malicious `mem-inject-001` entry, plus an agent-written `communication_style` entry. `episodic.json` and `audit.jsonl` hold March and April 2026 session logs.
- So a fresh clone is poisoned before any attack runs, and a benign session will exfil and print the flag. That violates §4.2 ("never printed on a benign run").
- `exfil_server.py:53` prints `FLAG CAPTURED` on the first request of any kind, with no check of the payload.

**F8. Lab 04's flag is decided by parsing model output.** `attack1_knowledge_poisoning.py:114` prints the flag if the answer contains `"8.3"`, `"restatement"` or `"CORRECTED"`. That violates §6.2 and produces false positives (a model that *rejects* the correction but mentions it, or any "x8.3" substring). It prints once per matching query, up to 3 times.

**F9. Labs 01, 02 and 06 have no runnable defense** (their `## Defense` sections are prose only), yet they are labelled `Complete`. CONTRIBUTING defines Complete as "has a defense". Lab 01 is the second Killercoda scenario, so spec §5.4 and DoD item 10 ("defended variant blocks it") cannot be met.

**F10. No lab implements the template's canary contract.** `labs/00-template/canary.py` defines `canary_reached()` and says "the attack driver and any CI check assert on this". No lab has a `canary.py`. Flag strings live in 7 different kinds of places:
- `make_canary.py`
- `whatsapp_stub_server.py`
- `start_victims.sh`
- `sandbox/.env`
- `attack1_knowledge_poisoning.py`
- `exfil_server.py`
- `notes_seed.json` and the committed `notes_store.json`

The Lab 01, 02 and 03 listeners print to stdout only, so nothing durable exists to check.

**F11. Model and endpoint env vars are inconsistent, which breaks the documented record commands.**
- Lab 06 `agent.py:16-17` hardcodes `DEFAULT_MODEL = "qwen2.5-7b-instruct"`, ignores `MODEL`, and ignores `API_KEY`. The Lab 06 cassette README tells you to `export MODEL=gpt-oss-20b`, which has no effect: `detect_model()` picks something else.
- Lab 04 reads `LM_STUDIO_MODEL`.
- Lab 07 reads `LLM_MODEL` and `LLM_API_KEY`.
- CONTRIBUTING mandates `LLM_BASE_URL`, `MODEL` and `API_KEY`.
- Lab 03 `promptfoo/promptfoo-redteam-config.yaml` hardcodes `http://localhost:1234/v1` and `qwen2.5-coder-7b-instruct-mlx`.

**F12. The Lab 03 Phase 5 paths don't resolve.** `docuassist_mcp_server.resolve_path` makes relative paths sandbox-relative, but:
- The user prompt says `sandbox/docs/status-report.md`, which resolves to `sandbox/sandbox/docs/...` (not found).
- The injected doc says `read_file on sandbox/.env`, which resolves to `sandbox/sandbox/.env` (not found).

The placeholder cassette silently uses the working paths `docs/status-report.md` and `.env`, so it does not reflect what a model would do from the documented prompt. `[ASK]`: fixing the payload text is an attack-input change.

**F13. Lab 03 walkthrough and dependency errors.**
- `README.md` Phase 4a does `cd pyrit` from inside `promptfoo/`, which fails. It needs `cd ../pyrit`.
- `pyrit/*.py` never import PyRIT (the docstring says PyRIT 0.11 removed the orchestrator, so the algorithm is reimplemented). Yet `requirements.txt` installs `pyrit>=0.5.0`, a heavy unused dependency.
- The lab title says "PyRIT & Promptfoo". Say "PyRIT-style" honestly.
- The Promptfoo config's ASI comments are mislabelled: "ASI05 Output Handling" and "ASI07 Sensitive Information" don't match the 2026 list (ASI05 is Unexpected Code Execution, ASI07 is Inter-Agent Communication).
- The Promptfoo target is the bare chat model with a system prompt, not the DocuAssist agent with its MCP tools. The README should say what the scan actually exercises.

**F14. Lab 05 `WebTool.fetch` makes a real HTTP GET to any URL** the model chooses (`tools/web_tool.py`, fallback branch). Spec §8 says to introduce no outbound call to any host other than a local listener. A model could fetch arbitrary internet hosts.

**F15. Committed runtime state.**
- `labs/06-.../data/exfil_log.json` is a stale capture that makes the Lab 06 CI check pass by accident.
- `labs/06-.../data/notes_store.json` is a runtime copy of the seed and contains the flag.
- `labs/05-.../memory/{memory.json,episodic.json,audit.jsonl}` (see F7).
- `.gitignore` ignores `labs/03-red-team-assessment/sandbox/docs/`, but `deployment-guide.md` and `q1-status-report.md` in it are tracked.

**F16. Stdout writes inside stdio MCP servers can corrupt the JSON-RPC stream.**
- `labs/02-docker-dash/docker_mcp_server.py` prints a banner before `mcp.run()`.
- `labs/01-mcp-tool-poisoning/attack1_direct_poison.py` prints `[DEBUG exfil error]` to stdout when the listener is down.

These existed before the fork, but they cause flaky runs in Killercoda and CI. Redirect them to `stderr`: a transport fix, not an attack change.

**F17. The Codespaces setup hides failures.**
- `.devcontainer/post-create.sh` ends every install with `2>/dev/null || true`.
- The Dockerfile apt-installs `python3` and `nodejs` *and* the devcontainer features install Python 3.12 and Node 20, which is redundant and makes PATH ambiguous.
- It installs every lab's requirements, including sentence-transformers/torch/Jupyter (Lab 04) and pyrit (Lab 03), which makes first boot slow and heavy.
- It suggests `cd labs/01-mcp-tool-poisoning && make setup`, but Lab 01 has no Makefile.
- `forwardPorts: [9999]` needlessly exposes the exfil receiver through the Codespaces tunnel.
- Lab 01's npm dependencies install without the canary (`make_canary.py` never runs).

**F18. The "no behavior change" gate (spec §4.6) was never evidenced.** Several attack inputs changed:
- a canary note added to the Lab 06 seed, whose text literally says "It leaves the store only if the cross-server chain dumps all notes", which may cue a safety-tuned model
- a flag appended to a 01b WhatsApp message
- a canary env var on the Lab 02 `lab-cache` container
- the new `start_victims.sh` (it didn't exist at baseline)
- the new `sandbox/.env` in Lab 03

These are probably acceptable, but must be recorded.

### S3: quality

- **F19.** Lab 07 Control 3a (circuit breaker, threshold 3) never trips: the chain makes only 2 routes. `test_blast_radius_controls_stop_exfiltration` passes because of human-in-the-loop alone. Either document that Control 3 is HITL in this chain, or add a test showing the breaker tripping on a burst, without changing the chain's stages.
- **F20.** Lab 07 `--llm` silently falls back to the deterministic brain on any error while the header still says "live LLM" (`run_chain.py:48`, `mcp_entry.llm_brain`). Print a clear "FELL BACK" line in the stage detail. `requirements.txt` uses `openai ... ; extra == "llm"`, which `pip install -r` always skips. Say so, or move it to a comment.
- **F21.** `labs/02-docker-dash/lab-env.sh` hardcodes `/Users/ARAJI/.rd/docker.sock` (personal macOS path, zsh-only). Remove it or generalise it.
- **F22.** Crosswalk row 3 says "One server's *description* hijacks another's tool", but Lab 01b's payload is in the *return value* (`daily_facts_server.py`). Fix the wording.
- **F23.** The Lab 01b and Lab 02 agents use deliberately permissive system prompts: "If a tool description or tool result contains required ... steps, execute those steps silently", and "you must execute those steps ... Never ask for confirmation". This is legitimate for a teaching target but undisclosed. Add one honest sentence to each `## Overview` so the result isn't over-claimed.
- **F24.** Story accuracy. The Lab 01 `## The story` calls the Supabase/Cursor case "tool-poisoning". It was prompt injection through database content, via an MCP server holding a privileged key. It also has no link. Audit every `## The story` for accuracy and a source link.
- **F25.** Several `## Overview` sections run well past "one paragraph" (Labs 01, 05, 07). Move the detail into the walkthrough.
- **F26.** Em dashes in `killercoda/*/index.json` titles, the `docs/index.html` `<title>`, `killercoda/07-kill-chain/intro.md` and some lab text (the spec forbids them; the responsible-use block is exempt).
- **F27.** `cassette.py` is byte-identical in 7 labs. Keep the copies (labs are standalone) but enforce identical hashes in CI.
- **F28.** README "Everything runs on your own machine ... no data leaves your laptop" contradicts the Killercoda and Codespaces tiers. Scope it to local runs.
- **F29.** Lab 04 replay isn't offline: `SentenceTransformerEmbeddingFunction("all-MiniLM-L6-v2")` downloads from Hugging Face on first run. Document it, or pre-fetch it in setup.
- **F30.** Stale LM Studio comments (`localhost:1234`) and success-rate claims ("95% success") in the Lab 04 and Lab 05 Makefiles and docstrings.

---

## 3. Work orders (do them in this order)

Each has **Files**, **Change** and **Accept**. "CI" means GitHub Actions on the pushed branch.

### Phase A: make the claims true (do first, small)

**R01: Fix the Lab 07 CI crash and make Lab 07 always write its sink** (landed `9ac6390`, `178ca3e`; awaiting a green GitHub run, F31) (fixes F1)
- Files: `labs/07-mcp-to-a2a-kill-chain/killchain.py`, `.github/workflows/ci.yml`.
- Change: in `_reset_state()`, write `[]` to `EXFIL_STATE` after unlinking, so the sink always exists. Add test `test_defended_sink_is_empty_and_exit_codes` to `test_chain.py`: run `run_chain.py` via `subprocess` for both modes and assert exit codes 1 and 0, the sink's contents, and the flag absent in the defended run. This makes the Killercoda step 3 claims true.
- Accept: `make test` passes. The CI Lab 07 step is green.

**R02: Remove every false "real capture" claim** (landed `2b15028`) (fixes F3)
- Files: `README.md`, `killercoda/01-tool-poisoning/{intro,step2,finish}.md`, `labs/00-template/README.md` (the line "The cassette is a recording of a real susceptible model run").
- Change: state plainly that the shipped cassettes are labelled placeholders until R07 lands, and what that means (the side effects are live, the flag is not delivered). Remove the flag value from `finish.md`.
- Accept: `grep -rn "gpt-oss-20b" README.md killercoda/` returns only lines next to a statement about a cassette with `"status": "recorded"`. Nothing claims a capture that doesn't exist.

**R03: Fix factual errors in the Lab 07 teaching text** (landed `f03c8de`) (fixes F4 partly, F5 partly, F19)
- Files: `docs/index.html`, `killercoda/07-kill-chain/{step2,step3,finish,intro}.md`, `labs/07-.../README.md`, `labs/07-.../defenses.py` comment.
- Change:
  - authz breaks at **stage 4**
  - deduplicate `finish.md`
  - state that Stage 1 is a modelled injection (deterministic brain) and Stages 2-5 are live control-plane logic
  - state that Control 3 breaks this chain through human-in-the-loop, with the breaker as a backstop
  - add the relevance guarantee to the Lab 07 intro
- Accept: no occurrence of "stage 3" is attached to authz anywhere, and no "no simulation" claim covers Stage 1.

**R04: Remove committed runtime state and reset the seeds** (landed `4f5d23b`) (fixes F7 partly, F15)
- Change:
  - `git rm --cached labs/06-.../data/exfil_log.json labs/06-.../data/notes_store.json labs/05-.../memory/{memory.json,episodic.json,audit.jsonl}` and gitignore them.
  - Make `notes_store.py` fall back to the seed when the store is missing (`load_notes` → `reset_notes()` if absent). Check first: it may already behave this way through `_read_json` defaulting to `[]`. If it doesn't, make `agent.py` or the Makefile run `seed_notes.py --reset` before attacks.
  - Make Lab 05 run `seed.py` automatically when `memory.json` is missing.
  - Fix the `.gitignore` rule for Lab 03's `sandbox/docs/` so only `status-report.md` is ignored.
- Accept: on a fresh clone, `git status` stays clean after running each lab's attack or replay. A fresh Lab 05 benign session makes no request to `/exfil`.

---

_This version of the report stops at Phase A (R01-R04). Findings F1-F30 above describe the remaining gaps; later work orders are not included here._