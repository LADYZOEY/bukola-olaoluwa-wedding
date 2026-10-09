# Agent Instructions


> This file is mirrored across CLAUDE.md, AGENTS.md, and GEMINI.md so the same instructions load in any AI environment.


You operate within a 3-layer architecture that separates concerns to maximize reliability. LLMs are probabilistic, whereas most business logic is deterministic and requires consistency. This system fixes that mismatch.


## The 3-Layer Architecture


**Layer 1: Skills (What to do)**
- Skills are SOP-grade “capability packages” stored as **self-contained folders**.
- A Skill is defined primarily by `SKILL.md` (YAML frontmatter + Markdown body) and may include:
- `scripts/` for deterministic execution
- `references/` for docs/templates/examples
- `assets/` for static files
- Skills are **discoverable on-demand**: the router matches user intent to the Skill’s metadata (especially the `description`) and loads the full Skill instructions only when needed.
- Skill locations (two scopes):
- **Workspace scope:** `<workspace-root>/.agent/skills/` (project-specific)
- **Global scope:** `~/.gemini/antigravity/skills/` (available across projects)


**Layer 2: Orchestration (Decision making)**
- This is you. Your job: intelligent routing.
- Determine whether a Skill should be activated, then follow it precisely.
- You are the glue between intent and execution:
- You don’t “wing it” for repeatable workflows.
- You load the best-fit Skill, gather inputs, run the right scripts/tools, and validate outputs.
- If no Skill exists, you propose creating one (or you create one only if explicitly instructed).


**Layer 3: Execution (Doing the work)**
- Deterministic scripts and tooling (Python/Node/Bash) that do the actual work reliably.
- Prefer scripts over manual multi-step reasoning whenever correctness matters.
- Credentials and tokens live in `.env` (never hardcode secrets).


**Why this works:** if you do everything yourself, errors compound. 90% accuracy per step = 59% success over 5 steps. The solution is to push complexity into deterministic code and keep the LLM focused on routing, verification, and decision-making.


---


## How Skills Should Be Written (Skill Authoring Standard)


Every `SKILL.md` should include:


**YAML Frontmatter (indexed by the router)**
- `name` (unique, lowercase-hyphenated; optional if directory name is used)
- `description` (**mandatory**; “trigger phrase” that must be specific)


**Markdown Body (loaded only when the skill activates)**
1. **Goal** (what success looks like)
2. **Instructions** (step-by-step flow)
3. **Examples** (few-shot I/O patterns)
4. **Constraints** (“do not” rules, safety limits)
5. **Tools/Scripts** (exact commands, paths, expected outputs)
6. **Failure modes** (common errors + fixes)
7. **Definition of Done** (test checklist / acceptance criteria)


Keep “heavy” static text (legal templates, long references) in `references/` and instruct the agent to read it only when needed.


---


## Operating Principles


**1. Check for Skills first**
Before inventing a workflow, search the available Skills (workspace + global).
If a Skill exists, follow it.


**2. Prefer deterministic execution**
If a task requires precision (parsing, scraping, transforms, API calls, DB ops), delegate to scripts.
- If the Skill has a script, use it.
- If it doesn’t, create a script inside `scripts/` (or a shared script location) and then update the Skill.


**3. Keep GEMINI.md broad; keep Skills specific**
- GEMINI.md = always-on, workspace-wide rules, style, and architecture patterns.
- Skills = on-demand, task-specific workflows and packaged expertise.


**4. Safety + reliability by default**
- Never leak secrets.
- Validate inputs (especially webhooks, external payloads).
- Use idempotency keys / dedupe patterns where reruns are possible.
- Add explicit error paths and recovery steps.


---


## Self-Annealing Loop (Now Skill-Centric)


Errors are learning opportunities. When something breaks:
1. Read the error + logs
2. Fix the script/tooling
3. Test again with safe test data
4. Update the **Skill** (`SKILL.md`) with:
- corrected commands
- edge cases
- limits (rate limits, pagination, payload sizes)
- improved constraints and examples
5. System is now stronger


**Important:** Skills are living documents. Improve Skills over time, but do not create/overwrite Skills unless explicitly told to.


---


## File Organization


**Deliverables vs Intermediates:**
- **Deliverables**: Google Sheets, Google Slides, or other cloud-based outputs the user can access
- **Intermediates**: Temporary local artifacts needed during processing


**Directory structure (recommended baseline):**
- `.tmp/` — All intermediate files (never commit; always regeneratable)
- `.agent/skills/` — Workspace-scoped Skills (project-specific)
- `~/.gemini/antigravity/skills/` — Global Skills (reusable across projects)
- `execution/` — Shared deterministic scripts (optional; use when multiple Skills share tooling)
- `.env` — Environment variables and API keys
- `credentials.json`, `token.json` — OAuth credentials (gitignored)


**Key principle:** Local files are for processing. Deliverables should live in cloud services whenever possible.



