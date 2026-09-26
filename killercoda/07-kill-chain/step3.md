## Step 3: Run the test suite

The pytest suite pins both the undefended and defended outcomes, and verifies that
each single control breaks its own stage. The system Python is protected
(PEP 668), so create a venv, install pytest into it, and run from there:

```bash
cd "$HOME/agentic-goat/labs/07-mcp-to-a2a-kill-chain"
python3 -m venv venv || (apt-get update -qq && apt-get install -y -qq python3-venv && python3 -m venv venv)
source venv/bin/activate
pip install pytest -q
python3 -m pytest test_chain.py -v
```

**You should now see:**

- All tests pass (exit code 0).
- Tests confirm: undefended run exits 1 with HR data in exfil state.
- Tests confirm: defended run exits 0 with empty exfil state.
- Tests confirm: each single control (`card`, `authz`, `blast`) breaks its own stage.
- Tests confirm: Stage 1 lands deterministically in all configurations.

These tests are the same ones that run in CI on every push. They prove the kill chain
is deterministic and the controls work exactly as specified.
