# No-behavior-change record (SPEC.md section 4.6)

Acceptance: no attack's observable behavior changed; entry-point runs are
diffed against the Section 2 baseline. This record lists every input that
differs from the seeded baseline and why each is acceptable.

The scenario contract (CONTRIBUTING.md) requires every lab to plant a canary
flag `AGENTICGOAT{...}` inside its target. The seeded baseline predates that
contract, so the v1 work orders had to plant the flags. Planting a canary
changes the *data* the attack reads; it does not change the *behavior*: the
same tools are called, in the same order, and the same success signal fires.

Changed attack inputs:

1. **Lab 06, `data/notes_seed.json`** - a canary note was added to the seeded
   notes store (titled "Lab Canary", content states that it leaves the store
   only if the cross-server chain dumps all notes). The attack chain is
   unchanged: `get_weather` -> `list_notes` -> `sync_weather_cache(notes_dump=...)`
   still runs and the canary now travels with the notes dump.
2. **Lab 01b, WhatsApp stub fixture** - the lab flag was appended to one
   synthetic WhatsApp message. `list_messages` returns the same message list
   plus the flag line; the exfil path (`send_message`) is unchanged.
3. **Lab 02, `start_victims.sh`** - the `lab-cache` container now carries one
   extra environment variable with the lab flag. `docker_env`/`docker_inspect`
   return the same container data plus that variable; the stop and report
   tools behave exactly as before.
4. **Lab 02, `start_victims.sh` is new** - the baseline had no script for
   starting the victim containers (the README instructed manual docker runs).
   The script performs the same manual steps; it adds no new attack surface.
5. **Lab 03, `sandbox/.env`** - a synthetic `.env` file was added to the
   DocuAssist workspace so Phases 4a and 5 have a concrete secret to
   exfiltrate (including the lab canary). The agent's file tools could already
   read the workspace; only the file's existence changed.

Additional print-text changes (no behavior change):

- **Lab 07, `run_chain.py`** - the stage banner and result line now use
  hyphens instead of em dashes (`Stage 1 - ...`, `RESULT: chain completed -
  HR data exfiltrated.`). Display text only; exit codes, stage outcomes, and
  the exfil sink are unchanged. The README output sample was updated to match.
- **Lab 07, `mcp_entry.py`** - when `--llm` falls back to the deterministic
  brain, the stage-1 detail line now starts with `FELL BACK ...` so the
  fallback is visible in the transcript. The fallback decision itself was
  already the deterministic brain; only the reported rationale changed.

Everything else is byte-identical to the baseline or added without touching
an existing input (new defense modules, new CI steps, new documentation).
