# HACA-SDK Skills

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
│   └── copilot-instructions.md
├── docs/                    # Design notes and workflow documentation
├── scripts/
│   ├── sync_haca_customizations.py
│   └── tool_mapping_template.json
└── README.md
```

The `.github/` directory contains the primary GitHub Copilot configuration and is the source of truth for the HACA workflow.

## Supported Platforms

This repository currently supports GitHub Copilot.

The Foxit SDK product references cover Desktop, Mobile, Harmony, Web, Cloud API, and Conversion SDK scenarios. See [.github/sdk-references/README.md](.github/sdk-references/README.md) for the reference material layout.

## Setup

### 1. Clone or copy the repository

Open the repository as a VS Code workspace so the `.github/` configuration is available to the assistant integration.

### 2. Install Superpowers skills manually

The `superpowers` directory is an installation location, not a bundled copy of the external Superpowers skill library. Users must download the Superpowers skills separately from their official source and place the skill files or directories into:

```text
.github/skills/superpowers/
```

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

Do not assume that the repository contains the full external Superpowers package. If the skills are missing, Superpowers-dependent workflows will not be available even though the local directory exists. See [.github/skills/superpowers/README.md](.github/skills/superpowers/README.md) for the expected role of this directory.

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

## Documentation

- [HACA execution flow](docs/haca-execution-flow.md)
- [Human-AI collaborative programming workflow](docs/human-ai-collaborative-programming-workflow.md)
- [SDK reference materials](.github/sdk-references/README.md)
- [Synchronization script details](scripts/README.md)

## Development Notes

Keep source changes in `.github/` and run the synchronization check before submitting changes. Do not commit credentials, license keys, downloaded SDK binaries, or private Superpowers distribution files to this repository.
