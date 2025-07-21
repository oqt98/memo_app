# 📝 CLIメモ帳アプリ

カテゴリ別にメモを登録・閲覧・削除・検索できる、Python製のシンプルなメモ帳アプリです。
CLI（ターミナル）上で動作し、色付きで見やすい表示を提供します。

---

## 📌 機能一覧

- ✅ メモの追加（カテゴリ・内容・日時）
- ✅ メモの表示（全件 / カテゴリ別）
- ✅ メモの削除（ID指定）
- ✅ 並び替え表示（ID順・日時順・カテゴリ順）
- ✅ 「戻る」機能付きで安心操作
- ✅ CLI上での色＆太字表示（UX向上）

---

## 🚀 使用方法

```cmd
# アプリ実行
python memo.py
表示されるメニューから操作を選んで進めます：

==== メモ帳アプリ ====
1: メモを追加
2: メモを表示
3: メモを削除
4: カテゴリで表示
5: 並び替えて表示
6: 終了

## ⚙️ インストール手順

```bash
# Clone this repo
git clone https://github.com/your-username/memo-cli.git
cd memo-cli

# coloramaをインストール（初回のみ）
pip install colorama

# 実行
python memo.py

📦 使用ライブラリ
colorama：CLI出力に色をつけて見やすくする

📁 フォルダ構成
memo_app/
├── memo.py          # メインスクリプト
├── memo.json        # メモデータ保存ファイル
└── README.md        # 本ファイル
💡 補足
メモは memo.json に保存され、アプリ終了後も保持されます。
初回起動時にファイルが自動生成されます。

🙋‍♂️ 作者
Fumiya Kawakami
「自動化×見やすさ×習得」をテーマにしたPMO志望のPython初学者が作成
---
