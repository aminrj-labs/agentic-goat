## What the scenario showed

- Undefended, all five stages succeed: the poisoned tool description lands, the
  rogue registers, work routes to it, it exfiltrates the HR record and the flag,
  and the registration survives removal of the malicious server. Exit code 1.
- With all controls on, the chain breaks at stage 2 (exit code 0) and the exfil
  sink is empty. Each control alone breaks a different stage: card at 2, authz
  and blast at 4.
- The test suite you ran in step 3 pins all of that, and the same tests run in
  CI on every push.

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
