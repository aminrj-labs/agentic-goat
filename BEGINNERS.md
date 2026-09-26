# AgenticGoat in plain words

A beginner's guide: what this repo is, what the terms mean, how a lab works, and
how to run your first one. No AI-security background assumed.

Before running anything, read the Responsible use section at the top of the
[README](./README.md). The targets are deliberately insecure; run them only on
your own machine or in a sandbox.

## The 30 second version

An AI agent is a program where a language model (a chatbot "brain") is given
tools it can call: read a file, run a Docker command, send an email, fetch a
web page. The model reads its instructions, reads the data the tools return,
and decides the next tool call. The catch is that the model cannot reliably
tell the difference between data and instructions. So a malicious sentence
hidden in a tool's result, a document, or a memory entry can redirect the whole
agent. That trick is **prompt injection**, and it is the core attack in this
repo.

AgenticGoat is a set of small, self-contained labs. Each lab builds a
deliberately vulnerable target, runs one real attack technique against it, and
pairs the attack with the defense that stops it. Everything is synthetic: fake
secrets, fake people, fake companies, and all "exfiltration" only ever goes to
`localhost`, your own machine.

## Key terms

- **Agent.** The program under test: a model plus a loop that calls tools and
  feeds the results back to the model.
- **MCP (Model Context Protocol).** The standard way agents get tools from
  "servers". Every tool has a name and a description, and the model reads both.
  Lab 01 poisons that description.
- **A2A (agent to agent).** Agents calling other agents across a trust
  boundary. Lab 07 crosses that boundary.
- **Prompt injection.** Malicious instructions smuggled into data the model
  reads: a document, a tool result, a memory entry, an image label.
- **Canary.** A synthetic secret (a "flag" such as `AGENTICGOAT{...}`) planted
  in the target. It is the proof: if it reaches the attacker's listener, the
  attack worked.
- **Exfil (exfiltration).** Getting data out of the target. In these labs it
  always means sending the canary to a listener on `localhost`.
- **Control (or defense).** The fix. Each lab ends with the control that makes
  the same attack fail.
- **Cassette.** A recording of the model's tool calls from one run. Replaying
  a cassette re-runs the side effects without needing a model. The cassettes
  shipped today are labelled `"status": "placeholder"`: they exercise the live
  plumbing, but they do not deliver the flag until a real capture is recorded.
- **Live vs replay.** Live points the agent at your own local model (Ollama or
  LM Studio). Replay plays the cassette.

## How a lab works

1. A canary is planted in the vulnerable target.
2. The attack runs: the agent is tricked into reading the canary and sending
   it to the attacker's listener.
3. Success is observable: the canary appears at the listener. A benign run
   never delivers it.
4. The control is switched on, the same attack is rerun, and it fails.

That loop is the whole game in every lab.

## The labs, in one line each

- **01, MCP tool poisoning.** A hidden instruction in a tool description makes
  the agent read a file it should not and send it away.
- **01b, cross server shadowing.** One server's tool result hijacks how the
  agent uses a second server's tool.
- **02, DockerDash.** An instruction hidden in Docker image metadata makes the
  agent destroy a container and leak the container inventory.
- **03, red team assessment.** A methodology lab: automated red teaming of an
  agent with PyRIT-style and Promptfoo-style tooling.
- **04, RAG security.** A poisoned document in the knowledge base steers the
  agent into leaking data.
- **05, agentic memory attacks.** A poisoned memory entry survives across
  sessions and makes a later, innocent session exfiltrate.
- **06, cross server MCP poisoning.** A malicious server steers the agent into
  abusing a second, trusted server.
- **07, MCP to A2A kill chain (flagship).** Five stages across two trust
  boundaries, from a poisoned tool to persistence after the rogue server is
  removed. Three controls, each breaking the chain at a specific stage. Runs
  with no model at all.

## Running your first lab

### Zero setup: Lab 07

Only Python is needed. No model, no GPU, no keys:

    cd labs/07-mcp-to-a2a-kill-chain
    make run        # the attack succeeds, HR data leaks (exit 1)
    make defended   # controls on, the chain breaks (exit 0)
    make test       # proves the above

### With a local model: Lab 06

1. Install Python 3.11+ and a local model server. Ollama is the default:
   install it, then pull a model:

       ollama pull qwen2.5-7b-instruct

   LM Studio works the same way. Some other labs also need Node.js 18+; the
   lab README will say.
2. Then, in two terminals:

       cd labs/06-ASI02-cross-server-mcp-poisoning
       make setup            # venv + dependencies
       source venv/bin/activate
       make verify           # checks your model does tool calling
       make seed             # plants the synthetic "sensitive" notes
       make exfil            # terminal 1: the attacker's listener
       make attack           # terminal 2: the vulnerable agent

You watch the agent answer a harmless weather question while the canary notes
arrive in Terminal 1.

Each lab has its own quick start in its README, and the top-level
[README](./README.md) covers the same ground.

### No install at all: Codespaces

The "Open in Codespaces" badge in the README starts a free cloud workspace
with everything preinstalled. You get the same labs, in the browser.

## Where to go next

- Read one lab end to end. Lab 01 is the gentlest introduction; Lab 07 is the
  most complete.
- Watch the [trace viewer](./docs/index.html): Lab 07's attack and defended
  runs side by side, step by step.
- See [CONTRIBUTING.md](./CONTRIBUTING.md) for what a lab must contain, and
  `labs/00-template/` for the fill-in scaffold.
