# Cloud API — 参考资料

此目录存放福昕 Cloud API 的官方文档抽取参考文件，供 HACA-SDK Step 2（方案设计）与
Step 4（SDK API 正确性校验）使用。文件为原始抽取内容，不做改写。

## 文件 → 语言 → 覆盖主题

| 文件 | 语言 | 覆盖主题 |
|------|------|----------|
| `CloudAPI_Javascript__82ec1cfe.txt` | JavaScript（Embed Viewer，REST 加载） | 概要、应用原理与快速上手、打开 PDF 文件（`previewFile` / `content` / `metaData`）、客户端 ID 生成、HTML 示例（Embed Viewer Full Window） |

> 该文件为**中文叙述式指南**，含完整 HTML/JS 示例，非 “How to …” 问答集合。
> 当前抽取内容仅覆盖 Embed Viewer 的打开文件流程；PDF Services 等其他云端能力尚未抽取。

## 样例风格注意事项

- **内容为抽取原文**：不修改、不摘要。示例为最小可用页面，非生产级完整工程。
- **必须替换占位值**：示例中的 `clientId=REPLACE_YOUR_CLIENT_ID` 等占位参数需替换为开发者控制台生成的真实客户端 ID；序列号/密钥等敏感值不得写入源码。
- **基础阅读能力说明**：Embed API 支持高性能 PDF 查看、文本处理、注释、填表（不支持带 JavaScript 的表单填写）与朗读；自定义能力包括主题、工具栏和导航设置。
- **服务端语言未覆盖**：Cloud API 为 REST 接口，理论上任意语言可调用，但本目录暂无其他语言的抽取文件。

## 产品概述

福昕 Cloud API 提供云端 PDF 处理服务，包含两个子产品：

### Embed Viewer API

只需几行代码即可在 Web 上嵌入 PDF 查看、渲染等功能。

### PDF Services API

通过云端访问福昕 PDF 提供的各类 API 功能。

### 特点

- 新用户获得 10000 次免费调用
- REST API 接口，支持任意编程语言调用

产品介绍（中文站）: https://cloudapi.fuxinsoft.cn/zh-CN

> Cloud API 目前仅有中文站（`cloudapi.fuxinsoft.cn`）；未提供对应的 `cloudapi.foxitsoftware.cn` 英文站入口。

文档主页: https://cloudapi.fuxinsoft.cn/docs/embed/quick-start
