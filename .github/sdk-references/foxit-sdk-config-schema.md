# Foxit SDK Configuration File Format (`foxit-sdk.config.json`)

Users can place `foxit-sdk.config.json` in the project root to pre-specify the SDK product, platform, architecture, and language, avoiding repeated confirmation on every interaction.

## Configuration File Format

```json
{
  "product": "<product name>",
  "platform": "<target platform>",
  "architecture": "<CPU architecture>",
  "language": "<programming language>",
  "sdk_version": "<SDK version number>",
  "license_key_env": "<environment variable name>",
  "sdk_path": "<SDK installation path>",
  "additional_modules": ["<optional module list>"]
}
```

## Field Descriptions

| Field | Required | Description | Accepted Values |
|-------|----------|-------------|----------------|
| `product` | ✅ | Foxit SDK product name | `desktop`, `mobile`, `harmony`, `web`, `cloud-api`, `conversion` |
| `platform` | ✅ | Target runtime platform | `windows`, `linux`, `macos`, `android`, `ios`, `harmonyos-next`, `openharmony`, `browser` |
| `architecture` | ⬜ | CPU architecture (desktop/server/mobile) | `x86`, `x86_64`, `armv7`, `armv8`, `arm64` |
| `language` | ✅ | Development language | `cpp`, `python`, `java`, `nodejs`, `csharp`, `c`, `go`, `objc`, `swift`, `arkts`, `javascript`, `typescript` |
| `sdk_version` | ⬜ | SDK version number | e.g. `10.1`, `9.8` |
| `license_key_env` | ⬜ | Environment variable name holding the License Key | e.g. `FOXIT_SDK_KEY` |
| `sdk_path` | ⬜ | Installation path for SDK library files | file system path |
| `additional_modules` | ⬜ | Additional SDK modules required | e.g. `["ocr", "conversion", "comparison"]` |

## Valid Configuration Combinations per Product

### PDF SDK for Desktop

```json
{
  "product": "desktop",
  "platform": "windows | linux | macos",
  "architecture": "x86 | x86_64 | armv7 | armv8 | arm64",
  "language": "cpp | python | java | nodejs | csharp | c | go | objc"
}
```

> Note: `c` language is only supported on `windows` platform; `objc` is only supported on `macos` platform.

### PDF SDK for Mobile

```json
{
  "product": "mobile",
  "platform": "android | ios",
  "language": "java | objc | swift"
}
```

> Note: Android only supports `java`; iOS supports `objc` and `swift`.

### PDF SDK for Harmony

```json
{
  "product": "harmony",
  "platform": "harmonyos-next | openharmony",
  "language": "arkts"
}
```

### PDF SDK for Web

```json
{
  "product": "web",
  "platform": "browser",
  "language": "javascript | typescript"
}
```

### Cloud API

```json
{
  "product": "cloud-api",
  "platform": "browser",
  "language": "javascript | typescript | python | java | csharp | nodejs"
}
```

> Cloud API is a REST API; the calling-side language is not restricted. The above lists only the most common languages.

### Conversion SDK

```json
{
  "product": "conversion",
  "platform": "windows | linux",
  "architecture": "x86 | x86_64 | armv7 | armv8",
  "language": "cpp | python | java | nodejs | csharp | c | go"
}
```

## Example Configurations

### Windows C++ Desktop Development

```json
{
  "product": "desktop",
  "platform": "windows",
  "architecture": "x86_64",
  "language": "cpp",
  "sdk_version": "10.1",
  "license_key_env": "FOXIT_SDK_KEY",
  "sdk_path": "C:/FoxitSDK/lib"
}
```

### Android Mobile Development

```json
{
  "product": "mobile",
  "platform": "android",
  "language": "java",
  "sdk_version": "10.1"
}
```

### HarmonyOS Next Development

```json
{
  "product": "harmony",
  "platform": "harmonyos-next",
  "language": "arkts",
  "sdk_version": "10.1"
}
```
