# Conversion SDK — 参考资料

此目录存放 Conversion SDK 的官方文档抽取参考文件，供 HACA-SDK Step 2（方案设计）与
Step 4（SDK API 正确性校验）使用。文件为原始抽取内容，不做改写。

## 文件 → 语言 → 覆盖主题

| 文件 | 语言 | 行数 | 覆盖主题 |
|------|------|------|----------|
| `ConversionSDK_C__b2be93fa.txt` | C | 1507 | 见下方“覆盖主题说明” |
| `ConversionSDK_C++__4f6e672c.txt` | C++ | 1429 | 同上 |
| `ConversionSDK_Python__51c1aa97.txt` | Python | 1206 | 同上 |
| `ConversionSDK_Java__183d1092.txt` | Java | 1164 | 同上 |
| `ConversionSDK_Javascript__1809d3ab.txt` | Node.js (JavaScript) | 1149 | 同上 |
| `ConversionSDK_C#__022fc064.txt` | C# | 1051 | 同上 |

### 覆盖主题说明

每个文件为英文 “How to …” 问答集合（约 16 条），主题一致，主要包括：

- **格式双向转换**：PDF ↔ Word / Excel / PowerPoint / RTF；Excel / Word / PowerPoint → PDF。
- **两种输入方式**：文件路径（file path）与流式读取（streaming + reader callback）。
- **受密码保护的 PDF**：带密码（如 `"123456"`）与无密码文件的转换。
- **回调机制**：`FileReaderCallback`（读取侧）与 convert callback（转换侧）的定义与使用。
- **机器学习识别开关**：可启用/禁用基于机器学习的版面识别（machine learning-based recognition）。

> 该目录**没有 Go 语言抽取文件**；若目标语言为 Go，请在 Step 2 标注参考不足并回退官方文档。

## 样例风格注意事项

- **内容为抽取原文**：不修改、不摘要；示例为“主要步骤”式代码片段，非完整可运行程序。
- **占位值**：示例中的密码（如 `"123456"`）为演示占位值，实际使用时由调用方传入，切勿硬编码。
- **回调必须实现**：流式转换依赖 `FileReaderCallback` 子类，使用前需按示例实现读取与转换回调。
- **平台限制**：部分方向（如 Excel/Word/PowerPoint → PDF 的某些示例）标注仅支持 Windows 或 Linux，跨平台前请核对。

## 产品概述

Conversion SDK 提供多种文档格式转换能力。

### 支持平台

| 平台 | 架构 | 支持语言 |
|------|------|----------|
| Windows | x86, x86_64 | C++, Python, Java, Node.js, C#, C, Go |
| Linux | x86, x86_64, armv7, armv8 | C++, Python, Java, Node.js, C#, C, Go |

> 说明：上表为产品对外支持的语言清单；本目录抽取文件覆盖 C / C++ / C# / Java / Node.js / Python，尚未包含 Go。
