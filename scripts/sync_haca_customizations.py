#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parent.parent
SOURCE_ROOT = ROOT / ".github"

REQUIRED_HACA_SKILLS = {
    "clarify-requirements",
    "risk-identification",
    "task-decomposition",
    "tdd-loop",
    "evidence-gate",
    "commit-message-rules",
}

TARGET_GOVERNANCE = {
    ".cursor": ".cursor/haca-governance.md",
    ".opencode": ".opencode/AGENTS.md",
}

MANUAL_ADAPTERS = {
    ".cursor/AGENTS.md",
    ".cursor/rules/haca.mdc",
    ".opencode/agents/haca.agent.md",
    "opencode.json",
}

MANAGED_TARGET_ROOTS = {
    ".github/agents",
    ".github/copilot-instructions.md",
    ".github/prompts",
    ".github/scripts",
    ".github/skills",
    ".github/templates",
    ".cursor/agents",
    ".cursor/commands",
    ".cursor/haca-governance.md",
    ".cursor/scripts",
    ".cursor/skills",
    ".cursor/templates",
    ".opencode/AGENTS.md",
    ".opencode/agents",
    ".opencode/prompts",
    ".opencode/scripts",
    ".opencode/skills",
    ".opencode/templates",
}

TOOL_MAPPING_TEMPLATE_JSON = ROOT / "scripts/tool_mapping_template.json"

TARGET_PLATFORM_BY_PREFIX = {
    ".cursor": "cursor_agent",
    ".opencode": "opencode_agent",
}

ALLOWED_SYNC_SUFFIXES = {
    ".md",
    ".mdc",
}

ALLOWED_SKILL_SYNC_SUFFIXES = {
    ".md",
    ".mdc",
    ".py",
}

# These prompts are maintenance-only and target .github/ exclusively;
# they must not be synced to .cursor/commands/ or .opencode/prompts/.
EXCLUDED_PROMPT_FILES = {
    "haca-apply-spec.prompt.md",
    "haca-sync.prompt.md",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Sync HACA customization files from .github into the "
            "Cursor and OpenCode runtime directories."
        )
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Only verify whether generated files are up to date.",
    )
    return parser.parse_args()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def should_skip_source_file(path: Path, allowed_suffixes: set[str]) -> bool:
    if path.suffix.lower() not in allowed_suffixes:
        return True
    return False


def should_audit_managed_target_file(path: Path) -> bool:
    return path.suffix.lower() in ALLOWED_SYNC_SUFFIXES


def is_manual_adapter_path(path: Path) -> bool:
    try:
        relative_path = path.relative_to(ROOT).as_posix()
    except ValueError:
        return False
    return relative_path in MANUAL_ADAPTERS


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def split_frontmatter(content: str) -> tuple[dict[str, object], str]:
    if not content.startswith("---\n"):
        return {}, content

    end = content.find("\n---\n", 4)
    if end == -1:
        raise ValueError("Invalid frontmatter block")

    raw_frontmatter = content[4:end]
    body = content[end + 5 :]
    result: dict[str, object] = {}
    current_list_key: str | None = None

    for line in raw_frontmatter.splitlines():
        if not line.strip():
            continue

        if line.startswith("  - "):
            if current_list_key is None:
                raise ValueError("Unexpected list item in frontmatter")
            current_value = result.setdefault(current_list_key, [])
            if not isinstance(current_value, list):
                raise ValueError("List item attached to non-list frontmatter key")
            current_value.append(line[4:].strip())
            continue

        if ":" not in line:
            raise ValueError(f"Unsupported frontmatter line: {line}")

        key, raw_value = line.split(":", 1)
        key = key.strip()
        value = raw_value.strip()
        current_list_key = None

        if not value:
            result[key] = []
            current_list_key = key
            continue

        if value.startswith(('"', "'")) and value.endswith(('"', "'")):
            value = value[1:-1]
        result[key] = value

    return result, body


def render_frontmatter(entries: Iterable[tuple[str, object]]) -> str:
    lines = ["---"]

    for key, value in entries:
        if isinstance(value, list):
            lines.append(f"{key}:")
            for item in value:
                lines.append(f"  - {item}")
            continue

        lines.append(f'{key}: {quote_yaml_string(str(value))}')

    lines.append("---")
    lines.append("")
    return "\n".join(lines)


def quote_yaml_string(value: str) -> str:
    escaped = value.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def normalize_content(content: str) -> str:
    normalized = content.replace("\r\n", "\n")
    if not normalized.endswith("\n"):
        normalized += "\n"
    return normalized


def load_tool_mapping_template() -> dict[str, object]:
    if not TOOL_MAPPING_TEMPLATE_JSON.exists():
        return {}

    return json.loads(read_text(TOOL_MAPPING_TEMPLATE_JSON))


def extract_platform_tool_replacements() -> dict[str, dict[str, str]]:
    template = load_tool_mapping_template()
    replacements_by_platform: dict[str, dict[str, str]] = {}

    direct_replacements = template.get("name_replacements", {})
    if isinstance(direct_replacements, dict):
        for platform, mapping in direct_replacements.items():
            if not isinstance(platform, str) or not isinstance(mapping, dict):
                continue

            normalized_mapping: dict[str, str] = {}
            for old_name, new_name in mapping.items():
                if not isinstance(old_name, str) or not isinstance(new_name, str):
                    continue
                if old_name and new_name and old_name != new_name:
                    normalized_mapping[old_name] = new_name

            if normalized_mapping:
                replacements_by_platform[platform] = normalized_mapping

    capabilities = template.get("capabilities", [])
    if not isinstance(capabilities, list):
        return replacements_by_platform

    for capability in capabilities:
        if not isinstance(capability, dict):
            continue

        adapters = capability.get("adapters", {})
        if not isinstance(adapters, dict):
            continue

        source_adapter = adapters.get("github_copilot_vscode", {})
        if not isinstance(source_adapter, dict):
            continue

        source_names = source_adapter.get("names", [])
        if not isinstance(source_names, list):
            continue

        normalized_source_names = [name for name in source_names if isinstance(name, str) and name]
        if not normalized_source_names:
            continue

        for platform_key, adapter in adapters.items():
            if platform_key == "github_copilot_vscode" or not isinstance(platform_key, str):
                continue
            if not isinstance(adapter, dict):
                continue

            target_names = adapter.get("names", [])
            if not isinstance(target_names, list) or not target_names:
                continue

            primary_target = target_names[0]
            if not isinstance(primary_target, str) or not primary_target:
                continue

            platform_map = replacements_by_platform.setdefault(platform_key, {})
            for source_name in normalized_source_names:
                if source_name != primary_target:
                    platform_map.setdefault(source_name, primary_target)

    return replacements_by_platform


def replace_tool_names(content: str, target_prefix: str) -> str:
    platform = TARGET_PLATFORM_BY_PREFIX.get(target_prefix)
    if platform is None:
        return content

    replacements = extract_platform_tool_replacements().get(platform, {})
    if not replacements:
        return content

    transformed = content
    for source_name, target_name in sorted(replacements.items(), key=lambda item: len(item[0]), reverse=True):
        if source_name.startswith("#"):
            transformed = transformed.replace(source_name, target_name)
            continue

        escaped = re.escape(source_name)
        transformed = re.sub(rf"(?<![A-Za-z0-9_]){escaped}(?![A-Za-z0-9_])", target_name, transformed)

    return transformed


def replace_tool_list(tool_names: list[str], target_prefix: str) -> list[str]:
    platform = TARGET_PLATFORM_BY_PREFIX.get(target_prefix)
    if platform is None:
        return tool_names

    replacements = extract_platform_tool_replacements().get(platform, {})
    if not replacements:
        return tool_names

    return [replacements.get(name, name) for name in tool_names]


def transform_for_target(content: str, target_prefix: str) -> str:
    with_paths = replace_paths(content, target_prefix)
    return replace_tool_names(with_paths, target_prefix)


def replace_paths(content: str, target_prefix: str) -> str:
    replaced = content.replace(".github/", f"{target_prefix}/")
    if target_prefix in TARGET_GOVERNANCE:
        replaced = replaced.replace(
            f"{target_prefix}/copilot-instructions.md",
            TARGET_GOVERNANCE[target_prefix],
        )
    return replaced


def replace_cursor_prompt_inputs(content: str) -> str:
    lines: list[str] = []

    for line in content.splitlines():
        stripped = line.strip()
        if stripped.startswith("${input:") and stripped.endswith("}"):
            prompt_text = extract_input_prompt(stripped)
            lines.append(prompt_text)
            continue

        if "${input:" in line and line.rstrip().endswith("}"):
            prefix, raw_placeholder = line.split("${input:", 1)
            prompt_text = extract_input_prompt("${input:" + raw_placeholder)
            lines.append(f"{prefix}{prompt_text}")
            continue

        lines.append(line)

    return "\n".join(lines)


def extract_input_prompt(placeholder: str) -> str:
    default_prompt = "Please provide the required input."
    if not placeholder.startswith("${input:") or not placeholder.endswith("}"):
        return default_prompt

    payload = placeholder[len("${input:") : -1]
    separator_index = payload.find(":")
    if separator_index == -1:
        return default_prompt

    prompt_text = payload[separator_index + 1 :].strip()
    return prompt_text or default_prompt


def render_cursor_command_title(source_path: Path) -> str:
    step_token = source_path.stem.replace(".prompt", "")
    parts = step_token.split("-")
    if len(parts) == 2 and parts[0].lower() == "haca":
        suffix = parts[1]
        if suffix.startswith("step") and suffix[4:].isdigit():
            return f"HACA Step {suffix[4:]}"
    return step_token.replace("-", " ").upper()


def sync_governance(sync_state: SyncState) -> None:
    source_content = read_text(SOURCE_ROOT / "copilot-instructions.md")

    sync_state.record(
        ROOT / ".github/copilot-instructions.md",
        normalize_content(source_content),
    )

    for target_prefix, target_rel_path in TARGET_GOVERNANCE.items():
        rendered = normalize_content(transform_for_target(source_content, target_prefix))
        sync_state.record(ROOT / target_rel_path, rendered)


def sync_skills(sync_state: SyncState) -> None:
    sync_tree(
        source_dir=SOURCE_ROOT / "skills",
        targets={
            ROOT / ".github/skills": ".github",
            ROOT / ".cursor/skills": ".cursor",
            ROOT / ".opencode/skills": ".opencode",
        },
        sync_state=sync_state,
        allowed_suffixes=ALLOWED_SKILL_SYNC_SUFFIXES,
    )


def sync_scripts(sync_state: SyncState) -> None:
    sync_tree(
        source_dir=SOURCE_ROOT / "scripts",
        targets={
            ROOT / ".github/scripts": ".github",
            ROOT / ".cursor/scripts": ".cursor",
            ROOT / ".opencode/scripts": ".opencode",
        },
        sync_state=sync_state,
        binary_safe=False,
    )


def sync_templates(sync_state: SyncState) -> None:
    sync_tree(
        source_dir=SOURCE_ROOT / "templates",
        targets={
            ROOT / ".github/templates": ".github",
            ROOT / ".cursor/templates": ".cursor",
            ROOT / ".opencode/templates": ".opencode",
        },
        sync_state=sync_state,
    )


def sync_agents(sync_state: SyncState) -> None:
    for source_path in sorted((SOURCE_ROOT / "agents").glob("*.md")):
        frontmatter, body = split_frontmatter(read_text(source_path))
        github_content = normalize_content(body if frontmatter == {} else read_text(source_path))
        description = str(frontmatter.get("description", "")).strip()
        apply_to = str(frontmatter.get("applyTo", "manual")).strip()
        raw_tools = frontmatter.get("tools", [])
        tools = [item for item in raw_tools if isinstance(item, str)] if isinstance(raw_tools, list) else []

        sync_state.record(ROOT / ".github/agents" / source_path.name, github_content)

        cursor_content = render_frontmatter(
            [
                ("name", "haca"),
                ("description", description),
                ("applyTo", apply_to),
                ("tools", replace_tool_list(tools, ".cursor")),
                ("model", "inherit"),
            ]
        ) + normalize_content(transform_for_target(body.lstrip("\n"), ".cursor"))
        sync_state.record(ROOT / ".cursor/agents" / source_path.name, cursor_content)

        if source_path.name == "haca.agent.md":
            continue

        opencode_content = render_frontmatter(
            [
                ("name", str(frontmatter.get("name", "HACA"))),
                ("description", description),
                ("applyTo", apply_to),
                ("tools", replace_tool_list(tools, ".opencode")),
            ]
        ) + normalize_content(transform_for_target(body.lstrip("\n"), ".opencode"))
        sync_state.record(ROOT / ".opencode/agents" / source_path.name, opencode_content)


def _truthy_frontmatter(value: object) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in ("true", "1", "yes")


def sync_prompts(sync_state: SyncState) -> None:
    for source_path in sorted((SOURCE_ROOT / "prompts").glob("*.prompt.md")):
        source_content = normalize_content(read_text(source_path))
        frontmatter, body = split_frontmatter(read_text(source_path))
        description = str(frontmatter.get("description", "")).strip()
        preserve_github_paths = _truthy_frontmatter(
            frontmatter.get("preserve_github_paths", False)
        )

        sync_state.record(ROOT / ".github/prompts" / source_path.name, source_content)

        if source_path.name in EXCLUDED_PROMPT_FILES:
            continue

        body_stripped = body.lstrip("\n")
        if preserve_github_paths:
            opencode_body = body_stripped
            cursor_body_raw = body_stripped
        else:
            opencode_body = transform_for_target(body_stripped, ".opencode")
            cursor_body_raw = transform_for_target(body_stripped, ".cursor")

        opencode_content = render_frontmatter(
            [
                ("mode", "agent"),
                ("description", description),
            ]
        ) + normalize_content(opencode_body)
        sync_state.record(ROOT / ".opencode/prompts" / source_path.name, opencode_content)

        cursor_name = source_path.name.replace(".prompt", "")
        step_title = render_cursor_command_title(source_path)
        cursor_body = replace_cursor_prompt_inputs(cursor_body_raw)
        cursor_body = normalize_content(cursor_body)
        cursor_content = normalize_content(f"# {step_title}\n\n{cursor_body}")
        sync_state.record(ROOT / ".cursor/commands" / cursor_name, cursor_content)


def sync_tree(
    source_dir: Path,
    targets: dict[Path, str],
    sync_state: SyncState,
    binary_safe: bool = False,
    allowed_suffixes: set[str] = ALLOWED_SYNC_SUFFIXES,
) -> None:
    for source_path in sorted(source_dir.rglob("*")):
        if source_path.is_dir():
            continue
        if should_skip_source_file(source_path, allowed_suffixes):
            continue

        relative_path = source_path.relative_to(source_dir)
        source_content = read_text(source_path)

        for target_dir, target_prefix in targets.items():
            rendered = source_content if binary_safe else transform_for_target(source_content, target_prefix)
            sync_state.record(target_dir / relative_path, normalize_content(rendered))


class SyncState:
    def __init__(self, check_only: bool) -> None:
        self.check_only = check_only
        self.changed: list[Path] = []
        self.stale: list[Path] = []
        self.expected_managed_files: set[Path] = set()
        self.unexpected_managed_files: list[Path] = []

    def record(self, target_path: Path, content: str) -> None:
        self.expected_managed_files.add(target_path)

        if target_path.exists() and read_text(target_path) == content:
            return

        if self.check_only:
            self.stale.append(target_path)
            return

        write_text(target_path, content)
        self.changed.append(target_path)


def audit_managed_targets(sync_state: SyncState) -> None:
    for root in sorted(MANAGED_TARGET_ROOTS):
        root_path = ROOT / root
        if root_path.is_file():
            if (
                should_audit_managed_target_file(root_path)
                and root_path not in sync_state.expected_managed_files
                and not is_manual_adapter_path(root_path)
            ):
                sync_state.unexpected_managed_files.append(root_path)
            continue

        if not root_path.exists():
            continue

        for candidate in sorted(path for path in root_path.rglob("*") if path.is_file()):
            if not should_audit_managed_target_file(candidate):
                continue
            if is_manual_adapter_path(candidate):
                continue
            if candidate not in sync_state.expected_managed_files:
                sync_state.unexpected_managed_files.append(candidate)


def validate_configuration_boundaries() -> None:
    if not SOURCE_ROOT.exists():
        raise ValueError(f"Source root not found: {SOURCE_ROOT}")

    for skill_name in sorted(REQUIRED_HACA_SKILLS):
        skill_file = SOURCE_ROOT / "skills" / skill_name / "SKILL.md"
        if not skill_file.exists():
            raise ValueError(f"Required HACA skill missing: {skill_file}")

    for manual_path in MANUAL_ADAPTERS:
        if manual_path in MANAGED_TARGET_ROOTS:
            raise ValueError(f"Manual adapter overlaps managed target root: {manual_path}")


def main() -> int:
    args = parse_args()
    validate_configuration_boundaries()
    sync_state = SyncState(check_only=args.check)

    sync_governance(sync_state)
    sync_skills(sync_state)
    sync_scripts(sync_state)
    sync_templates(sync_state)
    sync_agents(sync_state)
    sync_prompts(sync_state)
    audit_managed_targets(sync_state)

    if args.check:
        if sync_state.stale:
            for path in sync_state.stale:
                print(path.relative_to(ROOT).as_posix())
            print(f"CHECK FAILED: {len(sync_state.stale)} stale file(s).")
            return 1
        if sync_state.unexpected_managed_files:
            for path in sync_state.unexpected_managed_files:
                print(path.relative_to(ROOT).as_posix())
            print(f"CHECK FAILED: {len(sync_state.unexpected_managed_files)} unexpected file(s).")
            return 1
        print("CHECK OK: no stale markdown targets.")
        return 0

    if sync_state.changed:
        for path in sync_state.changed:
            print(path.relative_to(ROOT).as_posix())
        print(f"SYNC UPDATED: {len(sync_state.changed)} file(s).")
    else:
        print("SYNC OK: no markdown changes.")

    if sync_state.unexpected_managed_files:
        for path in sync_state.unexpected_managed_files:
            print(path.relative_to(ROOT).as_posix())
        print(f"SYNC FAILED: {len(sync_state.unexpected_managed_files)} unexpected file(s).")
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())