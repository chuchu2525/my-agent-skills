#!/usr/bin/env python3
from __future__ import annotations

import argparse
import shutil
import sys
from dataclasses import dataclass
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_SOURCE = Path.home() / ".agents" / "skills"
DEFAULT_DEST = REPO_ROOT / "skills"
SELF_SKILL_NAME = "import-local-skills"


@dataclass
class SkillEntry:
    name: str
    source_path: Path
    dest_path: Path

    @property
    def exists_in_dest(self) -> bool:
        return self.dest_path.exists()


def collect_skill_entries(source_dir: Path, dest_dir: Path) -> list[SkillEntry]:
    if not source_dir.exists():
        raise FileNotFoundError(f"Source directory not found: {source_dir}")
    if not source_dir.is_dir():
        raise NotADirectoryError(f"Source path is not a directory: {source_dir}")

    entries: list[SkillEntry] = []
    for child in sorted(source_dir.iterdir(), key=lambda path: path.name):
        if not child.is_dir():
            continue
        if child.name == SELF_SKILL_NAME:
            continue
        entries.append(
            SkillEntry(
                name=child.name,
                source_path=child,
                dest_path=dest_dir / child.name,
            )
        )
    return entries


def print_entries(entries: list[SkillEntry], source_dir: Path, dest_dir: Path) -> None:
    print(f"Source: {source_dir}")
    print(f"Destination: {dest_dir}")
    print("")

    if not entries:
        print("No local skills were found.")
        return

    print("Local skills:")
    for entry in entries:
        status = "already in repo" if entry.exists_in_dest else "ready to import"
        print(f"- {entry.name} [{status}]")


def copy_skill(entry: SkillEntry, overwrite: bool) -> str:
    if entry.exists_in_dest:
        if not overwrite:
            return f"skipped {entry.name}: destination already exists"
        shutil.rmtree(entry.dest_path)

    shutil.copytree(entry.source_path, entry.dest_path)
    return f"copied {entry.name} -> {entry.dest_path}"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Inspect local ~/.agents/skills and copy selected skills into this repository."
    )
    parser.add_argument("--list", action="store_true", help="List local skills and compare with destination")
    parser.add_argument("--copy", nargs="+", metavar="SKILL", help="Copy one or more skills by name")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite existing destination skills")
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE, help="Source skills directory")
    parser.add_argument("--dest", type=Path, default=DEFAULT_DEST, help="Destination skills directory")
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    if not args.list and not args.copy:
        print("Specify --list or --copy.", file=sys.stderr)
        return 2

    try:
        entries = collect_skill_entries(args.source, args.dest)
    except (FileNotFoundError, NotADirectoryError) as exc:
        print(str(exc), file=sys.stderr)
        return 1

    entry_by_name = {entry.name: entry for entry in entries}

    if args.list:
        print_entries(entries, args.source, args.dest)

    if args.copy:
        args.dest.mkdir(parents=True, exist_ok=True)
        requested = []
        for skill_name in args.copy:
            if skill_name == SELF_SKILL_NAME:
                print(f"skipped {skill_name}: self-import is not allowed")
                continue
            entry = entry_by_name.get(skill_name)
            if entry is None:
                print(f"skipped {skill_name}: not found in source")
                continue
            requested.append(entry)

        for entry in requested:
            print(copy_skill(entry, overwrite=args.overwrite))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
