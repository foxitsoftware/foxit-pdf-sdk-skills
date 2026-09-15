# Foxit SDK Product Matrix (Single Source of Truth)

> 本文件是仓库内 Foxit SDK **产品 × 平台 × 架构 × 语言**的唯一事实来源（Single Source of Truth）。
> `.github/copilot-instructions.md`、`.github/skills/clarify-requirements/SKILL.md`、
> `.github/sdk-references/foxit-sdk-config-schema.md` 与各产品 README 均引用本文件，不再各自维护副本。
> 修改产品支持口径时，只改本文件，并同步更新被引用处指向本文件的链接（而非复制内容）。

## 产品矩阵

| Product | Supported Platforms | Languages | Product Overview |
|---------|---------------------|-----------|------------------|
| **PDF SDK for Desktop** | Windows (x86/x86_64), Linux (x86/x86_64, armv7, armv8), Mac (x64/arm64) | C++, Python, Java, Node.js, C#, C (Windows only), Go, Objective-C (macOS only) | EN: https://developers.foxitsoftware.cn/pdfsdk-pc/ · ZH: https://developers.fuxinsoft.cn/pdfsdk-pc/ |
| **PDF SDK for Mobile** | Android, iOS | Java (Android), Objective-C / Swift (iOS) | EN: https://developers.foxitsoftware.cn/pdfsdk-mobile/ · ZH: https://developers.fuxinsoft.cn/pdfsdk-mobile/ |
| **PDF SDK for Harmony** | HarmonyOS Next, OpenHarmony | ArkTS (C++ native core + ArkTS wrapper) | EN: https://developers.foxitsoftware.cn/pdfsdk-harmony/ · ZH: https://developers.fuxinsoft.cn/pdfsdk-harmony/ |
| **PDF SDK for Web** | Browser | JavaScript / TypeScript | EN: https://developers.foxitsoftware.cn/pdfsdk-web/ · ZH: https://developers.fuxinsoft.cn/pdfsdk-web/ |
| **Cloud API** | Cloud service | REST API (Embed Viewer API + PDF Services API) | ZH only: https://cloudapi.fuxinsoft.cn/zh-CN (无英文站入口) |
| **Conversion SDK** | Windows (x86/x86_64), Linux (x86/x86_64, armv7, armv8) | C++, Python, Java, Node.js, C#, C, Go | — |

### 平台限制补充说明

- **Desktop**：`C` 语言仅支持 Windows；`Objective-C` 仅支持 macOS。
- **Mobile**：Android 仅支持 Java；iOS 支持 Objective-C 与 Swift。
- **Harmony**：OpenHarmony 平台暂不提供 UI Extensions 组件。
- **Conversion SDK**：与 Desktop 不同，Conversion SDK 的 Linux 版支持 `C` 语言。

## SDK 版本基准

各参考文件来源版本不一（例如 WebSDK 抽取文件提及 9.2.0 / 10.16.0，iOS RDK 提及 8.4）。
当前未设立统一基准版本；Step 2 / Step 4 使用参考文件时，以`.github/sdk-references/<product>/README.md`
头部标注的来源版本为准，并在 HACA Workflow Contract 中记录所用 SDK 版本。

## 配置枚举值映射（供 `foxit-sdk.config.json` 使用）

| 产品 | `product` 枚举 | `platform` 枚举 | `language` 枚举 |
|------|----------------|-----------------|-----------------|
| PDF SDK for Desktop | `desktop` | `windows`, `linux`, `macos` | `cpp`, `python`, `java`, `nodejs`, `csharp`, `c`, `go`, `objc` |
| PDF SDK for Mobile | `mobile` | `android`, `ios` | `java`, `objc`, `swift` |
| PDF SDK for Harmony | `harmony` | `harmonyos-next`, `openharmony` | `arkts` |
| PDF SDK for Web | `web` | `browser` | `javascript`, `typescript` |
| Cloud API | `cloud-api` | *(不适用)* | `javascript` (Embed Viewer 示例) |
| Conversion SDK | `conversion` | `windows`, `linux` | `cpp`, `python`, `java`, `nodejs`, `csharp`, `c`, `go` |

> 完整字段说明见 [foxit-sdk-config-schema.md](./foxit-sdk-config-schema.md)。

## 产品 / API 选择决策树（Decision Tree）

当用户只描述"要做什么"而未指明产品时，按以下顺序收敛到目标产品与关键类。**任何一步落到
"不支持"时，回到 Step 1 与用户确认，不要臆造 API。**

```text
任务描述
  │
  ├─ 运行在浏览器 / 网页内嵌？ ────────────────▶ PDF SDK for Web
  │     └─ 关键类：UIExtension.PDFUI（异步初始化，需 licenseSN/licenseKey）
  │
  ├─ 运行在移动端 App（Android / iOS）？ ──────▶ PDF SDK for Mobile
  │     └─ 关键类：Library（initialize/release）、PDFDoc、PDFPage（句柄需 close）
  │
  ├─ 运行在鸿蒙（HarmonyOS Next / OpenHarmony）？ ▶ PDF SDK for Harmony
  │     └─ 关键类：ArkTS 封装（C++ native core + ArkTS wrapper）
  │
  ├─ 无需本地运行、走 HTTP 服务？ ─────────────▶ Cloud API
  │     └─ 注意：REST 服务，无本地文件系统；文件经 HTTP 上传/下载
  │
  ├─ 核心诉求是"格式转换"（PDF↔Office/图片等）？ ▶ Conversion SDK
  │     └─ 关键类：转换引擎（与 Desktop 不同，Linux 版支持 C）
  │
  └─ 桌面端本地处理（Windows / Linux / macOS）？ ▶ PDF SDK for Desktop
        └─ 关键类：Library（Initialize/Release）、PDFDoc、PDFPage
           └─ 语言：C++ / Python / Java / Node.js / C# / C(仅 Windows) / Go / Objective-C(仅 macOS)
```

**关键类速查（跨产品共性）：**

| 关注点 | Desktop / Mobile | Web | Cloud API |
|--------|------------------|-----|-----------|
| 初始化 | `Library::Initialize(sn, key)` / `Library.initialize(sn, key)`，**必须检查返回码** | `new UIExtension.PDFUI({...})`（异步） | 无（HTTP 调用） |
| 文档 | `PDFDoc`（open/load → save → close） | viewer 加载文档 | 上传/下载接口 |
| 页面 | `PDFPage`（句柄需释放） | viewer 渲染 | 服务端处理 |
| 释放 | `Library::Release()` / `Library.release()`（全部文档关闭后调用一次） | 销毁 viewer 实例 | 无 |

> 领域示例（Desktop C++ 生命周期、Web 异步/WASM 初始化、Mobile 句柄释放）见
> [`../skills/clarify-requirements/references/examples.md`](../skills/clarify-requirements/references/examples.md)；
> 领域风险与反例见 [`../skills/risk-identification/references/risk-examples.md`](../skills/risk-identification/references/risk-examples.md)
> 与 [`../skills/task-decomposition/references/antipatterns.md`](../skills/task-decomposition/references/antipatterns.md)。