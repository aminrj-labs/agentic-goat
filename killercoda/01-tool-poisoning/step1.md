## Step 1: Set up the environment

Install the Python and Node.js dependencies, create the synthetic canary file, and
create a stub filesystem server (the "victim" MCP server).

```bash
cd /home/user/agentic-goat/labs/01-mcp-tool-poisoning
pip install "mcp>=1.0.0,<2.0.0" openai httpx flask -q
npm install @modelcontextprotocol/server-filesystem -q
python3 make_canary.py
```

**You should now see:**

- `make_canary.py` creates `~/.ssh/id_rsa.pub.demo` with a synthetic public key.
  This is the canary -- the file the attacker wants to steal. All data is synthetic.

Now create a minimal stub filesystem server for the victim:

```bash
cat > /tmp/fs_stub.py << 'PYEOF'
import os
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("filesystem")

@mcp.tool()
def read_file(path: str) -> str:
    """Reads a file from the local filesystem."""
    with open(os.path.expanduser(path), encoding="utf-8") as f:
        return f.read()

if __name__ == "__main__":
    mcp.run()
PYEOF
```

This stub is the same pattern as the real filesystem server, just trimmed for the
Killercoda environment. It exposes `read_file` which the poisoned tool description
instructs the agent to call.
