# Building the Kubernetes Goat of the agentic era

A strategy for turning `mcp-attack-labs` into the reference vulnerable-by-design environment for agentic AI security.

Date: 23 September 2026
Author: Amine (Molntek)

---

## The one-line answer

You already own the strongest starting point available: a runnable, honestly-scoped, framework-mapped set of attack chains that a competitor cannot buy their way past. The gap between what you have and "the goat" is not more attacks. It is the four things Madhu Akula did after the attacks existed: a zero-install front door, a fixed scenario contract, a framework crosswalk, and five years of showing up. This report maps his path, checks it against the rest of the goat family, surveys who else is building for agents right now, and gives you a named plan.

The recommendation: rename and reposition `mcp-attack-labs` as **AgenticGoat** (naming analysis in Part 5), keep the seven labs as the spine, and spend the next 90 days on distribution and the scenario contract rather than on new exploits.

---

## Part 1: How Kubernetes Goat actually got adopted

I read the origin story, the launch post, the scenario pages, the "how to run" matrix, the showcase page, and the OWASP crosswalk. Adoption did not come from the vulnerabilities. It came from a specific sequence.

### 1.1 The timeline that matters

- **2018 to 2019.** Before the Goat existed, Madhu was already running a three-day paid training, "Attacking and Auditing Docker Containers and Kubernetes Clusters," at Nullcon, Black Hat and DEF CON. The training came first. The scenarios were battle-tested on paying students who complained when something did not work.
- **25 June 2020.** Kubernetes Goat is announced with **14 scenarios** and, critically, a **free Katacoda browser playground** so anyone could try it "right from your browser" with no cluster to build. The launch post is explicit that setting up a real cluster is "complicated," so he removed that barrier on day one.
- **2020 to 2022.** It gets showcased at OWASP Bay Area, DEF CON Safe Mode Red Team Village, EkoParty, USENIX LISA 2021 (closing note), SANS CloudSecNext 2021 and 2022, Black Hat Europe 2021 Arsenal, and FIRST Amsterdam 2022. Featured in the Kubernetes Podcast, tl;dr sec, and CloudSecList.
- **Later.** Scenarios grow to **22**, an OWASP Kubernetes Top 10 crosswalk and a MITRE mapping get added, and the docs site becomes the actual product.
- **Today.** 5,700 stars, 1,000 forks, roughly 40 contributors, MIT license, its own Discord, a "Wall of Love," and an adopters page.

The lesson in one sentence: **the vulnerabilities were the easy part; the adoption came from removing setup friction, keeping a rigid scenario format, mapping to a framework people already cited, and being physically present at a dozen conferences a year for years.**

### 1.2 The five design decisions that did the work

**Decision 1: A zero-install front door.**
The single biggest lever. Katacoda (later the docs "how to run" matrix across kind, GKE, EKS, AKS, K3S) meant a curious person went from "heard about it" to "hands on a shell" in under a minute, with nothing to install. Everyone who tried it in the browser was a candidate to later run it for real, contribute a scenario, or put it in a talk. Your labs currently require Python 3.11, a local model with function calling, Node 18, and two terminals before the first attack lands. That is a wall.

**Decision 2: A rigid, repeatable scenario contract.**
Every Kubernetes Goat scenario page is the same shape: Overview, then The story, then Goal (find this specific flag), then Hints and Spoilers (collapsed), then Solution and Walkthrough (Method 1, Method 2), then References. The story is one paragraph of real-world framing. The goal is a concrete capture target (`k8s_goat_flag` via the `k8svaultapikey` secret). Hints are progressive so a learner can get unstuck without seeing the answer. This sameness is what lets a trainer drop any scenario into a class, a vendor drop one into a demo, and a contributor add a new one without a design meeting. Your labs already have a five-section structure (What it demonstrates, Prerequisites, Setup, Expected outcome, Defense), which is close, but it lacks the two things that make Goat scenarios *sticky*: a named capture flag and collapsed progressive hints.

**Decision 3: Map to a framework people already cite.**
The OWASP Kubernetes Top 10 crosswalk turned the Goat from "a pile of hacks" into "the hands-on companion to the framework." When someone reads K03 Overly Permissive RBAC, there is a Goat scenario waiting. The framework did the demand generation; the Goat captured it. You have the equivalent frameworks handed to you: the **OWASP Top 10 for Agentic Applications (ASI01 to ASI10, published 9 Dec 2025)** and the **OWASP MCP Top 10 (MCP01 to MCP10)**. You are a contributor to both working groups. Nobody is better positioned to own the crosswalk.

**Decision 4: Explicitly serve four audiences, including the ones who bring budget.**
The docs name them: attackers and red teams, defenders and blue teams, developers and DevOps, and the commercially decisive one, **products and vendors**. Madhu wrote openly that vendors started using the Goat in sales calls to show their tool catches real issues, and he leaned into it. That is what made the project infrastructure rather than a hobby: security vendors needed a neutral, credible target to demo against, and the Goat was it. The agentic security tool market is now in exactly that phase (MCP scanners, runtime gateways, agent-identity products all need a demo target), and no neutral, credible one has won yet.

**Decision 5: Attack and defense in the same environment.**
Goat is not only offense. Scenarios 17 to 22 are defensive: KubeAudit, Falco, Popeye, network policy, Cilium Tetragon, Kyverno. This is what let blue teams and vendors adopt it, not just red teams. Your labs already pair each attack with the control that stops it, and Lab 07's `--defended` flag is exactly this instinct done well. Keep and amplify it.

### 1.3 What did *not* drive adoption (so you can stop worrying about it)

- Not scenario count. It launched with 14 and was already spreading; it is at 22 six years later. Depth per scenario beat breadth.
- Not novel zero-days. Almost every scenario is a known misconfiguration class, documented well. The value was pedagogy, not novelty.
- Not a slick UI. The "home" app is a plain scenario launcher. The docs site is the product.

---

## Part 2: Cross-checking against the rest of the goat family

Kubernetes Goat is one data point. The pattern holds across the family, and each sibling adds one lever worth stealing.

| Project | Who | The lever that made it spread |
|---|---|---|
| **WebGoat** | OWASP | The original. Named the genre. "Goat" now signals "deliberately vulnerable teaching target" to every security person alive. |
| **OWASP Juice Shop** | Björn Kimminich | A **companion book** (*Pwning OWASP Juice Shop*), a **CTF export tool** (`juice-shop-ctf`) that plugs into CTFd and RootTheBox, and **MultiJuicer** to run one instance per student on Kubernetes. The lesson: the ecosystem *around* the target (book, CTF, multi-tenancy) drove classroom adoption more than the target itself. |
| **CI/CD Goat** | Cider Security (acquired by Palo Alto) | **The taxonomy author shipped the goat.** Cider wrote the Top 10 CI/CD Security Risks, then released the Goat as its hands-on companion, themed around Alice in Wonderland with 11 challenges in CTFd. Owning the framework and the lab together is the strongest possible position, and it is the one available to you. |
| **CloudGoat, TerraGoat, AI Goat (Orca)** | Rhino, Bridgecrew, Orca | Vendor-built goats as **top-of-funnel marketing** that also became genuine community tools. Proves the goat-as-lead-generator model that your Scorecard already implements. |
| **AI Goat (AI Security Consortium)** | Community | 17 labs, 9 CTF challenges, **3 progressive defense levels (L0 vulnerable, L1 hardened, L2 NeMo Guardrails)**. The defense-level ladder is a strong pattern: same attack, watch it succeed then fail as you turn on controls. |

Three levers to lift directly: **a companion artifact** (you have the book, *Agentic Security in Practice*, and the labs should be its runnable appendix), **a CTF/flag layer** (Juice Shop's `-ctf` export), and **a defense-level ladder** (AI Goat's L0/L1/L2, which generalizes your Lab 07 `--defended` flag to every lab).

---

## Part 3: The competitive landscape for an agentic goat

I surveyed everything currently being built or used. This is the part that decides your positioning, so I am being blunt about where each one is strong and where the gap sits.

### 3.1 The field, grouped by what they actually are

**Single-vector teaching agents (narrow, mature, well-known)**

- **Damn Vulnerable LLM Agent (DVLA)**, Reversec/WithSecure, from a BSides London 2023 CTF. A LangChain ReAct banking chatbot for Thought/Action/Observation injection. One idea, taught very well. The template most people copy. Narrow by design.
- **Damn Vulnerable MCP Server (DVMCP)**, Harish Santhanalakshmi Ganesan. 10 challenges across easy/medium/hard (prompt injection, tool poisoning, rug pull, shadowing, token theft, RCE), each on its own port, Docker. The best-known MCP-specific lab. Widely cited (Bishop Fox, tl;dr sec). Static challenges, single-server, no agent-to-agent, no orchestration.

**MCP-server target collections (scanner fodder)**

- **Appsecco Vulnerable MCP Servers Lab**, 9 realistic vulnerable servers, each with a ready `claude_config.json`, roughly 263 stars. More production-like than DVMCP; good for testing whether client-side mitigations hold. From the Appsecco lineage (Madhu's old company). A collection, not a graded course, and not agentic, since it stops at the MCP server boundary.
- **MCPGoat / mcp-goat (several unrelated projects)**, the name is already crowded and contested. One (SabyasachiDhal) has 26 challenges across 3 difficulty levels, 78 flags in total, with a victim-agent harness; it explicitly disclaims affiliation with any other "vulnerable MCP" project. Another (anmolparida) is a scanner punching bag with mocked tool bodies. This name collision is a real problem you must route around (see Part 5).

**Full agentic CTF platforms (your actual competition)**

- **OWASP FinBot CTF**, the serious one. Positioned explicitly as "the Juice Shop for Agentic AI," under the OWASP GenAI Security Project's Agentic Security Initiative. A multi-agent fintech vendor-management platform with real MCP tools (Findrive, FinStripe, FinMail, TaxCalc), event-driven exploit detection (no static flags), namespace isolation per player, and a hosted `owasp-finbot-ctf.org`. Mapped to LLM Top 10, Agentic Top 10, CWE, ATLAS. GSoC 2026 project, RSAC 2026 demo. **Weaknesses:** it requires an OpenAI key (or Ollama), it is Docker Compose or hosted only (no Kubernetes story), and it sits at 87 stars with 234 open issues and 182 open PRs, so it is a large, ambitious, still-stabilizing community build. It is single-domain (fintech), and it is a *platform you play*, not a *toolkit you learn the mechanisms from and rebuild*.
- **Damn Vulnerable AI Agent (DVAA)**, OpenA2A. 21 agents across API/MCP/A2A, 12 vulnerability categories, 22 CTF challenges (5,900 pts), 85 infra scenarios, 5 multi-step kill chains, a dashboard, and OASB benchmark integration. Docker one-liner, simulated LLM backend so it runs with **zero external dependencies and no key** (a real strength). **Weakness, and it is the important one:** it is a funnel for OpenA2A's own commercial products. Every "from attack to defense" row routes you to their AIM, HackMyAgent, Secretless, BrowserGuard. It is marked "reference-only," sits at 112 stars, and is single-vendor. It is not neutral, and neutrality is the whole game for a goat.

**Games and benchmarks (adjacent, not goats)**

- **Lakera Gandalf: Agent Breaker** (Sept 2025), a polished hosted game, 10 mock GenAI apps, tool abuse and exfiltration, feeding Lakera's products and their open LLM-backend benchmark (19,433 crowdsourced attacks, 31 models). Closed, hosted, commercial. Not self-hostable, not a teaching toolkit. You already flagged Lakera as the reason "first hosted playground" is gone, which is correct, and it does not threaten a self-hostable-toolkit position.
- **AgentDojo** (ETH Zurich, Debenedetti et al., NeurIPS 2024), the academic *benchmark* for indirect prompt injection across Workspace/Banking/Travel/Slack, with deterministic success checks. This is the research standard, not a learning lab, and note: **there is already a well-known thing called "AgentDojo."** Your internal `agentdojo-live` name collides with it. Do not ship anything publicly under an "AgentDojo" name.
- **Microsoft AI Red Teaming Playground Labs**, 12 Chat-Copilot-based challenges from the Black Hat USA 2024 course, PyRIT integration, 2.1k stars. Prompt-injection and RAI focused, not agentic/MCP/A2A. Adjacent.
- **Steck43/owasp-dual-top10-lab, AASTF, precize/Agentic-AI-Top10**, smaller framework-crosswalk and scenario-registry efforts. Fragmented, early.

### 3.2 The honest read: is the seat taken?

**The "hosted single-domain CTF you play" seat is being taken by FinBot**, with OWASP's brand behind it. Do not fight there. You will not out-resource an OWASP workstream with GSoC students on a hosted fintech platform.

**The "vulnerable-by-design *toolkit* you learn the mechanisms from, self-host anywhere, and map to the frameworks" seat is open.** This is precisely what Kubernetes Goat is for its domain, and precisely what no agentic project has won:

- DVMCP and DVLA are too narrow (one protocol, one vector).
- FinBot and DVAA are platforms you *play*, not toolkits you *dissect and rebuild*, and one needs a key while the other is a vendor funnel.
- Nobody covers the **full chain** (MCP tool layer, then memory/RAG, then agent identity, then the **A2A trust boundary and multi-agent orchestration**) as reproducible, framework-mapped, defense-paired scenarios. Your Lab 07 already does the hardest part of this that everyone else is missing: it crosses the MCP-to-A2A boundary and shows a control breaking the chain.

That is your wedge, and it is defensible for three reasons a competitor cannot copy quickly:

1. **The A2A / multi-agent kill chain.** Everyone else stops at a single agent or a single MCP server. You already run a five-stage chain across the agent-to-agent trust boundary. This is the frontier and it is the hardest to build.
2. **Framework authorship.** You contribute to the OWASP Agentic Top 10 and MCP Top 10 working groups. FinBot maps to the frameworks; you help write them. Own the *canonical crosswalk*, the way CI/CD Goat's authors owned theirs.
3. **Radical neutrality.** DVAA funnels to OpenA2A's products; Lakera funnels to Lakera; FinBot is a single OWASP workstream's platform. A vendor-neutral, self-hostable teaching toolkit is the thing MCP-security vendors, trainers, and universities can all adopt without endorsing anyone. That is the Kubernetes Goat position exactly.

---

## Part 4: What the project should be

### 4.1 Positioning statement

> The vulnerable-by-design toolkit for learning agentic AI security by breaking and defending it. Self-hostable anywhere, runs on a local model with no API keys, and mapped scenario-for-scenario to the OWASP Top 10 for Agentic Applications and the OWASP MCP Top 10. From a single poisoned tool description to a five-stage multi-agent kill chain, every attack is paired with the control that stops it.

The three claims a competitor cannot match, stated plainly on the landing page: **it runs offline on a local model** (unlike FinBot's key), **it is vendor-neutral** (unlike DVAA), and **it covers the full chain through A2A and multi-agent** (unlike DVMCP and everyone else).

### 4.2 The scenario contract (adopt this before writing any new lab)

Rewrite every lab README to a fixed shape, lifted from Kubernetes Goat and adapted for agents:

1. **Overview.** One paragraph, the mechanism.
2. **The story.** One paragraph of real-world framing tied to a named public incident (EchoLeak, the Supabase/Cursor tool-poisoning case, the Amazon Q extension, the Sept 2026 OpenAI/Hugging Face agentic breach, the Unit 42 A2A session-smuggling write-up). This is what makes it memorable and what a vendor quotes in a demo.
3. **Goal / flag.** A concrete capture target with a named flag (for example, `agent_goat_flag` recovered by exfiltrating a synthetic secret through the poisoned tool). Deterministic, checkable, the thing that makes it CTF-able.
4. **Framework mapping.** The ASI0x and/or MCP0x IDs, plus MITRE ATLAS, in a fixed header block.
5. **Hints and spoilers.** Collapsed, progressive (2 to 3 nudges), so learners get unstuck without the answer.
6. **Solution and walkthrough.** The working attack, step by step.
7. **Defense / mitigation.** The control that stops it, with a `--defended` (or defense-level) toggle so the learner watches it break, then hold.

The two things you are adding to your current structure are the **named flag** (item 3) and the **collapsed progressive hints** (item 5). Those two turn a demonstration into a course.

### 4.3 The scenario catalog, mapped to the frameworks

Your seven labs already cover the core. Here is the full target catalog against ASI01 to ASI10 and MCP01 to MCP10, marking what you have (done), what is partial (partial), and what to build (build). This crosswalk *is* a shippable artifact on its own, so publish it as the README table.

| ASI / MCP | Risk | Scenario | Status |
|---|---|---|---|
| **ASI01** | Agent Goal Hijack | Indirect prompt injection via tool output / RAG (Lab 04) | done |
| **ASI02 / MCP03** | Tool Misuse and Exploitation / Tool Poisoning | Poisoned tool description leading to silent file read and exfil (Lab 01); cross-server poisoning (Lab 06) | done |
| **ASI02 / MCP03** | Cross-server shadowing | One server's description hijacks another's tool (Lab 01b) | partial, finish it |
| **ASI03 / MCP01, MCP02, MCP07** | Identity and Privilege Abuse | Agent runs with over-broad capability; token theft from context; scope creep. This is your **highest-value gap**: it is the theme of your whole brand (delegation-not-impersonation, per-agent identity) and nobody has a clean teaching lab for it | build |
| **ASI04 / MCP04** | Agentic Supply Chain | Malicious MCP server registers a backdoored tool; poisoned dependency (Lab 02 DockerDash covers the container-metadata angle) | partial, extend to the MCP-registry angle |
| **ASI05 / MCP05** | Unexpected Code Execution | Agent generates and runs code; command injection through a tool | build (sandbox-escape framing) |
| **ASI06** | Memory and Context Poisoning | Persistent memory poisoning, cross-session persistence (Lab 05) | done |
| **ASI07 / MCP10** | Insecure Inter-Agent Communication | Forged A2A message / agent-card spoofing (part of Lab 07) | done, isolate as its own lab too |
| **ASI08** | Cascading Failures | One compromised agent's error propagates through an orchestration chain; blast-radius demo | build (this is your "blast radius" thesis made runnable) |
| **ASI09** | Human-Agent Trust Exploitation | Agent confidently recommends a harmful action a human approves | build (lightweight, high-impact for talks) |
| **ASI10** | Rogue Agents | Persistence after server removal; rogue agent acting legitimately (the tail of Lab 07) | done |
| **MCP08** | Lack of Audit and Telemetry | Defensive lab: show the same kill chain *with* tool-call logging and how it changes detection | build (defensive) |
| **MCP09** | Shadow MCP Servers | Unsanctioned server joins; governance/discovery control stops it | build (defensive) |
| **The chain** | Full MCP-to-A2A kill chain | Five stages, one control breaks it (Lab 07, flagship) | done |

You are covering roughly half the two Top 10s today. The four highest-value builds, in order: **ASI03 agent identity** (your brand's core, and empty in the market), **ASI08 cascading failures** (your blast-radius thesis, runnable), the **MCP09/MCP08 defensive pair** (what vendors and blue teams need), and **ASI09 human-trust** (cheap, and it plays beautifully live in a talk).

### 4.4 The architecture, in three tiers

Kubernetes Goat's genius was one project serving "try it in a browser," "run it locally," and "run it on your real cloud." Mirror that.

**Tier 0: Zero-install front door (the missing piece, build first).**
The equivalent of Katacoda. Options, cheapest first:

- **Killercoda** (Katacoda's successor) hosts free interactive scenarios; author two or three flagship labs (tool poisoning, the kill chain) as browser scenarios. This is the closest analogue to what Madhu did and the single highest-return move in this whole document.
- A hosted read-only walkthrough at a `labs.` or `goat.` subdomain that shows the poisoned-tool trace and the kill-chain stages playing out, so someone with zero setup sees the payoff in 30 seconds. This is what your `agentdojo-live` post-solve trace panel was already designed to be, so repurpose it as the front door rather than a separate product.

Without Tier 0 you have a good repo. With it you have a funnel.

**Tier 1: Local (what you have, harden it).**
A Docker Compose one-liner that stands up the vulnerable agent, the MCP servers, a local model via Ollama, and the dashboard, with **zero external dependencies**. Copy DVAA's "simulated LLM backend, no key" trick so a learner who has not installed Ollama can still watch the deterministic runs. Keep the "no cloud, no keys, no data leaves your laptop" promise; it is a genuine differentiator against FinBot. `make attack` and `make defend` per lab.

**Tier 2: Kubernetes (your unfair advantage, nobody else has it).**
A Helm chart that deploys the whole environment into a cluster, kind for laptops and EKS/GKE/AKS for real. **This is the direct Kubernetes Goat lineage and no agentic goat offers it.** It matters because production agents run on Kubernetes, because it lets you demo agent-identity and blast-radius scenarios with real RBAC and network policy (your home turf), and because it is the natural bridge from your existing homelab and HolmesGPT work. It also makes the project legible to exactly the cloud-native security crowd Kubernetes Goat owns. A MultiJuicer-style per-student deployment for trainings is the Tier-2 stretch goal.

### 4.5 Determinism (the hard technical problem, and your credibility)

Local models are unreliable ReAct agents, and you already hit this (`qwen2.5-7b` baseline, some attacks need `gpt-oss-20b`). Kubernetes Goat never had this problem because clusters are deterministic. FinBot and DVAA solve it two ways you should combine:

- **Deterministic verdicts via canaries, not model output.** You already do this in the labs (a synthetic secret reaches a localhost listener, so the attack succeeded). Make it universal: every flag is captured by an observable side effect (a canary HTTP hit, a file read, a DB row), never by parsing what the model said. This is FinBot's "event-driven detection, no static flags" done locally.
- **A simulated-agent mode for the front door and CI.** For Tier 0 and for CI, ship a scripted agent that reproduces the vulnerable behavior deterministically (DVAA's offline mode). The learner sees the mechanism every time; the "will the model comply today" lottery is reserved for the advanced local run where it is part of the lesson.

State this determinism design explicitly in the README. It is the difference between a demo that works on stage and one that embarrasses you, and it signals rigor to the people evaluating whether to adopt.

### 4.6 The ecosystem around the target

The Juice Shop lesson: the target spreads because of what surrounds it.

- **The companion book.** *Agentic Security in Practice* becomes the narrative; the goat is its runnable lab appendix. Each chapter ends "now run Lab N." This is your strongest asset and it is already in flight.
- **A CTF/flag export.** A `--ctf` mode that emits flags in CTFd-compatible format (Juice Shop's `juice-shop-ctf` model). This is what makes universities and conference villages run it.
- **The defense-level ladder.** Generalize Lab 07's `--defended` to every lab as L0 (vulnerable), L1 (basic control), L2 (hardened), the AI Goat pattern. Same attack, watch it die as controls come on. This is the single most demo-friendly feature for a talk or a vendor.
- **The Scorecard as the top of funnel.** Your existing Agent Security Scorecard already grades a posture; wire "you scored Exposed on Cognition Integrity, so run Lab 01 to see why" so the assessment and the lab reinforce each other.

---

## Part 5: Naming

Constraints, from the research:

- **Do not use "OWASP" in the name.** OWASP branding rules are explicit: "OWASP" alone cannot preface a non-OWASP project, and the mark may not be used as a noun or to imply endorsement. You *can* say "mapped to the OWASP Top 10 for Agentic Applications" in the description with the non-endorsement disclaimer. You cannot call it OWASP-anything.
- **Do not use "AgentDojo."** It is taken by the ETH Zurich NeurIPS benchmark. Retire the internal `agentdojo-live` name for anything public.
- **"MCP Goat" / "MCPGoat" is a crowded, contested name** with at least three unrelated projects, one of which publicly disclaims the others. Avoid it; it buys a naming fight and dilutes you.
- **"AI Goat" is taken** (Orca, and separately the AI Security Consortium).
- **"Damn Vulnerable ..." is a crowded prefix** (DVMCP, DVLA, DVAA, DV-email-agent). You would be the fourth. Skip it.

What is open and on-brand: the goat lineage says "deliberately vulnerable teaching target" instantly, and no one has claimed the agentic/A2A niche of it.

**Recommended: `AgenticGoat`** (repo `agentic-goat`).

- It says exactly what it is to anyone who knows WebGoat or Kubernetes Goat, which is your whole target audience.
- It scopes to *agentic* (agents, MCP, A2A, orchestration), which is broader and more future-proof than "MCP," and is precisely the space no goat owns.
- GitHub `agentic-goat` and the `AgenticGoat` name appear unclaimed as a vulnerable-by-design project (the only `AgentGoat` hits are an unrelated e-commerce SaaS). Verify the exact org/repo and the domain before you commit.
- A clean home: `agenticgoat.dev`, or a `goat.` subdomain on a domain you hold.

Strong alternatives if `AgenticGoat` is unavailable or you want a distinct wordmark:

- **`AgentGoat`**, punchier, but check the SaaS name collision does not cause confusion.
- **`A2A Goat` / `AgentChainGoat`**, leans into your unique kill-chain differentiator, narrower.
- **`GoatSwarm` / `HerdGoat`**, plays on multi-agent, more distinctive, less instantly legible.

Keep `mcp-attack-labs` alive as a redirect/alias so existing stars and inbound links survive the rename; GitHub preserves redirects on rename.

---

## Part 6: The 90-day plan

Sequenced so the highest-value, lowest-effort moves land first, and so momentum is public early. This assumes the labs already exist (they do), so almost all of it is packaging, distribution, and the two or three highest-value new scenarios, not a rebuild.

**Weeks 1 to 2: Reposition and publish the crosswalk.**

- Rename to `AgenticGoat`, set up the org, secure the domain, keep the `mcp-attack-labs` redirect.
- Publish the **ASI/MCP crosswalk table** (Part 4.3) as the README. This is a shippable artifact today and it is the thing that gets shared, because it is the map everyone in both working groups wants. Post it to the OWASP ASI and MCP channels through an internal referral, not cold.
- Rewrite the seven existing labs to the **scenario contract** (Part 4.2): add named flags and collapsed hints. This is a weekend of editing, not engineering.

**Weeks 3 to 5: Build the zero-install front door (Tier 0).**

- Author the two flagship labs (Lab 01 tool poisoning, Lab 07 kill chain) as **Killercoda scenarios**, or stand up the hosted read-only trace/kill-chain walkthrough at `goat.<domain>`. This is the Katacoda move and the single biggest adoption lever. Ship it before any new attack.
- Repurpose the `agentdojo-live` post-solve trace panel as this front door rather than a separate product.

**Weeks 6 to 9: Close the two highest-value scenario gaps and the ladder.**

- Build **ASI03 Agent Identity and Privilege Abuse**, the empty seat in the market and the core of your brand. This is the lab that makes AgenticGoat *yours* and not a repackaging.
- Build **ASI09 Human-Agent Trust**, cheap, and it is the scenario you demo live on stage.
- Generalize the **defense-level ladder** (L0/L1/L2) across all labs.
- Add the **`--ctf` flag export** (CTFd format).

**Weeks 10 to 13: Kubernetes tier and the launch.**

- Ship the **Helm chart** (Tier 2) for kind plus one managed cloud. This is the Kubernetes Goat lineage move and your durable moat; it also connects to your homelab and HolmesGPT work for content.
- Write the **launch post** ("Introducing AgenticGoat," mirroring Madhu's launch post structure), tie it to a newsletter issue, and line it up with a CFP. The whole project is exactly the kind of thing fwd:cloudsec, an OWASP AppSec Days, or an agentic-AI conference wants a talk on, and the talk *is* a live walkthrough of the goat, which satisfies your "CFP backed by real work" requirement in one move.
- Add the **book cross-references** so each chapter of *Agentic Security in Practice* ends by running a lab.

**Ongoing: the part Madhu got right that most people skip.**
Adoption came from *showing up for years*. Every talk you give, every workshop, every newsletter issue should run a scenario live. Add a `Showcase`/`Adopters` page from day one and ask every person who uses it to add themselves (Kubernetes Goat's exact move). The goat becomes infrastructure only when other people are demoing with it, not when you are.

---

## Part 7: How you'll know it worked

Concrete signals, in rough order of appearance:

- **Month 1 to 2:** the crosswalk table gets shared in the OWASP working-group channels; the Killercoda scenarios get completions from people who are not you.
- **Month 3 to 4:** the first external contributor adds a scenario to the contract; the first vendor or trainer mentions using AgenticGoat in a demo or class; a talk is accepted whose content is the live walkthrough.
- **Month 6:** it is cited alongside DVMCP and FinBot in a "vulnerable AI apps" roundup (tl;dr sec, CloudSecList, the OWASP VWAD directory, so get it listed there deliberately, the way Kubernetes Goat is); an OWASP working group references it as the hands-on companion to the Top 10.
- **The real one:** someone you have never met opens a PR fixing a lab, files an issue because a flag did not capture, or puts it in *their* conference talk. That is the moment it stopped being your project and became the goat.

---

## The single most important sentence

You do not have an attacks problem. Your labs are ahead of the field on the hardest part, the A2A kill chain. You have a *front door and contract* problem. Spend the next month on Tier 0 (zero-install) and the scenario contract (named flags, progressive hints, the published ASI/MCP crosswalk), not on new exploits. That is the exact order in which Kubernetes Goat was actually built, and it is the gap between what you have and the goat of the agentic era.

---

### Sources

- [Kubernetes Goat repo](https://github.com/madhuakula/kubernetes-goat) and [docs](https://madhuakula.com/kubernetes-goat/docs/), including the [motivation](https://madhuakula.com/kubernetes-goat/docs/why-kubernetes-goat-and-the-motivation), [showcase](https://madhuakula.com/kubernetes-goat/docs/showcase), [OWASP K8s Top 10 crosswalk](https://madhuakula.com/kubernetes-goat/docs/owasp-kubernetes-top-ten), and [scenario format](https://madhuakula.com/kubernetes-goat/docs/scenarios/scenario-16/rbac-least-privileges-misconfiguration-in-kubernetes-cluster/welcome)
- [Introducing Kubernetes Goat](https://medium.com/@madhuakula/introducing-kubernetes-goat-8624f6d70e9e) (25 Jun 2020, 14 scenarios plus Katacoda)
- [OWASP Juice Shop / MultiJuicer](https://github.com/juice-shop/multi-juicer) and [Trainer's guide](https://help.owasp-juice.shop/appendix/trainers.html)
- [CI/CD Goat](https://github.com/cider-security-research/cicd-goat) and the [Top 10 CI/CD Security Risks](https://github.com/cider-security-research/top-10-cicd-security-risks)
- [Orca AI Goat](https://orca.security/resources/blog/orca-ai-goat-open-source-environment-owasp-risks/) and [AI Security Consortium AIGoat](https://github.com/AISecurityConsortium/AIGoat)
- [OWASP FinBot CTF](https://github.com/GenAI-Security-Project/finbot-ctf) and [genai.owasp.org announcement](https://genai.owasp.org/2026/04/14/finbot-ctf-is-live-a-hands-on-companion-to-the-owasp-genai-security-project/)
- [Damn Vulnerable AI Agent (OpenA2A)](https://github.com/opena2a-org/damn-vulnerable-ai-agent)
- [Damn Vulnerable MCP Server](https://github.com/harishsg993010/damn-vulnerable-MCP-server), [Damn Vulnerable LLM Agent](https://github.com/ReversecLabs/damn-vulnerable-llm-agent), [Appsecco Vulnerable MCP Servers Lab](https://vwad.owasp.org/app/vulnerable-mcp-servers-lab/)
- [Lakera Gandalf: Agent Breaker](https://www.lakera.ai/blog/inside-agent-breaker) and its [LLM-backend benchmark](https://www.businesswire.com/news/home/20251028168283/en/Lakera-Launches-Open-Source-Security-Benchmark-for-LLM-Backends-in-AI-Agents)
- [AgentDojo (NeurIPS 2024)](https://neurips.cc/virtual/2024/poster/97522) and [Invariant/ETH write-up](https://invariantlabs.ai/blog/agentdojo)
- [OWASP MCP Top 10](https://owasp.org/www-project-mcp-top-10/), [OWASP Top 10 for Agentic Applications 2026](https://cycode.com/blog/owasp-top-10-agentic-applications/), and [OWASP GenAI branding rules](https://genai.owasp.org/branding/)
- Your own [mcp-attack-labs](https://github.com/aminrj-labs/mcp-attack-labs)
