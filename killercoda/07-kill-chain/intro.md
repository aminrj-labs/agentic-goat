# Watch a five-stage kill chain play out — no model, no GPU, no setup

This scenario runs the **MCP to A2A Kill Chain** (Lab 07) live and deterministically.
Every stage is real control-plane logic on the Python standard library -- no simulation,
no model, no GPU.

## What you will do

1. Run the **undefended** chain: five stages, HR data exfiltrated, exit code 1.
2. Run with **all controls** on: the chain breaks at stage 2, exit code 0.
3. Run the **test suite** that proves each control independently breaks its own stage.

## Why this matters

From a single poisoned tool description to a five-stage multi-agent kill chain that
crosses the MCP-to-A2A trust boundary -- then survives removal of the malicious server.
Each of three controls provably breaks the chain at a specific stage.

This is the flagship scenario of [AgenticGoat](https://github.com/aminrj-labs/agentic-goat).

## Prerequisites

None. Just this terminal. Python 3.11+ is pre-installed on the Ubuntu image.
