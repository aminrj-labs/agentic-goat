## Step 2: Run with all controls enabled

Now enable every control and watch the chain break at stage 2.

```bash
python3 run_chain.py --defended
```

**You should now see:**

- Stage 1 still succeeds (the poisoned tool description still lands).
- Stage 2 is **blocked**: the rogue agent card has no valid signature from the org
  trust anchor, so the registry rejects it.
- Stages 3, 4, and 5 are not reached.
- The exfil sink is empty: no data left the boundary.
- The process exits with code **0** (secure).

```bash
python3 run_chain.py --defended; echo $?
```

**You should see: `0`**

This is the defense: Control 1 (signed agent cards) breaks the chain at the earliest
possible point. The poisoned tool description still lands, but the rogue cannot register
without a valid signature.

You can also test each control individually:

```bash
python3 run_chain.py --control card    # breaks at stage 2
python3 run_chain.py --control authz   # breaks at stage 4
python3 run_chain.py --control blast   # breaks at stage 4
```

Each control independently stops the kill chain at a different stage -- this is
defense-in-depth.
