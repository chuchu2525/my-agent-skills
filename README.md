# my-agent-skills

## 注意点

**このリポジトリは自己責任で活用してください。セキュリティリスクやその他の潜在的な問題については、ご自身で評価・判断してください。**

このリポジトリは、ローカルで使っている agent skills のうち、公開してよいものを置くためのリポジトリです。

ローカルの原本は以下です。

- `~/.agents/skills`

このリポジトリは共有・公開用のコピー置き場です。
公開前には `~/.agents` 側の内容を確認し、公開してよいものだけをここにコピーします。

現在入っている skills:

- `find-skills`
- `import-local-skills`
- `slide-reviewer`

注意:

- `~/.agents` 配下のすべてが公開向きとは限りません。
- コピー前に各 skill の内容を必ず見直してください。
- 秘匿情報、ローカル固有のパス、ログ、一時ファイルはこのリポジトリに含めないでください。

推奨フロー:

1. `~/.agents/skills` で skill を編集する
2. 秘匿情報や環境依存の内容がないか確認する
3. 公開してよい内容だけをこのリポジトリへコピーする
4. このリポジトリから commit / publish する

### ローカル skill をこのリポジトリへ取り込む

`import-local-skills` を使うと、`~/.agents/skills` にあるローカル skill を見て、
どれをこのリポジトリに追加するか確認しながら取り込めます。

候補一覧を見る:

```bash
python3 skills/import-local-skills/scripts/import_local_skills.py --list
```

選んだ skill をコピーする:

```bash
python3 skills/import-local-skills/scripts/import_local_skills.py --copy slides walica
```

既存 skill を上書きする場合:

```bash
python3 skills/import-local-skills/scripts/import_local_skills.py --copy find-skills --overwrite
```
