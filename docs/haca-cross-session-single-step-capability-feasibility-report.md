# HACA 跨会话的单步能力提供可行性研究报告

- 报告日期：2026-03-27

## 1. 当前版本 HACA 在研发使用中的痛点问题

这份可行性研究首先回答的是：当前版本 HACA 在真实研发使用中到底卡在哪里，为什么值得引入一条新的使用路径。只有问题定义清楚，后续方案、改造范围和验收标准才有意义。

### 1.1 当前机制（已实现）

当前 HACA 已支持 /haca-stepN 作为入口命令，但存在强前置门禁：

- 请求 /haca-step2 时，必须在会话历史中存在“已确认的 Step 1 输出”。
- 请求 /haca-step3 时，必须在会话历史中存在“已确认的 Step 2 输出”。
- 请求 /haca-step4 时，必须在会话历史中存在“已确认的 Step 3 输出”。

不满足时会被重定向回 Step 1，因此命令入口本质是“同一会话内的便捷跳转”，而非“跨会话独立调用”。

### 1.2 研发反馈对应问题

- 多次中断后需要在新会话继续，历史上下文无法自然继承。
- 仅需要某一步能力（例如只做风险识别）时，也被流程门禁牵制。
- 强制串行对流程完整性有利，但对高频、碎片化协作场景的操作成本偏高。

### 1.3 本次研究要解决的核心问题

围绕上述痛点，本次研究需要回答以下问题：

1. 当前 HACA 的 `/haca-stepN` 为什么还不能真正支持跨 session 独立使用？
2. 是否有必要在保留现有主路径的前提下，再提供一条“按步骤取用能力”的补充路径？
3. 如果允许单独执行 Step1 到 Step4，阶段之间应该依赖什么介质衔接，才能替代会话历史？
4. 契约文档应放在哪里、如何按任务组织、如何恢复、如何避免并发冲突？
5. 新路径是否会削弱当前强制四步串行流程的门禁能力，尤其是 Evidence Gate 和 Step 4 质量链？
6. 契约文档最终是否应该随代码一起提交，怎样在“可追溯性”和“仓库洁净度”之间取得平衡？

范围说明：文档真实性校验不纳入本次研究范围。

这些问题如果不能被系统回答，那么“独立步骤路径”即使实现出来，也更像绕过流程，而不是增强 HACA。

## 2. 解决这些痛点的思路

解决这些问题的思路不是新增一条并行流程，而是对现有 HACA 做一个小而关键的机制改造：把步骤衔接从“依赖同一会话上下文”切换为“依赖落盘文档上下文”。

### 2.1 核心思路

- 保留 HACA Step1-Step4 的整体流程结构不变。
- 将步骤衔接机制从“会话历史”改为“文档上下文”，使 `haca-step1` 到 `haca-step4` 可以在跨 session 场景稳定执行。
- Step1 到 Step4 的每一步都只读取文档输入，不依赖会话历史上下文。
- 人类通过 `haca-step[1..4]` 并提供落盘文档路径启动作业时，视为已认可上阶段输出并同意启动下一步骤。
- Step4 在本次范围内按“整体步骤”执行，不下钻到 `tdd-loop` 内部子任务级执行编排。
- 契约文档统一存放在仓库根目录 `artifacts/` 下，按任务维度组织。
- 契约文档不提交到代码仓库，仅作为输入输出媒介，由开发者自行管理。
- 本方案范围内不考虑“文档真实性校验”。

### 2.2 目标能力定义

在不削弱现有串行主流程的前提下，实施“文档上下文衔接机制”，满足以下能力：

- 能单独触发任一步（haca-step1..4）。
- 每一步都读取上一阶段文档产物，而非依赖同一会话历史。
- 允许 Step 1 与 Step 2、Step 3 与 Step 4 在不同会话、不同时间执行。
- Step4 以整体步骤执行，不要求拆解 `tdd-loop` 的子任务执行链。
- 维持 Evidence Gate 的阻断能力：文档不完整即禁止进入下一步。
- 每个 Step 完成后都固定落盘并询问是否继续下一步；若人类离开会话，可在任意时刻通过 `haca-step[1..4] + 文档路径` 恢复。

### 2.3 结论摘要（Executive Summary）

- 结论：可行，建议在现有 HACA 流程上直接实施“文档上下文衔接机制”改造。
- 改造方式：不改变四步结构，只替换步骤间的上下文传递介质。
- 预估改造成本：低到中（主要是编排规则、文档契约和步骤门禁增强，不涉及业务代码）。
- 本次前提：文档不提交仓库，由开发者自行管理；文档真实性校验不在本次范围内。

## 3. 从实现层面评估可行性

### 3.1 技术可行性：高

原因：

- 当前架构已经分层（治理层、编排层、技能层），天然支持在编排层增加“文档上下文路由分支”。
- 各步骤 SKILL 已有标准输出结构，可直接映射为文档输入输出契约。
- Evidence Gate 已经承担跨步骤校验职责，扩展为“会话外文档校验”改造成本可控。

### 3.2 流程可行性：中高

原因：

- 保留四步结构，仅替换上下文载体，认知迁移成本较低。
- Step1 到 Step4 直接基于文档执行，且 Step4 先按整体步骤落地，复杂度可控。

挑战：

- 需要定义“确认状态”的离线表达（不能只依赖聊天里一句 confirm）。
- 需要控制开发者本地文档管理成本（命名、归档、清理）。

### 3.3 运维可行性：中

原因：

- 文档上下文衔接机制降低了会话依赖，但把状态管理责任转移给开发者。
- 文档不入库可减少 PR 噪音，但需要本地自管理规范，否则容易丢失或混淆。

## 4. 建议方案设计

### 4.1 机制改造设计

- 改造前：步骤衔接依赖会话历史中的已确认输出。
- 改造后：步骤衔接依赖 `artifacts/` 下的阶段文档。
- 不变项：四步流程结构、各步骤能力边界、Step4 作为整体步骤执行（本次范围）。
- 变化项：Step2/3/4 的输入来源从“会话上下文”改为“文档上下文”。

### 4.2 建议契约目录结构（根目录 artifacts）

建议在仓库根目录新增 `artifacts/`，并按任务维度创建子目录（示意）：

- artifacts/<task-id>/haca-workflow.md

说明：

- `task-id` 采用创建时间自动生成，建议格式：`YYYYMMDDHHMM`，例如 `202603271430`。
- `haca-workflow.md` 采用渐进式更新：Step1 到 Step4 结果按章节持续追加，状态索引写在同一文件头部元数据中。
- 该目录默认不纳入版本控制，仅作为本地输入输出媒介。

### 4.2.1 每任务目录如何实现（建议）

实现目标：保证“同一任务固定目录、跨 session 可恢复、并发时可检测冲突”。

实现建议：

1. 目录创建时机
  - 首次执行 `haca-step1` 时自动生成 `task-id`（创建时间 `YYYYMMDDHHMM`）并创建：`artifacts/<task-id>/`。
  - 若目录已存在，进入恢复流程而不是重新初始化。
  - 若传入的 `haca-workflow.md` 路径不存在：
    - 执行 `haca-step1` 时自动创建目录与文件并初始化模板；
    - 执行 `haca-step2/3/4` 时阻断，并提示先用同一路径执行 `haca-step1` 完成初始化。

2. task-id 生成与校验
  - 首次运行自动按创建时间生成：`YYYYMMDDHHMM`。
  - 同一分钟内重复创建时，自动顺延到下一个可用分钟值，保证唯一性。
  - task-id 为纯数字时间戳，不含空格和特殊字符。

3. 初始化文件
  - 首次创建目录时初始化 `haca-workflow.md` 模板。
  - 文件头部元数据初始字段建议：`task_id`、`current_step`、`last_updated_at`。

4. 恢复流程
  - 后续在任意 session 执行 `haca-stepN` 时，先读取 `artifacts/<task-id>/haca-workflow.md`。
  - 根据文件头部 `current_step` 与各 Step 章节的 `status` 判断是否放行或阻断。

5. 并发保护
  - 作为可选增强项保留，不作为首批必做。
  - 首批按“单开发者自管理”模型执行，减少流程复杂度。

### 4.3 文档契约

建议在 `haca-workflow.md` 文件头部使用统一元数据：

- task_id
- current_step
- last_updated_at（最后更新时间）

**设计原则：** 信任人类的自管理能力。Evidence Gate 仅检查下一步骤所需的内容是否完整，不对上阶段输出做内容真实性或哈希校验。允许人类在任何时刻更新、修正或完善上一阶段的输出，系统自动将更新后的内容作为下一阶段的输入。

**示例：** 以下为一个完整的 `artifacts/202603271430/haca-workflow.md` 文件示例：

```markdown
---
task_id: 202603271430
current_step: step3_confirmed
last_updated_at: 2026-03-27T14:45:00Z
---

# HACA 工作流文件

## Workflow Status

### Overall
- Workflow overall status: Step 3 已确认
- Current step: `step3_confirmed`
- Last updated at: `2026-03-27T14:45:00Z`

### Step Status Matrix
| Step | Name | Status |
| --- | --- | --- |
| Step 1 | 需求澄清 | confirmed |
| Step 2 | 风险识别 | confirmed |
| Step 3 | 任务分解 | confirmed |
| Step 4 | 开发与证据链 | draft |

## Step 1: 需求澄清

### 需求输出
（Step1 输出内容...）

---

## Step 2: 风险识别

### 风险识别输出
（Step2 输出内容...）

---

## Step 3: 任务分解

### 任务分解输出
（Step3 输出内容...）

---

## Step 4: 开发与证据链

### Step4 证据与提交清单
（待 Step4 执行时追加...）
```

说明：

- 文件头部 YAML frontmatter 包含全局元数据，便于跨 session 快速识别任务上下文。
- 步骤状态统一由 `Workflow Status` 下的 `Step Status Matrix` 管理。
- Step 完成后，更新 `Step Status Matrix` 对应步骤为 `confirmed` 并刷新 `last_updated_at`。
- **允许人类随时修改或补充上一阶段的输出**，系统自动将最新内容作为下一阶段的输入来源。
- Evidence Gate 仅检查下一步骤所需的必要内容字段是否存在，不对内容本身做哈希校验。
- 开发者可在任意时刻通过 `haca-step[N] + 文档路径` 恢复并继续，系统自动读取文件头部状态。

### 4.4 步骤衔接规则（文档上下文衔接机制）

- haca-step1：初始化并写入 `haca-workflow.md` 的 Step1 章节；当人类后续输入 `haca-step2 + haca-workflow.md 路径` 时，系统读取已确认的 Step1 结果并推进到下一步。
- haca-step2：人类输入 `haca-step2` 并提供 `haca-workflow.md` 路径后，系统在契约完整且 Step1 已 confirmed 时把 Step2 内容追加到同一文件。
- haca-step3：人类输入 `haca-step3` 并提供 `haca-workflow.md` 路径后，系统在契约完整且 Step2 已 confirmed 时把 Step3 内容追加到同一文件。
- haca-step4：人类输入 `haca-step4` 并提供 `haca-workflow.md` 路径后，系统在契约完整且 Step3 已 confirmed 时把 Step4 证据追加到同一文件。

补充规则：
- 每个 Step 完成后，系统都要询问人类是否继续下一步。
- 若人类输入显式批准词语，则在当前会话继续下一步。
- 若人类离开会话，则可在任意时刻使用 `haca-step[1..4] + 文档路径` 恢复；恢复时应以前置步骤的 `confirmed` 状态作为推进依据，而非将命令调用本身视为隐式确认。
- **人类可在任何时刻返回并修改上一阶段的输出**（例如完善 Step1 的需求澄清、修正 Step2 的风险识别等），无需重新运行当前/后续步骤。更新后的内容会作为下一步骤的有效输入。
- 若同时存在可用会话历史与显式文档路径，优先采用文档上下文路由，避免路由歧义。

上述规则即为"当前 HACA 默认衔接方式"的替换目标，不再把会话历史作为必要前提，同时充分信任人类的文档管理能力。

### 4.5 关键风险与缓解

### 风险 1：文档丢失或命名混乱

- 触发条件：文档由开发者本地管理且无统一命名约束。
- 影响：跨 session 恢复失败，无法定位最新状态。
- 缓解：统一 `task-id` 命名规则与单文件模板，要求每次步骤结束在 `haca-workflow.md` 中更新状态元数据。

### 风险 2：并发 session 写冲突（次要）

- 触发条件：多人或多会话同时修改同一 run 目录。
- 影响：状态错乱，证据不可审计。
- 缓解：首批按单开发者自管理模型实施；多人协作场景后续再引入锁机制。

### 风险 3：Step4 提交链复杂度上升

- 触发条件：Step4 在文档上下文衔接机制下若同时引入子任务级执行与证据链，会显著增复杂度。
- 影响：流程复杂，失败点增多。
- 缓解：当前阶段只把 Step4 作为整体步骤落地，不展开子任务级编排。

## 6. 最终交付物与验收标准

### 6.1 最终交付物

建议最终交付物至少包括：

1. 支持文档上下文衔接的 HACA 编排规则（替换会话上下文依赖）。
2. 支持文档上下文校验的 Evidence Gate 扩展规则。
3. `artifacts/<task-id>/haca-workflow.md` 的最小模板与状态流转规范。
4. Step1-Step4 的文档输入输出契约（Step4 按整体步骤）。
5. 本地文档自管理说明（不提交仓库）。

### 6.2 验收标准（Go/No-Go）

建议 Go 的最低条件：

- 不改变现有四步流程结构与步骤门禁语义。
- 文档上下文衔接机制下，任意步骤都能在缺失前置证据时被阻断。
- 文档上下文衔接机制下，跨 session 恢复成功率达到可接受水平（建议 >= 90%）。
- Step1 到 Step4 均可独立基于文档执行，且 Step4 以整体步骤运行。
- 契约文档不提交代码仓库，且不影响业务 PR。
- 人类使用 `haca-step[1..4] + 文档路径` 启动作业时，系统能正确将其解释为“认可上阶段输出并同意启动下一步骤”。

任一条件不满足，建议 No-Go 或仅保留试点范围。

## 7. 最小改造清单（仅方案，不改代码）

本清单用于后续实现阶段的最小闭环设计，目标是以最少改动支持“文档驱动独立步骤路径”。

### 7.1 文件级改造点（建议）

1. `.github/agents/haca.agent.md`
  - 将 `/haca-stepN` 的前置判断从“会话历史确认”改造为“文档契约确认”。
  - 在 `/haca-stepN` 路由处读取指定 run 文档判断前置步骤是否 confirmed。
  - 去除对“同一会话上下文”作为必要前提的依赖。

2. `.github/skills/evidence-gate/SKILL.md`
  - 扩展"Step 转换校验"到文档上下文衔接机制：校验前置步骤的 confirmed 字段状态，检查当前步骤所需的必要内容字段是否存在。
  - 增加"文档上下文阻断原因"标准文案，便于识别是会话门禁失败还是文档契约失败。
  - 不对内容本身做哈希校验或真实性校验，信任人类的文档管理能力。

3. `.github/skills/clarify-requirements/SKILL.md`
  - 在输出格式增加“可落盘元数据建议”，使 Step 1 输出可直接写入 step1 文档。

4. `.github/skills/risk-identification/SKILL.md`
  - 在输出格式中约定输入来源：明确本次输入来自 `artifacts/<task-id>/haca-workflow.md` 的 Step1 章节。
  - 保证 Step 2 可在文档中追溯其输入源。

5. `.github/skills/task-decomposition/SKILL.md`
  - 在输出格式中约定输入来源：明确本次输入来自 `artifacts/<task-id>/haca-workflow.md` 的 Step2 章节。
  - 保证 Step 3 输出可被 Step 4 文档上下文衔接机制直接消费。

6. `.github/skills/tdd-loop/SKILL.md`
  - 明确 Step4 在本次范围按整体步骤执行，暂不要求 `tdd-loop` 子任务级落盘编排。

7. `artifacts/`（新增运行契约规范）
  - 形成统一模板说明：`artifacts/<task-id>/haca-workflow.md` 的章节结构、字段和状态流转规则。
  - 标注该目录默认不提交仓库，由开发者本地自管理。

8. `.github/prompts/haca-step1.prompt.md` ~ `.github/prompts/haca-step4.prompt.md`
  - 增加双路由入参约定：支持会话历史路由与 `artifact-path` 文档路由。
  - 当同时具备会话历史上下文与 `artifact-path` 时，统一优先 `artifact-path`。

### 7.2 元数据与状态机最小规范（建议）

`haca-workflow.md` 文件头部至少包含：

- task_id
- current_step
- last_updated_at

每个 Step 章节至少包含：

- step（步骤标识：step1/step2/step3/step4）
- status（draft | confirmed）
- last_updated_at

最小状态机：

- Step 1: draft -> confirmed
- Step 2: 仅在 Step 1 confirmed 时可创建
- Step 3: 仅在 Step 2 confirmed 时可创建
- Step 4: 仅在 Step 3 confirmed 时可执行

Evidence Gate 校验规则：启动 haca-step[N] 时，仅检查该步骤所依赖的前置步骤 status 是否为 confirmed，以及该步骤所需的必要内容字段是否存在，不对内容本身做哈希校验或真实性校验。

### 7.3 优先级与实施顺序（建议）

P0（必须先做）：

1. `haca.agent` 增加文档上下文路由与门禁规则。
2. `evidence-gate` 增加文档契约校验与阻断文案。
3. 定义 `artifacts/<task-id>/` 的最小模板和本地管理规则（不提交）。

P1（建议紧随其后）：

1. Step1-Step4 四个步骤补齐输入来源与输出落盘字段约定（Step4 按整体步骤）。
2. 增加本地文档目录清理与归档建议，降低维护成本。

P2（第二阶段）：

1. 评估是否引入 Step4 子任务级证据链。
2. 评估是否引入多人协作时的锁机制。

### 7.4 最小验收标准（DoD）

1. 在新 session 中，直接执行 `/haca-step2`，当 `haca-workflow.md` 中 Step1 状态为 confirmed 且所需内容字段存在时可通过；否则被阻断并返回明确缺失项。
2. 在新 session 中，`/haca-step3`、`/haca-step4` 均能按文档契约正确放行或阻断。
3. 无同一会话上下文时，Step1-Step4 仍可仅依赖文档契约稳定运行。
4. 任一步契约字段缺失，Evidence Gate 必须阻断且给出可操作修复提示；不对内容本身做哈希或真实性校验。
5. Step1-Step4 可在不同 session 连续推进，且允许人类在任何时刻返回修改上一阶段的输出。
6. `artifacts/` 文档默认不进入业务提交，不影响代码 PR。
7. 每步结束后均有继续下一步的询问；同会话下显式批准词可继续，跨会话下 `haca-step[1..4] + 文档路径` 可恢复并自动视作上阶段（含可能更新的结果）的确认。

### 7.5 试点范围建议

- 首批仅在一个低风险任务类型中试点（例如文档类或小型配置类变更）。
- 试点成功后扩展到一般研发任务，再评估是否启用 Step 4 子任务级增强。

## 8. 契约文档是否随代码提交（讨论与建议）

根据本次确认范围，契约文档不提交代码仓库，仅作为本地输入输出媒介。

### 8.1 本次决策

- 决策：`artifacts/` 下契约文档默认不提交。
- 原因：降低 PR 噪音、减少治理摩擦、满足跨 session 衔接的最小目标。
- 前提：开发者自管理文档；文档真实性校验不在本次范围内。

### 8.2 可执行治理建议

1. 在团队规范中明确 `artifacts/` 为本地工作介质，不进入常规代码提交。
2. 每个 task-id 完成后由开发者自行归档或清理，避免本地目录失控。
3. 如后续出现多人协作审计需求，再评估引入分层提交策略。

结论：在本次目标范围内，“文档不提交、开发者自管理”是更轻量且足够有效的方案。

## 9. 最小运行手册（开发者视角）

本手册用于指导开发者在不依赖会话上下文的情况下，基于单文件 `artifacts/<task-id>/haca-workflow.md` 完成 Step1 到 Step4 的跨会话执行。

### 9.1 一次性准备

1. 首次运行 `haca-step1`。
2. 系统自动生成 `task-id`（`YYYYMMDDHHMM`）并创建目录：`artifacts/<task-id>/`。
3. 系统初始化 `haca-workflow.md`，至少包含头部元数据：`task_id`、`current_step`、`last_updated_at`。

### 9.2 Step1 运行

1. 执行 `haca-step1`，输出写入 `haca-workflow.md` 的 Step1 章节。
2. Step1 完成后系统询问是否继续下一步。
3. 若同会话继续，人工输入显式批准词语并进入 Step2；若离开会话，后续通过 `haca-step2 + haca-workflow.md 路径` 恢复。
4. 在 `haca-workflow.md` 头部更新 `current_step=step1_confirmed`。

### 9.3 Step2 运行

1. 人类输入 `haca-step2` 并提供 `haca-workflow.md` 路径。
2. 系统将该动作视为“认可 step1 输出并同意启动 Step2”。
3. 执行 `haca-step2`，输出追加写入 `haca-workflow.md` 的 Step2 章节。
4. Step2 完成后系统询问是否继续；按同会话显式批准或跨会话命令恢复两种方式进入下一步。
5. 更新当前 Step 章节 `status` 与文件头部 `current_step`。

### 9.4 Step3 运行

1. 人类输入 `haca-step3` 并提供 `haca-workflow.md` 路径。
2. 系统将该动作视为“认可 step2 输出并同意启动 Step3”。
3. 执行 `haca-step3`，输出追加写入 `haca-workflow.md` 的 Step3 章节。
4. Step3 完成后系统询问是否继续；按同会话显式批准或跨会话命令恢复两种方式进入下一步。
5. 更新当前 Step 章节 `status` 与文件头部 `current_step`。

### 9.5 Step4 运行（整体步骤）

1. 人类输入 `haca-step4` 并提供 `haca-workflow.md` 路径。
2. 系统将该动作视为“认可 step3 输出并同意启动 Step4”。
3. 执行 `haca-step4`（按整体步骤执行，不展开 `tdd-loop` 子任务级编排）。
4. 输出追加写入 `haca-workflow.md` 的 Step4 章节（含证据摘要）。
5. 更新 `haca-workflow.md` 头部的最终状态。

### 9.6 常见阻断与处理

1. 若某步无法执行，优先检查传入文档路径是否正确且前置步骤文档契约字段完整。
2. 若需要修改或补充前面步骤的输出，直接编辑 `haca-workflow.md` 中对应章节，系统会自动读取最新内容作为下一步的输入。
3. 若出现目录混乱，按 `task-id` 重新归档并修正 `haca-workflow.md` 头部状态。

### 9.7 收尾建议

1. 任务完成后，开发者自行决定归档或清理 `artifacts/<task-id>/`。
2. 默认不将该目录纳入代码提交。

---

## 附录：一句话定义

- 现有路径：会话驱动的强制串行 HACA。
- 改造后路径：文档驱动的跨会话 HACA 能力调用（Step4 按整体步骤执行）。
- 关系定义：流程结构不变，上下文载体从会话切换为文档。

## 10. 实施 SOP

本章节给出落地“文档上下文衔接机制”的可执行改造清单。目标是让实现结果与 `docs/haca-execution-flow.md` 完全一致，并让 Prompt 设计满足 `docs/prompt-writing-best-practices-research-report.md` 中的高质量标准。

### 10.1 实施原则（先审计后落地）

1. 以 `docs/haca-execution-flow.md` 作为唯一规范源，逐文件对照实现层（`.github/`）。
2. 每次改动后都执行“路由一致性检查 + 证据门禁检查 + Prompt 质量检查”。
3. Prompt 仅承载输入模板，不承载编排逻辑；编排逻辑统一放在 Agent/Skill。

### 10.2 文件级实施清单（必须修改）

1. `.github/agents/haca.agent.md`
  - 增加 `/haca-stepN` 双路由入口判定：
    - 有 `artifact-path` -> Route B（文档上下文）。
    - 无 `artifact-path` -> Route A（会话历史）。
  - 明确路由优先级：当会话历史与 `artifact-path` 同时存在时，强制 Route B。
  - 增加缺失文件初始化规则：
    - `haca-step1` + 不存在路径：自动初始化 `artifacts/<task-id>/haca-workflow.md`。
    - `haca-step2/3/4` + 不存在路径：阻断并提示先运行 `haca-step1`。
  - 补充文档路由下 Step4 首批粒度：默认整体步骤执行；若人类显式要求拆分，再进入子任务链。

2. `.github/skills/evidence-gate/SKILL.md`
  - 增加 Route B 前置校验：前序步骤 `status=confirmed` 且必填字段完整。
  - 增加 Route B 阻断文案模板：缺失字段、前序状态不满足、输入路径不合法。
  - 明确“不做哈希真实性校验”，只做字段完整性与状态校验。
  - 保持 Route A 现有校验语义不变，避免回归。

3. `.github/skills/clarify-requirements/SKILL.md`
  - 输出模板补充“可落盘字段映射”，确保 Step1 输出可直接写入 `haca-workflow.md`。
  - 当携带 `artifact-path` 执行时，输出末尾追加“文件更新动作”说明。

4. `.github/skills/risk-identification/SKILL.md`
  - 文档路由时显式声明输入来源：`artifacts/<task-id>/haca-workflow.md` 的 Step1 章节。
  - 输出中保留可追溯字段，便于写回 Step2 章节。

5. `.github/skills/task-decomposition/SKILL.md`
  - 文档路由时显式声明输入来源：Step2 章节。
  - 明确单任务/多子任务两种输出分支，保证 Step4 可消费。

6. `.github/skills/tdd-loop/SKILL.md`
  - 增加文档路由首批范围说明：支持 Step4 整体步骤执行。
  - 若人类显式要求子任务级执行，仍复用现有 Red-Green-Refactor 质量链。

7. `.github/prompts/haca-step1.prompt.md`
  - 输入变量支持：`${input:task}` + 可选 `${input:artifact_path}`。
  - 提示词中明确输出目标：结构化 Step1 结果 + 可落盘元数据。

8. `.github/prompts/haca-step2.prompt.md`
  - 输入变量支持双路由：`${input:task_input}`（Route A）或 `${input:artifact_path}`（Route B）。
  - 指令中明确风险输出格式与阻断前提，避免模糊指令。

9. `.github/prompts/haca-step3.prompt.md`
  - 输入变量支持双路由：`${input:decision_summary}`（Route A）或 `${input:artifact_path}`（Route B）。
  - 输出指示器明确：子任务列表、执行顺序、是否需要 Step4 模式选择。

10. `.github/prompts/haca-step4.prompt.md`
  - 输入变量支持双路由：`${input:subtasks}`（Route A）或 `${input:artifact_path}`（Route B）。
  - 明确文档路由首批可走“整体步骤执行”分支，且输出证据摘要。

11. `.github/prompts/haca-apply-spec.prompt.md`
  - 增加“规范差异检查清单”：路由优先级、初始化策略、Prompt 双路由变量、Evidence Gate 差异。

12. `.github/prompts/haca-sync.prompt.md`
  - 在同步后检查中加入“Prompt 入参一致性检查”，确保 `.github/` 与适配层不漂移。

13. `artifacts/`（目录与模板规范）
  - 提供最小 `haca-workflow.md` 模板（frontmatter + Step1-4 章节元数据骨架）。
  - 在仓库忽略规则中确保该目录默认不进入业务提交。

### 10.3 Prompt 高质量对照清单（与研究报告逐项对齐）

以下清单用于审计 `haca-step*.prompt.md` 是否满足高质量 Prompt 规范：

1. 四元素完整
  - 每个 Prompt 都包含 Instruction、Context、Input Data、Output Indicator。

2. 指令清晰且可执行
  - 使用明确动作动词（如 analyze、summarize、validate、generate）。
  - 禁止“尽量”“适当”等模糊词作为核心约束。

3. 分隔清晰
  - 使用稳定分隔结构（标题/分段/标记）隔离“任务说明”“输入变量”“输出格式”。

4. 输出格式显式
  - 必须给出固定输出骨架或字段列表，避免自由散文输出。

5. 说“要做什么”，不说“不要做什么”
  - 将负向禁令转为正向执行规则，减少歧义。

6. 角色边界清晰
  - Prompt 不承载编排逻辑与门禁判断，相关逻辑仅引用 Agent/Skill。

7. 变量命名一致
  - `artifact_path` 在四个步骤 Prompt 中命名一致，不混用别名。

8. 示例与格式一致
  - 若提供示例，示例字段名必须与最终输出字段完全同名。

### 10.4 实施顺序（操作步骤）

1. 先改 `haca.agent` 与 `evidence-gate`，打通路由与门禁。
2. 再改四个步骤 Skill，补齐文档路由输入输出契约。
3. 再改四个步骤 Prompt，统一双路由入参和输出指示器。
4. 最后改 apply-spec/sync Prompt 与 artifacts 模板，完成发布准备。
5. 回到 `docs/haca-execution-flow.md` 执行逐项复核，确认无偏差再进入试点。

### 10.5 完成定义（SOP DoD）

1. Route A 与 Route B 在 `haca.agent` 可被稳定区分，且冲突时稳定走 Route B。
2. `haca-step1` 可在缺失文件时自动初始化，`haca-step2/3/4` 在缺失文件时必阻断。
3. Evidence Gate 在文档路由仅校验字段与状态，不做哈希校验。
4. 四个步骤 Prompt 均满足高质量 Prompt 清单，且输入变量定义一致。
5. `docs/haca-execution-flow.md` 与 `.github/` 规则语义一致，无冲突项。