## Step 1: Set up the environment

Clone the repository, install the dependencies into a venv, and create the
synthetic canary file.

```bash
git clone https://github.com/aminrj-labs/agentic-goat.git "$HOME/agentic-goat"
cd "$HOME/agentic-goat/labs/01-mcp-tool-poisoning"
python3 -m venv venv || (apt-get update -qq && apt-get install -y -qq python3-venv && python3 -m venv venv)
source venv/bin/activate
pip install "mcp>=1.0.0,<2.0.0" httpx flask openai -q
npm install
python3 make_canary.py
```

**You should now see:**

- The repository cloned to `~/agentic-goat` (on this image `~` is `/root`).
- `pip install` puts the Python dependencies into the venv. The system Python is
  protected (PEP 668), so the scenario uses a venv instead of a system-wide pip.
- `npm install` puts the real MCP filesystem server into `node_modules/`, at the
  version pinned by the lab's `package.json`.
- `make_canary.py` creates `~/.ssh/id_rsa.pub.demo` with a synthetic public key.
  This is the canary -- the file the attacker wants to steal. All data is synthetic.

The victim server is the real, unmodified npm package
`@modelcontextprotocol/server-filesystem`, which exposes the `read_file` tool the
poisoned description instructs the agent to call. `agent.py` launches it with the
syntax `@modelcontextprotocol/server-filesystem:~`, which roots it at the home
directory.
