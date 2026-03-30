# my-agent-skills

## Caution

**Please use this repository at your own risk. You are responsible for evaluating and judging any security risks or other potential issues associated with using these skills.**

This repository stores publishable copies of my local agent skills.

The local source of truth is:

- `~/.agents/skills`

This repository is a curated copy for sharing and publishing.
Before publishing, review the local skills and copy only the content that is safe to share.

See the `skills/` directory for the full list of available skills.
For example:

- `import-local-skills` — copy local skills into this repository
- `slide-reviewer` — review business presentation slides

Notes:

- Do not assume everything under `~/.agents` is safe to publish.
- Review each skill before copying it here.
- Keep private prompts, secrets, local paths, logs, and temporary files out of this repository.

Suggested workflow:

1. Edit skills locally under `~/.agents/skills`.
2. Review the contents for private or environment-specific information.
3. Copy the publishable version into this repository.
4. Commit and publish from this repository.

### Importing local skills into this repository

Use `import-local-skills` when you want to inspect local skills under `~/.agents/skills`
and selectively copy them into this repository.

List candidates:

```bash
python3 skills/import-local-skills/scripts/import_local_skills.py --list
```

Copy selected skills:

```bash
python3 skills/import-local-skills/scripts/import_local_skills.py --copy slides walica
```

Overwrite existing copied skills only after confirmation:

```bash
python3 skills/import-local-skills/scripts/import_local_skills.py --copy find-skills --overwrite
```
