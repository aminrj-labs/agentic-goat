# ~/mcp-lab/defenses/read_only_docker_server.py
# The Lab 02 defense: separate inspection from actuation.

# The vulnerable docker_mcp_server.py mixes inspection (docker_ps,
# docker_inspect) with actuation (docker_stop) and outbound collection
# (docker_env, docker_health_report, which POSTs data to an external
# endpoint). This server exposes only the inspection tools. An agent
# served by it cannot stop containers, cannot read container
# environments, and has no tool that sends data anywhere, which is the
# "Separate inspection from actuation" control from the lab README.

import subprocess, json
from mcp.server.fastmcp import FastMCP

mcp = FastMCP('docker-mcp-readonly')

@mcp.tool()
def docker_ps() -> str:
    """List all running Docker containers. Returns container IDs, names, status."""
    result = subprocess.run(['docker', 'ps', '--format',
        '{{.ID}}|{{.Names}}|{{.Status}}|{{.Image}}'],
        capture_output=True, text=True)
    return result.stdout or 'No containers running'

@mcp.tool()
def docker_inspect(image_name: str) -> str:
    """Inspect a Docker image and return its metadata (read-only, no labels-based actions)."""
    result = subprocess.run(['docker', 'inspect', image_name],
        capture_output=True, text=True)
    return result.stdout[:3000] if result.returncode == 0 else f'Error: {result.stderr}'

@mcp.tool()
def docker_mcp_tools_list() -> str:
    """List the tools available on this read-only server."""
    tools = [
        {'name': 'docker-mcp-readonly', 'tools': ['docker_ps', 'docker_inspect', 'docker_mcp_tools_list']},
    ]
    return json.dumps(tools, indent=2)

if __name__ == '__main__':
    mcp.run()
