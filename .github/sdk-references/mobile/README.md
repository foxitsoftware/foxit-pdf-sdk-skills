# PDF SDK for Mobile — 参考资料

此目录存放 PDF SDK for Mobile 的官方文档抽取参考文件，供 HACA-SDK Step 2（方案设计）与
Step 4（SDK API 正确性校验）使用。文件为原始抽取内容，不做改写。

## 文件 → 语言 → 覆盖主题

| 文件 | 语言 | 主题条数 | 覆盖主题 |
|------|------|----------|----------|
| `RDK_Java__59c6b256.txt` | Java（Android） | 103 | 注释与标注、表单、签名与验签、加解密与权限、渲染/打印、页面组织、文本搜索与替换、格式转换、OCR 与版面识别、元数据 |
| `RDK_Objective-C__a86b7d84.txt` | Objective-C（iOS） | 60 | 注释与标注、表单、签名与验签、渲染/打印、页面组织、文本搜索与替换、格式转换、OCR 与版面识别、元数据（安全类条目少于 Android） |

> 均为英文 “How to …” 问答式条目集合。

## 样例风格注意事项

- **内容为抽取原文**：不修改、不摘要；示例多为最小代码片段，非完整可运行程序。
- **占位值**：部分示例含占位参数（如序列号/密钥等），需替换为真实值后再运行。
- **仅限本语言 API**：Android 用 Java API、iOS 用 Objective-C API，请勿跨语言混用。
- **Swift 参考缺失**：本目录暂无 Swift 抽取文件；若目标语言为 Swift，请在 Step 2 标注参考不足并回退官方文档。

## 产品概述

福昕 PDF SDK 移动版面向 Android 和 iOS 平台提供高性能的 PDF 引擎与完善的开发接口。

### 主要框架

- **PDF Core**: SDK 底层核心引擎，覆盖渲染、解析、提取、搜索、注释、表单、签名等基础功能
- **PDF View Control**: PDF 渲染视图的核心交互控制模块
- **UI Extension**: PDF 交互场景的专业能力模块（阅读、批注、手写墨迹、电子签名等）
- **Cordova**: 混合应用的桥接能力

### 支持平台

| 平台 | 语言 |
|------|------|
| Android | Java |
| iOS | Objective-C, Swift |

产品介绍（英文站）: https://developers.foxitsoftware.cn/pdfsdk-mobile/
产品介绍（中文站）: https://developers.fuxinsoft.cn/pdfsdk-mobile/
