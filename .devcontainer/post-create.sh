#!/usr/bin/env bash
set -euo pipefail

# Install Python dependencies for all labs. Failures are not swallowed:
# if a lab's requirements cannot be installed, boot should stop so the
# gap is visible.
#
# Lab 04 is skipped by default: its requirements pull in the heavy
# chromadb + sentence-transformers + Jupyter stack. Install it on demand:
#   pip install -r labs/04-rag-security/requirements.txt
for lab in labs/*/; do
  if [ -f "${lab}requirements.txt" ]; then
    name="$(basename "$lab")"
    if [ "$name" = "04-rag-security" ]; then
      echo "Skipping ${name}: heavy ML stack (chromadb, sentence-transformers, Jupyter)."
      echo "  Install on demand: pip install -r labs/04-rag-security/requirements.txt"
      continue
    fi
    echo "Installing Python deps for ${name}..."
    pip install -r "${lab}requirements.txt" -q
  fi
done

# Install npm dependencies for labs that need them
for lab in labs/*/; do
  if [ -f "${lab}package.json" ]; then
    echo "Installing npm deps for $(basename "$lab")..."
    (cd "$lab" && npm install --silent)
  fi
done

# Lab 01's replay reads the canary file; create it now so the replay
# walkthrough works immediately after boot.
python3 labs/01-mcp-tool-poisoning/make_canary.py

# Install pytest (needed for Lab 07 tests)
pip install pytest -q

echo "AgenticGoat environment ready."
echo "  - Python $(python3 --version 2>&1)"
echo "  - Node.js $(node --version 2>&1)"
echo "  - Pip packages installed for all labs (Lab 04's ML stack on demand)"
echo ""
echo "Quick start:"
echo "  cd labs/07-mcp-to-a2a-kill-chain && make run   # zero-install kill chain"
echo "  cd labs/01-mcp-tool-poisoning && python3 agent.py --replay cassettes/attack1.json \\"
echo "    attack1_direct_poison.py \"@modelcontextprotocol/server-filesystem:~\" \"What is 47 plus 38?\"   # replay, no model needed"
