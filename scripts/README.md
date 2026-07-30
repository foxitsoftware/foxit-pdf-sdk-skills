# HACA Sync Scripts

This directory contains cross-platform maintenance scripts.

Currently provided:

- `sync_haca_customizations.py`: Syncs HACA source configuration from `.github/` to `.cursor/` and `.opencode/`, and validates consistency of managed target directories, eliminating the need for manual duplication across multiple directory sets.
- `tool_mapping_template.json`: Tool name and capability mapping template for three platforms (GitHub Copilot / Cursor / OpenCode).  
  **Note**: The "capability layer" here refers to the tool abstraction tier in the mapping template, which is **not the same concept** as the three HACA repository configuration layers (governance layer / orchestration layer / skill layer, see `../docs/haca-execution-flow.md` §2).

The script enforces three categories of boundaries:

- **Primary edit source** (manually maintained as needed): `.github/copilot-instructions.md`, `.github/agents`, `.github/prompts`, `.github/scripts`, `.github/skills`, `.github/templates`
- **Sync-generated targets** (synced to these two destinations only): `.cursor/agents`, `.cursor/commands`, `.cursor/haca-governance.md`, `.cursor/scripts`, `.cursor/skills`, `.cursor/templates`, `.opencode/AGENTS.md`, `.opencode/agents`, `.opencode/prompts`, `.opencode/scripts`, `.opencode/skills`, `.opencode/templates`
- **Manually maintained adapter layer**: `.cursor/AGENTS.md`, `.cursor/rules/haca.mdc`, `.opencode/agents/haca.agent.md`, `opencode.json`

When syncing to `.cursor/` and `.opencode/`, `sync_haca_customizations.py` automatically replaces tool names according to the `name_replacements` and capability mapping rules in the root `scripts/tool_mapping_template.json`, ensuring the target platform configuration remains usable.

The script also validates that all required HACA skills are present (currently: `clarify-requirements`, `risk-identification`, `task-decomposition`, `tdd-loop`, `evidence-gate`, `commit-message-rules`), preventing multi-platform configuration inconsistencies caused by missing new skills.

`.opencode/agents/haca.agent.md` is a special case: it is not auto-generated through the common agent frontmatter template but is kept as a manually maintained file. This is because the OpenCode agent's header field requirements are incompatible with `.github/agents/haca.agent.md` and `.cursor/agents/haca.agent.md` — running it through unified generation would corrupt the frontmatter.

Two maintenance-only prompt files exist exclusively in `.github/prompts/` and will not generate corresponding `.cursor/commands/` or `.opencode/prompts/` targets when syncing: `haca-apply-spec.prompt.md` and `haca-sync.prompt.md`. They correspond to the `/haca-apply-spec` and `/haca-sync` commands respectively, and their content hard-references `.github/` paths, making them unsuitable for syncing to other platforms.

`sync_tree` currently processes `.md` and `.mdc` files by default; for `.github/skills/**` it additionally supports syncing `.py` files (for executable resources inside a skill's `scripts/` directory).

`--check` not only verifies that no files are missing from the sync but also checks whether any uncontrolled files have been mixed into managed directories.

Usage:

```bash
python3 scripts/sync_haca_customizations.py
python3 scripts/sync_haca_customizations.py --check
```

In CI, `python3 scripts/sync_haca_customizations.py --check` is also run to block commits of un-synced generated files.