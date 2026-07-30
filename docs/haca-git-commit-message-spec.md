# HACA-Git Commit Message 规范

## 目录

- [一、为什么现在必须谈这个问题](#一为什么现在必须谈这个问题)
- [二、AI Agent 工作模式下，Commit Message 面临哪些新挑战](#二ai-agent-工作模式下commit-message-面临哪些新挑战)
- [三、规范：我们的 Commit Message 标准](#三规范我们的-commit-message-标准)
- [四、参考资料与工具](#四参考资料与工具)
- [五、参考文献](#五参考文献)

*适用范围：AI Agent 自主编程工作模式下的代码提交。*

## 一、为什么现在必须谈这个问题

当 AI Agent 开始为我们写代码，它也在为我们写历史。而那段历史，将决定我们能否在一年后、两年后，还读得懂自己的代码库。我们团队已开始大量使用 Cursor、GitHub Copilot 等 AI 编程工具。这些工具极大地提升了编码速度，但也带来了一个需要认真面对的问题：

**Git 历史正在失去意义。**

打开任意一个近期迭代的分支，你很可能看到这样的 commit 记录：

```
fix: update function
refactor: clean up utils
feat: add new feature
chore: misc changes
```

这些 commit 是 AI Agent 生成的。它们符合 Conventional Commits 格式，但几乎没有传递任何有效信息——它们描述的是 `diff` 已经告诉你的事，而不是 `diff` 无法告诉你的事。

2026 年 3 月，来自 arXiv 的一篇论文《Lore: Repurposing Git Commit Messages as a Structured Knowledge Protocol for AI Coding Agents》提出了一个发人深省的观点：**每一次 commit 都会产生一个"决策阴影"（Decision Shadow）**——开发者（或 AI Agent）做了某个决策，但只有最终的 diff 被保存下来，背后的问题定义、考虑过的备选方案、取舍权衡、约束条件，全部蒸发了。[1]

更麻烦的是，AI Agent 既是代码的生产者，也越来越多地成为代码的消费者——当它在下一个任务中尝试理解代码库时，它读到的是一份缺失上下文的历史记录。**知识损耗在加速。**

这不是 AI 的问题，是我们没有给 AI 设定正确规范的问题。

---

## 二、AI Agent 工作模式下，Commit Message 面临哪些新挑战

### 2.1 "自动生成"不等于"高质量"

当前的 AI 工具（Cursor、GitHub Copilot 等）均内置了自动生成 commit message 的能力。它们的工作原理是：读取 `git diff`，然后生成一段描述。

这个机制的根本局限在于：**diff 只能告诉 AI 改了什么，无法告诉 AI 为什么改**。一个函数的错误处理逻辑被重写，AI 只能看到新旧代码，但不知道：

- 旧代码在什么场景下出过 bug？
- 有没有考虑过其他修复方案？
- 这次修改引入了什么新的权衡？

不加约束的 AI 生成结果，往往就像 `fix: updated function` 这样——比懒惰的人类写得还要苍白。[6]

### 2.2 Commit 粒度失控

在 AI Agent 自主执行任务时，它可能会在一次 session 里完成数十个文件的修改，然后产生 1-2 个大而宽泛的 commit，或者反过来，每修改一个文件就提交一次，产生碎片化的历史记录。

Anthropic 在其关于长时运行 Agent 的工程实践文章中明确指出：**要求 Agent 以增量方式提交进度（make incremental progress commits），这让 Agent 能够使用 git revert 回滚错误的代码变更，并恢复到可工作的状态。**[7][14] 好的 commit 粒度不只是为了人类阅读，也是为了让 Agent 自身能有效地自我修正。

### 2.3 "谁写的代码"变得模糊

当 AI Agent 负责实现，人类负责审查，commit author 还是人类，但代码的实际作者是 AI。这在追溯问题、Code Review、责任归属时都会造成混淆。

### 2.4 多任务并行场景下的上下文断裂

在 Cursor 的 Agent 模式或 GitHub Copilot Workspace 执行复杂任务时，AI 可能跨多个文件、多个 session 分阶段完成工作，每次接续时的上下文窗口是独立的。如果没有结构化的 commit message 作为"状态交接点"，后续的 AI 在接手时会不知道已经做了什么、还有什么遗留问题，只能从头重新理解代码库。

---

## 三、规范：我们的 Commit Message 标准

基于以上问题，我们制定了以下团队规范。本规范在 Conventional Commits [2] 基础上扩展，专门适配 AI Agent 与人类协作的工作模式。

### 3.1 完整格式

```
[category-tag] <type>(<scope>): <subject>

## 任务输入
- Jira 任务单：[任务单链接，如无则填"无"]
- 需求描述：[需求的关键元素，包括明确的目标（解决什么问题/达成什么目的）、
  具体功能要求（需执行的动作）、非功能质量属性（如性能、安全、可用性）、
  约束条件（时间/成本/技术等限制）、相关方期望及可验证的验收标准。]

## AI 决策摘要
- 理解的需求：[AI 对任务的理解描述]
- 采用方案：[选择的实现方式及原因]
- 放弃的方案：[考虑过但未采用的方案及原因]
- 关键假设：[AI 做出的前提假设]
- 已知风险：[AI 自识别的潜在问题]
- 未覆盖场景：[AI 明确标注需人工确认的部分]
```

### 3.2 category-tag 说明

`[category-tag]` 是区分提交来源的前缀标签，是本规范最核心的创新点：

| tag | 含义 | 使用场景 |
|-----|------|----------|
| `[AI]` | 由 AI Agent 主导编写并提交 | Cursor Agent、GitHub Copilot 等工具自主完成的 commit |
| `[CI]` | 由 CI/CD 流水线自动提交 | 自动化脚本、版本 bump、changelog 生成等 |
| _(空)_ | 由人类开发者手动提交 | 不加任何 tag，即为人工提交 |

这个设计解决了"谁写的代码"模糊的问题，无需改变 git author 信息，即可在 `git log` 中一眼识别提交来源：

```
# git log --oneline 示例
a3f1c2e [AI] feat(auth): add JWT refresh token rotation
b7d8e1f fix(cart): prevent negative quantity on item removal
c9a2d3b [CI] chore(release): bump version to 2.4.1
```

### 3.3 type 类型表

| type | 用途 |
|------|------|
| `feat` | 新功能 |
| `fix` | Bug 修复 |
| `refactor` | 重构（不改变功能） |
| `perf` | 性能优化 |
| `test` | 新增或修改测试 |
| `docs` | 文档变更 |
| `style` | 代码格式（不影响逻辑） |
| `chore` | 构建、依赖、工具链 |
| `revert` | 回滚 |
| `wip` | 进行中（仅用于临时保存，合并前必须整理） |

### 3.4 Subject 写作要求

- 使用**祈使句**（英文）或**动宾短语**（中文）：`Add OAuth2 login` 而非 `Added OAuth2 login`[2][15]
- 不超过 72 个字符[15]
- 末尾不加句号
- **必须说明"做了什么"，且让人不看 diff 就能理解改动意图**

❌ 错误示例（AI 常见输出，禁止使用）：
```
[AI] fix: update function
[AI] refactor: clean up utils
[AI] feat: add new feature
```

✅ 正确示例：
```
[AI] fix(auth): handle expired JWT token refresh to prevent silent logout
[AI] refactor(utils): extract date formatting into shared helper to reduce duplication
[AI] feat(payment): add Alipay checkout flow with order status polling
```

### 3.5 Body 两段式结构详解

Body 分为两个独立的区块，分别对应任务的**输入侧**与**输出侧**（此结构借鉴了 Nygard 的架构决策记录（ADR）实践 [5]，将决策背景与决策推理共同纳入版本历史）：

#### 第一区块：任务输入

描述这个 commit 要解决的是什么问题。由需求发起方（人类工程师）在任务开始前定义，或由 AI Agent 理解任务后补全，并经人类审查确认。

```
## 任务输入
- Jira 任务单：[PROJ-1234](https://jira.example.com/browse/PROJ-1234)
- 需求描述：用户在登录态过期后，前端静默发起 refresh token 请求失败时，
  会出现无响应的白屏状态而非跳转登录页。需在 token 刷新失败时主动清除
  本地会话并重定向至登录页。验收标准：模拟 401 响应时，300ms 内完成
  跳转且不残留过期 token。
```

**填写要点：**
- Jira 任务单无则填"无"，不可省略该行
- 需求描述不是原始需求的复制粘贴，而是提炼其中的**目标、功能要求、验收标准和约束**
- 此字段的质量，直接决定后续 AI Agent 或人类接手时能否快速理解背景

#### 第二区块：AI 决策摘要

描述 AI Agent 如何理解并执行这个任务。由 AI 自动生成，人类审查后保留或修正。

```
## AI 决策摘要
- 理解的需求：在 axios 拦截器层面捕获 401 响应，当 refresh token 接口
  也返回 401 时，清除 localStorage 中的 token 并调用 router.push('/login')。
- 采用方案：在 responseError 拦截器中添加 isRefreshing 标志位，防止
  并发请求触发多次跳转；使用队列机制保证跳转前所有待处理请求得到妥善处理。
- 放弃的方案：考虑过在每个 API 调用处单独处理，但会导致大量重复代码，
  且漏网风险高；考虑过 Vuex action 统一处理，但增加了不必要的状态层耦合。
- 关键假设：refresh token 接口路径为 /api/auth/refresh，与现有代码一致。
- 已知风险：若存在不经过 axios 的原生 fetch 调用，本次修改无法覆盖。
- 未覆盖场景：SSR 场景下的 token 过期处理需人工确认是否适用同一逻辑。
```

**各字段填写要点：**

| 字段 | 要求 | 无内容时 |
|------|------|---------|
| 理解的需求 | AI 用自己的语言复述任务，暴露理解偏差 | 始终必填 |
| 采用方案 | 说明实现路径及关键技术决策 | 始终必填 |
| 放弃的方案 | 列出被否定的备选方案及原因 | 填"无" |
| 关键假设 | 实现时隐含的前提条件 | 填"无" |
| 已知风险 | AI 自识别的潜在问题（不需要已有解决方案） | 填"无" |
| 未覆盖场景 | 边界模糊、需人工介入确认的情况 | 填"无" |

### 3.6 完整示例

```
[AI] fix(auth): clear session and redirect on refresh token failure

## 任务输入
- Jira 任务单：[PROJ-1234](https://jira.example.com/browse/PROJ-1234)
- 需求描述：用户登录态过期后，refresh token 刷新失败时前端出现白屏而非
  跳转登录页。需在刷新失败时主动清除本地会话并重定向至 /login。
  验收标准：模拟 401 响应时 300ms 内完成跳转，不残留过期 token。

## AI 决策摘要
- 理解的需求：在 axios 拦截器中捕获 refresh 接口的 401 响应，触发登出流程。
- 采用方案：responseError 拦截器添加 isRefreshing 标志位防止并发跳转，
  队列机制确保跳转前所有请求妥善处理。
- 放弃的方案：各 API 调用处单独处理（重复代码多，易遗漏）；
  Vuex action 统一处理（增加不必要的状态耦合）。
- 关键假设：refresh 接口路径为 /api/auth/refresh，与现有配置一致。
- 已知风险：不经过 axios 的原生 fetch 调用无法被本次修改覆盖。
- 未覆盖场景：SSR 场景的 token 过期处理是否适用同一逻辑，需人工确认。
```

---


## 四、参考资料与工具

| 资源 | 说明 |
|------|------|
| [Conventional Commits](https://www.conventionalcommits.org/) | 业界主流 commit message 规范，本规范的基础 |
| [commitlint](https://commitlint.js.org/) | Commit message 格式校验工具 |
| [Cursor Rules 文档](https://docs.cursor.com/context/rules) | `.cursor/rules/` 配置指南 |
| [Cursor Agent Skills 文档](https://cursor.com/docs/context/skills) | `.cursor/skills/` 配置指南 |
| [Cursor Agent Best Practices](https://cursor.com/blog/agent-best-practices) | Cursor 官方 Agent 最佳实践，含 Rules vs Skills 详解 |
| [GitHub Copilot Custom Instructions](https://docs.github.com/en/copilot/customizing-copilot/adding-custom-instructions-for-github-copilot) | `.github/copilot-instructions.md` 配置指南 |
| [Lore Protocol (arXiv 2603.15566)](https://arxiv.org/abs/2603.15566) | 将 commit message 作为 AI Agent 知识协议的前沿研究 |

## 五、参考文献

> **文献质量标注说明**
> - 🔬 同行评审学术论文（期刊 / 会议）
> - 📄 arXiv 预印本（未经同行评审，结论需审慎引用）
> - 📘 权威规范 / 官方手册
> - 📊 行业研究报告
> - 📝 官方工程博客
> - 💬 实践博客（质量参差，仅作工具参考）

[1] Stetsenko, I. (2026). *Lore: Repurposing Git Commit Messages as a Structured Knowledge Protocol for AI Coding Agents*. arXiv preprint arXiv:2603.15566. https://arxiv.org/abs/2603.15566 📄

[2] Conventional Commits. (2024). *Conventional Commits Specification v1.0.0*. https://www.conventionalcommits.org/ 📘

[3] Peng, X., & Wang, C. (2025). *Code Digital Twin: Empowering LLMs with Tacit Knowledge for Complex Software Development*. arXiv preprint arXiv:2503.07967. 📄

[4] Terragni, V., Vella, A., Roop, P., & Blincoe, K. (2025). *The Future of AI-Driven Software Engineering*. ACM Transactions on Software Engineering and Methodology. 🔬

[5] Nygard, M. (2011). *Documenting Architecture Decisions*. Cognitect Blog. https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions 📝

[6] Harding, B. (2024). *Coding on Copilot: 2023 Data Suggests Downward Pressure on Code Quality*. GitClear. https://www.gitclear.com/coding_on_copilot_data_shows_ais_downward_pressure_on_code_quality 📊

[7] Anthropic. (2025). *Effective Harnesses for Long-Running Agents*. Anthropic Engineering Blog. https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents 📝

[8] Lawson, C. (2024). *Git Commit: When AI Met Human Insight*. Versent Tech Blog, Medium. https://medium.com/versent-tech-blog/git-commit-when-ai-met-human-insight-c3ae00f03cfb 💬

[9] Goortani, F. (2025). *Git Best Practices and AI-Driven Development: Rethinking Documentation and Coding Standards*. Medium. https://medium.com/@FrankGoortani/git-best-practices-and-ai-driven-development-rethinking-documentation-and-coding-standards-bca75567566a 💬

[10] Robinson, L. (2026). *Best Practices for Coding with Agents*. Cursor Blog. https://cursor.com/blog/agent-best-practices 📝

[11] Deschryver, T. (2025). *Gain Control Over Commit Messages Generated by GitHub Copilot*. https://timdeschryver.dev/blog/gain-control-over-commit-messages-generated-by-github-copilot 💬

[12] GitHub Docs. (2025). *Adding Repository Custom Instructions for GitHub Copilot*. https://docs.github.com/en/copilot/customizing-copilot/adding-custom-instructions-for-github-copilot 📘

[13] commitlint. (2024). *commitlint — Lint commit messages*. https://commitlint.js.org/ 📘

[14] Anthropic. (2024). *Building Effective Agents*. Anthropic Research Blog, December 2024. https://www.anthropic.com/research/building-effective-agents 📝
> 注：这是 Anthropic 被广泛引用的 Agent 构建实践指南，系统阐述了 Agent 工作流设计、分步提交（checkpoint commits）与人机协作（human-in-the-loop）原则，与 [7] 互为补充。

[15] Chacon, S., & Straub, B. (2014). *Pro Git* (2nd ed.). Apress. https://git-scm.com/book/en/v2 📘
> 本书第 5 章"Distributed Git"系统阐述了 commit 粒度（atomic commits）、祈使句主题行以及 50/72 字符列宽惯例的成因，是业界书写规范的权威来源。

[16] Jiang, S., Armaly, A., & McMillan, C. (2017). Automatically Generating Commit Messages from Diffs Using Neural Machine Translation. In *Proceedings of the 32nd IEEE/ACM International Conference on Automated Software Engineering (ASE 2017)*, pp. 135–144. 🔬
> 该研究系统分析了从 diff 自动生成 commit message 的方法与局限，实证表明纯 diff 驱动的生成结果在"解释决策动机"上存在根本性缺失，直接支撑本规范第二章的问题分析。


---
