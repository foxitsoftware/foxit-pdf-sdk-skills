# HACA 与 superpowers 融合可行性分析报告

## 目录

- [1. 报告目的](#1-报告目的)
- [2. 结论摘要（Executive Summary）](#2-结论摘要executive-summary)
- [3. 范围与边界](#3-范围与边界)
- [4. 双系统现状解析](#4-双系统现状解析)
- [5. 能力互补性分析](#5-能力互补性分析)
- [6. 融合架构设计](#6-融合架构设计)
- [7. 按需调用机制](#7-按需调用机制)
- [8. 关键差异处理方案](#8-关键差异处理方案)
- [9. 可行性分析](#9-可行性分析)
- [10. 风险与缓解](#10-风险与缓解)
- [11. 回滚与退出机制](#11-回滚与退出机制)
- [12. Go/No-Go 评审清单](#12-gono-go-评审清单)
- [13. 建议决策](#13-建议决策)
- [附录 A：术语表](#附录-a术语表)

## 1. 报告目的
- 基于对 superpowers 全部 14 个 Skill 的实际阅读，重新评估两个系统的融合可行性。
- 保持 HACA 四步人工确认门禁为主治理流程，将 superpowers 能力作为各步骤内部的执行方法论层。
- 输出具有实操价值的融合架构设计与按需调用机制，供 maintainer 评审。

## 2. 结论摘要（Executive Summary）
- **结论：高度可行，建议采用"治理层 + 方法论层"双层架构**
- **核心判断：** superpowers 并非一组专项检查工具，而是一套完整的开发生命周期工作流方法论（14 个 Skill 覆盖从需求到合并的全链路）。融合的本质是：**HACA 负责人工确认节点治理，superpowers 负责每个节点内部的执行质量保障**。
- **成本：** 低至中（无需自研新能力，仅需建立调用映射规则与证据回写协议）。
- **风险：** 可控，主要矛盾在于 HACA 的高频人工确认与 superpowers 的自主执行设计取向之间的张力，可通过架构分层解决。

## 3. 范围与边界

### 3.1 本次范围
- 仅面向当前仓库的 HACA 脚手架。
- 基于对 superpowers 全部 Skill 的实际内容分析，评估技术互补性与融合架构。
- 不改动 HACA 四步流程的语义与人工确认节点。

### 3.2 不在本次范围
- 企业级多仓库统一治理。
- 超出当前 superpowers 已有 Skill 范围的新能力研发。
- 自动化评估平台建设。

---

## 4. 双系统现状解析

### 4.1 HACA 核心机制

HACA 是以**人工确认节点**为主轴的四步编程协作治理框架：

| 步骤 | 职责 | 输出 | 关口 |
|---|---|---|---|
| Step 1：需求澄清 | 结构化验证需求完整性 | Task Input + AI Decision Summary v0 | Evidence Gate → 等待人工确认 |
| Step 2：方案设计 | 五维风险识别与方案决策 | 完整 AI Decision Summary（含风险） | Evidence Gate → 等待人工确认 |
| Step 3：任务分解 | 拆分为可评审子任务 | Subtask List + Execution Order | Evidence Gate → 等待人工确认 |
| Step 4：实施与验收交接 | TDD 循环 + 证据采集 + 交接 | 每个子任务的代码 + 证据包 | Evidence Gate（每个子任务交接前） |

**HACA 的核心价值：** 通过结构化人工关口，保证每个阶段的决策可审计、可回溯。

### 4.2 Superpowers 能力全景（14 个 Skill 实际内容）

Superpowers 是一套**面向编程 Agent 的完整开发生命周期方法论**，通过 14 个可组合 Skill 构成流水线，每个 Skill 都有明确的触发条件、iron law 和流程图：

#### 元治理层（1 个）
| Skill | 核心机制 | 关键规则 |
|---|---|---|
| **using-superpowers** | Agent 在任何响应前先检查是否有适用 Skill，有 1% 可能就必须调用；用户指令 > Skill > 默认系统行为 | 优先级：用户指令 > Skills > 默认行为；强制调用，无例外 |

#### 前期探索与设计层（1 个）
| Skill | 触发条件 | 核心机制 | Iron Law |
|---|---|---|---|
| **brainstorming** | 任何创建功能、实现特性的任务 | 逐一提问 → 提出 2-3 个方案及权衡 → 分段展示设计 → 用户确认 → 写 spec 文档 → subagent spec review loop → 调用 writing-plans | **Hard Gate：** 用户确认设计前不得写任何代码 |

#### 规划层（2 个）
| Skill | 触发条件 | 核心机制 |
|---|---|---|
| **writing-plans** | 有确认的 spec 或需求、准备动手前 | 零上下文假设（假设执行者不了解代码库）；每个步骤 2-5 分钟粒度；TDD/DRY/YAGNI；文件结构前置映射；保存到 `docs/superpowers/plans/` |
| **using-git-worktrees** | 开始功能开发或执行计划前 | 创建隔离 worktree；优先检查 `.worktrees`、`CLAUDE.md` 偏好；强制安全校验（gitignore 验证） |

#### 执行层（3 个）
| Skill | 触发条件 | 核心机制 |
|---|---|---|
| **subagent-driven-development** | 有 implementation plan、任务相互独立 | 每个 task 派发一个全新 subagent（无上下文污染）；双重审查（spec 合规性审查 → 代码质量审查）；失败则修复后重审 |
| **executing-plans** | 有 implementation plan、无 subagent 支持时 | 串行执行；遇到阻塞立即暂停询问；完成后调用 finishing-a-development-branch |
| **dispatching-parallel-agents** | 2+ 个互相独立的问题域并发存在 | 精准构造每个 agent 的指令与上下文（不继承会话历史）；并行调度；结果汇总去冲突 |

#### 代码质量保障层（4 个）
| Skill | 触发条件 | 核心机制 | Iron Law |
|---|---|---|---|
| **test-driven-development** | 任何特性实现或 bug 修复前 | RED（写失败测试）→ 验证失败 → GREEN（最少代码通过）→ REFACTOR | **No production code without a failing test first；** 先写代码的必须删掉重来 |
| **systematic-debugging** | 遇到任何 bug、测试失败、异常行为 | 4 阶段：根因调查 → 假设定位 → 验证修复 → 防御强化；多组件场景先加诊断埋点 | **No fixes without root cause investigation first** |
| **verification-before-completion** | 任何声称工作完成、测试通过、bug 已修 | 先跑命令 → 读完整输出 → 验证 exit code → 确认符合声明后才能说"完成" | **No completion claims without fresh verification evidence** |
| **requesting-code-review** | 每个子任务完成后、主要特性完成、合并前 | dispatch superpowers:code-reviewer subagent（精确上下文，不含会话历史）；Critical 必须修；Important 合并前修；Minor 记录备后 |

#### 协作与品质层（2 个）
| Skill | 触发条件 | 核心机制 |
|---|---|---|
| **receiving-code-review** | 收到代码审查反馈时 | 技术性评估而非情绪表演；全读 → 理解 → 验证 → 评估 → 有理由才推回；不明确则先问清楚后执行 |
| **finishing-a-development-branch** | 实现完成、测试全绿后 | 验证测试 → 确定基础分支 → 呈现 4 个选项（本地合并/PR/保留/丢弃）→ 执行选择 → 清理 |

#### 自我演进层（1 个）
| Skill | 核心机制 |
|---|---|
| **writing-skills** | TDD 应用于流程文档；新 Skill 必须先跑 baseline（不带 Skill 让 Agent 失败），再写 Skill，再验证；遵循 RED-GREEN-REFACTOR |

---

## 5. 能力互补性分析

### 5.1 相似点（可复用/对齐）

| 维度 | HACA | Superpowers | 对齐程度 |
|---|---|---|---|
| 设计先行 | Step 1 结构化需求澄清 | brainstorming Hard Gate（代码前必有设计） | 高 |
| 任务分解 | Step 3 可评审粒度拆分 | writing-plans 2-5 分钟粒度计划 | 高 |
| TDD | Step 4 tdd-loop SKILL | test-driven-development Iron Law | 高，superpowers 规则更严格 |
| 交接前验证 | Evidence Gate（每个子任务交接前） | verification-before-completion Iron Law | 高 |
| 代码审查 | （无内置，依赖人工） | requesting-code-review + receiving-code-review | Superpowers 有完整 subagent 驱动的审查链 |
| 风险识别 | Step 2 五维风险识别 | brainstorming（提出 2-3 方案含权衡） | 中，HACA 更系统，superpowers 更对话式 |

### 5.2 关键差异（架构张力）

| 维度 | HACA 取向 | Superpowers 取向 | 张力 |
|---|---|---|---|
| **人工参与频率** | 每步都必须人工确认，无法绕过 | subagent-driven-development 设计为自主运行数小时，最小化打断 | **核心张力**，需要架构分层解决 |
| **需求澄清方式** | 结构化模板（Task Input + AI Decision Summary + blocking/non-blocking 分类） | 对话式逐问（一次一问，提出 2-3 个方案） | 形式不同，可在 Step 1 内组合 |
| **TDD 严格性** | tdd-loop SKILL（证据留存为主） | Iron Law（先写代码必须删掉重来） | superpowers 更严格，向 superpowers 对齐不降级 |
| **Skill 调用方式** | 显式、受控、可追踪地按规则执行 | Agent 基于元规则自动触发（1% 可能就调用） | HACA 下需保留人工可见的决策痕迹 |
| **计划文档位置** | 无强约定（Step 3 输出在对话中） | `docs/superpowers/plans/YYYY-MM-DD-*.md`（持久化文件） | superpowers 更便于 subagent 读取执行 |

---

## 6. 融合架构设计

### 6.1 架构原则
1. **治理不降级：** HACA 四步流程与人工确认门禁不因引入 superpowers 而弱化。
2. **方法论提升：** 每个 HACA 步骤内部的执行质量由 superpowers 对应 Skill 保障。
3. **不替代，只增强：** superpowers Skill 的输出必须回写到 HACA 证据包与 AI 决策摘要。
4. **冲突时 HACA 胜出：** HACA 规则 > superpowers Skill 建议 > Agent 默认行为；用户显式指令始终最高优先级。
5. **可裁剪：** 同一任务可按需选择 0 到 N 个 Skill 增强，简单任务可不引入。

### 6.2 双层架构图

```
┌─────────────────────────────────────────────────────────────────────┐
│                    HACA 治理层（主流程）                              │
│  Step 1 → [确认] → Step 2 → [确认] → Step 3 → [确认] → Step 4       │
│               ↑ Evidence Gate（每个确认点 + 每个子任务交接前）        │
└──────────────────────────┬──────────────────────────────────────────┘
                           │ 各步骤内部调用
┌──────────────────────────▼──────────────────────────────────────────┐
│                Superpowers 方法论层（执行质量保障）                   │
│  brainstorming │ writing-plans │ TDD │ debugging │ code-review ...  │
└─────────────────────────────────────────────────────────────────────┘
```

### 6.3 各步骤融合方案

#### Step 1：需求澄清

| 场景 | Superpowers Skill | 作用 | 触发条件 |
|---|---|---|---|
| 需求模糊、目标发散 | **brainstorming** | 逐步提问澄清意图，探索方案取向 | 需求描述含歧义或缺少功能边界 |
| 复杂多子系统任务 | **brainstorming**（子项目拆解模式） | 识别边界并建议先分拆再各自澄清 | 单个需求描述涵盖 3+ 独立子系统 |

> **回写要求：** brainstorming 探索结果（用户确认的意图理解与设计取向）写入 AI Decision Summary 的"需求理解"字段；探索中的分歧方案写入"拒绝方案"。

#### Step 2：方案设计

| 场景 | Superpowers Skill | 作用 | 触发条件 |
|---|---|---|---|
| 多方案权衡 | **brainstorming**（方案提议阶段） | 提出 2-3 个具体方案含文字权衡说明 | 任何需要方案决策的任务 |
| 需要子系统并行分析 | **dispatching-parallel-agents** | 并行 agent 分别分析不同方案子域 | 方案中存在 2+ 独立技术子域 |

> **回写要求：** 方案分析结果写入 AI Decision Summary 的"采用方案""拒绝方案""已知风险""未覆盖场景"字段。

#### Step 3：任务分解

| 场景 | Superpowers Skill | 作用 | 触发条件 |
|---|---|---|---|
| 任务计划生成 | **writing-plans** | 生成零上下文假设的详细实施计划，含文件映射、TDD 步骤、2-5 分钟粒度 | 所有需要 Step 4 执行的任务 |
| 隔离工作区 | **using-git-worktrees** | 为特性开发创建独立 worktree | 功能开发、多任务并行时 |

> **回写要求：** writing-plans 输出的计划文档路径与任务清单写入 Subtask List；worktree 路径写入证据包执行上下文字段。计划文件持久化存放于 `docs/superpowers/plans/YYYY-MM-DD-<feature>.md`，供 subagent 读取。

#### Step 4：实施与验收交接

Step 4 的执行引擎与质量保障全面借用 superpowers 的执行层：

**执行引擎（二选一）：**
- **有 subagent 支持时：** 使用 **subagent-driven-development**（每个子任务 → 新 subagent → 双重审查循环）
- **无 subagent 支持时：** 使用 **executing-plans**（串行执行，阻塞即暂停询问）

**代码质量保障（每个子任务内）：**

```
每个子任务的执行流：
  1. [test-driven-development] RED → GREEN → REFACTOR
  2. [verification-before-completion] 跑完整验证命令，保留输出作证据
  3. [systematic-debugging] 若出现失败/异常，先做根因分析；无失败则记录 Not Triggered
  4. [requesting-code-review] dispatch code-reviewer subagent
  5. [receiving-code-review] 技术评估反馈、修复 Critical/Important 项
  6. [Evidence Gate] 校验当前子任务 mandatory capabilities 证据完整性
  7. 输出人工验收交接材料（Evidence Gate 通过后）
```

**遇到阻塞时：**
- 代码/构建问题 → **systematic-debugging**（4 阶段根因分析，不得跳过直接猜测修复）
- 独立子问题并发 → **dispatching-parallel-agents**

**Step 4 完成后：**
- 先执行 Human Acceptance Gate 并写入验收证据（验收人、时间、结果、发现摘要、go/no-go）。
- 验收通过后，再由人工决定是否执行提交，并可使用 **finishing-a-development-branch** 进行后续测试验证、PR 或清理。
- 验收失败时，不改写历史，追加修复变更后重新执行 Human Acceptance Gate。

---

## 7. 按需调用机制

### 7.1 触发类型与优先级

| 触发类型 | 说明 | 优先级 |
|---|---|---|
| **用户显式指令** | 用户直接要求使用某 Skill | 最高 |
| **步骤规则触发** | 某步骤的进入/执行条件匹配触发矩阵 | 高 |
| **Evidence Gate 补证触发** | 门禁发现证据不足，要求补充特定 Skill 的输出 | 高 |
| **Agent 自主判断** | Agent 评估有 ≥1% 可能性适用时主动建议 | 中（须在步骤确认点经 Human 裁决） |

### 7.2 触发矩阵（基于实际 Skill）

| HACA 步骤 | 触发条件 | Superpowers Skill | 输出回写位置 |
|---|---|---|---|
| Step 1 | 需求含歧义 / 目标不清晰 | brainstorming（澄清模式） | AI Decision Summary：需求理解 |
| Step 1 | 任务可能跨多个独立子系统 | brainstorming（子项目拆解模式） | AI Decision Summary：约束与边界 |
| Step 2 | 任何需要方案决策的任务 | brainstorming（方案提议阶段） | AI Decision Summary：采用/拒绝方案 |
| Step 2 | 方案含 2+ 独立技术子域 | dispatching-parallel-agents | AI Decision Summary：已知风险 |
| Step 3 | 所有需要 Step 4 执行的任务 | writing-plans | Subtask List；docs/superpowers/plans/ |
| Step 3 | 需要特性开发隔离 | using-git-worktrees | 证据包：执行上下文 |
| Step 4（每子任务） | 始终 | test-driven-development | 证据包：测试证据（RED/GREEN 截图/日志） |
| Step 4（每子任务） | 始终 | verification-before-completion | 证据包：验证命令输出 |
| Step 4（每子任务） | 始终（失败时执行；无失败记 Not Triggered） | systematic-debugging | 证据包：根因分析或 Not Triggered 记录 |
| Step 4（每子任务） | 始终 | requesting-code-review | 证据包：代码审查结论 |
| Step 4（每子任务） | 始终 | receiving-code-review | 证据包：反馈处理记录 |
| Step 4（2+ 独立失败） | 多个不相关失败并发 | dispatching-parallel-agents | 证据包：各子域修复摘要 |
| 所有步骤 | 将声称"完成" | verification-before-completion | 证据包：验证输出 |
| Step 4 全部完成后 | 所有子任务绿灯 | Human Acceptance Gate（HACA 治理层） | Human Acceptance 证据与 go/no-go 决策 |
| Step 4 验收通过后 | 需要后续分支整理时 | finishing-a-development-branch | PR / 合并 / 清理选项 |

### 7.3 证据回写最小字段（统一标准）

所有 Skill 调用结果必须以如下结构写入当前子任务的证据包或 AI 决策摘要：

```
- Skill 名称：[skill name]
- Skill 来源路径：[.github/skills/superpowers/<skill-name>/SKILL.md]
- 触发原因：[触发条件的简短描述]
- 关键发现：[该 Skill 执行后的核心结论]
- 建议动作：[Skill 建议的行动]
- 是否采纳：[已采纳 / 部分采纳 / 未采纳]
- 采纳理由：[决策依据，未采纳时必填]
```

未回写视为未执行，Evidence Gate 将阻断子任务交接。

---

## 8. 关键差异处理方案

### 8.1 人工确认频率 vs. 自主执行（核心张力）

**问题：** HACA 的步骤确认点要求人工参与；superpowers 的 subagent-driven-development 设计为最小打断、数小时自主运行。

**解决方案（架构分层）：**
- HACA 步骤边界（Step 1/2/3 确认点、Step 4 每个子任务交接前的 Evidence Gate）的人工关口**不可妥协**。
- subagent-driven-development 运行在**每个子任务的内部循环**中（两阶段 subagent review 无需人工介入）。
- 唯一进入人工视野的是：Evidence Gate 校验结果 + 人工验收决策。

**结果：** 自主执行发生在 HACA 划定的安全边界内，不突破治理关口。

### 8.2 TDD 严格性对齐

**问题：** Superpowers 的 TDD Iron Law 比 HACA 的 tdd-loop SKILL 更严格（先写代码必须删掉重来）。

**解决方案：** 向 superpowers TDD Iron Law 对齐，在 Step 4 的 SKILL.md 中明确引用此规则，不降级。

### 8.3 计划文档持久化

**问题：** HACA Step 3 的输出当前存在于对话中，不便于 subagent 读取。

**解决方案：** Step 3 完成后，by default 使用 writing-plans 生成并持久化计划文件到 `docs/superpowers/plans/YYYY-MM-DD-<feature>.md`，作为 Step 4 执行引擎的输入。

---

## 9. 可行性分析

### 9.1 技术可行性
- **高**：HACA 当前已有 skills/agents 目录结构；superpowers 的 Skill 均以 Markdown + frontmatter 形式存在，与 HACA 技术栈完全兼容。
- **依赖项：** 仅需在 HACA 各步骤 SKILL.md 中添加 superpowers Skill 的调用建议规则；证据回写字段标准化。

### 9.2 流程可行性
- **高**：HACA 步骤确认点是天然的"建议调用 → 人工裁决 → 执行 → 证据回写"节点。
- **关键约定：** 明确"未回写视为未执行"；Evidence Gate 检查 Skill 调用证据字段。

### 9.3 组织可行性
- **中高**：需要 maintainer 维护触发矩阵并在各 SKILL.md 中更新调用建议；superpowers Skill 自身有 writing-skills 方法论保障持续演进。
- **关键：** 触发矩阵与 SKILL.md 同仓库管理，版本一致。

### 9.4 经济可行性
- **优于预期**：superpowers 的 subagent-driven-development + 双重代码审查可提升每次提交的初始质量，减少后期返工；systematic-debugging 防止"猜测修复"浪费上下文窗口。
- **额外成本：** 仅证据回写的维护规范（一次性建立，低后续成本）。

---

## 10. 风险与缓解

| 风险 | 描述 | 缓解措施 |
|---|---|---|
| **规则冲突** | Superpowers Skill 建议与 HACA 规则矛盾 | 明确优先级：用户指令 > HACA 规则 > Superpowers 建议 > Agent 默认行为 |
| **证据回写遗漏** | Skill 调用了但未留证据，Evidence Gate 无法校验 | Evidence Gate 增加"Skill 执行证据"检查项；未回写字段即拒绝提交 |
| **过度自主** | subagent-driven-development 跳过 HACA 步骤确认点 | 明确：subagent 仅在子任务内部循环运行；步骤边界由主 Agent 持有并不委托给 subagent |
| **TDD Iron Law 绕过** | 时间压力下跳过红灯阶段 | writing-plans 的每个 Task 均包含"写失败测试"步骤；Evidence Gate 要求测试证据（含失败截图） |
| **调用建议噪音** | Agent 频繁建议调用 Skill 打断流程 | 触发矩阵以步骤规则触发为主（明确条件）；Agent 自主建议须在步骤确认点统一提出，不中途打断 |
| **Skill 版本漂移** | superpowers Skill 更新但 HACA 触发矩阵未同步 | Skill 文件与触发矩阵同仓库，PR 合并须附带触发矩阵一致性检查 |

---

## 11. 回滚与退出机制

**回滚触发条件（任意一项）：**
- Evidence Gate 因 Skill 证据校验不稳定导致连续阻断 → 临时下线对应 Skill 的门禁规则，回退到原生 HACA 校验。
- Subagent review 循环导致单子任务执行耗时显著超出预期 → 切换到 executing-plans 串行模式。
- 触发矩阵规则与实际场景匹配度低导致频繁误触发 → 收紧触发条件为高置信度场景白名单。

**完全回退路径：**
1. 在各步骤 SKILL.md 中注释掉 superpowers Skill 调用建议。
2. Evidence Gate 恢复到纯 HACA 原生证据字段校验。
3. 保留 writing-plans 生成的计划文件（记录价值不变）。

---

## 12. Go/No-Go 评审清单

- [ ] HACA 四步流程与人工确认节点保持不变。
- [ ] Superpowers Skill 仅在 HACA 步骤内部调用，不创建新的步骤。
- [ ] 所有 Skill 调用结果有统一证据回写字段，Evidence Gate 可验证。
- [ ] Step 4 五项 mandatory quality controls 均有执行证据，或有 Not Triggered/批准例外记录。
- [ ] TDD Iron Law 被采纳（不低于 superpowers 原始严格度）。
- [ ] Subagent 自主运行边界被明确隔离在子任务内部循环。
- [ ] 触发矩阵与 SKILL.md 在同一仓库管理，版本一致性可审计。
- [ ] 存在完整的分层回退路径（Skill 级 → 模式级 → 完全回退）。
- [ ] Human Acceptance Gate 在主线集成前执行且结果为 pass。

---

## 13. 建议决策

**建议 Go（高置信度）：**
- 融合策略：**治理层 (HACA) + 方法论层 (Superpowers)**，两层在架构上清晰分离。
- 优先落地 Step 4 执行链（subagent-driven-development + TDD + verification + code-review），质量收益最直接。
- 其次落地 Step 3 的 writing-plans 计划持久化，解决 subagent 上下文获取问题。
- 最后扩展 Step 1/2 的 brainstorming 集成（可选，视任务复杂度）。

---

## 附录 A：术语表

| 术语 | 定义 |
|---|---|
| HACA Core | 四步流程（需求澄清/方案设计/任务分解/实施提交）+ Evidence Gate + 人工确认关口 |
| Superpowers | 14 个可组合的编程 Agent 方法论 Skill，覆盖从需求到合并的完整开发生命周期 |
| 触发矩阵 | 定义"在哪个 HACA 步骤、满足哪些条件时，调用哪个 Superpowers Skill"的规则集合 |
| 证据回写 | 将 Skill 执行结论按统一格式写入 HACA 当前步骤的 AI 决策摘要或证据包 |
| Iron Law | Superpowers Skill 中无例外强制规则（如：无失败测试不写生产代码） |
| 方法论层 | Superpowers Skill 在 HACA 各步骤内部提供的执行质量保障机制 |
| subagent | 由主 Agent 派发的专项子代理，持有精确构造的指令与上下文，不继承会话历史 |
