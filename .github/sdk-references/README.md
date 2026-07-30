# Foxit SDK Reference Materials

This directory contains reference materials for each Foxit SDK product, used by HACA-SDK Step 2 (Solution Design).

## Directory Structure

```
sdk-references/
├── README.md                          # This file
├── foxit-sdk-config-schema.md         # SDK configuration file format reference
├── desktop/                           # PDF SDK for Desktop reference materials
│   ├── api-summary.md                 # API documentation summary
│   ├── capability-matrix.md           # Feature capability matrix
│   └── code-samples/                  # Sample code templates
├── mobile/                            # PDF SDK for Mobile reference materials
│   ├── android/
│   └── ios/
├── harmony/                           # PDF SDK for Harmony reference materials
├── web/                               # PDF SDK for Web reference materials
├── cloud-api/                         # Cloud API reference materials
│   ├── embed-viewer-api/
│   └── pdf-services-api/
└── conversion/                        # Conversion SDK reference materials
```

## How to Add Reference Materials

1. Place API documentation summaries in `api-summary.md` under the corresponding product subdirectory.
2. Place feature capability matrices in `capability-matrix.md`.
3. Place sample code in the `code-samples/` subdirectory, organized by language.

## Usage

HACA-SDK Step 2 (Solution Design) automatically reads reference materials from this directory to provide optimal solutions. The quality and accuracy of solution design directly depends on the content here.
