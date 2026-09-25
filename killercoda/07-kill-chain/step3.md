## Step 3: Run the test suite

The pytest suite pins both the undefended and defended outcomes, and verifies that
each single control breaks its own stage. Install pytest first, then run:

```bash
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
