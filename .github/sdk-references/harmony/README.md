# PDF SDK for Harmony — 参考资料

此目录存放 PDF SDK for Harmony（鸿蒙）的官方文档抽取参考文件，供 HACA-SDK Step 2（方案设计）与
Step 4（SDK API 正确性校验）使用。文件为原始抽取内容，不做改写。

## 文件 → 语言 → 覆盖主题

| 文件 | 语言 | 覆盖主题 |
|------|------|----------|
| `RDK_ArkTS__d1718172.txt` | ArkTS | 产品介绍与主要框架（PDF Core / PDF View Control / UI Extension）、组件与 API 说明 |

> 该文件为**中文叙述式指南**（含 Table of Contents），非 “How to …” 问答集合，结构与桌面/移动/转换类不同。

## 样例风格注意事项

- **内容为抽取原文**：不修改、不摘要。此文件偏产品与架构说明，API 粒度的用法示例较少。
- **平台差异**：OpenHarmony 平台暂不提供 UI Extension 组件；macOS 可通过 Catalyst 技术复用 iOS SDK。
- **参考粒度有限**：若任务需要具体 API 级示例，请在 Step 2 标注参考不足并回退到官方文档。

## 产品概述

福昕 PDF SDK 鸿蒙版是专为鸿蒙生态打造的专业级 PDF 处理开发库，采用"C++ 原生核心 + ArkTS 封装"架构实现高效跨平台兼容。

### 主要框架

- **PDF Core**: 核心 API，基于福昕底层 PDF 技术
- **PDF View Control**: 渲染的 PDF 文档交互接口
- **UI Extension**: 高扩展性 PDF 交互组件库（注意：OpenHarmony 平台暂不提供 UI Extensions 组件）

### 支持平台

| 平台 | 语言 |
|------|------|
| HarmonyOS Next | ArkTS |
| OpenHarmony | ArkTS |

产品介绍（英文站）: https://developers.foxitsoftware.cn/pdfsdk-harmony/
产品介绍（中文站）: https://developers.fuxinsoft.cn/pdfsdk-harmony/
