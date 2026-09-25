## Step 3: Run the test suite

The pytest suite pins both the undefended and defended outcomes, and verifies that
each single control breaks its own stage.

```bash
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

---

## What next?

- **Read the full lab** at [labs/07-mcp-to-a2a-kill-chain/README.md](https://github.com/aminrj-labs/agentic-goat/blob/main/labs/07-mcp-to-a2a-kill-chain/README.md) for the detailed walkthrough.
- **Watch the traces** side by side at the [static trace viewer](https://aminrj-labs.github.io/agentic-goat/).
- **Run it locally** with your own model: `cd labs/07-mcp-to-a2a-kill-chain && make run`.
- **Open in Codespaces** for a full dev environment: click the "Open in Codespaces" badge in the repo README.

## Flag captured

```
AGENTICGOAT{07_kill-chain}
```

Captured by observing the undefended run exfiltrate the HR record and flag to the
exfil sink. The defended run produces an empty sink.
