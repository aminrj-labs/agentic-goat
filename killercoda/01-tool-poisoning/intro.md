# Watch a poisoned MCP tool description coerce an agent into stealing data

This scenario replays an MCP tool poisoning attack against live, unmodified lab
components -- no model, no GPU. The agent runs in **replay mode** against a
placeholder cassette (`"status": "placeholder"`): the MCP servers, exfil receiver,
and canary all execute live, and the side effects you observe are real, but the
recorded payload is not a capture, so it does not contain the lab flag.

## What you will do

1. Clone the repository, install dependencies, and create the synthetic canary file.
2. Replay the attack: the agent reads the canary and passes it silently to the attacker.
3. Watch the exfiltration arrive at the localhost receiver.

## Why this matters

MCP tool poisoning exploits the fact that **LLMs read tool descriptions before calling
tools**. A malicious MCP server embeds hidden instructions inside a tool's description
field. When the model loads the tool, it follows those instructions: it silently reads
a file and passes the contents as an innocent-looking parameter, before completing the
user's visible request.

The user sees a normal answer. The attacker receives stolen data.

This is the foundational attack that [Lab 01](https://github.com/aminrj-labs/agentic-goat/blob/main/labs/01-mcp-tool-poisoning/README.md)
teaches, and the entry point to the full kill chain in [Lab 07](https://github.com/aminrj-labs/agentic-goat/blob/main/labs/07-mcp-to-a2a-kill-chain/README.md).

## Prerequisites

None. Just this terminal. Python 3.11+ and Node.js 18+ are pre-installed on the
Ubuntu image; step 1 creates the venv (installing `python3-venv` first if it is
missing).

## Relevance guarantee

The vulnerable components (MCP servers, exfil receiver, canary) are the **real,
unmodified lab components**. Only the model's inference is pre-recorded in a
cassette, and the exploit's side effects are produced live. The shipped cassette is
a placeholder (`"status": "placeholder"`), not a capture: replay exercises the live
plumbing, but the payload it delivers does not contain the lab flag. Record a real
capture as described in `labs/01-mcp-tool-poisoning/cassettes/README.md` to change
that. This is falsifiable: run with `--llm` against your own model to see if it
complies.
