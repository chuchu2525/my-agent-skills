# walica skill

[walica.jp](https://walica.jp) のグループページを AI エージェントから自然言語で操作するスキル。
`playwright-cli` を使ってブラウザを自動操作し、支出の追加・修正やメンバー管理を行う。

## 対応エージェント

| エージェント | 認識方式 |
|---|---|
| **Claude Code** (`claude`) | `~/.claude/skills/` 以下の SKILL.md を自動認識 |
| **OpenAI Codex CLI** (`@openai/codex`) | プロジェクトの `AGENTS.md` から SKILL.md を参照 |

---

## セットアップ

### playwright-cli のインストール（共通）

```bash
npm install -g @playwright/cli@latest
playwright-cli --version  # 確認
```

---

### Claude Code の場合

**インストール確認**
```bash
claude --version
```

**権限設定**

プロジェクトの `.claude/settings.local.json` に追加する：

```json
{
  "permissions": {
    "allow": [
      "Bash(playwright-cli*)",
      "WebFetch(domain:walica.jp)"
    ]
  }
}
```

**スキルの配置**

このディレクトリを `~/.agents/skills/walica/` に配置する。
`~/.claude/skills/` が `~/.agents/skills/` のシムリンクになっていれば自動認識される。

---

### Codex CLI の場合

**インストール確認**
```bash
codex --version
```

**権限設定**

プロジェクトの `.codex/config.toml` に追加する：

```toml
[[rules]]
pattern = "^playwright-cli"
decision = "allow"
justification = "walica skill による walica.jp のブラウザ自動操作"
```

> Codex CLI のルールはプロジェクトルートの `.codex/config.toml`（プロジェクト単位）または
> `~/.codex/config.toml`（グローバル）に記述する。
> パターンは正規表現プレフィックスで、`^playwright-cli` は `playwright-cli` で始まる全コマンドに一致する。

**SKILL.md の参照**

プロジェクトルートに `AGENTS.md` を作成し、SKILL.md のパスを記述する：

```markdown
# Agent Instructions

## walica skill
@~/.agents/skills/walica/SKILL.md
```

---

## 対応操作

| 操作 | 内容 |
|------|------|
| メンバー管理 | メンバーの追加・削除・一覧確認 |
| 支出を追加 | 立て替え金額・支払者・参加者を登録 |
| 支出を修正 | 既存の支出の金額・支払者などを変更 |

## 使い方

自然言語で指示するだけでよい。

```
walicaのグループに山田さんを追加して
https://walica.jp/group/XXXXX

walicaに昨日の夕食代3000円を追加して。払ったのは田中さん、参加者は全員。

walicaのコンビニの金額を600円に修正して
```

グループURLを一度伝えると次回から確認しながら使い回してくれる。
ブラウザを表示したい場合は「ブラウザ表示して」と伝える。

---

## スクリプト埋め込みに関するリスク

このスキルは `playwright-cli` コマンドをエージェントが直接生成・実行する方式を採用しており、
`scripts/` ディレクトリにスクリプトを事前に埋め込む方式は**意図的に採用していない**。

スキルにスクリプトを埋め込む場合、以下のリスクがある：

- **任意コード実行**: スクリプトファイルはエージェントが自動的に実行するため、スキルを配布・共有する際に悪意のあるコードが混入するリスクがある
- **レビューの困難さ**: SKILL.md 本文に記載されたコマンドは人間が読んで確認できるが、スクリプトファイルはスキルインストール時に見落としやすい
- **更新時の検証漏れ**: スキルをアップデートした際、スクリプトファイルの変更が見逃されやすい

同様のリスクは Codex CLI の `.codex/rules/` ファイルにも存在する。
スキルを配布・受け取る際は、`SKILL.md` 本文だけでなく同梱の設定ファイルや
スクリプトの内容も必ず確認すること。

このスキルのように外部サービスを操作する用途では、**実行するコマンドを SKILL.md に明示し、
エージェントがその都度生成・確認できる形式**にしておくことが望ましい。

---

## ファイル構成

```
walica/
├── SKILL.md        # エージェントが読む操作手順（playwright-cli コマンド集）
├── README.md       # このファイル
└── evals/
    └── evals.json  # テストケース
```
