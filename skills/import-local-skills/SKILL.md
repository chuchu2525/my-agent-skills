---
name: import-local-skills
description: >
  ローカルの ~/.agents/skills を読み取り、公開用リポジトリへ追加したい skill を対話的に選んで取り込むためのスキル。
  ユーザーが「ローカルの skills を公開用 repo に追加したい」「どの skill をコピーするか確認しながら取り込みたい」
  「~/.agents/skills から my-agent-skills に移したい」といった依頼をしたときに使うこと。
---

# Import Local Skills

## Purpose

Read local skills from `~/.agents/skills`, show the user which skills are available,
confirm which ones should be added to this repository, and then copy the selected
skill directories into `skills/`.

Use this skill when the user wants to:

- publish one or more local skills
- compare local skills with the public repository
- selectively import skills into this repository with confirmation

## Source and Destination

- Source: `~/.agents/skills`
- Destination: this repository's `skills/`

Always treat the local directory as the candidate source and this repository as the
publishable copy.

## Workflow

1. Run the listing script first:

```bash
python3 skills/import-local-skills/scripts/import_local_skills.py --list
```

2. Show the user:
   - which local skills exist
   - which ones are already present in this repository
   - which ones are importable

3. Ask the user which skills to add.

4. If a selected skill already exists in this repository, explicitly ask whether it
   should be overwritten.

5. Run the copy command with the confirmed selection:

```bash
python3 skills/import-local-skills/scripts/import_local_skills.py --copy <skill-name>...
```

If the user approved overwriting an existing skill, include `--overwrite`.

## Rules

- Copy the entire skill directory, not only `SKILL.md`
- Preserve bundled files such as `scripts/`, `references/`, `assets/`, `agents/`, and `evals/`
- Do not import this skill itself (`import-local-skills`) even if it exists locally
- Summarize what was copied and whether any selected skills were skipped

## Script Reference

The helper script supports:

- `--list`: inspect local skills and compare them with this repository
- `--copy <skill>...`: copy the selected skills into `skills/`
- `--overwrite`: allow replacing existing destination directories
- `--source <path>`: override the default source directory
- `--dest <path>`: override the default destination directory

Prefer the defaults unless the user explicitly asks to inspect another location.
