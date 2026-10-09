# Foxit SDK Reference Materials

This directory contains the Foxit SDK reference materials used by HACA-SDK Step 2 (Solution Design)
and Step 4 (SDK API correctness verification).

Each product subdirectory holds one or more **reference source files** extracted from the official
Foxit developer documentation. These files are verbatim extracts, not hand-edited summaries — see
[Sample style notes](#sample-style-notes) below.

## Directory Structure

```text
sdk-references/
├── README.md                                   # This file (directory-wide index)
├── sdk-matrix.md                               # SINGLE SOURCE OF TRUTH: product x platform x arch x language
├── foxit-sdk-config-schema.md                  # foxit-sdk.config.json schema reference
├── desktop/                                    # PDF SDK for Desktop
│   ├── README.md                               # Product index: file -> language -> covered topics
│   ├── GSDK_C__dcf1ba34.txt                    # C
│   ├── GSDK_C++__f8fe7687.txt                  # C++
│   ├── GSDK_C#__0399c0be.txt                   # C#
│   ├── GSDK_Java__508cc580.txt                 # Java
│   ├── GSDK_Python__503b7c42.txt               # Python
│   ├── GSDK_Javascript__abb8e7fc.txt           # Node.js (JavaScript)
│   └── GSDK_Objective-C__a1768bb5.txt          # Objective-C
├── mobile/                                     # PDF SDK for Mobile
│   ├── README.md
│   ├── RDK_Java__59c6b256.txt                  # Java (Android)
│   └── RDK_Objective-C__a86b7d84.txt           # Objective-C (iOS)
├── harmony/                                    # PDF SDK for Harmony
│   ├── README.md
│   └── RDK_ArkTS__d1718172.txt                 # ArkTS
├── web/                                        # PDF SDK for Web
│   ├── README.md
│   ├── WebSDK_Javascript__74dab367.txt         # JavaScript (Web SDK)
│   └── CollabAddonForWebSDK_Javascript__e2500d68.txt  # JavaScript (Collaboration Add-on)
├── cloud-api/                                  # Cloud API
│   ├── README.md
│   └── CloudAPI_Javascript__82ec1cfe.txt       # REST API (JavaScript examples)
└── conversion/                                 # Conversion SDK
    ├── README.md
    ├── ConversionSDK_C__b2be93fa.txt           # C
    ├── ConversionSDK_C++__4f6e672c.txt         # C++
    ├── ConversionSDK_C#__022fc064.txt          # C#
    ├── ConversionSDK_Java__183d1092.txt        # Java
    ├── ConversionSDK_Javascript__1809d3ab.txt  # Node.js (JavaScript)
    └── ConversionSDK_Python__51c1aa97.txt      # Python
```

## How to locate the right reference

1. Identify the Foxit SDK product from HACA Step 1 (see the single source of truth
   [`sdk-matrix.md`](./sdk-matrix.md)).
2. Open that product's `README.md` and use its **file -> language -> covered topics** index to pick
   the file for the target language and topic.
3. Read the matching section inside the `.txt` reference file. Search for the topic keyword (most
   desktop / mobile / web / conversion files are organized as a list of "How to ..." entries).

## Sample style notes

The `.txt` files are **verbatim extracts** from Foxit's official developer documentation and sample
repositories. They are intentionally not rewritten. When you consume them:

- **File naming**: `<ProductAbbrev>_<Language>__<hash>.txt`. The hash is a stable identifier from the
  extraction process; ignore it when referencing a file by content.
- **Style varies by product**: desktop / mobile / conversion files are "How to ..." question-answer
  collections; the Web / Cloud API / Harmony files are longer narrative guides or numbered tutorial
  lists. Do not assume a uniform heading structure across files.
- **Content is snippet-oriented**: most entries show a minimal code snippet, not a full runnable
  program. Treat them as API-usage references, not drop-in code.
- **Language conventions differ per file**: each file uses only its own language's API and naming
  conventions. Do not mix API names across languages.
- **Copyright**: these extracts are Foxit documentation content. Do not re-publish them outside this
  repository; use them only as in-context references for Step 2 design and Step 4 API verification.

## How to add or refresh reference materials

1. Add the new extract under the correct product subdirectory, named
   `<ProductAbbrev>_<Language>__<hash>.txt`.
2. Add a row to that product's `README.md` index table (file, language, covered topics).
3. Keep the extract verbatim; do not hand-edit or summarize it in place.

## Official documentation domains

Foxit maintains **two** official developer sites, and both are provided throughout the product
indexes and the governance layer:

| Domain | Language |
|--------|----------|
| `https://developers.foxitsoftware.cn/...` | English site |
| `https://developers.fuxinsoft.cn/...` | Chinese site (中文站) |

> Exception: Cloud API has a Chinese-only entry (`cloudapi.fuxinsoft.cn`); no English counterpart
> exists for it.

## Usage

- **Step 2 (Solution Design)** reads the relevant product index and reference file(s) to compare
  implementation options and identify risks.
- **Step 3 (Task Decomposition)** references the product capability matrix (single source:
  [`sdk-matrix.md`](./sdk-matrix.md)).
- **Step 4 (Build)** verifies SDK API correctness (class names, method signatures, parameter and
  return types) against the same reference file(s).

The accuracy of solution design and code directly depends on the content of this directory.
