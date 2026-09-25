## Step 1: Run the undefended kill chain

The undefended run is the attack. Every stage succeeds.

```bash
cd /home/user/agentic-goat/labs/07-mcp-to-a2a-kill-chain
python3 run_chain.py
```

**You should now see:**

- Five stages listed, each marked as succeeded by the attacker.
- Stage 4 exfiltrates the HR record: `EMP-4471 Jane Okafor salary=182000 SSN=***-**-4471`.
- The flag `AGENTICGOAT{07_kill-chain}` is captured.
- The process exits with code **1** (compromise reached).

```bash
echo $?
```

**You should see: `1`**

This is the vulnerability: without any controls, a poisoned MCP tool description is the
entry point to a five-stage kill chain that exfiltrates HR data and persists after the
malicious server is removed.
