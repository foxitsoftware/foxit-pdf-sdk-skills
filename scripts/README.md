# HACA Validation Scripts

This directory contains maintenance/validation scripts for the HACA customization
tree. **This repository targets GitHub Copilot only** — there is no cross-platform
mirror, so nothing is generated into `.cursor/` or `.opencode/`.

Currently provided:

- `sync_haca_customizations.py`: Validates the `.github/` customization tree. Despite
  its historical name, it no longer syncs between platforms (the multi-platform sync
  targets were removed); it now acts as a Copilot-only consistency validator.

## What `sync_haca_customizations.py` checks

1. **Required skills** — every required HACA skill exists and is non-empty:
   `clarify-requirements`, `risk-identification`, `task-decomposition`, `tdd-loop`,
   `evidence-gate`, `commit-message-rules`.
2. **Internal reference existence** — every `.github/...` path referenced from a
   `.github/**/*.md` file points at a real file. Optional Superpowers install paths
   (`.github/skills/superpowers/...`) are intentionally exempt because Superpowers is
   installed by the user and is not bundled in this repository.
3. **SKILL frontmatter** — every non-superpowers `SKILL.md` declares the required
   frontmatter keys (`name`, `description`).
4. **Multi-platform purity (warning)** — shipped Copilot assets should not reference
   `.cursor/`, `.opencode/`, `opencode.json`, or `tool_mapping_template`. This is a
   **warning**, not a failure, because the maintainer-only prompts
   (`haca-apply-spec.prompt.md`, `haca-sync.prompt.md`) and the `superpowers/README.md`
   legitimately mention other harnesses for Superpowers installation. Those files are
   tracked as a known release risk in the release report.

The script prints the legacy success line `CHECK OK: no stale markdown targets.` on
success so existing maintenance prompts stay compatible.

Usage:

```bash
python3 scripts/sync_haca_customizations.py
python3 scripts/sync_haca_customizations.py --check
```

`--check` is retained for backward compatibility; validation always runs.

In CI, `.github/workflows/validate.yml` runs this script together with self-tests of
the commit-message validators (`verify_commit_message.py`,
`check_commit_message_length.py`) on every push to `main` and on pull requests.