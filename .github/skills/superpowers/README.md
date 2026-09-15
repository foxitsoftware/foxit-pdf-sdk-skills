# Superpowers Skills (Optional Enhancement Layer)

This directory is an **installation slot**, not a bundled copy of the external Superpowers library.
HACA works without it. When the skills are absent, every Superpowers-backed step degrades gracefully
to the built-in HACA behavior described below.

## Status

| Item | Value |
|------|-------|
| Bundled with this repository | **No** |
| Required for HACA Step 1-4 | **No** — all steps have built-in fallbacks |
| Maintained by | Upstream project ([obra/superpowers](https://github.com/obra/superpowers), MIT) |

## Expected skills (if you choose to install)

| Skill | Consumed by HACA step |
|-------|----------------------|
| `brainstorming` | Step 1 (clarifying questions), Step 2 (option comparison) |
| `dispatching-parallel-agents` | Step 2 (independent-domain analysis) |
| `writing-plans` | Step 3 (persistent execution plan) |
| `using-git-worktrees` | Step 3 (isolated workspace) |
| `test-driven-development` | Step 4 (quality control) |
| `verification-before-completion` | Step 4 (quality control) |
| `systematic-debugging` | Step 4 (quality control) |
| `requesting-code-review` | Step 4 (quality control) |
| `receiving-code-review` | Step 4 (quality control) |
| `finishing-a-development-branch` | Step 4 (branch wrap-up) |

Expected layout after installation:

```text
.github/skills/superpowers/
├── brainstorming/SKILL.md
├── dispatching-parallel-agents/SKILL.md
├── writing-plans/SKILL.md
├── using-git-worktrees/SKILL.md
├── test-driven-development/SKILL.md
├── verification-before-completion/SKILL.md
├── systematic-debugging/SKILL.md
├── requesting-code-review/SKILL.md
├── receiving-code-review/SKILL.md
└── finishing-a-development-branch/SKILL.md
```

## How to install (user action required)

Superpowers is installed by the user, separately for each coding agent harness. The commands below
are the upstream-documented installers; use the one that matches your harness.

| Harness | Command / entry point |
|---------|----------------------|
| GitHub Copilot CLI | `copilot plugin marketplace add obra/superpowers-marketplace` then `copilot plugin install superpowers@superpowers-marketplace` |
| Claude Code | `/plugin install superpowers@claude-plugins-official` |
| Cursor | `/add-plugin superpowers` |
| Codex CLI | `/plugins` → search `superpowers` → Install Plugin |
| OpenCode | Fetch and follow `https://raw.githubusercontent.com/obra/superpowers/refs/heads/main/.opencode/INSTALL.md` |
| Gemini CLI | `gemini extensions install https://github.com/obra/superpowers` |
| Other harnesses | See the "Installation" section of the upstream README |

> Plugin installers place skills in the harness's own location. HACA reads skills from
> `.github/skills/superpowers/<skill-name>/SKILL.md`. If your installer uses a different path, copy or
> symlink the installed `SKILL.md` files into the layout shown above.

For a manual, offline installation: clone the upstream repository and copy the `skills/` directory
contents into `.github/skills/superpowers/`, keeping one subdirectory per skill.

```bash
git clone https://github.com/obra/superpowers.git /tmp/superpowers
cp -r /tmp/superpowers/skills/* .github/skills/superpowers/
```

Do not commit third-party Superpowers distribution files to this repository unless your project's
licensing review explicitly approves redistribution.

## What you must configure yourself

1. **Install the skills** using one of the methods above — this repository does not ship them.
2. **Verify the layout** matches the expected tree, otherwise HACA treats them as unavailable.
3. **Keep them updated** — Superpowers is versioned upstream; re-run your harness's update command
   after major releases.
4. **Optional telemetry opt-out** — upstream's brainstorming visual companion loads an image from the
   Prime Radiant website. Set `SUPERPOWERS_DISABLE_TELEMETRY=true` to disable it.

## Degradation behavior when a skill is missing

HACA never blocks a step solely because a Superpowers skill is absent. When a referenced
`SKILL.md` is not present:

1. Record `Superpowers capability: Not Available (<capability-name>)` in the step output.
2. Execute the built-in HACA behavior instead:
   - Step 1: batch clarifying questions from the HACA question template.
   - Step 2: the five-dimension risk checklist and the solution comparison template.
   - Step 3: the HACA subtask contract (`Task Input` + `AI Decision Summary`) and execution order.
   - Step 4: the TDD Red-Green-Refactor cycle and the SDK Code Quality Chain (Q1-Q3).
3. Do not fabricate capability execution evidence for a skill that was not actually loaded.

The Evidence Gate treats a documented `Not Available` record as valid evidence for the capability
requirement, so a missing Superpowers installation cannot deadlock Step 4.

