# Cassettes (record/replay)

A cassette records the lab's LLM answers (in call order) as plain JSON so the
attack can be replayed with **no model, no endpoint and no API key**.
Everything else stays live: document ingestion, ChromaDB retrieval with the
local sentence-transformer embeddings and the `ask` pipeline. See the module
docstring of `cassette.py` for the file format.

Attack 1 makes exactly three model calls (one per query in
`demonstrate_attack`), so the cassette always holds three turns.

The cassette `knowledge-poisoning.json` shipped with this repo is a
**placeholder** (`"status": "placeholder"`). It is not a capture: its answers
are illustrative and contain none of the poisoned figures, and replaying it
prints a loud warning. Replay still exercises the real side effects: the
poisoned documents are really injected into ChromaDB and really retrieved by
each query; only the final answers are replayed. Because the placeholder
answers carry no fabricated figures, the driver does not print the flag.
Record a real capture as below to get the flag capture.

## Replay (no model needed)

```
make seed                                  # legitimate company docs into ChromaDB
python3 attack1_knowledge_poisoning.py \
  --replay cassettes/knowledge-poisoning.json
```

Expected: the three poisoned documents are injected, each query retrieves the
poisoned chunks (watch the `[Retrieve]` lines), and the three replayed
answers are printed. With a recorded cassette whose answers contain the
fabricated figures, each matching answer is followed by the `POISONING
SUCCESS` marker and the flag named in the lab README's Goal section.

## Record a real capture

Prerequisites: the knowledge base seeded (`make seed`) and an
OpenAI-compatible chat endpoint (for example `ollama serve` with an
instruct model pulled).

```
export LLM_BASE_URL=http://localhost:11434/v1
export LM_STUDIO_MODEL=qwen2.5-7b-instruct

python3 attack1_knowledge_poisoning.py \
  --record cassettes/knowledge-poisoning.json
```

The run overwrites `cassettes/knowledge-poisoning.json` with
`"status": "recorded"`. Commit the capture (it contains only the company's
synthetic figures). The model must answer with the poisoned figures on the
recorded run; if it does not, retry or note the failure in the cassette commit
message. A recorded capture is verified by replaying it (as above) and
confirming the `FLAG CAPTURED` line appears.
