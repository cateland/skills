#!/usr/bin/env python3
"""Validate the skills in this repository.

Checks:
1. SKILL.md frontmatter against the Agent Skills spec, via skills-ref 0.1.1,
   plus the spec rules that release does not enforce.
2. Relative Markdown links in each SKILL.md and its agents/ helper files.
3. skills/ directories match the ### `<name>` sections under "## Skills".

Python is used so this can call the skills-ref API and parse frontmatter with
strictyaml, which that package already installs.
"""

from __future__ import annotations

import re
import sys
from collections import Counter
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parent.parent
REQUIRED_SKILLS_REF = "0.1.1"

try:
    import strictyaml
    from skills_ref import validate
except ImportError:
    sys.stderr.write(
        "skills-ref=="
        + REQUIRED_SKILLS_REF
        + " is required.\n"
        + "Install it with: python -m pip install skills-ref=="
        + REQUIRED_SKILLS_REF
        + "\n"
    )
    raise SystemExit(1)


def require_pinned_skills_ref() -> None:
    try:
        found = version("skills-ref")
    except PackageNotFoundError:
        found = "not installed"
    if found != REQUIRED_SKILLS_REF:
        sys.stderr.write(
            f"skills-ref {REQUIRED_SKILLS_REF} is required, found {found}.\n"
        )
        raise SystemExit(1)


def skill_dirs() -> list[Path]:
    skills = ROOT / "skills"
    if not skills.is_dir():
        return []
    return sorted(path for path in skills.iterdir() if path.is_dir())


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def raw_frontmatter(text: str) -> dict | None:
    """Parse frontmatter without the string coercion skills-ref applies."""
    if not text.startswith("---"):
        return None
    parts = text.split("---", 2)
    if len(parts) < 3:
        return None
    try:
        data = strictyaml.load(parts[1]).data
    except strictyaml.YAMLError:
        return None
    if not isinstance(data, dict):
        return None
    return data


def frontmatter_gaps(data: dict) -> list[str]:
    """Spec rules that skills-ref 0.1.1 does not enforce."""
    errors: list[str] = []

    if "metadata" in data:
        meta = data["metadata"]
        if not isinstance(meta, dict):
            errors.append(
                "Field 'metadata' must be a map of string keys to string values"
            )
        else:
            for key, value in meta.items():
                if not isinstance(value, str):
                    errors.append(f"Field 'metadata.{key}' must be a string")

    if "allowed-tools" in data and not isinstance(data["allowed-tools"], str):
        errors.append("Field 'allowed-tools' must be a space-separated string")

    if "license" in data and not isinstance(data["license"], str):
        errors.append("Field 'license' must be a string")

    if "compatibility" in data:
        compatibility = data["compatibility"]
        if isinstance(compatibility, str) and len(compatibility) < 1:
            errors.append(
                "Field 'compatibility' must be 1-500 characters when provided"
            )

    return errors


def check_frontmatter(skill_dir: Path) -> list[str]:
    errors = [f"skills/{skill_dir.name}: {error}" for error in validate(skill_dir)]

    skill_md = skill_dir / "SKILL.md"
    if not skill_md.is_file():
        if (skill_dir / "skill.md").is_file():
            errors.append(
                f"skills/{skill_dir.name}: skill file must be named SKILL.md"
            )
            skill_md = skill_dir / "skill.md"
        else:
            return errors

    data = raw_frontmatter(read_text(skill_md))
    if data is None:
        return errors
    errors.extend(
        f"skills/{skill_dir.name}: {error}" for error in frontmatter_gaps(data)
    )
    return errors


def strip_fences(text: str) -> str:
    kept: list[str] = []
    fence_char = ""
    fence_len = 0
    for line in text.splitlines():
        marker = re.match(r"[ \t]{0,3}(`{3,}|~{3,})", line)
        if fence_char:
            if (
                marker
                and marker.group(1)[0] == fence_char
                and len(marker.group(1)) >= fence_len
                and line.strip() == marker.group(1)
            ):
                fence_char = ""
            continue
        if marker:
            fence_char = marker.group(1)[0]
            fence_len = len(marker.group(1))
            continue
        kept.append(line)
    return "\n".join(kept)


def read_destination(rest: str) -> str | None:
    rest = rest.lstrip(" \t")
    if not rest:
        return None
    if rest[0] == "<":
        end = rest.find(">")
        if end == -1:
            return None
        return rest[1:end].strip()
    end = 0
    while end < len(rest) and rest[end] not in " \t\r\n)":
        end += 1
    if end == 0:
        return None
    return rest[:end]


def link_destinations(text: str) -> list[str]:
    text = strip_fences(text)
    destinations: list[str] = []
    patterns = (
        r"!?\[[^\]\n]*\]\(",
        r"(?m)^[ \t]{0,3}\[[^\]\n]+\]:[ \t]*",
    )
    for pattern in patterns:
        for match in re.finditer(pattern, text):
            destination = read_destination(text[match.end() :])
            if destination:
                destinations.append(destination)
    for match in re.finditer(
        r"(?i)\b(?:href|src)\s*=\s*[\"']([^\"']+)[\"']", text
    ):
        destinations.append(match.group(1).strip())
    return destinations


def is_external(destination: str) -> bool:
    if destination.startswith("#") or destination.startswith("//"):
        return True
    return re.match(r"^[A-Za-z][A-Za-z0-9+.-]*:", destination) is not None


def check_links(skill_dir: Path) -> list[str]:
    files = []
    skill_md = skill_dir / "SKILL.md"
    if skill_md.is_file():
        files.append(skill_md)
    agents = skill_dir / "agents"
    if agents.is_dir():
        files.extend(sorted(path for path in agents.rglob("*") if path.is_file()))

    errors: list[str] = []
    root = ROOT.resolve()
    for path in files:
        location = path.relative_to(ROOT).as_posix()
        try:
            text = read_text(path)
        except UnicodeDecodeError:
            errors.append(f"{location}: is not UTF-8 text")
            continue
        for destination in link_destinations(text):
            if is_external(destination):
                continue
            raw_path = unquote(urlsplit(destination).path)
            if not raw_path:
                continue
            target = (path.parent / raw_path).resolve()
            try:
                target.relative_to(root)
            except ValueError:
                errors.append(
                    f"{location}: link '{destination}' resolves outside the repository"
                )
                continue
            if not target.is_file():
                errors.append(
                    f"{location}: link '{destination}' does not resolve to a file"
                )
    return errors


def readme_skill_names(text: str) -> tuple[list[str], str | None]:
    match = re.search(r"(?m)^## Skills[ \t]*$", text)
    if match is None:
        return [], 'README.md has no "## Skills" section'
    rest = text[match.end() :]
    next_heading = re.search(r"(?m)^## ", rest)
    section = rest[: next_heading.start()] if next_heading else rest
    return re.findall(r"(?m)^### `([^`]+)`[ \t]*$", section), None


def check_readme(dirs: list[Path]) -> list[str]:
    readme = ROOT / "README.md"
    if not readme.is_file():
        return ["README.md is missing"]
    names, section_error = readme_skill_names(read_text(readme))
    errors: list[str] = []
    if section_error:
        errors.append(section_error)

    folders = {path.name for path in dirs}
    listed = set(names)
    for name, count in Counter(names).items():
        if count > 1:
            errors.append(
                f'README.md has {count} "### `{name}`" sections under "## Skills"'
            )

    for name in sorted(folders - listed):
        errors.append(
            f'skills/{name}/ has no "### `{name}`" section under "## Skills"'
        )
    for name in sorted(listed - folders):
        errors.append(
            f'README.md section "### `{name}`" has no skills/{name}/ directory'
        )
    return errors


def report(title: str, errors: list[str]) -> None:
    print(title)
    if errors:
        for error in errors:
            print(f"  {error}")
    else:
        print("  ok")


def main() -> int:
    require_pinned_skills_ref()
    dirs = skill_dirs()
    frontmatter: list[str] = []
    links: list[str] = []
    if not (ROOT / "skills").is_dir():
        frontmatter.append("skills/ directory is missing")
    for skill_dir in dirs:
        frontmatter.extend(check_frontmatter(skill_dir))
        links.extend(check_links(skill_dir))
    readme = check_readme(dirs)

    report("Frontmatter", frontmatter)
    report("Links", links)
    report("README", readme)

    if frontmatter or links or readme:
        print("Validation failed.")
        return 1
    print("All checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
