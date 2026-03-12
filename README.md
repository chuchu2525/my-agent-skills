# my-agent-skills

## English

This repository stores publishable copies of my local agent skills.

The local source of truth is:

- `~/.agent/skills`

This repository is a curated copy for sharing and publishing.
Before publishing, review the local skills and copy only the content that is safe to share.

Current skills:

- `find-skills`
- `slide-reviewer`

Notes:

- Do not assume everything under `~/.agent` is safe to publish.
- Review each skill before copying it here.
- Keep private prompts, secrets, local paths, logs, and temporary files out of this repository.

Suggested workflow:

1. Edit skills locally under `~/.agent/skills`.
2. Review the contents for private or environment-specific information.
3. Copy the publishable version into this repository.
4. Commit and publish from this repository.

## 日本語

このリポジトリは、ローカルで使っている agent skills のうち、公開してよいものを置くためのリポジトリです。

ローカルの原本は以下です。

- `~/.agent/skills`

このリポジトリは共有・公開用のコピー置き場です。
公開前には `~/.agent` 側の内容を確認し、公開してよいものだけをここにコピーします。

現在入っている skills:

- `find-skills`
- `slide-reviewer`

注意:

- `~/.agent` 配下のすべてが公開向きとは限りません。
- コピー前に各 skill の内容を必ず見直してください。
- 秘匿情報、ローカル固有のパス、ログ、一時ファイルはこのリポジトリに含めないでください。

推奨フロー:

1. `~/.agent/skills` で skill を編集する
2. 秘匿情報や環境依存の内容がないか確認する
3. 公開してよい内容だけをこのリポジトリへコピーする
4. このリポジトリから commit / publish する

PR protection test note:

- Added a documentation-only change to verify `main` branch protection with `CODEOWNERS`.
