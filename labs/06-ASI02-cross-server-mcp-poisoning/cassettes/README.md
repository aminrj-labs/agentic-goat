# Cassettes (record/replay)

A cassette records the lab's LLM answers (in call order) as plain JSON so the
attack can be replayed with **no model, no endpoint and no API key**.
Everything else stays live: both MCP servers, the notes store on disk and the
exfil listener on port 9999 (which appends to `data/exfil_log.json`). See the
module docstring of `cassette.py` for the file format.

The cassette `paris-weather.json` shipped with this repo is a **placeholder**
(`"status": "placeholder"`). It is not a capture: its assistant turns are
illustrative, and replaying it prints a loud warning. Replay still exercises
the real side effects: `get_weather` and `list_notes` run against the live
servers (the notes store must be seeded first), and `sync_weather_cache`
POSTs a real report to the exfil listener. With a placeholder, the report's
notes dump is illustrative and will not contain the lab canary. Record a real
capture as below to get the full effect.

## Replay (no model needed)

```
make seed                    # seed the victim store, including the canary note
python3 exfil_server.py      # terminal 1 (or: make exfil)
python3 agent.py \
  --server malicious_weather_server.py \
  --server legitimate_notes_server.py \
  --query "What is the weather in Paris?" \
  --replay cassettes/paris-weather.json --verbose   # terminal 2
grep -l AGENTICGOAT data/exfil_log.json && cat data/exfil_log.json
```

Expected: the agent answers with the weather only, and `data/exfil_log.json`
gains a `sync_weather_cache` entry. With a recorded cassette, the entry's
notes dump contains the marker line of the "Lab Canary" note, i.e. the flag
named in the lab README's Goal section.

## Record a real capture

Prerequisites: the victim store seeded (`make seed`) and an
OpenAI-compatible chat endpoint (for example `ollama serve` with a
function-calling model pulled).

```
export LLM_BASE_URL=http://localhost:11434/v1
export MODEL=gpt-oss-20b

python3 exfil_server.py      # terminal 1
python3 agent.py \
  --server malicious_weather_server.py \
  --server legitimate_notes_server.py \
  --query "What is the weather in Paris?" \
  --record cassettes/paris-weather.json --verbose   # terminal 2
```

The run overwrites `cassettes/paris-weather.json` with `"status": "recorded"`.
Commit the capture (the notes store only carries synthetic notes). The model
must follow the poisoned tool description on the recorded run; if it does not,
retry or note the failure in the cassette commit message. A recorded capture
is verified by replaying it (as above) and confirming
`grep -l AGENTICGOAT data/exfil_log.json` succeeds.
