# Prompt 书写规范与最佳实践研究报告

本报告总结了来自国际权威机构和研究机构关于 AI 模型 Prompt 书写的规范、规则和最佳实践。每个观点均明确标注引用来源。

## 目录

1. [Prompt 的基本构成](#prompt-的基本构成)
2. [核心书写规范](#核心书写规范)
3. [Prompt 结构与格式](#prompt-结构与格式)
4. [高级技巧与策略](#高级技巧与策略)
5. [常见错误与避免方法](#常见错误与避免方法)
6. [参考文献](#参考文献)

---

## Prompt 的基本构成

### 四个关键元素

Prompt 通常包含以下四个关键元素：

1. **Instruction（指令）** - 具体的任务或指令，说明模型需要执行什么操作
   - 来源：[DAIR.AI Prompt Engineering Guide - Elements of a Prompt](https://www.promptingguide.ai/introduction/elements)

2. **Context（上下文）** - 外部信息或额外的背景信息，用于引导模型生成更好的响应
   - 来源：[DAIR.AI Prompt Engineering Guide - Elements of a Prompt](https://www.promptingguide.ai/introduction/elements)

3. **Input Data（输入数据）** - 具体的输入或问题，用户期望获得的响应对象
   - 来源：[DAIR.AI Prompt Engineering Guide - Elements of a Prompt](https://www.promptingguide.ai/introduction/elements)

4. **Output Indicator（输出指示器）** - 期望的输出类型或格式
   - 来源：[DAIR.AI Prompt Engineering Guide - Elements of a Prompt](https://www.promptingguide.ai/introduction/elements)

**注意**：不是所有 Prompt 都需要包含这四个元素，具体取决于任务性质。

### 示例：基本 Prompt 结构

```
Classify the text into neutral, negative, or positive
Text: I think the food was okay.
Sentiment:
```

在上述示例中：
- **Instruction**: "Classify the text into neutral, negative, or positive"
- **Input Data**: "I think the food was okay."
- **Output Indicator**: "Sentiment:"

来源：[DAIR.AI Prompt Engineering Guide - Elements of a Prompt](https://www.promptingguide.ai/introduction/elements)

---

## 核心书写规范

### 1. 从简单开始，逐步迭代

**规范**：从简单的 Prompt 开始，然后根据结果逐步添加更多元素和上下文。

**理由**：这种渐进式的方法有助于避免在设计过程初期引入过多复杂性，并使得问题诊断更容易。

**应用**：
- 使用简单的 Playground（例如 OpenAI Playground 或 Cohere）作为起点
- 根据结果不断迭代改进
- 当面对较大任务时，将其分解为更简单的子任务

来源：[DAIR.AI - General Tips for Designing Prompts](https://www.promptingguide.ai/introduction/tips)

---

### 2. 指令要明确清晰

**规范**：使用命令式动词来设置 Prompt，说明模型需要执行的具体操作。

**常用动词**：
- Write（编写）
- Classify（分类）
- Summarize（总结）
- Translate（翻译）
- Order（排序）
- Extract（提取）

**关键点**：
- 更具体和相关的上下文通常会产生更好的结果
- 应在 Prompt 的开头放置指令
- 建议使用清晰的分隔符（如 `###` 或 `"""` 作为指令和上下文之间的分隔符）

来源：[DAIR.AI - General Tips for Designing Prompts](https://www.promptingguide.ai/introduction/tips)

---

### 3. 具体性规范（Specificity）

**规范**：Prompt 应尽可能具体、详细和描述性，包括期望的成果、长度、格式、风格等。

**详细的 Prompt 比笼统的 Prompt 产生更好的结果**。

**示例对比**：

❌ **不够具体**：
```
提取以下文本中的地点信息。
```

✅ **具体清晰**：
```
从以下文本中提取所有地点名称。
所需格式：Place: <逗号分隔的地点列表>
```

**重要考虑**：
- 虽然细节很重要，但也要考虑 Prompt 长度的限制
- 不要添加不必要的细节，只包含与任务相关的详细信息
- 这需要大量实验才能找到最佳平衡

来源：[DAIR.AI - General Tips for Designing Prompts](https://www.promptingguide.ai/introduction/tips)

---

### 4. 避免模糊不清

**规范**：避免含糊其辞的描述，要直接明确。

**原则**：直接的沟通通常比模糊的沟通更有效。

**示例对比**：

❌ **模糊不清**：
```
Explain the concept prompt engineering. Keep the explanation short, 
only a few sentences, and don't be too descriptive.
```

✅ **明确清晰**：
```
Use 2-3 sentences to explain the concept of prompt engineering 
to a high school student.
```

来源：[DAIR.AI - General Tips for Designing Prompts](https://www.promptingguide.ai/introduction/tips)

---

### 5. 指导做什么，而非不做什么

**规范**：在 Prompt 中应该说明模型应该做什么，而不是强调不应该做什么。

**理由**：强调"不做什么"往往会导致模型误解，反而做出你试图避免的行为。

**示例对比**：

❌ **不推荐**：
```
The following is an agent that recommends movies to a customer. 
DO NOT ASK FOR INTERESTS. DO NOT ASK FOR PERSONAL INFORMATION.
Customer: Please recommend a movie based on my interests.
Agent:
```

✅ **推荐**：
```
The following is an agent that recommends movies to a customer. 
The agent is responsible to recommend a movie from the top global 
trending movies. It should refrain from asking users for their 
preferences and avoid asking for personal information. If the agent 
doesn't have a movie to recommend, it should respond "Sorry, couldn't 
find a movie to recommend today."
Customer: Please recommend a movie based on my interests.
Agent:
```

来源：[DAIR.AI - General Tips for Designing Prompts](https://www.promptingguide.ai/introduction/tips) 和 [OpenAI Help Center - Best practices for prompt engineering](https://help.openai.com/en/articles/6654000-best-practices-for-prompt-engineering)

---

## Prompt 结构与格式

### 1. 结构化格式规范

#### 使用 Markdown 和 XML 标签

**规范**：使用 Markdown 标题和列表以及 XML 标签来帮助模型理解 Prompt 的逻辑边界。

**优势**：
- 使 Prompt 更易读
- 帮助模型理解不同部分的分层关系
- 让代码更易维护

**标准 Developer Message 结构**（由上到下）：

1. **Identity（身份）** - 描述助手的目的、沟通风格和高层目标
2. **Instructions（指令）** - 提供关于如何生成响应的指导
3. **Examples（示例）** - 提供示例输入和期望的输出
4. **Context（上下文）** - 提供额外的信息或专有数据

来源：[OpenAI - Prompt engineering - Message formatting with Markdown and XML](https://developers.openai.com/api/docs/guides/prompt-engineering)

#### 示例：结构化 Prompt

```markdown
# Identity

You are a coding assistant that helps enforce the use of snake case 
variables in JavaScript code, and writing code that will run in 
Internet Explorer version 6.

# Instructions

* When defining variables, use snake case names (e.g. my_variable) 
  instead of camel case names (e.g. myVariable).
* To support old browsers, declare variables using the older 
  "var" keyword.
* Do not give responses with Markdown formatting, just return 
  the code as requested.

# Examples

<user_query>
How do I declare a string variable for a first name?
</user_query>

<assistant_response>
var first_name = "Anna";
</assistant_response>
```

来源：[OpenAI - Prompt engineering - Message formatting with Markdown and XML](https://developers.openai.com/api/docs/guides/prompt-engineering)

---

### 2. 指令分隔符规范

**规范**：使用清晰的分隔符（如 `###` 或 `"""` 或 `---`）将指令部分与输入数据部分分开。

**示例**：

```
### Instruction ###
Translate the text below to Spanish:

Text: "hello!"
```

**优势**：
- 增强 Prompt 的可读性
- 帮助模型清楚地识别不同部分的边界
- 便于版本管理和维护

来源：[DAIR.AI - General Tips for Designing Prompts](https://www.promptingguide.ai/introduction/tips)

---

### 3. 输出格式规范

**规范**：明确指定期望的输出格式，并通过示例来展示。

**原则**：展示（Show）比讲述（Tell）更有效。通过具体的格式示例帮助模型理解期望的输出。

**示例对比**：

❌ **仅用文字描述**：
```
Extract the important entities mentioned in the text below. 
Extract the following 4 entity types: company names, people names, 
specific topics and themes.
```

✅ **提供格式示例**：
```
Extract the important entities mentioned in the text below. 
First extract all company names, then extract all people names, 
then extract specific topics which fit the content and finally 
extract general overarching themes.

Desired format:
Company names: <comma_separated_list_of_company_names>
People names: <comma_separated_list_of_people_names>
Specific topics: <comma_separated_list_of_topics>
General themes: <comma_separated_list_of_themes>
```

来源：[OpenAI Help Center - Best practices for prompt engineering](https://help.openai.com/en/articles/6654000-best-practices-for-prompt-engineering)

---

### 4. 角色和消息结构规范（Role-based Messaging）

**规范**：使用不同的消息角色来区分指令的权威级别和来源。

**角色层级**（根据 OpenAI Model Spec）：

| 角色 | 优先级 | 说明 |
|------|--------|------|
| `developer` | 最高 | 由应用开发者提供的系统规则和业务逻辑 |
| `user` | 中等 | 最终用户提供的输入和配置 |
| `assistant` | 最低 | 模型生成的响应 |

**类比**：
- `developer` message 类似于函数定义
- `user` message 类似于函数参数

来源：[OpenAI - Prompt engineering - Message roles and instruction following](https://developers.openai.com/api/docs/guides/prompt-engineering)

---

## 高级技巧与策略

### 1. 零样本学习（Zero-shot Prompting）

**定义**：无需示例，直接向模型提示任务的方法。

**格式**：
```
<Question>?
```
或
```
<Instruction>
```

**适用场景**：
- 较简单和明确的任务
- 模型在训练中已接触过的任务类型

来源：[DAIR.AI - Basics of Prompting](https://www.promptingguide.ai/introduction/basics)

---

### 2. 少样本学习（Few-shot Prompting）

**定义**：通过提供少量的示例（通常2-5个）来引导模型学习任务的方法。

**特点**：
- 启用上下文中的学习（In-context Learning）
- 模型隐式地"学习"示例中的模式并应用到新的输入
- 对于需要特定输出格式的任务特别有效

**格式示例**（问答格式）：
```
Q: <Question 1>?
A: <Answer 1>
Q: <Question 2>?
A: <Answer 2>
Q: <Question 3>?
A: <Answer 3>
Q: <New Question>?
A:
```

**分类任务格式示例**：
```
This is awesome! // Positive
This is bad! // Negative
Wow that movie was rad! // Positive
What a horrible show! //
```

**关键点**：
- 提供多样化的示例
- 示例应该代表不同的输入变体
- 示例顺序和质量影响效果

来源：[DAIR.AI - Basics of Prompting](https://www.promptingguide.ai/introduction/basics)

---

### 3. 思维链提示（Chain-of-Thought Prompting）

**定义**：要求模型展示推理步骤，逐步解决复杂问题的方法。

**优势**：
- 提高复杂推理任务的准确性
- 使问题解决过程更透明
- 适合多步骤的逻辑问题

来源：[DAIR.AI - Prompting Techniques](https://www.promptingguide.ai/techniques/cot)

---

### 4. 知识生成提示（Generate Knowledge Prompting）

**定义**：在回答问题前让模型先生成相关知识的方法。

**流程**：
1. 要求模型生成相关的知识或背景信息
2. 在此基础上回答原始问题

**优势**：
- 对知识密集型任务有帮助
- 减少幻想（Hallucination）

来源：[DAIR.AI - Prompting Techniques](https://www.promptingguide.ai/techniques/knowledge)

---

### 5. 检索增强生成（RAG - Retrieval Augmented Generation）

**定义**：向 Prompt 添加从外部知识库检索的相关信息，以提高响应准确性的方法。

**应用场景**：
- 提供模型训练数据之外的专有数据
- 约束模型响应到特定的资源集合
- 减少模型的幻想和不准确

**实现方式**：
- 从向量数据库查询并包含相关文本
- 使用 OpenAI 的文件搜索工具
- 包含相关文档片段作为上下文

来源：[OpenAI - Prompt engineering - Include relevant context information](https://developers.openai.com/api/docs/guides/prompt-engineering)

---

## 常见错误与避免方法

### 1. 过于冗长和模糊的指令

**错误示例**：
```
Please write something about how to make a cake, you know, something 
that is interesting and engaging, and maybe include some tips and tricks, 
but not too many, and make sure it's not too long.
```

**问题**：
- "interesting"、"engaging"、"too many"、"not too long" 等词汇含意不明确
- 模型无法精确理解期望

**改进方案**：
```
Write a 300-word recipe guide for baking a chocolate cake, including:
- List of 8-10 key ingredients
- Step-by-step instructions (5-7 steps)
- 3 pro tips for best results
```

---

### 2. 缺乏结构和格式指导

**错误示例**：
```
Extract information from this text.
```

**问题**：
- 模型不知道应该提取什么信息
- 不知道输出的格式

**改进方案**：
```
Extract the following information from the text below:
- Person's name
- Job title
- Company name
- Contact email

Format each piece of information as:
Name: [name]
Title: [title]
Company: [company]
Email: [email]

Text: [input text]
```

---

### 3. 忽视上下文的重要性

**错误示例**：
```
Classify this sentiment.
The package arrived late.
```

**问题**：
- 缺乏背景信息
- 可能导致错误的分类

**改进方案**：
```
You are a customer service sentiment analyst. Classify the following 
customer review as positive, negative, or neutral. Consider the 
context of the purchase and delivery experience.

Customer Review: "The package arrived late, but the product quality 
is excellent and customer service was very helpful."

Classification:
```

---

### 4. 使用模糊的否定表述

**错误示例**：
```
DO NOT mention price, DO NOT ask for personal information, 
DO NOT use technical jargon.
```

**问题**：
- 模型可能反而强调遵守这些禁止事项
- 得到与预期相反的结果

**改进方案**：
```
When responding, always:
- Focus on product benefits rather than pricing details
- Use simple, everyday language to explain concepts
- Ask only for information strictly necessary for assistance
```

---

## 参考文献

### 官方文档和权威指南

1. **OpenAI - Prompt Engineering Guide**
   - 链接：https://developers.openai.com/api/docs/guides/prompt-engineering
   - 涵盖：消息角色、指令跟随、格式化、上下文、推理模型提示
   - 日期：2025年

2. **OpenAI - Best practices for prompt engineering with the OpenAI API**
   - 链接：https://help.openai.com/en/articles/6654000-best-practices-for-prompt-engineering
   - 涵盖：9个核心最佳实践规则和示例
   - 内容包括：指令位置、具体性、输出格式、零样本/少样本/微调、避免冗余描述等
   - 日期：更新于2024年10月

3. **DAIR.AI - Prompt Engineering Guide**
   - 链接：https://www.promptingguide.ai/
   - 涵盖：基础概念、提示技巧、高级技术、应用案例、模型特定指南
   - 组织：包含学科分类的 Prompt Hub，收集社区优质示例

4. **DAIR.AI - Basics of Prompting**
   - 链接：https://www.promptingguide.ai/introduction/basics
   - 涵盖：基本 Prompt 格式、零样本、少样本提示、上下文学习
   - 日期：更新于2026年2月

5. **DAIR.AI - General Tips for Designing Prompts**
   - 链接：https://www.promptingguide.ai/introduction/tips
   - 涵盖：6大关键建议——从简开始、明确指令、具体性、避免模糊、做什么而非不做什么、迭代
   - 日期：更新于2026年2月

6. **DAIR.AI - Prompt Elements**
   - 链接：https://www.promptingguide.ai/introduction/elements
   - 涵盖：Prompt 的4个关键元素：Instruction, Context, Input Data, Output Indicator
   - 日期：更新于2026年2月

---

## 总结与建议

### Prompt 书写的黄金规则

1. **清晰为首** - 使用清晰、直接、具体的语言
2. **结构重要** - 合理组织 Prompt 的结构，使用分隔符和格式化
3. **示例有力** - 不是告诉模型什么是对的，而是展示什么是对的
4. **迭代优化** - 从简单开始，逐步迭代改进
5. **避免歧义** - 不要让模型猜测你的意图
6. **提供上下文** - 充分的背景信息有助于正确理解任务

### 快速检查清单

在提交 Prompt 前，请检查：

- [ ] 指令是否清晰明确？
- [ ] 是否使用了具体的示例或格式说明？
- [ ] 输出格式是否明确定义？
- [ ] 是否避免了模糊的表述（如"稍微一点"、"不太长"）？
- [ ] 是否使用了正面表述而不是负面禁止？
- [ ] Prompt 的结构是否合理（身份、指令、示例、上下文）？
- [ ] 是否提供了充分的背景信息或上下文？

---

**报告最后更新时间**：2026年3月26日

**文献收集来源**：
- OpenAI 官方文档（2025年）
- DAIR.AI Prompt Engineering Guide（2026年）
- OpenAI Help Center（2024-2025年）
