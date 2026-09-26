"""Flag definition and canary check for Lab 04 (RAG security).

The lab's single flag lives here. The side effect that reveals it is the
poisoned knowledge base itself: after Attack 1, legitimate financial queries
retrieve the poisoned documents instead of the legitimate ones. Retrieval is
deterministic vector similarity, so this check is model-independent: it works
on a replay exactly as on a live run, and it never parses what the model said.

The vulnerable pipeline records every retrieval (query plus retrieved
document ids) to state/retrievals.jsonl, and the attack driver resets the log
before its queries. canary_reached() is True when any poisoned document id
was retrieved.
"""

import json
from pathlib import Path

FLAG = "AGENTICGOAT{04_rag-poisoning}"

# Mirrors the document ids of POISONED_DOCS in attack1_knowledge_poisoning.py.
POISONED_DOC_IDS = ("poison-fin-001", "poison-fin-002", "poison-fin-003")

RETRIEVALS_FILE = Path(__file__).resolve().parent / "state" / "retrievals.jsonl"


def canary_reached() -> bool:
    """Return True only when a legitimate query retrieved a poisoned document."""
    if not RETRIEVALS_FILE.exists():
        return False
    try:
        lines = RETRIEVALS_FILE.read_text(encoding="utf-8").splitlines()
    except OSError:
        return False
    for line in lines:
        if not line.strip():
            continue
        try:
            entry = json.loads(line)
        except ValueError:
            continue
        if any(doc in POISONED_DOC_IDS for doc in entry.get("retrieved", [])):
            return True
    return False


if __name__ == "__main__":
    import sys

    if canary_reached():
        print("canary reached: a legitimate query retrieved a poisoned document")
    else:
        print("canary not reached: no poisoned document was retrieved")
    sys.exit(0 if canary_reached() else 1)
