📝 README.md（GUIメモ帳用）
# 📝 GUIメモ帳アプリ（Tkinter × Python）

## 📌 概要 / Overview

このアプリは、PythonのGUIライブラリ「Tkinter」を用いて作成したシンプルなメモ帳アプリです。  
メモの追加・表示・カテゴリ分け・並び替え・編集・削除・検索といった基本機能を備えています。  
CLI版と共通のデータ（memo.json）を使用し、GUIでより直感的に操作できるようになっています。

This is a simple note-taking application built with Python and Tkinter.  
You can add, view, categorize, sort, edit, delete, and search notes.  
It uses a shared `memo.json` file that can be used with both CLI and GUI versions.

---

## 🖥️ 機能 / Features

- 💾 メモの追加（カテゴリ付き）
- 📖 全メモの表示
- 📂 カテゴリごとの表示
- 🔽 並び替え（ID順 / カテゴリ順 / 投稿日順）
- ✏️ メモの編集
- ❌ メモの削除（確認ダイアログ付き）
- 🔍 検索（キーワード含むメモを抽出）
- ✅ データは `memo.json` に保存

---

## 🧰 使用技術 / Tech Stack

- Python 3.x
- Tkinter（標準GUIライブラリ）
- JSON（データ保存形式）

---

## 🚀 起動方法 / How to Run

1. Pythonをインストール（3.x）
2. このリポジトリをクローン

```bash
git clone https://github.com/your-username/memo_app.git
cd memo_app
実行！


python memo_gui.py
📁 ファイル構成 / File Structure
bash
コピーする
編集する
memo_app/
├── memo_gui.py        # GUIメモ帳アプリ本体
├── memo_cli.py        # CLI版メモ帳（オプション）
├── memo.json          # メモデータ保存ファイル（共通）
└── README.md
🧪 補足メモ
データ永続化：アプリを閉じても memo.json に保存されているので安心です

カテゴリの登録ゆれ防止：既存カテゴリはプルダウンで選択

UIデザイン：Meiryo フォント＋白背景＋ボタンアイコンで統一

📮 今後の拡張（アイデア）
🔐 パスワード保護機能

☁️ クラウド同期（Google Driveなど）

📱 モバイル対応（Kivy等）

👤 Author
Fumiya Kawakami（@your_github_id）
PMOを目指してPython・自動化・GUIにチャレンジ中！

📄 License
MIT License