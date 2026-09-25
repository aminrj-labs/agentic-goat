#!/usr/bin/env bash
set -e

# Install Python dependencies for all labs
for lab in labs/*/; do
  if [ -f "${lab}requirements.txt" ]; then
    echo "Installing Python deps for $(basename $lab)..."
    pip install -r "${lab}requirements.txt" -q 2>/dev/null || true
  fi
done

# Install npm dependencies for labs that need them
for lab in labs/*/; do
  if [ -f "${lab}package.json" ]; then
    echo "Installing npm deps for $(basename $lab)..."
    (cd "$lab" && npm install --silent 2>/dev/null || true)
  fi
done

# Install pytest (needed for Lab 07 tests)
pip install pytest -q 2>/dev/null || true

echo "AgenticGoat environment ready."
echo "  - Python $(python3 --version 2>&1)"
echo "  - Node.js $(node --version 2>&1)"
echo "  - Pip packages installed for all labs"
echo ""
echo "Quick start:"
echo "  cd labs/07-mcp-to-a2a-kill-chain && make run   # zero-install kill chain"
echo "  cd labs/01-mcp-tool-poisoning && make setup    # model-dependent lab"
