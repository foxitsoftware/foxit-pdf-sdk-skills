# HACA-SDK Skills

> 面向福昕 PDF SDK 的人机协作编程

[English](README.md) | **简体中文**

HACA-SDK 是基于人机协作编程（HACA）工作流构建的福昕 PDF SDK 编程助手配置，为 GitHub Copilot 提供共享的治理规则、代理（agents）、提示词（prompts）、技能（skills）以及 SDK 参考资料。

## 仓库结构

```text
.
├── .github/
│   ├── agents/              # GitHub Copilot 自定义代理
│   ├── prompts/             # HACA 工作流提示词入口
│   ├── skills/              # HACA 工作流使用的源技能
│   │   └── superpowers/     # 本地 Superpowers 技能安装目录
│   ├── sdk-references/      # 福昕 SDK 能力与配置参考
│   ├── templates/           # 工作流契约模板
│   ├── workflows/           # CI 校验工作流
│   └── copilot-instructions.md
├── docs/                    # 设计说明与工作流文档
├── scripts/                 # HACA 校验脚本
│   └── sync_haca_customizations.py
└── README.md
```

`.github/` 目录包含 GitHub Copilot 的主配置，是 HACA 工作流的唯一事实来源（source of truth）。

## 支持平台

本仓库当前支持 GitHub Copilot。

福昕 SDK 产品参考覆盖桌面端（Desktop）、移动端（Mobile）、鸿蒙（Harmony）、Web、云 API（Cloud API）以及转换 SDK（Conversion SDK）等场景。参考资料布局请参阅 [.github/sdk-references/README.md](.github/sdk-references/README.md)。

## 安装设置

### 1. 克隆或复制仓库

将仓库作为 VS Code 工作区打开，以便 `.github/` 配置对助手集成可用。

### 2. 手动安装 Superpowers 技能（可选）

`superpowers` 目录是一个安装位置，而不是外部 Superpowers 技能库的捆绑副本。**HACA 不依赖它即可工作**——每个由 Superpowers 支撑的步骤都会优雅降级为内置的 HACA 等价流程，并记录 `Not Available` 证据。安装它是可选的，仅用于升级步骤 1-4 内部的质量控制工具。

用户需从官方上游来源（[obra/superpowers](https://github.com/obra/superpowers)）下载 Superpowers 技能，并将技能文件或目录放入：

```text
.github/skills/superpowers/
```

各宿主环境的安装命令（上游文档）：

| 宿主环境 | 命令 / 入口 |
|---------|------------|
| GitHub Copilot CLI | `copilot plugin marketplace add obra/superpowers-marketplace` 然后 `copilot plugin install superpowers@superpowers-marketplace` |
| Claude Code | `/plugin install superpowers@claude-plugins-official` |
| Cursor | `/add-plugin superpowers` |
| Codex CLI | `/plugins` → 搜索 `superpowers` → Install Plugin |
| OpenCode | 获取并遵循 `https://raw.githubusercontent.com/obra/superpowers/refs/heads/main/.opencode/INSTALL.md` |
| Gemini CLI | `gemini extensions install https://github.com/obra/superpowers` |
| 其他宿主环境 | 参见上游 README 的 "Installation" 章节 |

例如，安装后该目录可能包含如下技能：

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

请不要假设仓库中包含完整的外部 Superpowers 包。若技能缺失，相关步骤会使用内置的 HACA 等价流程，并在步骤输出中记录 `Superpowers capability: Not Available (<capability-name>)`。技能缺失时该步骤仍可正常完成，仅无法获得 Superpowers 的质量增强。该目录的预期作用与完整安装矩阵请参阅 [.github/skills/superpowers/README.md](.github/skills/superpowers/README.md)。

### 3. （可选）SDK 配置

为避免重复确认 SDK 环境，请在仓库根目录创建 `foxit-sdk.config.json`。该文件可指定福昕 SDK 产品、平台、架构、语言、SDK 版本、许可证环境变量以及 SDK 路径。Schema 及示例请参阅 [.github/sdk-references/foxit-sdk-config-schema.md](.github/sdk-references/foxit-sdk-config-schema.md)。

## 使用 HACA 工作流

HACA 通过四个确认步骤处理编程任务：

1. **需求澄清**：确定福昕 SDK 产品、平台、架构、语言、验收标准与范围。
2. **方案设计**：查阅 SDK 参考资料，比较实现方案并识别风险。
3. **任务分解**：将确认后的方案拆分为可执行的子任务及依赖关系。
4. **构建**：通过测试、编译、运行时检查与证据验证实现工作内容。

在 GitHub Copilot 中，请使用 HACA 代理或 `.github/prompts/` 下对应的提示词命令：

```text
/haca-step1
/haca-step2
/haca-step3
/haca-step4
```

每个步骤在推进前都需要用户明确确认。工作流激活后，HACA 代理会将确认的任务上下文存储在工作流契约文件 `artifacts/<task-id>/haca-workflow.md` 中。

## 技能

| 技能 | 用途 |
|------|------|
| `clarify-requirements` | 步骤 1 —— 确定目标 SDK 产品、平台、架构与语言，澄清编程任务需求。 |
| `risk-identification` | 步骤 2 —— 查阅 SDK 参考资料，比较方案并识别风险。 |
| `task-decomposition` | 步骤 3 —— 将确认后的方案拆分为便于代码评审的子任务及依赖。 |
| `tdd-loop` | 步骤 4 —— 强制 Red-Green-Refactor 以及编译/运行时正确性。 |
| `evidence-gate` | 维护单一证据包，在证据不完整时阻止步骤推进。 |
| `commit-message-rules` | 标准化提交消息的内部规则（模板、长度检查、校验器）。 |

## 文档

- [HACA 执行流程](docs/haca-execution-flow.md)
- [人机协作编程工作流](docs/human-ai-collaborative-programming-workflow.md)
- [SDK 参考资料](.github/sdk-references/README.md)
- [校验脚本说明](scripts/README.md)

## 开发说明

请在 `.github/` 中进行源文件修改，并在提交更改前运行校验检查。`sync_haca_customizations.py` 脚本用于校验 `.github/` Copilot 配置树（它不再进行跨平台同步——本仓库仅面向 GitHub Copilot）。请勿将凭据、许可证密钥、下载的 SDK 二进制文件或私有 Superpowers 发行文件提交到本仓库。

```bash
python3 scripts/sync_haca_customizations.py --check
```
