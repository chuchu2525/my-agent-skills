---
name: ft-explain-bookmarks
description: Xブックマーク差分から説明Markdownを生成する。new_ids.txt、bookmarks.jsonl、関連ブックマーク探索、Web調査、Obsidianノート化を行うときに使う。
---

# FT Explain Bookmarks

## 目的

差分に含まれる新規ブックマークを、あとで読み返せる知識ノートに変換する。

## 使うタイミング

- `ft-sync-diff` で差分が見つかったあと
- ユーザーが「おすすめ: 説明の Markdown を作る」を選んだとき

## 前提

- `.cache/new_ids.txt` が存在する
- `FT_DATA_DIR` が正しく設定されている
- `bookmarks.jsonl` を読める
- 出力先は vault 配下の `x-bookmarks/` を使う
- private ノート前提で作る

## 入力

1. `.cache/new_ids.txt`
2. `$FT_DATA_DIR/bookmarks.jsonl`
3. 必要に応じて `ft search`
4. 必要に応じて `WebSearch`

## 出力

- 1件ごと: `x-bookmarks/items/x-{tweetId}.md`
- まとめ: `x-bookmarks/batches/batch-{YYYY-MM-DD}-{HHmm}.md`

既定では、1件ごとのMDとまとめMDを両方作る。

## ファイル名規則

- 1件ごと: `x-{tweetId}.md`
  - tweet ID は一意で安定しているので、タイトルが変わってもファイル名を変えなくてよい
- まとめ: `batch-{YYYY-MM-DD}-{HHmm}.md`
  - 同期単位の時系列管理がしやすい

## 実行フロー

1. `.cache/new_ids.txt` を読んで対象ID一覧を取得する
2. `bookmarks.jsonl` から対象IDに対応するレコードを取り出す
3. 件数が多い場合は、全件生成するか上位だけに絞るかを確認する
   - 目安: 20件以上
4. 各ブックマークについて、次を集める
   - 元の本文・URL・著者・日時
   - 関連ブックマーク
   - Web調査での関連リンク
5. 1件ごとのMDを生成する
6. 同期単位のまとめMDを生成する
7. 作成したファイルパスと件数をユーザーに報告する

## 関連ブックマークの探し方

まずは次の順で探す。

1. 同じ著者
2. 同じドメインやリンク先
3. 本文キーワードでの `ft search`

関連が弱い場合は、無理に増やさず 0〜3件程度に抑える。

## Web調査の方針

- 公式ドキュメントや公式サイトを優先する
- 関連リンクは 2〜5 件を目安に絞る
- 調査結果が弱い場合は、無理に埋めず「追加調査候補」として残してよい

## 1件ごとの MD テンプレ

```markdown
---
source_type: x-bookmark
tweet_id: "1234567890"
tweet_url: "https://x.com/.../status/1234567890"
author: "example_user"
bookmarked_at: "2026-04-15T00:00:00Z"
synced_at: "2026-04-15T00:10:00Z"
generated_at: "2026-04-15T00:15:00Z"
tags:
  - x-bookmark
  - inbox
related_bookmark_ids:
  - "2345678901"
status: inbox
---

# [短いタイトル]

## 元ポスト
[tweet_url]

## 要約
[何が書かれているか]

## なぜ重要か
[この情報の価値、文脈、使いどころ]

## 関連ブックマーク
- [[x-2345678901]]

## 関連リンク
- [リンク1](https://example.com)

## 次アクション
- [読む]
- [試す]
- [別ノートに整理する]
```

## まとめ MD テンプレ

```markdown
---
source_type: x-bookmark-batch
generated_at: "2026-04-15T00:15:00Z"
synced_at: "2026-04-15T00:10:00Z"
new_count: 12
tags:
  - x-bookmarks
  - batch
---

# X Bookmark Batch 2026-04-15 00:10

## 全体サマリ
[今回の差分全体の傾向]

## 主要トピック
- トピックA
- トピックB

## 注目ブックマーク
- [[x-1234567890]]: [一言コメント]
- [[x-2345678901]]: [一言コメント]

## 次に掘る候補
- [深掘り候補1]
- [深掘り候補2]
```

## ユーザー確認が必要な場合

- 差分件数が多いとき
  - 全件作成するか、上位数件に絞るかを聞く
- 既存ファイルがあるとき
  - 上書き、追記、スキップのどれにするかを聞く
- Web調査が弱いとき
  - 浅い調査のまま進めるかを聞く

確認するときの優先順位:

1. まずは 1件ごと + まとめ の両方作成を提案する
2. 件数が多いときだけ絞り込み確認をする

## 報告フォーマット

生成後は次を短く伝える。

- 作成した件数
- 1件ごとの保存先
- まとめファイルの保存先
- 次にできること

例:

```text
説明MDを 8 件作成しました。
個別ノート: x-bookmarks/items/
まとめノート: x-bookmarks/batches/batch-2026-04-15-0010.md

次は、気になるノートを開いて整理するか、実践用ノートに分けられます。
```

## セキュリティ注意

- raw data の `bookmarks.jsonl` や `bookmarks.db` をそのまま公開しない
- Cookie や token の値を本文に書かない
- 外部リンクは必要最小限にする

## 将来拡張

- 実践用ノートを別フォルダに自動生成する
- 生成ノートだけを git add / commit / push する
- 分類タグを `ft classify` の結果と連携する
