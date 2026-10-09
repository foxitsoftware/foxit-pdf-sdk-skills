# PDF SDK for Desktop — 参考资料

此目录存放 PDF SDK for Desktop 的官方文档抽取参考文件，供 HACA-SDK Step 2（方案设计）与
Step 4（SDK API 正确性校验）使用。文件为原始抽取内容，不做改写。

## 文件 → 语言 → 覆盖主题

| 文件 | 语言 | 主题条数 | 覆盖主题 |
|------|------|----------|----------|
| `GSDK_C__dcf1ba34.txt` | C | 175 | 注释与标注、表单、签名与验签、加解密与权限、渲染/打印、页面组织、文本搜索与替换、格式转换、OCR 与版面识别、元数据 |
| `GSDK_C++__f8fe7687.txt` | C++ | 161 | 同上（注释/表单/签名/安全/渲染/页面组织/文本/转换/OCR/元数据） |
| `GSDK_Python__503b7c42.txt` | Python | 160 | 同上 |
| `GSDK_Java__508cc580.txt` | Java | 159 | 同上 |
| `GSDK_C#__0399c0be.txt` | C# | 158 | 同上 |
| `GSDK_Objective-C__a1768bb5.txt` | Objective-C (macOS) | 137 | 同上 |
| `GSDK_Javascript__abb8e7fc.txt` | Node.js (JavaScript) | 1 | 仅一个中文示例（“如何用 Foxit PDF SDK …”），覆盖面远小于其他语言，使用时请以官方文档补充 |

> 各文件均为英文 “How to …” 问答式条目集合，一个条目对应一个最小 API 用法示例。

## 样例风格注意事项

- **内容为抽取原文**：不修改、不摘要。示例多为最小代码片段，并非可直接运行的完整程序，请作为 API 用法参考。
- **占位值**：部分示例含占位参数（如序列号/密钥等），需替换为真实值后再运行。
- **仅限本语言 API**：每个文件只使用其对应语言的 API 命名与调用约定，请勿跨语言混用。
- **Node.js（JavaScript）参考严重不足**：该文件仅含 1 条示例，若目标语言为 Node.js，请在 Step 2 明确标注参考不足并回退到官方文档。

## 产品概述

PDF SDK for Desktop 是为开发者打造的高性能 PDF 开发库，集成新一代渲染内核与智能 OCR 技术，全面支持 Windows、Mac、Linux 多平台，并提供 C++、Python、Java、Node.js、C#、C、Go、Objective-C 等主流语言接口。

### 核心功能

- 渲染与缩放：高性能渲染、高清缩放
- 注释与标注：文本、手绘、图形标注，多媒体与印章
- 表单与交互：AcroForm 及 XFA 表单填写
- 文本与图像处理：全文搜索、OCR 识别
- 安全与权限控制：密码、权限、电子签名、水印、RMS/DRM
- 文件操作：合并、拆分、页面管理、格式转换

### 支持平台

| 平台 | 架构 | 支持语言 |
|------|------|----------|
| Windows | x86, x86_64 | C++, Python, Java, Node.js, C#, C, Go |
| Linux | x86, x86_64, armv7, armv8 | C++, Python, Java, Node.js, C#, Go |
| macOS | x64, arm64 | C++, Python, Java, Objective-C, Go |

产品介绍（英文站）: https://developers.foxitsoftware.cn/pdfsdk-pc/
产品介绍（中文站）: https://developers.fuxinsoft.cn/pdfsdk-pc/
