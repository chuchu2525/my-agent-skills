---
name: ft-sync-diff
description: Field Theory CLIでXブックマークを同期し、bookmarks.jsonl の前後比較で新規ブックマーク差分を検知して、次アクションを確認する。ft sync、差分確認、new_ids.txt 作成、説明Markdown作成前の入口、Obsidian連携の開始時に使う。
---

# FT Sync Diff

## 目的

`ft sync` の定期運用で、新規ブックマークだけを安定して抽出する。

## 前提

- `fieldtheory-cli` が使える状態である
- `FT_DATA_DIR` を本番保存先に固定している
- Chrome で x.com にログイン済み

## コマンド方針

- 基本は `ft ...` を使う
- `ft` が未インストール、またはローカル clone の固定版を明示的に使いたい場合だけ `node bin/ft.mjs ...` を使う

違いは次の通り。

- `ft sync`
  - PATH 上の `ft` コマンドを呼ぶ
  - 普段の運用向き
  - グローバルインストールやシェル設定が済んでいる前提
- `node bin/ft.mjs sync`
  - その clone 内の `bin/ft.mjs` を直接実行する
  - まだ `ft` を入れていない段階や、特定 clone の版を固定して試したいとき向き
  - ローカルリポジトリの `dist/` が必要

## 実行フロー

1. データ保存先を確認する。

```bash
echo "$FT_DATA_DIR"
ft path
```

2. 同期前のIDスナップショットを保存する。

```bash
mkdir -p .cache
python - <<'PY'
import json, pathlib
data_dir = pathlib.Path.home() / "Documents/obsidian/obsidian/ft-bookmarks"
src = data_dir / "bookmarks.jsonl"
dst = pathlib.Path(".cache/before_ids.txt")
ids = []
if src.exists():
    for line in src.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
            if obj.get("id"):
                ids.append(str(obj["id"]))
        except Exception:
            pass
dst.write_text("\n".join(sorted(set(ids))), encoding="utf-8")
print(f"saved_before={len(set(ids))}")
PY
```

3. 同期を実行する。

```bash
ft sync
```

4. 同期後スナップショットを作って差分を計算する。

```bash
python - <<'PY'
import json, pathlib
data_dir = pathlib.Path.home() / "Documents/obsidian/obsidian/ft-bookmarks"
src = data_dir / "bookmarks.jsonl"
after = pathlib.Path(".cache/after_ids.txt")
newf = pathlib.Path(".cache/new_ids.txt")
ids = []
if src.exists():
    for line in src.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
            if obj.get("id"):
                ids.append(str(obj["id"]))
        except Exception:
            pass
after_ids = sorted(set(ids))
after.write_text("\n".join(after_ids), encoding="utf-8")
before_ids = set(pathlib.Path(".cache/before_ids.txt").read_text(encoding="utf-8").splitlines()) if pathlib.Path(".cache/before_ids.txt").exists() else set()
new_ids = [i for i in after_ids if i not in before_ids]
newf.write_text("\n".join(new_ids), encoding="utf-8")
print(f"new_count={len(new_ids)}")
for i in new_ids[:20]:
    print(i)
PY
```

## 出力物

- `.cache/before_ids.txt`: 同期前ID一覧
- `.cache/after_ids.txt`: 同期後ID一覧
- `.cache/new_ids.txt`: 新規ID一覧

## 差分があったときの対話フロー

`new_count=0` なら、「新規ブックマークはなし」とだけ短く伝える。

`new_count>0` なら、次をまとめて提示する。

- 新規件数
- 先頭数件のID
- `.cache/new_ids.txt` の保存先

そのうえで、次に何をしたいかを必ず確認する。既定のおすすめは「説明の Markdown を作る」。
確認項目は次のいずれか。

1. おすすめ: 説明の Markdown を作りたい
2. その内容をもとに自分で実践してみたい
3. いまは差分だけ確認したい

対話例:

```text
新規ブックマークが 12 件あります。
差分IDは `.cache/new_ids.txt` に保存しました。

次に何をしますか？
1. おすすめ: 説明のMarkdownを作る
2. この差分をもとに自分で実践する
3. いまは差分確認だけにする
```

エージェントが `AskQuestion` を使える場合は、それを優先して 3 択で聞く。
使えない場合は通常の会話で同じ 3 択を聞く。

## 失敗時の確認ポイント

- `Could not read Chrome Cookies database` が出る場合
  - Chrome を完全終了して再実行
- `No ct0 CSRF cookie found` が出る場合
  - Chrome 側で x.com ログインを確認
- 保存先が想定と違う場合
  - `echo $FT_DATA_DIR` と `ft path` を再確認

## セキュリティ注意

- `bookmarks.jsonl` と `bookmarks.db` は GitHub に直接コミットしない
- Cookie/Token をCIや外部実行環境に渡さない

## 次の拡張

- `.cache/new_ids.txt` を入力にして MD 自動生成
- 生成ノートのみを git add/commit/push
