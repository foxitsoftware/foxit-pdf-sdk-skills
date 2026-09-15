# PDF SDK for Web — 参考资料

此目录存放 PDF SDK for Web 的官方文档抽取参考文件，供 HACA-SDK Step 2（方案设计）与
Step 4（SDK API 正确性校验）使用。文件为原始抽取内容，不做改写。

## 文件 → 语言 → 覆盖主题

| 文件 | 语言 | 主题条数 | 覆盖主题 |
|------|------|----------|----------|
| `WebSDK_Javascript__74dab367.txt` | JavaScript（Web SDK） | 164 | 注释与标注、表单、签名与验签、加解密与权限、渲染/打印、页面组织、文本搜索与替换、格式转换、OCR 与版面识别、元数据 |
| `CollabAddonForWebSDK_Javascript__e2500d68.txt` | JavaScript（协作插件） | — | 协作会话、消息/事件、认证、ScreenSync 屏幕同步、协作服务器配置 |

> Web SDK 文件为编号式 “1. How to …” 列表 + JS 代码；协作插件文件为 Markdown 标题式
> “## How to …” 小节 + JS 代码。

## 样例风格注意事项

- **内容为抽取原文**：不修改、不摘要；示例多为最小代码片段，非完整可运行程序。
- **占位值**：部分示例含占位参数（如序列号/密钥等），需替换为真实值后再运行。
- **仅限本语言 API**：Web 侧统一使用 JavaScript/TypeScript API，请勿混用服务端语言 API。
- **浏览器环境假设**：Web SDK 示例默认运行在现代浏览器中，需要 DOM 元素承载 PDF 阅读器。

## 产品概述

福昕 PDF SDK 网页版是一款高性能的轻量级库，可无缝集成于现代前端框架。仅需一个 DOM 元素，即可为应用嵌入功能强大的 PDF 阅读器。

### 功能亮点

- 高性能跨平台 PDF 渲染（无需插件）
- 深度编辑：页面管理、内容编辑
- 高级协作：批注释义、导入导出
- 智能表单与签名
- 安全可控：水印、密文擦除、DRM、密码加密

### 支持环境

| 平台 | 语言 |
|------|------|
| 浏览器 | JavaScript / TypeScript |

产品介绍（英文站）: https://developers.foxitsoftware.cn/pdfsdk-web/
产品介绍（中文站）: https://developers.fuxinsoft.cn/pdfsdk-web/
