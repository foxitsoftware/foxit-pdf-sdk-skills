# HACA-SDK Skills

> Human-AI Collaborative Programming for Foxit PDF SDK

**English** | [简体中文](README.zh-CN.md)

HACA-SDK is a Foxit PDF SDK programming assistant configuration built on the Human-AI Collaborative Programming (HACA) workflow. It provides shared governance rules, agents, prompts, skills, and SDK reference materials for GitHub Copilot.

## Repository Structure

```text
.
├── .github/
│   ├── agents/              # GitHub Copilot custom agents
│   ├── prompts/             # HACA workflow prompt entry points
│   ├── skills/              # Source skills used by the HACA workflow
│   │   └── superpowers/     # Local Superpowers skill installation directory
│   ├── sdk-references/      # Foxit SDK capability and configuration references
│   ├── templates/           # Workflow contract templates
│   ├── workflows/           # CI validation workflow
│   └── copilot-instructions.md
├── docs/                    # Design notes and workflow documentation
├── scripts/                 # HACA validation scripts
│   └── sync_haca_customizations.py
└── README.md
```

The `.github/` directory contains the primary GitHub Copilot configuration and is the source of truth for the HACA workflow.

## Supported Platforms

This repository currently supports GitHub Copilot.

The Foxit SDK product references cover Desktop, Mobile, Harmony, Web, Cloud API, and Conversion SDK scenarios. See [.github/sdk-references/README.md](.github/sdk-references/README.md) for the reference material layout.

## Setup

### 1. Clone or copy the repository

Open the repository as a VS Code workspace so the `.github/` configuration is available to the assistant integration.

### 2. Install Superpowers skills manually (optional)

The `superpowers` directory is an installation location, not a bundled copy of the external
Superpowers skill library. **HACA works without it** — every Superpowers-backed step degrades
gracefully to a built-in HACA equivalent and records `Not Available` evidence. Installing it is
optional and only upgrades the quality-control tooling inside Step 1-4.

Users must download the Superpowers skills from their official upstream source
([obra/superpowers](https://github.com/obra/superpowers)) and place the skill files or directories into:

```text
.github/skills/superpowers/
```

Installation commands per harness (upstream-documented):

| Harness | Command / entry point |
|---------|----------------------|
| GitHub Copilot CLI | `copilot plugin marketplace add obra/superpowers-marketplace` then `copilot plugin install superpowers@superpowers-marketplace` |
| Claude Code | `/plugin install superpowers@claude-plugins-official` |
| Cursor | `/add-plugin superpowers` |
| Codex CLI | `/plugins` → search `superpowers` → Install Plugin |
| OpenCode | Fetch and follow `https://raw.githubusercontent.com/obra/superpowers/refs/heads/main/.opencode/INSTALL.md` |
| Gemini CLI | `gemini extensions install https://github.com/obra/superpowers` |
| Other harnesses | See the "Installation" section of the upstream README |

For example, after installation this directory may contain skills such as:

```text
.github/skills/superpowers/
├── brainstorming/
├── dispatching-parallel-agents/
├── writing-plans/
├── using-git-worktrees/
├── test-driven-development/
├── verification-before-completion/
└── ...
```

Do not assume that the repository contains the full external Superpowers package. If the skills are
missing, the affected steps still work through the built-in HACA equivalents, and the step output
records `Superpowers capability: Not Available (<capability-name>)`. See
[.github/skills/superpowers/README.md](.github/skills/superpowers/README.md) for the expected role of
this directory and the full install matrix.

### 3. Optional SDK configuration

To avoid confirming the SDK environment repeatedly, create `foxit-sdk.config.json` in the repository root. It can specify the Foxit SDK product, platform, architecture, language, SDK version, license environment variable, and SDK path. See [.github/sdk-references/foxit-sdk-config-schema.md](.github/sdk-references/foxit-sdk-config-schema.md) for the schema and examples.

## Using the HACA Workflow

HACA processes a programming task in four confirmed steps:

1. **Requirement Clarification**: Identify the Foxit SDK product, platform, architecture, language, acceptance criteria, and scope.
2. **Solution Design**: Consult the SDK references, compare implementation options, and identify risks.
3. **Task Decomposition**: Break the confirmed solution into executable subtasks and dependencies.
4. **Build**: Implement the work with tests, compilation, runtime checks, and evidence validation.

In GitHub Copilot, use the HACA agent or the corresponding prompt commands under `.github/prompts/`:

```text
/haca-step1
/haca-step2
/haca-step3
/haca-step4
```

Each step requires explicit human confirmation before the workflow advances. The HACA agent stores the confirmed task context in a workflow contract under `artifacts/<task-id>/haca-workflow.md` when the workflow is activated.

## Skills

| Skill | Purpose |
|-------|---------|
| `clarify-requirements` | Step 1 — Identify the target SDK product, platform, architecture, and language; clarify task requirements. |
| `risk-identification` | Step 2 — Consult SDK references, compare solutions, and identify risks. |
| `task-decomposition` | Step 3 — Split the confirmed solution into code-review-friendly subtasks and dependencies. |
| `tdd-loop` | Step 4 — Enforce Red-Green-Refactor and compilation/runtime correctness. |
| `evidence-gate` | Maintain a single evidence pack and block step transitions when evidence is incomplete. |
| `commit-message-rules` | Internal rules for standardized commit messages (templates, length checks, validators). |

## Documentation

- [HACA execution flow](docs/haca-execution-flow.md)
- [Human-AI collaborative programming workflow](docs/human-ai-collaborative-programming-workflow.md)
- [SDK reference materials](.github/sdk-references/README.md)
- [Validation script details](scripts/README.md)

## Development Notes

Keep source changes in `.github/` and run the validation check before submitting changes. The `sync_haca_customizations.py` script validates the `.github/` Copilot tree (it no longer syncs between platforms — this repository targets GitHub Copilot only). Do not commit credentials, license keys, downloaded SDK binaries, or private Superpowers distribution files to this repository.

```bash
python3 scripts/sync_haca_customizations.py --check
```
