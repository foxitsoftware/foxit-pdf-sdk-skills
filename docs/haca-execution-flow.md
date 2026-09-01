# HACA 执行流程详细描述

- **报告范围**：HACA 在仓库中的目标行为与配置关系（与 `.github/` 下实现相互对照）。
- **报告目的**：形成可供人类与 AI 共同评审的 HACA 流程完整描述；并作为「先改文档、再落实现」时的规范输入。
- **更新日期**：2026-03-28 10:30（随流程演进更新本日期或修订记录即可）。

### 与 `.github/` 实现的关系（维护约定）

| 方式 | 说明 |
|------|------|
| **实现优先** | 若直接在 `.github/` 修改了 HACA 行为，应同步更新本文档，使描述与代码一致。 |
| **规范优先** | 若先修改本文档以调整目标行为，应在评审后使用仓库提示 **`haca-apply-spec`**（源：`.github/prompts/haca-apply-spec.prompt.md`；Cursor 中对应 `/haca-apply-spec`）将变更落实到 `.github/`，再运行 **`/haca-sync`** 将 `.github/` 同步到 `.cursor/`、`.opencode/` 并校准手工适配层。 |

上述两种方式可以并存；合并前须保证 **本文档 ↔ `.github/`** 无未解决的语义冲突。

---

## 1. 配置文件清单

下列文件为当前 HACA 的**实现清单**；编写/修订本文档时以这些路径为对照。当采用「规范优先」流程时，以**本文档与已确认的差异**为准更新这些文件。

### **治理层**
1. `.github/copilot-instructions.md` — 仓库级治理约束（仅定义"什么允许、什么禁止"）

### **编排层**
2. `.github/agents/haca.agent.md` — HACA Agent 定义（人格、命令、步骤识别、Build Loop、异常处理）

### **技能层**
3. `.github/skills/clarify-requirements/SKILL.md` — Step 1 需求澄清技能
4. `.github/skills/risk-identification/SKILL.md` — Step 2 方案设计与风险识别技能
5. `.github/skills/task-decomposition/SKILL.md` — Step 3 任务分解技能
6. `.github/skills/tdd-loop/SKILL.md` — Step 4 TDD 循环与质量链技能
7. `.github/skills/evidence-gate/SKILL.md` — 跨步骤证据门禁技能

### **输入模板**
8. `.github/prompts/haca-step1.prompt.md` — Step 1 prompt 入口
9. `.github/prompts/haca-step2.prompt.md` — Step 2 prompt 入口
10. `.github/prompts/haca-step3.prompt.md` — Step 3 prompt 入口
11. `.github/prompts/haca-step4.prompt.md` — Step 4 prompt 入口
12. `.github/prompts/commit-message.prompt.md` — 独立快捷入口：生成提交信息，并在人工明确确认后才执行提交
13. `.github/prompts/haca-apply-spec.prompt.md` — 依据 `docs/haca-execution-flow.md` 将规范变更落实到 `.github/` 的执行入口
14. `.github/prompts/haca-sync.prompt.md` — 将 `.github/` 同步到 `.cursor/`、`.opencode/` 并校准手工适配层的执行入口
15. `.github/templates/haca-workflow-contract.template.md` — `HACA Workflow Contract` 单一模板源（初始化 artifacts 合同时使用）

### **Superpowers 能力库**
16. `.github/skills/superpowers/` — 本地离线能力源（brainstorming、dispatching-parallel-agents、writing-plans、using-git-worktrees、test-driven-development、verification-before-completion、systematic-debugging、requesting-code-review、receiving-code-review、finishing-a-development-branch）

### **参考示例（辅助，非执行规则）**
17. `.github/skills/clarify-requirements/references/examples.md` — Step 1 澜清提问场景示例
18. `.github/skills/risk-identification/references/risk-examples.md` — Step 2 五维度风险示例
19. `.github/skills/task-decomposition/references/antipatterns.md` — Step 3 常见拆分反模式与纠正示例

---

## 2. 三层架构

HACA 的配置职责被分为三层，禁止跨层重复定义：

| 层级 | 文件 | 职责 |
|------|------|------|
| 治理层 | `copilot-instructions.md` | 定义全局约束与禁止项；不包含命令级执行顺序或步骤内操作细节 |
| 编排层 | `haca.agent.md` | 定义 Agent 人格、命令入口、步骤识别表、Build Loop 流程、异常处理 |
| 技能层 | 各 `SKILL.md` | 定义每个步骤的具体执行规程、输出格式、内部判定逻辑 |

Prompt 文件（`.github/prompts/haca-step*.prompt.md`）仅作为输入模板，不包含编排逻辑、门禁规则或提交策略；它们引用治理层和技能层作为唯一事实来源。

独立 Prompt（如 `.github/prompts/commit-message.prompt.md`）可用于 HACA 之外的快捷操作，但同样不得复制技能内部的校验细节，只负责提供明确入口与交互边界。

---

## 3. 激活条件与隔离规则

**激活**：HACA 工作流仅在以下显式方式触发时激活：选择 HACA Agent、`@HACA`、`/HACA` 或 `/haca-stepN`。

**会话保持**：HACA 一旦在当前对话中被激活，后续请求默认继续按 HACA 模式处理，直到用户显式退出 HACA、切换到其他 Agent 或模式、或开启新对话。

**隔离**：未显式调用 HACA 时，禁止读取或执行以下技能文件：
- `clarify-requirements/SKILL.md`
- `risk-identification/SKILL.md`
- `task-decomposition/SKILL.md`
- `tdd-loop/SKILL.md`
- `evidence-gate/SKILL.md`

此时使用默认编码工作流处理请求。

**例外**：
- `commit-message.prompt.md` 可在任何工作流中独立调用，用于快捷生成提交信息，并在人工明确确认后执行提交。
- 非 HACA 技能（如 Superpowers 子能力）在相关时可按需调用或引导加载；不保证平台层面的自动发现与自动加载。

**Step 1 确认前约束**：在 Step 1 获得人工确认之前，禁止读取业务代码、编写代码或运行构建/测试命令。唯一例外：可读取执行 Step 1 和 Evidence Gate 所需的工作流规则文件（具体路径：`.github/copilot-instructions.md`、`.github/agents/haca.agent.md`、`.github/skills/clarify-requirements/SKILL.md`、`.github/skills/evidence-gate/SKILL.md`）。

---

## 4. 总体治理模型

### 4.1 四步串行工作流

```
Step 1: Requirement Clarification（需求澄清）
    ↓ [人工确认] + [Evidence Gate]
Step 2: Solution Design（方案设计）
    ↓ [人工确认] + [Evidence Gate]
Step 3: Task Decomposition（任务分解）
  ↓ [人工确认] + [Evidence Gate]
Step 4: Build（构建）
    ↓ [每子任务循环：TDD → 验证 → 门禁 → 验收交接]
    ↓ [最终 Evidence Gate]
    → 输出完成提示语，等待人工验收与人工提交
```

### 4.2 核心治理原则

1. **逐步确认**：每一步结束后必须等待人工明确确认，才能进入下一步。
2. **确认信号**：只有显式的批准词语（如 "confirm"、"ok"、"continue"、"LGTM"）才构成有效确认。实质性修改反馈不算确认——收到修改意见时必须重新生成完整输出后再次等待确认。
3. **Evidence Gate**：每次步骤转换前和 Step 4 每个子任务完成交接前，必须执行 Evidence Gate。
4. **证据闭环**：Step 4 中每个子任务都必须产出可追踪的测试与验证证据。
5. **完成等待**：Step 4 全部完成后，必须输出固定完成提示语并等待人工后续指令，禁止自动进行集成操作。
6. **契约优先输入**：只要 `artifacts/<task-id>/haca-workflow.md` 存在，开始处理步骤前必须先从该文件对应章节读取输入，禁止依赖记忆和当前对话上下文作为步骤输入源。

### 4.3 语言规则

所有人类可读输出必须遵循人机交互中使用的主要语言，除非用户另行指定。

### 4.4 严格禁止项

以下行为在任何情况下均被禁止：

1. 当前步骤未经确认就进入下一步。
2. Step 4 中由 AI 直接执行 `git commit`。
3. 输出完成提示语后，人工未给后续指令就进行集成操作。
4. Step 4 中遇到意外问题后，未先上报就擅自变更计划。

---

## 5. 命令入口与前置检查

### 5.1 命令映射

| 命令 | 对应步骤 | 加载的技能文件 |
|------|----------|---------------|
| `/haca-step1` | Step 1 需求澄清 | `clarify-requirements/SKILL.md` |
| `/haca-step2` | Step 2 方案设计 | `risk-identification/SKILL.md` |
| `/haca-step3` | Step 3 任务分解 | `task-decomposition/SKILL.md` |
| `/haca-step4` | Step 4 构建 | `tdd-loop/SKILL.md` + `evidence-gate/SKILL.md` |

### 5.2 命令入口门禁（Command Entry Gate）

`/haca-stepN` 命令是便捷入口，不是旁路。Agent 在执行前必须验证前置步骤的确认状态。**支持三条路由**：会话历史路由（Route A）、显式文档上下文路由（Route B）和打开文件回退路由（Route C）。

**重跑规则（强制）**：`/haca-step1` 到 `/haca-step4` 均允许重跑目标步骤，即使该步骤在 `Step Status Matrix` 中已经 `confirmed`。重跑后仍按同一持久化流程写回契约文档：执行阶段将当前步骤行写为 `draft`，确认后提升为 `confirmed`，并刷新 `last_updated_at`。

**契约优先输入规则（强制）**：只要识别到当前任务存在 `artifacts/<task-id>/haca-workflow.md`，开始处理前必须从契约文件读取所需输入；会话历史/当前对话仅可用于确认信号识别，不得作为步骤输入主来源。

**契约文件识别来源（无歧义定义）**：满足任一即视为"契约文件存在"。
1. 显式路径：命令参数明确提供 `artifact-path`（例如 `/haca-step2 artifacts/202603271430/haca-workflow.md`）。
2. 打开文件回退：当前编辑器打开的文件命中 `artifacts/*/haca-workflow.md`。
3. 当前任务活动契约：Route A 已存在并绑定当前任务的 `artifacts/<task-id>/haca-workflow.md`。

**统一执行动作（Route A/B/C 一致）**：
1. 先读取契约文件中前置步骤章节作为本步骤输入（Step2<-Step1、Step3<-Step2、Step4<-Step3）。
2. 再做 `Step Status Matrix` 中前置步骤 `status: confirmed` 与必填字段校验。
3. 任一校验失败即阻断，不得回退为“从记忆或当前对话推断输入”。

**draft 阻塞规则（适用于 Step 2/3/4）**：若文件头部仍为 `current_step: step1_draft`、`step2_draft`、`step3_draft`，或 `Step Status Matrix` 中对应前置步骤仍为 `draft`，则 `/haca-step2`、`/haca-step3`、`/haca-step4` 必须在前置门禁处阻塞。命令调用本身、提供 `artifact-path`、或仅仅打开契约文件，都不能视为对前置步骤的隐式确认。

#### 路由 A：会话历史路由（主流程）

**契约文档持久化（强制）**：Step 1 首次启动时，生成 `task-id`（`YYYYMMDDHHMM` 格式），自动创建 `artifacts/<task-id>/` 目录和 `haca-workflow.md` 文件（模板来源：`.github/templates/haca-workflow-contract.template.md`）。该文档贯穿全部四个步骤，确保即使在会话历史路由下也有持久化工作介质。每步在输出等待确认标签之前，必须先将当前步骤输出写入文档并将 `Step Status Matrix` 对应步骤设为 `draft`；收到显式确认后，再将该步骤状态提升为 `confirmed`，并刷新文件头部 `current_step` 和 `last_updated_at`。

| 请求 | 前置条件 |
|------|----------|
| `/haca-step2` | 契约文件中 `Step Status Matrix -> Step 1 = confirmed`，且 Step 2 输入从 `## Step 1` 章节读取 |
| `/haca-step3` | 契约文件中 `Step Status Matrix -> Step 2 = confirmed`，且 Step 3 输入从 `## Step 2` 章节读取 |
| `/haca-step4` | 契约文件中 `Step Status Matrix -> Step 3 = confirmed`，且 Step 4 输入从 `## Step 3` 章节读取 |

满足前置条件时，允许对同一步进行重跑。

前置条件不满足时：
1. 不执行所请求的步骤。
2. 重定向到 Step 1 并执行需求澄清。
3. 以 `[HACA Step 1/4: Requirement Clarification] - Artifacts: artifacts/<task-id>/haca-workflow.md (draft written before confirmation; you may edit this file, then confirm next step or terminate) - Wait for your confirmation before moving to the next step` 结束输出。

#### 路由 B：显式文档上下文路由（跨会话支持）

见 §5.2a 详述。当 `/haca-step[N]` 命令附带 `artifacts/<task-id>/haca-workflow.md` 文件路径时（如 `/haca-step2 artifacts/202603271430/haca-workflow.md`），使用文档上下文而非会话历史，支持跨会话继续执行。

对于 `N>1`，若前置步骤仍为 draft，则该路由只能用于恢复并检查契约，不得绕过确认直接进入下一步执行。

#### 路由 C：打开文件回退路由

当命令未显式提供文件路径，但当前编辑器打开的文件中存在 `artifacts/*/haca-workflow.md` 时，自动采用该文件作为恢复上下文，按路由 B 的校验与持久化规则执行。

若存在多个匹配文件导致歧义，必须先要求人类显式指定 `artifact-path` 后再执行。

#### 路由优先级

1. 若命令显式指定了文件路径，使用路由 B。
2. 若命令未指定文件路径但检测到已打开的 `artifacts/*/haca-workflow.md`，使用路由 C。
3. 其他情况使用路由 A。
4. 若同时存在可用会话历史与路由 B/路由 C 的文档上下文，优先文档上下文以避免歧义。

---

### 5.2a 跨会话恢复机制（文档上下文衔接）

**模板单一来源（强制）**：自动初始化 `artifacts/<task-id>/haca-workflow.md` 时，必须使用 `.github/templates/haca-workflow-contract.template.md`。本节仅描述契约字段与流程规则，不作为模板源文件。

#### 前提与设计原则

- **文档作为真实源**：由开发者自管理，不提交仓库。
- **人类修改权利**：可在任何时刻修改、补充或完善上一阶段输出；修改后的内容自动成为下一阶段的有效输入。
- **信任模型**：系统仅检查必要字段是否存在，不做真实性校验或哈希检查。

#### 契约文档位置与组织

**位置**：`artifacts/<task-id>/haca-workflow.md`

**task-id 生成**：创建时自动生成为 `YYYYMMDDHHMM` 格式（例如 `202603271430`）。同一分钟内若重复创建，自动顺延到下一个可用分钟值。

**形式**：单个 Markdown 文件，Step1-4 的结果按章节持续追加，状态索引在文件头部元数据。

#### 文档契约规范

##### 文件头部元数据（YAML Frontmatter）

```yaml
---
task_id: 202603271430
current_step: step3_confirmed
last_updated_at: 2026-03-27T14:45:00Z
---
```

必填字段：`task_id`、`current_step`、`last_updated_at`

##### Workflow Status（集中状态管理）

```markdown
## Workflow Status

### Overall
- Workflow overall status: [可读描述]
- Current step: `stepN_draft | stepN_confirmed`
- Last updated at: `2026-03-27T10:00:00Z`

### Step Status Matrix
| Step | Name | Status |
| --- | --- | --- |
| Step 1 | 需求澄清 | draft \| confirmed |
| Step 2 | 方案设计 | draft \| confirmed |
| Step 3 | 任务分解 | draft \| confirmed |
| Step 4 | 构建实施 | draft \| confirmed |
```

说明：Step 章节正文不再重复维护独立 `status` 元数据；步骤状态统一由 `Workflow Status` 中的 `Step Status Matrix` 承载。

#### 跨会话恢复流程

1. 在新会话中，选择以下任一方式恢复：
   - **Route B（显式路径）**：执行 `/haca-step[N] artifacts/202603271430/haca-workflow.md`
   - **Route C（打开文件）**：在编辑器中打开 `artifacts/202603271430/haca-workflow.md`，然后执行 `/haca-step[N]`（不附路径，Agent 自动识别已打开的契约文件）
2. 若文件不存在：
  - 当 `N=1`：自动创建 `artifacts/<task-id>/` 和 `haca-workflow.md`，并写入最小模板。
  - 当 `N>1`：阻断并提示先运行 `/haca-step1 <同一路径>` 完成初始化。
3. Agent 读取文件头部 `current_step` 和 `Workflow Status -> Step Status Matrix`。
4. 当 `N>1` 时，若 Step N-1 已 confirmed，允许执行 Step N；否则阻断。
5. 提供 `artifact-path`（Route B）或打开文件（Route C）本身**不构成**确认信号。仅当 `N>1` 且 Step N-1 为 `confirmed` 时，从文件对应章节读取输入并执行 Step N。
6. 若 Step N 已是 `confirmed`，允许重跑，并用本次输出覆盖 Step N 章节内容。
7. 在输出等待确认标签之前，先写入文件：将 `Step Status Matrix` 中 Step N 设为 `draft`，文件头部设置为 `current_step: stepN_draft`，并刷新 `last_updated_at`。
8. 收到显式确认后，再更新文件：将 `Step Status Matrix` 中 Step N 设为 `confirmed`，文件头部更新为 `current_step: stepN_confirmed`，`last_updated_at` 刷新。

#### 人类修改上一阶段输出

可直接编辑 `artifacts/<task-id>/haca-workflow.md` 中的当前或上一阶段章节。系统自动读取最新版本作为下一阶段的有效输入，**无需重新运行中间步骤**。

#### 输入来源约束（Route A/B/C 通用）

- 只要契约文件存在，必须先读取其中前置步骤章节作为当前步骤输入。
- 禁止依赖记忆、当前对话历史或手工粘贴的会话摘要作为步骤输入主来源。
- 若契约文件不存在，仅允许按初始化规则创建或阻断，不得跳过契约直接依赖会话上下文推进步骤。

#### 终止与恢复

- 在任一步等待确认时，人类可选择：确认进入下一步，或终止当前执行。
- 终止后可在任意时刻恢复，选择任一方式：在编辑器中打开 `artifacts/<task-id>/haca-workflow.md` 后执行 `/haca-step[N]`（Route C），或直接执行 `/haca-step[N] artifacts/<task-id>/haca-workflow.md`（Route B）。
- 恢复时以契约文档最新内容为准（信任模型，不做哈希校验）。

### 5.3 文档管理规范（artifacts/ 目录）

#### 目录结构

```
repository-root/
├── artifacts/              # 本地工作介质（.gitignore）
│   ├── 202603271430/
│   │   └── haca-workflow.md
│   ├── 202603271431/
│   │   └── haca-workflow.md
│   └── ...
```

#### 重要规则

1. **不提交仓库**：`artifacts/` 被 `.gitignore` 忽略，由开发者自管理。
2. **本地持久化**：完成后自行决定保留、归档或删除。
3. **团队规范**：建议明确 `artifacts/` 的管理策略。

---

## 6. Step 1：需求澄清

**目标**：消除需求歧义，输出结构化的任务描述作为后续步骤的共识基线。

### 6.1 核心决策：问 vs 假设

| 场景 | 动作 |
|------|------|
| 影响整体目标方向 | **问（阻塞型）** — 必须得到回答才能继续 |
| 可依赖行业惯例 | **假设并标注** — 写入"关键假设" |
| 纠正成本高（架构/数据模型/安全） | **问** — 附说明为何需要确认 |
| 纠正成本低（命名/日志/格式） | **假设并标注** — 写入"关键假设" |

### 6.2 执行规则

1. **批量提问**：所有问题一轮提出，分为阻塞型和非阻塞型，不逐条往返。
2. **提供默认值**：每个问题附一个推荐默认答案，方便人类快速确认或纠正。
3. **阻塞问题不超过 3 个**：若需要更多，说明请求过于模糊，应先要求补充上下文。
### 6.2a 提问模板

```markdown
**必须确认（阻塞型）：**
1. [问题] — 我的理解是 [默认答案]。是否正确？
2. [问题] — 除非您另行说明，我将使用 [默认値]。

**以下将作为假设（非阻塞型）：**
- 假设 A：[内容]（依据：[行业惯例 / 上下文推断]）
- 假设 B：[内容]
```
### 6.3 需求完整性检查清单

收到请求后逐项验证：

- [ ] 目标：解决什么问题 / 达成什么结果
- [ ] 功能需求：需要哪些具体操作
- [ ] 非功能属性：性能、安全、可用性要求
- [ ] 约束条件：技术栈限制、禁用模块
- [ ] 验收标准：如何验证完成（必须可测试）
- [ ] 影响范围：涉及哪些模块、服务、数据表

### 6.4 Superpowers 辅助

- **触发条件**：需求模糊、用户意图分歧、或范围跨多个独立子系统。
- **可借用能力**：`brainstorming` 的澄清提问方法，用以提高覆盖度。
- **边界约束**：仅借用澄清提问能力，不执行 brainstorming 的完整流程（设计文档编写、git commit、spec review loop、writing-plans 过渡）。Step 1 的批量提问规则优先于 brainstorming 的逐条提问规则。
- **禁区**：不进行实现操作，不做 Step 2 设计决策。

### 6.5 输出格式

```markdown
## Task Input
- Requirement description:
  - Goal:
  - Functional requirements:
  - Non-functional attributes:
  - Constraints:
  - Acceptance criteria:

## AI Decision Summary
- Requirement understanding: [完整理解]

[HACA Step 1/4: Requirement Clarification] - Artifacts: artifacts/<task-id>/haca-workflow.md (draft written before confirmation; you may edit this file, then confirm next step or terminate) - Wait for your confirmation before moving to the next step
```

确认前可反复修订。每次修订必须更新完整输出而非增量补丁。

---

## 7. Step 2：方案设计与风险识别

**目标**：在已确认需求上提出方案，系统化识别已知风险并迭代缓解，输出完整的 AI Decision Summary。

### 7.1 有效风险描述格式

每条风险**必须**包含三要素：

```
[风险名称]: [触发条件] -> [影响]. Mitigation: [具体措施]
```

有效示例：
```
缺少分页: getUserList() 在数据集 >10k 时无分页，导致 DB 超时 (>30s)。
Mitigation: 改用游标分页，每次查询限制 100 条。
```

无效示例（不被接受）：
```
可能有性能问题。        <- 无触发条件、无影响、无缓解措施
需要更好的错误处理。    <- 过于笼统且非任务特定
```

### 7.2 五维度检查清单

#### 维度 1：逻辑边界
- 输入边界值（0、负数、最大值、空字符串）
- null / undefined / nil 处理路径
- 并发场景：多请求操作同一资源
- 竞态条件：非确定性操作顺序下的行为
- 超时与重试：外部调用失败时的回退逻辑

#### 维度 2：依赖耦合
- 依赖的外部 API 版本变更风险
- 新第三方库与现有依赖的兼容性
- 通过全局状态、单例或环境变量产生的隐式耦合
- 模块间循环依赖

#### 维度 3：数据完整性
- 不可逆操作（DELETE、无 WHERE 的 UPDATE、文件覆写）
- 数据库迁移回滚可行性
- 事务边界：多步操作的原子性保证
- 大数据操作的表锁风险

#### 维度 4：安全
- SQL 注入 / NoSQL 注入 / 命令注入
- 越权访问：操作前的权限检查
- 权限提升：用户 A 能否操作用户 B 的数据
- 敏感数据泄露：日志或响应中的密码、token、PII

#### 维度 5：影响范围
- 被修改函数/接口的其他调用方
- 共享工具类、基类、中间件变更的波及范围
- DB schema 变更对现有查询的影响
- API 契约变更对下游服务的影响

### 7.3 迭代缓解循环

```
识别风险 -> 调整方案以缓解 -> 重新检查
  ^____________________________v （仍有风险且 < 10 次迭代）
          v （无风险或达到阈值）
        输出 AI Decision Summary
```

三种缓解方法：

| 方法 | 适用场景 | 示例 |
|------|----------|------|
| 变更方案结构 | 风险源于设计，可通过重新设计规避 | 全量加载改为分页 |
| 添加技术约束 | 保留方案，增加防护措施 | 添加事务和输入校验 |
| 标记为未覆盖场景 | 当前范围内无法缓解，需人工决策 | 合规要求需产品确认 |

达到阈值（10 次迭代）时：将未解决风险移入"未覆盖场景"，声明因迭代上限而非遗漏。

### 7.4 已知风险 vs 未覆盖场景

- **已知风险**（Known Risks）：已识别且已通过方案调整解决。
- **未覆盖场景**（Uncovered Scenarios）：已识别但在当前信息/能力范围内无法缓解，标注人工决策点。

### 7.5 Superpowers 辅助

- **触发条件 A**：方案选项需要带有权衡分析的对比时，SHOULD 借用 `brainstorming` 的选项对比方法。
- **触发条件 B**：分析领域相互独立时，SHOULD 使用 `dispatching-parallel-agents`。
- **边界约束**：仅借用 brainstorming 的选项对比和权衡分析能力，不执行其完整流程。并行分派仅限各领域独立且无共享状态耦合时使用。

### 7.6 输出格式

```markdown
## AI Decision Summary
- Requirement understanding:
- Adopted approach:
- Rejected approach:
- Key assumptions:
- Known risks:
- Uncovered scenarios:

### Decomposition Strategy Choice
Please choose Step 3 decomposition strategy: Decompose into subtasks (default) or Single-task execution (no decomposition). Reply with "Decompose" or "Single-task".

[HACA Step 2/4: Solution Design] - Artifacts: artifacts/<task-id>/haca-workflow.md (draft written before confirmation; you may edit this file, then confirm next step or terminate) - Wait for confirmation before moving to Step 3
```

人类可请求修订或增加约束。持续更新 Summary 直至获得显式确认。

---

## 8. Step 3：任务分解

**目标**：基于 Step 2 已确认内容，按用户选择执行以下两种策略之一，并输出 Step 4 执行计划：
- 默认策略：将方案拆分为原子子任务，并输出依赖图。
- 单任务策略（no decomposition）：不拆分子任务，输出一个可独立执行的单一单元。

### 8.0 /haca-step3 调用时必须选择拆分策略

**规则：拆分策略（Decomposition Strategy）必须由用户在调用 `/haca-step3` 时显式选择，不得从 Step 2 确认回复中解析，不得静默默认。**

若输入为空或无效，Agent 必须阻塞并要求用户补充选择，不得继续生成 Step 3 输出。

#### 8.0.1 拆分策略选择规则（从高到低）

| 优先级 | 条件 | 结果 |
|--------|------|------|
| 1 | 用户调用时选择 `Decompose` | 进入标准任务分解流程 |
| 2 | 用户调用时选择 `Single-task` | 跳过拆分，生成 1 个子任务 |
| 3 | 输入为空或无效 | **阻塞**，要求用户选择，不得静默默认 |

当选择 `Single-task` 时：
- 仍需输出完整子任务模板（Task Input + AI Decision Summary）。
- `Execution Order` 固定为单任务串行。
- 不适用并行/汇聚依赖描述。

### 8.1 三项粒度条件（全部必须满足）

```
1. 能否用一句话说清子任务意图？（不使用 "and" 连接两个不同动作）
   否 -> 继续拆分

2. 合并后仓库是否仍可构建和测试？
   否 -> 继续拆分

3. 评审者能否在 30 分钟内完全理解？
   否 -> 继续拆分

三项全部通过 -> 粒度合适 [OK]
```

### 8.2 强制拆分规则

以下场景**必须**拆分为独立子任务，无例外：

**规则 1：refactor 与 feat 分离**
```
[✗] 错误：在一个子任务中重构 UserService 并添加批量导出功能
[✓] 正确：
  T1: refactor(user): 提取 UserService 共用查询方法
  T2: feat(user): 添加用户数据批量导出 API
```
原因：混合后评审者无法区分行为变更来自重构副作用还是有意的新功能。

**规则 2：数据库迁移必须独立且优先执行**
```
[✓] 正确顺序：
  T1: chore(db): 添加 orders.status 迁移脚本  <- 必须在前
  T2: feat(order): 实现订单状态流转逻辑
```

**规则 3：配置变更先于依赖代码**
```
[✓] 正确顺序：
  T1: chore(config): 添加 FEATURE_NEW_CHECKOUT 功能标志
  T2: feat(checkout): 实现新结账流程（由标志控制）
```

**规则 4：测试基础设施先于业务测试用例**
```
[✓] 正确顺序：
  T1: test(setup): 搭建集成测试 mock 服务器
  T2: test(order): 添加订单创建流程集成测试
```

### 8.3 提交类型速查表

| 类型 | 含义 | 粒度约束 |
|------|------|----------|
| `feat` | 一个用户可见功能点 | 不混入重构、不混入无关修复 |
| `fix` | 一个独立 bug 修复 | 不合并无关 bug |
| `refactor` | 仅结构变更，无外部行为变化 | 不包含功能变更 |
| `test` | 测试代码 | 可与简单实现合并；测试基础设施保持独立 |
| `chore` | 构建/依赖/配置变更 | 不包含业务逻辑 |
| `docs` | 文档变更 | 不包含代码变更 |
| `perf` | 性能优化，无行为变更 | 不包含功能变更 |

子任务标题格式（带 `[AI]` 前缀）：
```
[AI] <type>(<scope>): <subject>
```

### 8.4 依赖标注

拆分时识别以下四种依赖关系：

| 类型 | 识别信号 | 示例 |
|------|----------|------|
| 代码依赖 | T2 调用 T1 的新函数/接口/类 | T1 添加 helper，T2 使用 |
| 数据依赖 | T2 依赖 T1 的 schema 变更 | T1 添加字段，T2 写入该字段 |
| 测试依赖 | T2 的测试依赖 T1 的测试基础设施 | T1 搭建 mock，T2 使用 mock |
| 配置依赖 | T2 依赖 T1 引入的配置 | T1 添加 flag，T2 读取 flag |

### 8.5 Superpowers 辅助

- **触发条件 A**：分解需要持久化执行计划供 worker agent 使用时，**MUST** 使用 `writing-plans`。
- **触发条件 B**：需要隔离执行工作区时，**MUST** 使用 `using-git-worktrees`。
- **边界**：保持 HACA 子任务粒度和输出契约不变，不用 plan-only 产物替代 Step 3 输出。

### 8.6 输出格式

每个子任务必须输出完整描述：

```markdown
---
## [AI] <type>(<scope>): <subject>

### Task Input
- Requirement description: [本子任务的具体目标和验收标准]

### AI Decision Summary
- Requirement understanding:
- Adopted approach:
- Rejected approach:
- Key assumptions:
- Known risks:
- Uncovered scenarios:
---
```

所有子任务描述后，附加执行顺序：

```markdown
## Execution Order
- Serial: T1 -> T2 -> T3
- Parallel: T4 and T5 have no dependency and can run together
- Converge: T6 runs after both T4 and T5 are completed
```

最后附加：

```
[HACA Step 3/4: Task Decomposition] - Artifacts: artifacts/<task-id>/haca-workflow.md (draft written before confirmation; you may edit this file, then confirm next step or terminate) - Wait for confirmation before moving to Step 4
```

---

## 9. Step 4：构建

**目标**：按依赖顺序执行每个子任务，完成 TDD → 验证 → 门禁 → 验收交接的闭环。

### 9.1 /haca-step4 的提交边界

**规则：Step 4 中 AI 不执行 `git commit`。**

- AI 负责完成实现、测试、门禁与证据输出。
- AI 在每个子任务结束时输出可验收交接信息。
- 人工验收通过后，由人工决定是否以及何时执行 `git commit`。

**Step 4 入口阻塞规则（强制）**：若契约文件头部为 `current_step: step3_draft`，或 `Step Status Matrix` 中 Step 3 的 `status != confirmed`（例如 `draft` / `pending`），则 `/haca-step4` 必须在前置门禁处阻塞。命令调用本身、提供 `artifact-path`、或仅仅打开契约文件，都不能视为对 Step 3 的隐式确认。

同理，`/haca-step2` 和 `/haca-step3` 也必须分别对 `current_step: step1_draft` / `step2_draft` 以及 `Step Status Matrix` 中 Step 1 / Step 2 的 `status != confirmed` 执行同等级别的前置阻塞。

### 9.3 子任务执行链（Build Loop）

对于每个子任务，按以下顺序执行：

```
┌─────────────────────────────────────────────────────────────────┐
│ 步骤 1: 执行 Step 4 质量链（tdd-loop/SKILL.md）                  │
│   ├─ TDD: Red → Green → Refactor                               │
│   │   - Red: 先写/更新测试，执行，观察失败，记录                    │
│   │   - Green: 实现最小改动使测试通过，不做无关优化                  │
│   │   - Refactor: 仅在测试全绿时重构，保持外部行为和契约不变         │
│   │   - 若子任务为纯文档/格式化：记录 TDD Evidence: N/A 并附理由    │
│   ├─ 验证证据（verification-before-completion）                   │
│   ├─ 调试证据（systematic-debugging）或 Not Triggered             │
│   └─ 审查请求 + 审查接收证据（requesting/receiving-code-review）   │
│                                                                  │
│ 步骤 2: 运行子任务完成门禁                                         │
│   ├─ Evidence Gate（evidence-gate/SKILL.md）                      │
│   ├─ 子任务范围一致性检查                                          │
│   └─ 可用项目检查（build / test / lint / type check）             │
│                                                                  │
│ 步骤 3: 验收交接输出                                                │
│   ├─ 输出变更文件摘要、测试结果和遗留风险                            │
│   ├─ 标注可由人工直接验收的检查项                                   │
│   └─ 继续下一子任务                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 9.4 TDD 硬门禁

| 条件 | 结果 |
|------|------|
| 无 Red 证据 | 阻断进入 Green |
| 无 Green 证据 | 阻断进入 Refactor |
| Refactor 引入测试失败 | 阻断子任务完成 |
| 行为变更子任务缺少 TDD 证据 | 阻断子任务完成 |
| 已完成子任务缺少门禁与验证证据 | 阻断进入下一子任务 |

### 9.5 TDD Evidence: N/A 的条件

当且仅当以下全部条件为真时，可使用 `TDD Evidence: N/A`：

1. 子任务为纯文档或纯格式化变更。
2. 无运行时行为、API 契约、schema 或权限变更。
3. 现有测试不受影响。

需附理由和最低限度的回归检查。

每个子任务的 TDD 证据必须按以下格式输出：

```markdown
## TDD Evidence
- Subtask ID:
- Red evidence:
- Green evidence:
- Refactor notes:
- Regression checks:
- Uncovered scenarios:
```

### 9.6 五类强制能力证据

Step 4 中，以下五项 Superpowers 能力作为强制质量控制执行：

| 能力 | 职责 |
|------|------|
| `test-driven-development` | 强制行为变更工作使用 failing-test-first 执行 |
| `verification-before-completion` | 在声称完成前要求提供新鲜的命令执行证据 |
| `systematic-debugging` | 在尝试修复前要求先做根因分析 |
| `requesting-code-review` | 完成前要求结构化审查 |
| `receiving-code-review` | 在接受审查结果前要求技术评估和反馈处理 |

对于每项能力：
- 若触发：记录能力名称、触发原因、关键发现、建议措施、采纳/拒绝及理由。
- 若未触发：记录 `Not Triggered` 及理由，或提供显式批准的例外。
- 缺失任何强制能力证据 → 阻断子任务完成（除非有 `Not Triggered` 证据或显式批准的例外记录）。

### 9.7 子任务全部完成后

1. 执行最终 Evidence Gate 校验。
2. 若通过，输出固定文本：`All subtasks are complete, pending human verification before human-led git commit.`
3. 输出后等待人工后续指令。禁止自动进行提交、合并或集成操作。

---

## 10. Evidence Gate 详解

### 10.1 定义

Evidence Gate 维护一个跨 HACA 步骤的统一证据包，在证据不完整时阻断步骤转换。

### 10.2 触发时机

1. Step 1 → Step 2 之前
2. Step 2 → Step 3 之前
3. Step 3 → Step 4 之前
4. Step 4 中每个子任务完成交接之前
5. Step 4 所有子任务完成后、输出最终完成提示语之前

对于第 3 类触发（Step 3 → Step 4 之前），如果契约文件仍显示 `current_step: step3_draft` 或 `Step Status Matrix` 中 Step 3 为 `draft`，Evidence Gate 必须直接阻塞 Step 4，且不得生成任何 Step 4 draft 内容。

同一原则适用于 Step 1 → Step 2 与 Step 2 → Step 3：若契约文件仍显示 `current_step: step1_draft` / `step2_draft` 或 `Step Status Matrix` 中对应前置步骤为 `draft`，Evidence Gate 必须直接阻塞 Step 2 / Step 3，且不得生成任何下一步骤的 draft 内容。

### 10.3 证据包结构

| 证据类别 | 内容 | 必需时机 | 跨会话持久化 |
|----------|------|----------|-------------|
| 需求证据 | 目标、约束、可测试验收标准、影响范围 | 所有步骤 | Step 1 章节（artifacts/）|
| 设计证据 | 采用方案、拒绝方案、关键假设 | Step 2+ | Step 2 章节（artifacts/）|
| 风险证据 | 已知风险及缓解措施 | Step 2+ | Step 2 章节（artifacts/）|
| 测试证据 | Red-Green-Refactor 记录和回归检查 | Step 1-3 可为 N/A；Step 4 强制 | Step 4 章节（artifacts/）|
| 决策证据 | 未覆盖场景和决策责任人 | 所有步骤 | 各步骤章节（artifacts/）|
| 能力执行证据 | Superpowers 使用记录（名称、源路径、触发原因、关键发现、建议措施、采纳/拒绝决策及理由） | 使用了 Superpowers 时 | 步骤章节补注（artifacts/）|
| Step 4 强制能力证据 | 五类强制能力的执行证据或 Not Triggered 记录 | Step 4 | Step 4 章节（artifacts/）|
| 子任务交接证据 | 子任务完成状态、变更摘要、测试与门禁结果 | Step 4 | Step 4 章节（artifacts/）|
| 完成提示语证据 | 精确的完成提示语文本和输出时间戳 | Step 4 最终门禁 | Step 4 章节（artifacts/）|

### 10.4 阻断规则

#### 会话历史路由中的阻断规则

**所有步骤通用**：
- 当前步骤的必需证据缺失 → 阻断步骤转换。
- 会话历史路由下，若契约文件中前置步骤 `status != confirmed` → 阻断步骤转换。
- 契约文件存在但未从对应前置章节读取当前步骤输入（改为依赖记忆/当前对话上下文）→ 阻断步骤转换。
- 验收标准不可测试 → 回退到 Step 1。
- 风险条目缺少"触发-影响-缓解"格式 → 回退到 Step 2。
- 子任务边界不清或依赖冲突 → 回退到 Step 3。
- 使用了 Superpowers 但缺少能力执行证据 → 阻断步骤转换。
- 使用了 Superpowers 但能力源路径不在 `.github/skills/superpowers/` 下 → 阻断步骤转换。

**Step 4 专用**：
- Step 1-3 转换中，测试证据可为 `N/A`（非阻断）。
- Step 4 中测试证据为强制项。纯文档/非行为变更子任务在提供理由和最低回归检查的前提下可接受 `TDD Evidence: N/A`。
- 缺失任何强制能力证据（五类中的任一项）→ 阻断子任务完成（除非记录了 `Not Triggered` 或显式批准的例外）。
- 已完成子任务缺少交接证据（变更摘要/测试结果/门禁结果）→ 阻断进入下一子任务。
- 完成提示语文本不完全等于 `All subtasks are complete, pending human verification before human-led git commit.` → 阻断 Step 4 完成。

#### 文档上下文路由中的阻断规则

（应用于 `/haca-step[N] artifact-path` 命令）

**前置条件阻断**：
- 前置步骤（Step N-1）在文档中的 `status` 字段不为 `confirmed` → 阻断，返工该步骤。
- 前置步骤输出缺少 Step N 所需的必要内容字段 → 阻断，列出缺失项。
- 未从契约文件前置章节读取当前步骤输入（改为依赖记忆/当前对话上下文）→ 阻断。

**证据字段阻断**（基本同会话历史路由）：
- 当前步骤内验收标准不可测试 → 阻断。
- 风险条目格式不符 → 阻断。
- 子任务依赖冲突 → 阻断。
- Superpowers 证据缺失或源路径不合法 → 阻断。

**Step 4 特殊阻断**（文档模式）：
- TDD 证据缺失（纯文档子任务除外，需提供理由）→ 阻断子任务完成。
- 强制能力证据缺失 → 阻断子任务完成。
- 子任务交接证据缺失 → 阻断 Step 4 完成。
- 完成提示语不符 → 阻断 Step 4 完成。

#### 关键差异：真实性检查

文档上下文路由中，**不执行** `based_on_hash` 校验或内容摘要比对。仅检查"必要字段是否存在"和"前置步骤是否 confirmed"，采用信任模型对待人类的文档管理和更新能力。

### 10.5 轻量模式

术语澄清（避免混淆）：
- **轻量模式**是 Evidence Gate 的证据收集与校验粒度策略，回答的是"需要提供多少证据"。
- **验收交接策略**是 Step 4 的交接组织方式，回答的是"如何组织验收证据并交给人类"。

仅当以下所有条件为真时允许使用轻量模式：
- 变更仅触及一个模块
- 无数据迁移或权限模型变更
- 预期评审时间 ≤ 30 分钟

轻量模式下仍必须提供：
- 可测试的验收标准
- 已知风险
- 未覆盖场景
- 最低测试证据（Step 1-3 可附理由写 N/A；Step 4 需执行证据）

### 10.6 输出格式

```markdown
## Evidence Check Result
- Current step:
- Passed items:
- Missing items:
- Blocking items:
- Rollback recommendation:
- Decision:
```

- `Decision: Pass`：不输出单独的 Gate 等待行。
- 存在阻断项时，追加：`[HACA Gate: Evidence Validation] - Artifacts: artifacts/<task-id>/haca-workflow.md - Blocked until required evidence is complete`

### 10.7 职责边界

Evidence Gate 仅负责证据的采集与校验。它**不定义**人类验收策略细节，**也不执行** `git commit`。Step 4 中门禁通过后，验收交接行为必须遵循 `.github/agents/haca.agent.md` 的规定。

---

## 11. 异常处理

Step 4 中出现意外问题时，Agent 必须立即停止并按以下格式上报，等待人工决策：

```
[!] Unexpected Execution Issue - Your Decision Required

Type: [technical blocker / dependency order issue / requirement change]
Description: [发生了什么]
Impact: [哪些仍有效，哪些需要重新规划]

Recommendation: roll back to Step N, reason: [具体原因]
Confirm?
```

**回滚目标映射**：

| 问题类型 | 回滚到 |
|----------|--------|
| 技术阻断 | Step 2 |
| 依赖顺序问题 | Step 3 |
| 需求变更 | Step 1 |

**TDD 层面的异常处理**：

| 情况 | 动作 |
|------|------|
| 测试无法稳定复现 | 回滚到 Step 2 |
| 子任务边界与失败测试不匹配 | 回滚到 Step 3 |
| 需求变更 | 回滚到 Step 1 |
| 子任务符合 docs-only 例外 | 记录 `TDD Evidence: N/A` 附理由和最低回归检查 |

---

## 12. Superpowers 融合汇总

### 13.1 总体规则

- 能力仅可在当前已确认的 HACA 步骤内使用。
- 触发的能力结果必须记录在 AI Decision Summary 或证据包中。
- 所有能力源路径必须在 `.github/skills/superpowers/` 下。

### 13.2 各步骤可用能力

| 步骤 | 能力 | 触发条件 | 强度 | 边界约束 |
|------|------|----------|------|----------|
| Step 1 | `brainstorming` | 需求模糊/意图分歧/跨子系统 | SHOULD | 仅借用澄清提问，不执行完整流程；批量提问优先 |
| Step 2 | `brainstorming` | 方案选项需带权衡对比 | SHOULD | 仅借用选项对比和权衡分析 |
| Step 2 | `dispatching-parallel-agents` | 分析领域独立 | SHOULD | 仅限无共享状态耦合 |
| Step 3 | `writing-plans` | 分解需要持久化执行计划 | MUST | 不替代 Step 3 输出 |
| Step 3 | `using-git-worktrees` | 需要隔离工作区 | MUST | 保持子任务粒度不变 |
| Step 4 | `test-driven-development` | 行为变更工作 | 强制 | — |
| Step 4 | `verification-before-completion` | 声称完成前 | 强制 | — |
| Step 4 | `systematic-debugging` | 出现失败或意外结果 | 强制 | — |
| Step 4 | `requesting-code-review` | 完成前 | 强制 | — |
| Step 4 | `receiving-code-review` | 接受审查前 | 强制 | — |

### 13.3 能力使用记录格式

触发并使用时，在 AI Decision Summary 或证据包中记录：
- 能力名称
- 能力源路径
- 触发原因
- 关键发现
- 建议措施
- 采纳/拒绝决策及理由

---

## 13. Prompt 入口模板

六个 HACA Prompt 文件均为输入模板，不包含业务代码实现：

另有一个独立快捷 Prompt 用于非 HACA 提交场景。

| 文件 | 指向的技能 | 输入变量 |
|------|-----------|----------|
| `haca-step1.prompt.md` | `clarify-requirements/SKILL.md` | `${input:task}`（可选 `${input:artifact_path}`） |
| `haca-step2.prompt.md` | `risk-identification/SKILL.md` | `${input:task_input}`（会话路由）或 `${input:artifact_path}`（文档路由） |
| `haca-step3.prompt.md` | `task-decomposition/SKILL.md` | `${input:decision_summary}`（会话路由）或 `${input:artifact_path}`（文档路由） |
| `haca-step4.prompt.md` | `tdd-loop/SKILL.md` + `evidence-gate/SKILL.md` | `${input:subtasks}`（会话路由）或 `${input:artifact_path}`（文档路由） |
| `commit-message.prompt.md` | `commit-message-rules/SKILL.md` | `${input:change_summary}`（可选）+ `${input:language}`（可选） |
| `haca-apply-spec.prompt.md` | HACA 规范落地流程（针对 `.github/`） | 读取 `docs/haca-execution-flow.md` 变更集 |
| `haca-sync.prompt.md` | HACA 同步维护流程（`.github/` → `.cursor/`/`.opencode/`） | 同步后进行 `--check` 一致性检查 |

所有 Prompt 文件明确引用 `copilot-instructions.md` 和对应技能文件作为单一事实来源。

### 13.1 双路由入参约定（artifact-path 适配）

- `haca-step1.prompt.md`：支持无参初始化（自动生成 `task-id`）与显式 `artifact-path` 两种入口。
- `haca-step2.prompt.md`、`haca-step3.prompt.md`、`haca-step4.prompt.md`：支持会话历史路由（不传 `artifact-path`）与文档上下文路由（传 `artifact-path`）两种入口。
- 当同时存在会话历史上下文与 `artifact-path` 参数时，Prompt 层必须传递 `artifact-path` 并由编排层按路由 B 处理。

`haca-sync.prompt.md` 严格限制只能操作以下**手工维护适配层文件**（其他文件禁止修改）：
- `.cursor/AGENTS.md`
- `.cursor/rules/haca.mdc`
- `.opencode/agents/haca.agent.md`
- `opencode.json`

### 13.2 平台 Frontmatter 属性说明

各配置文件 YAML frontmatter 字段的含义：

| 属性 | 出现文件 | 含义 |
|------|---------|------|
| `agent: HACA` | `haca-step*.prompt.md` | 将 Prompt 绑定到 HACA Agent 上下文执行 |
| `tools: [read, search, edit, execute, agent]` | `haca.agent.md` | 声明该 Agent 的工具权限 |
| `preserve_github_paths: true` | apply-spec / sync prompts | 防止同步脚本覆盖 `.github/` 下的源文件 |

---

## 14. 完整执行序列总览

```
用户调用 @HACA 或 /haca-step1
  │
  ▼
┌──────────────────────────────────────────────────────────┐
│ Step 1: 需求澄清                                         │
│  ├─ 读取 clarify-requirements/SKILL.md                   │
│  ├─ 批量问题 + 假设标注                                    │
│  ├─ 输出 Task Input + AI Decision Summary                │
│  └─ 等待确认 [HACA Step 1/4]                              │
├──────────────────────────────────────────────────────────┤
│ Evidence Gate → 通过后进入 Step 2                          │
├──────────────────────────────────────────────────────────┤
│ Step 2: 方案设计与风险识别                                  │
│  ├─ 读取 risk-identification/SKILL.md                     │
│  ├─ 五维度风险检查 + 迭代缓解（≤10 次）                     │
│  ├─ 输出完整 AI Decision Summary                          │
│  ├─ 输出 Step 3 分解策略选择提示（默认 Decompose）            │
│  └─ 等待确认 [HACA Step 2/4]                               │
├──────────────────────────────────────────────────────────┤
│ Evidence Gate → 通过后进入 Step 3                           │
├──────────────────────────────────────────────────────────┤
│ Step 3: 任务分解                                           │
│  ├─ 读取 task-decomposition/SKILL.md                      │
│  ├─ 解析分解策略：Decompose（默认）或 Single-task            │
│  ├─ Decompose: 三条件粒度验证 + 强制拆分规则                 │
│  ├─ Single-task: 产出 1 个可独立执行单元                     │
│  ├─ 输出子任务列表 + 执行顺序                                │
│  └─ 等待确认 [HACA Step 3/4]                                │
├──────────────────────────────────────────────────────────┤
│ Evidence Gate → 通过后进入 Step 4                            │
├──────────────────────────────────────────────────────────┤
│ Step 4: 构建（循环每个子任务）                                │
│  ├─ 对每个子任务:                                           │
│  │  ├─ TDD (Red → Green → Refactor) 或 N/A                │
│  │  ├─ 验证证据                                             │
│  │  ├─ 调试证据 / Not Triggered                             │
│  │  ├─ 审查请求 + 接收证据                                   │
│  │  ├─ Evidence Gate                                        │
│  │  ├─ 输出子任务交接证据                                    │
│  │  └─ 报告进度                                              │
│  ├─ 最终 Evidence Gate                                      │
│  └─ 输出: "All subtasks are complete, pending human         │
│     verification before human-led git commit."              │
│  等待人工后续指令                                             │
└──────────────────────────────────────────────────────────┘
```

---

## 15. 每步输出结尾标签

每个步骤的输出必须以固定标签结尾。`<task-id>` 占位符替换为实际生成的 task ID（`YYYYMMDDHHMM` 格式；在 Step 1 中生成，贯穿所有后续步骤）：

```
[HACA Step 1/4: Requirement Clarification] - Artifacts: artifacts/<task-id>/haca-workflow.md (draft written before confirmation; you may edit this file, then confirm next step or terminate) - Wait for your confirmation before moving to the next step
[HACA Step 2/4: Solution Design] - Artifacts: artifacts/<task-id>/haca-workflow.md (draft written before confirmation; you may edit this file, then confirm next step or terminate) - Wait for confirmation before moving to Step 3
[HACA Step 3/4: Task Decomposition] - Artifacts: artifacts/<task-id>/haca-workflow.md (draft written before confirmation; you may edit this file, then confirm next step or terminate) - Wait for confirmation before moving to Step 4
[HACA Step 4/4: Build] - Artifacts: artifacts/<task-id>/haca-workflow.md (draft written before confirmation; you may edit this file, then start human acceptance and human-led commit actions)
```

Evidence Gate 阻断时：
```
[HACA Gate: Evidence Validation] - Artifacts: artifacts/<task-id>/haca-workflow.md - Blocked until required evidence is complete
```

---

本文档为当前仓库 `.github/` 配置的快照描述。若规则文件更新，本文档应同步刷新。
