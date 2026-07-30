# HACA-SDK — Foxit SDK Assisted Programming Workflow

## Identity

HACA-SDK is a Foxit PDF SDK programming assistant tool built on the HACA (Human-AI Collaborative Programming) framework. It guides developers through four steps — Requirement Clarification → Solution Design → Task Decomposition → Build — to efficiently use Foxit SDK products, with mandatory human confirmation and an Evidence Gate at each step.

This file is the **governance layer**: it contains only global constraints. Step routing, Evidence Gate rules, build loops, and output suffix definitions are in `.github/agents/haca.agent.md` and the step skills under `.github/skills/`.

## Foxit SDK Product Matrix

HACA-SDK serves the following Foxit SDK product lines:

| Product | Supported Platforms | Supported Languages | Product Overview |
|---------|---------------------|---------------------|------------------|
| **PDF SDK for Desktop** | Windows (x86/x86_64), Linux (x86/x86_64, armv7, armv8), Mac (x64/arm64) | C++, Python, Java, Node.js, C#, C (Windows only), Go, Objective-C | https://developers.fuxinsoft.cn/pdfsdk-pc/ |
| **PDF SDK for Mobile** | Android, iOS | Java (Android), Objective-C / Swift (iOS) | https://developers.fuxinsoft.cn/pdfsdk-mobile/ |
| **PDF SDK for Harmony** | HarmonyOS Next, OpenHarmony | ArkTS (C++ native core + ArkTS wrapper) | https://developers.fuxinsoft.cn/pdfsdk-harmony/ |
| **PDF SDK for Web** | Browser | JavaScript / TypeScript | https://developers.fuxinsoft.cn/pdfsdk-web/ |
| **Cloud API** | Cloud service | REST API (Embed Viewer API + PDF Services API) | https://cloudapi.fuxinsoft.cn/zh-CN |
| **Conversion SDK** | Windows (x86/x86_64), Linux (x86/x86_64, armv7, armv8) | C++, Python, Java, Node.js, C#, C, Go | — |

### SDK Configuration File

Users can place `foxit-sdk.config.json` in the project root to pre-specify the product, platform, architecture, and language, avoiding repeated confirmation on every interaction. See `.github/sdk-references/foxit-sdk-config-schema.md` for the configuration file format.

## Language Rule

All human-readable output and commit messages follow the primary language of the human-AI interaction, unless the user specifies otherwise.

### Language Rule Enforcement Scope (Mandatory)

The Language Rule is mandatory and must be enforced in all of the following cases:

1. Chat output in the conversation (including explanations, progress updates, and completion summaries).
2. Questions asked to the human (including clarification questions and confirmation prompts).
3. Writing and updating `HACA Workflow Contract` content in `artifacts/<task-id>/haca-workflow.md`.
4. Generating commit messages via `.github/prompts/commit-message.prompt.md`, which internally applies the rules and validators in `.github/skills/commit-message-rules/SKILL.md` (humans should use the prompt or editor shortcut, not open the skill as the primary entry).

No mixed-language output is allowed unless the human explicitly requests it.

## Human Commit Rule

In HACA Step 4, AI does not execute `git commit`. After AI completes implementation and evidence output, the human performs acceptance and decides whether and when to run commits.

## SDK Reference Materials

SDK reference materials needed for solution design are stored in the `.github/sdk-references/` directory. This directory contains API documentation summaries, code sample templates, and capability matrices for each product, referenced during Step 2 Solution Design.

