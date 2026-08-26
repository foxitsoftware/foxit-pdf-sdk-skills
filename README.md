# HACA-SDK Skills

> Human-AI Collaborative Programming for Foxit PDF SDK — 面向福昕 PDF SDK 的人机协作编程

HACA-SDK is a Foxit PDF SDK programming assistant configuration built on the Human-AI Collaborative Programming (HACA) workflow. It provides shared governance rules, agents, prompts, skills, and SDK reference materials for GitHub Copilot.

HACA-SDK 是基于人机协作编程（HACA）工作流构建的福昕 PDF SDK 编程助手配置，为 GitHub Copilot 提供共享的治理规则、代理（agents）、提示词（prompts）、技能（skills）以及 SDK 参考资料。

## Repository Structure / 仓库结构

```text
.
├── .github/
│   ├── agents/              # GitHub Copilot custom agents / GitHub Copilot 自定义代理
│   ├── prompts/             # HACA workflow prompt entry points / HACA 工作流提示词入口
│   ├── skills/              # Source skills used by the HACA workflow / HACA 工作流使用的源技能
│   │   └── superpowers/     # Local Superpowers skill installation directory / 本地 Superpowers 技能安装目录
│   ├── sdk-references/      # Foxit SDK capability and configuration references / 福昕 SDK 能力与配置参考
│   ├── templates/           # Workflow contract templates / 工作流契约模板
│   └── copilot-instructions.md
├── docs/                    # Design notes and workflow documentation / 设计说明与工作流文档
├── scripts/
│   ├── sync_haca_customizations.py
│   └── tool_mapping_template.json
└── README.md
```

The `.github/` directory contains the primary GitHub Copilot configuration and is the source of truth for the HACA workflow.

`.github/` 目录包含 GitHub Copilot 的主配置，是 HACA 工作流的唯一事实来源（source of truth）。

## Supported Platforms / 支持平台

This repository currently supports GitHub Copilot.

本仓库当前支持 GitHub Copilot。

The Foxit SDK product references cover Desktop, Mobile, Harmony, Web, Cloud API, and Conversion SDK scenarios. See [.github/sdk-references/README.md](.github/sdk-references/README.md) for the reference material layout.

福昕 SDK 产品参考覆盖桌面端（Desktop）、移动端（Mobile）、鸿蒙（Harmony）、Web、云 API（Cloud API）以及转换 SDK（Conversion SDK）等场景。参考资料布局请参阅 [.github/sdk-references/README.md](.github/sdk-references/README.md)。

## Setup / 安装设置

### 1. Clone or copy the repository / 克隆或复制仓库

Open the repository as a VS Code workspace so the `.github/` configuration is available to the assistant integration.

将仓库作为 VS Code 工作区打开，以便 `.github/` 配置对助手集成可用。

### 2. Install Superpowers skills manually / 手动安装 Superpowers 技能

The `superpowers` directory is an installation location, not a bundled copy of the external Superpowers skill library. Users must download the Superpowers skills separately from their official source and place the skill files or directories into:

`superpowers` 目录是安装位置，而非外部 Superpowers 技能库的捆绑副本。用户需要从其官方来源单独下载 Superpowers 技能，并将技能文件或目录放入：

```text
.github/skills/superpowers/
```

For example, after installation this directory may contain skills such as:

例如，安装后该目录可能包含以下技能：

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

请不要假设仓库中包含完整的外部 Superpowers 包。如果技能缺失，即使本地目录存在，依赖 Superpowers 的工作流也无法使用。该目录的预期作用请参阅 [.github/skills/superpowers/README.md](.github/skills/superpowers/README.md)。

### 3. Optional SDK configuration / （可选）SDK 配置

To avoid confirming the SDK environment repeatedly, create `foxit-sdk.config.json` in the repository root. It can specify the Foxit SDK product, platform, architecture, language, SDK version, license environment variable, and SDK path. See [.github/sdk-references/foxit-sdk-config-schema.md](.github/sdk-references/foxit-sdk-config-schema.md) for the schema and examples.

为避免重复确认 SDK 环境，请在仓库根目录创建 `foxit-sdk.config.json`。该文件可指定福昕 SDK 产品、平台、架构、语言、SDK 版本、许可证环境变量以及 SDK 路径。Schema 及示例请参阅 [.github/sdk-references/foxit-sdk-config-schema.md](.github/sdk-references/foxit-sdk-config-schema.md)。

## Using the HACA Workflow / 使用 HACA 工作流

HACA processes a programming task in four confirmed steps:

HACA 通过四个确认步骤处理编程任务：

1. **Requirement Clarification / 需求澄清**：Identify the Foxit SDK product, platform, architecture, language, acceptance criteria, and scope. —— 确定福昕 SDK 产品、平台、架构、语言、验收标准与范围。
2. **Solution Design / 方案设计**：Consult the SDK references, compare implementation options, and identify risks. —— 查阅 SDK 参考资料，比较实现方案并识别风险。
3. **Task Decomposition / 任务分解**：Break the confirmed solution into executable subtasks and dependencies. —— 将确认后的方案拆分为可执行的子任务及依赖关系。
4. **Build / 构建**：Implement the work with tests, compilation, runtime checks, and evidence validation. —— 通过测试、编译、运行时检查与证据验证实现工作内容。

In GitHub Copilot, use the HACA agent or the corresponding prompt commands under `.github/prompts/`:

在 GitHub Copilot 中，请使用 HACA 代理或 `.github/prompts/` 下对应的提示词命令：

```text
/haca-step1
/haca-step2
/haca-step3
/haca-step4
```

Each step requires explicit human confirmation before the workflow advances. The HACA agent stores the confirmed task context in a workflow contract under `artifacts/<task-id>/haca-workflow.md` when the workflow is activated.

每个步骤在推进前都需要用户明确确认。工作流激活后，HACA 代理会将确认的任务上下文存储在工作流契约文件 `artifacts/<task-id>/haca-workflow.md` 中。

## Documentation / 文档

- [HACA execution flow / HACA 执行流程](docs/haca-execution-flow.md)
- [Human-AI collaborative programming workflow / 人机协作编程工作流](docs/human-ai-collaborative-programming-workflow.md)
- [SDK reference materials / SDK 参考资料](.github/sdk-references/README.md)
- [Synchronization script details / 同步脚本说明](scripts/README.md)

## Development Notes / 开发说明

Keep source changes in `.github/` and run the synchronization check before submitting changes. Do not commit credentials, license keys, downloaded SDK binaries, or private Superpowers distribution files to this repository.

请在 `.github/` 中进行源文件修改，并在提交更改前运行同步检查。请勿将凭据、许可证密钥、下载的 SDK 二进制文件或私有 Superpowers 发行文件提交到本仓库。

```bash
python3 scripts/sync_haca_customizations.py --check
```
