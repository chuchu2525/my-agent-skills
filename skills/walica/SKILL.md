---
name: walica
description: >
  walica.jp でのグループ割り勘・精算管理をplaywright-cliで自動操作するskill。
  支出の追加・修正、メンバーの追加・確認をwalica.jpで行いたいときは必ずこのskillを使う。
  "walica"、"割り勘"、"精算"、"支出追加"、"支出修正"、"メンバー追加" などのキーワードが
  出たら即座にトリガーする。ユーザーがwalica.jpのURLを提示したときも必ずトリガーする。
compatibility:
  tools:
    - "@playwright/cli — npm install -g @playwright/cli@latest"
  permissions:
    - "Bash(playwright-cli*)"
    - "WebFetch(domain:walica.jp)"
---

# walica Playwright CLI Skill

`playwright-cli`（`@playwright/cli`）を使ってwalica.jpのグループページを操作する。
対応操作：支出の追加・修正、メンバーの管理。

## セットアップ

### 1. インストール確認

```bash
playwright-cli --version
```

インストールされていない場合：
```bash
npm install -g @playwright/cli@latest
```

### 2. Claude の権限設定

このskillを使うプロジェクトの `.claude/settings.local.json` に以下を追加する：

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

## URLの管理

ユーザーとのやりとりでグループURLを `WALICA_GROUP_URL` として管理する。

**URLを受け取ったとき：**
- `https://walica.jp/group/...` が来たら `WALICA_GROUP_URL` として記憶し「このグループで操作します」と確認する

**次回以降：**
- 操作前に「グループ: `[URL]` でよいですか？」と確認する
- 依頼内容が以前と明らかに異なるグループ（別の旅行・別のグループ名）なら新たにURLを求める

**URLがない場合：**
- 記憶済みURLがあれば「前回の `[URL]` を使いますか？」と提案する
- まったく初めての場合は「walica.jpのグループURLを教えてください」と聞く

## 実行モードの確認

操作実行前に確認する：
- **ブラウザ表示あり（headed）**: `playwright-cli -s=walica --headed open [url]`
- **バックグラウンド（headless）**: `playwright-cli -s=walica open [url]`（デフォルト）

ユーザーが「見たい」「確認したい」「表示して」と言っていれば headed で開く。

## 基本操作パターン

### セッションの開き方

```bash
# 新規セッション（headless）
playwright-cli -s=walica open "[WALICA_GROUP_URL]"

# ブラウザ表示あり
playwright-cli -s=walica --headed open "[WALICA_GROUP_URL]"

# セッションが既にある場合（再利用）
playwright-cli -s=walica goto "[WALICA_GROUP_URL]"
```

### 広告を閉じる（必ず最初に行う）

ページを開いたら広告が表示されることがある。操作前に閉じる：
```bash
playwright-cli -s=walica click "Close advertisement"
```
広告が出ていない場合はエラーになるが無視してよい。

### ページ状態の確認（snapshot）

操作前後にスナップショットで要素を確認する。snapshotの結果には `[ref=eXX]` という参照IDが含まれ、これを `fill` や `click` に使える：
```bash
playwright-cli -s=walica snapshot
```

---

## メンバー管理

### メンバー一覧を確認する

```bash
# グループページのメンバー表示で確認（snapshotに含まれる）
playwright-cli -s=walica goto "[WALICA_GROUP_URL]"
playwright-cli -s=walica snapshot
# → text: あおい・あかり・ゆうき... のように表示される
```

### メンバーを追加する

複数人でも一度に追加できる。編集ページ（`/edit`）でテキストボックスに入力→「追加」を繰り返し、最後に「更新」で保存する：

```bash
# 1. 編集ページへ移動
playwright-cli -s=walica goto "[WALICA_GROUP_URL]/edit"

# 2. 広告を閉じる（念のため）
playwright-cli -s=walica click "Close advertisement"

# 3. メンバーを1人ずつ追加（テキストボックスに入力 → 「追加」クリックを繰り返す）
playwright-cli -s=walica fill "メンバー名テキストボックスのref" "名前1"
playwright-cli -s=walica click "追加"
playwright-cli -s=walica fill "メンバー名テキストボックスのref" "名前2"
playwright-cli -s=walica click "追加"
# ...

# 4. 全員追加したら「更新」で保存
playwright-cli -s=walica click "更新"
```

**メンバー名テキストボックスのrefを特定するには：**
`playwright-cli -s=walica snapshot` を実行し、`textbox` のrefを確認する。
例：`textbox "あおい" [ref=e80]` → `e80` がref。

**複数人を一括追加する場合のシェルループ：**
```bash
for name in 名前1 名前2 名前3; do
  playwright-cli -s=walica fill e80 "$name"
  playwright-cli -s=walica click "追加"
done
playwright-cli -s=walica click "更新"
```

### メンバーを削除する

編集ページでメンバー名の横にある削除ボタン（×アイコン）をクリックする：
```bash
playwright-cli -s=walica goto "[WALICA_GROUP_URL]/edit"
playwright-cli -s=walica snapshot
# → 削除したいメンバーの横のimgボタンのrefを確認して click
playwright-cli -s=walica click "[削除ボタンのref]"
playwright-cli -s=walica click "更新"
```

---

## 支出（立て替え）管理

### 支出一覧を確認する

```bash
playwright-cli -s=walica goto "[WALICA_GROUP_URL]"
playwright-cli -s=walica snapshot
# → 支出一覧が表示される
```

### 支出を追加する

ユーザーから以下の情報を収集してから実行する：
- 支出名（例：夕食、コンビニ）
- 金額（円）
- 支払者（誰が払ったか）
- 参加者（割り勘する人たち）

```bash
# 1. 「立て替えを追加」ボタンをクリック
playwright-cli -s=walica click "立て替えを追加"

# 2. フォームをsnapshotで確認
playwright-cli -s=walica snapshot

# 3. snapshotで得たrefを使ってフォームに入力
playwright-cli -s=walica fill "[支出名フィールドのref]" "夕食"
playwright-cli -s=walica fill "[金額フィールドのref]" "3000"

# 4. 支払者を選択（snapshotで確認してからクリック）
playwright-cli -s=walica click "[支払者のref]"

# 5. 参加者のチェックボックスを操作（snapshotで確認）
playwright-cli -s=walica check "[参加者チェックボックスのref]"

# 6. 保存
playwright-cli -s=walica click "[保存ボタンのref]"
```

**重要**: 支出追加フォームは実際に開いてみるまで要素が不明なため、必ず `snapshot` で確認してからrefを使う。

### 支出を修正する

```bash
# 1. 支出一覧をsnapshotで確認
playwright-cli -s=walica goto "[WALICA_GROUP_URL]"
playwright-cli -s=walica snapshot

# 2. 対象の支出をクリック
playwright-cli -s=walica click "[対象支出のref]"

# 3. 編集フォームをsnapshotで確認
playwright-cli -s=walica snapshot

# 4. 変更内容を入力・保存
playwright-cli -s=walica fill "[金額フィールドのref]" "新しい金額"
playwright-cli -s=walica click "[保存ボタンのref]"
```

---

## エラー時の対処

- **要素が見つからない**: `playwright-cli -s=walica snapshot` で現在の状態を確認する
- **クリックできない（overlay interception）**: 広告が残っていないか確認し `click "Close advertisement"` を試す
- **スクリーンショットで視覚確認**: `playwright-cli -s=walica screenshot walica_debug.png`
- **セッションが固まった**: `playwright-cli kill-all` でリセットして再度 `open` する
