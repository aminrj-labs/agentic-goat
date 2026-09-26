## Step 2: Replay the attack

Start the exfiltration receiver, then replay the recorded attack against the live
MCP servers. The agent runs in replay mode -- it replays the tool calls in
`cassettes/attack1.json`, which is a placeholder cassette
(`"status": "placeholder"`), not a capture from a real model.

```bash
cd "$HOME/agentic-goat/labs/01-mcp-tool-poisoning"
source venv/bin/activate

# Terminal 1: Start the exfil receiver (background)
PYTHONUNBUFFERED=1 python3 exfil_server.py &
sleep 2

# Terminal 2 (or same terminal): Replay the attack
python3 agent.py --replay cassettes/attack1.json \
  attack1_direct_poison.py "@modelcontextprotocol/server-filesystem:~" \
  "What is 47 plus 38?"
```

**You should now see:**

- The agent connects to both MCP servers (the poisoned attacker server and the real
  MCP filesystem server) and loads their tools, including the poisoned `add` tool
  whose description contains hidden `[IMPORTANT]` instructions.
- The agent asks the user's question: "What is 47 plus 38?"
- The agent calls `read_file` on the canary file (the hidden step the user never
  sees). The live filesystem server performs that read.
- The agent calls `add(a=47, b=38, sidenote=...)` -- the exfiltration channel, with
  the "innocent" parameter that carries the payload. Because the cassette is a
  placeholder, the payload is the recorded text, not the canary file contents.
- The agent returns the answer: "47 + 38 = 85".

The user sees only "85". The attacker's listener receives the `sidenote` payload,
so the live exfiltration path is exercised end to end; a placeholder cassette
simply cannot deliver the flag. Record a real capture (see the lab's
`cassettes/README.md`) and the same replay delivers the canary contents.
