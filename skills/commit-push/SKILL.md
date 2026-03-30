---
name: commit-push
description: >
  変更をコミットしてリモートにプッシュする。
  コミットメッセージは日本語、Co-Authored-By 不要、push は origin <branch> を明示する。
  「コミットして」「pushして」「コミットしてpushして」「良い感じのコミットメッセージで」
  などのキーワードが出たら即座にこのスキルを使う。
compatibility:
  permissions:
    - "Bash(git add*)"
    - "Bash(git status*)"
    - "Bash(git diff*)"
    - "Bash(git log*)"
    - "Bash(git commit*)"
    - "Bash(git push*)"
    - "Bash(git branch*)"
---

## When to Use

- ユーザーが「コミットして」「pushして」「コミットしてpushして」と言ったとき
- 「良い感じのコミットメッセージで」「日本語でコミット」など、コミット操作を依頼されたとき
- コードの変更が完了し、リモートへの反映を求められたとき

## Rules（必ず守ること）

1. **コミットメッセージは日本語**で書く
2. **`Co-Authored-By` などのフッターは一切含めない**
3. **push は `git push origin <branch>` とブランチ名を明示**する（`git push` だけはNG）
4. **コミット前・push前に必ずユーザーの確認を取る**（以下のワークフロー参照）

## Workflow

```bash
# 1. 現在の状態を確認
git status

# 2. 差分を確認してコミットメッセージを考える
git diff HEAD

# 3. 直近のコミット履歴でメッセージのトーンを把握
git log --oneline -5
```

**【確認①】コミット前にユーザーへ確認する**

差分をもとにコミットメッセージの案を作り、以下の形式でユーザーに確認を求める：

> `「<考えたコミットメッセージ>」でコミットしていい？`

ユーザーが OK を出したら次へ進む。別のメッセージを提案された場合はそちらを使う。

```bash
# 4. ファイルをステージング
git add <files>   # 基本はファイルを個別指定。不明なら git status で確認してから

# 5. コミット（日本語メッセージ、フッターなし）
git commit -m "確認済みのコミットメッセージ"
```

**【確認②】push前にユーザーへ確認する**

コミット完了後、以下の形式でユーザーに確認を求める：

> `<branch名> にpushしていい？`

ユーザーが OK を出したら push する。

```bash
# 6. 現在のブランチ名を取得してpush
git branch --show-current
git push origin <branch>
```

## Commit Message Guidelines

- **動詞＋目的語**の形にする（例：「〇〇を追加」「〇〇を修正」「〇〇を削除」）
- **50字以内**を目安に簡潔に
- 「何を」だけでなく「なぜ」が非自明な場合は含める
- 良い例：
  - `READMEを日本語と英語のファイルに分割`
  - `ログイン画面のバリデーションエラー表示を修正`
  - `不要なデバッグログを削除`
- 悪い例：
  - `update` （何を更新したか不明）
  - `fix bug` （英語かつ内容が不明）
  - `変更` （内容が不明）

## Notes

- `.env` や秘匿情報を含むファイルは `git add` しない
- push 前に `git status` でステージング状態を必ず確認する
- コンフリクトがある場合はユーザーに報告して解決を促す
