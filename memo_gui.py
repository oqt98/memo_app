import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import json
import os
from datetime import datetime

MEMO_FILE = "memo.json"

if not os.path.exists(MEMO_FILE):
    with open(MEMO_FILE, "w", encoding="utf-8") as f:
        json.dump([], f, ensure_ascii=False, indent=2)

def load_memos():
    with open(MEMO_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_memos(memos):
    with open(MEMO_FILE, "w", encoding="utf-8") as f:
        json.dump(memos, f, ensure_ascii=False, indent=2)

def add_memo():
    category = category_var.get().strip()
    new_category = new_category_entry.get().strip()
    content = memo_text.get("1.0", tk.END).strip()

    if new_category:
        category = new_category

    if not category or not content:
        messagebox.showwarning("⚠️ 入力エラー", "カテゴリと内容を入力してください。")
        return

    memos = load_memos()
    new_id = memos[-1]["id"] + 1 if memos else 1
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M")

    memos.append({
        "id": new_id,
        "category": category,
        "content": content,
        "created_at": created_at
    })

    save_memos(memos)
    messagebox.showinfo("✅ 完了", "メモを追加しました！")
    memo_text.delete("1.0", tk.END)
    new_category_entry.delete(0, tk.END)

def open_display_window():
    display_win = tk.Toplevel(root)
    display_win.title("📖 メモ一覧")
    display_win.geometry("520x500")
    display_win.configure(bg="#fdfdfd")

    tk.Label(display_win, text="📃 メモ一覧", font=("Meiryo", 11), bg="#fdfdfd").pack(pady=(10, 0))

    # スクロール付きText
    text_frame = tk.Frame(display_win)
    text_frame.pack(expand=True, fill="both", padx=10, pady=10)

    scrollbar = tk.Scrollbar(text_frame)
    scrollbar.pack(side="right", fill="y")

    text_area = tk.Text(text_frame, wrap="word", font=("Meiryo", 11), spacing3=6,
                        bg="#ffffff", relief="groove", yscrollcommand=scrollbar.set)
    text_area.pack(expand=True, fill="both")
    scrollbar.config(command=text_area.yview)

    # 削除欄
    delete_frame = tk.Frame(display_win, bg="#fdfdfd")
    delete_frame.pack(pady=5)
    tk.Label(delete_frame, text="🆔 削除するID：", bg="#fdfdfd", font=("Meiryo", 10)).pack(side="left")
    delete_id_entry = tk.Entry(delete_frame, width=10, font=("Meiryo", 10))
    delete_id_entry.pack(side="left", padx=5)

    def delete_by_id():
        try:
            delete_id = int(delete_id_entry.get())
        except ValueError:
            messagebox.showerror("❌ エラー", "数字でIDを入力してください。")
            return

        memos = load_memos()
        updated_memos = [memo for memo in memos if memo["id"] != delete_id]

        if len(updated_memos) == len(memos):
            messagebox.showwarning("⚠️ 警告", f"ID {delete_id} は存在しません。")
            return

        save_memos(updated_memos)
        messagebox.showinfo("✅ 完了", f"ID {delete_id} を削除しました！")
        refresh_display()

    tk.Button(delete_frame, text="🗑 削除", font=("Meiryo", 10), command=delete_by_id).pack(side="left", padx=5)

    def refresh_display():
        text_area.delete("1.0", tk.END)
        memos = load_memos()
        if not memos:
            text_area.insert(tk.END, "📭 メモがありません。\n")
            return
        for memo in memos:
            text_area.insert(tk.END, f"📝 ID: {memo['id']}\n", "bold")
            text_area.insert(tk.END, f"📂 カテゴリ: {memo['category']}\n")
            text_area.insert(tk.END, f"⏰ 投稿日時: {memo['created_at']}\n")
            text_area.insert(tk.END, f"{memo['content']}\n")
            text_area.insert(tk.END, "-" * 40 + "\n")

    tk.Button(display_win, text="🔄 表示を更新", font=("Meiryo", 10), command=refresh_display).pack(pady=5)
    refresh_display()

def open_filter_window():
    filter_win = tk.Toplevel(root)
    filter_win.title("📂 カテゴリ別に表示")
    filter_win.geometry("500x400")

    tk.Label(filter_win, text="📚 表示したいカテゴリを選んでください：").pack(pady=(10, 0))

    memos = load_memos()
    categories = sorted(set(m["category"] for m in memos))
    category_var_local = tk.StringVar()
    category_combo = ttk.Combobox(filter_win, textvariable=category_var_local, values=categories, state="readonly")
    category_combo.pack(pady=5, padx=10, fill="x")
    category_combo.bind("<<ComboboxSelected>>", lambda event: filter_display())

    text_area = tk.Text(filter_win, wrap="word")
    text_area.pack(expand=True, fill="both", padx=10, pady=10)

    def filter_display():
        selected = category_var_local.get()
        memos = load_memos()
        filtered = [m for m in memos if m["category"] == selected]
        text_area.delete("1.0", tk.END)
        if not filtered:
            text_area.insert(tk.END, "📭 メモが見つかりませんでした。\n")
            return
        for memo in filtered:
            text_area.insert(tk.END, f"📝 ID: {memo['id']}\n")
            text_area.insert(tk.END, f"📂 カテゴリ: {memo['category']}\n")
            text_area.insert(tk.END, f"⏰ 投稿日時: {memo['created_at']}\n")
            text_area.insert(tk.END, f"{memo['content']}\n")
            text_area.insert(tk.END, "-" * 40 + "\n")

    tk.Button(filter_win, text="🔍 表示する", command=filter_display).pack(pady=5)

def open_sort_window():
    sort_win = tk.Toplevel(root)
    sort_win.title("🔽 並び替えて表示")
    sort_win.geometry("520x500")
    sort_win.configure(bg="#fdfdfd")

    tk.Label(sort_win, text="📌 並び替え方法を選んでください：", bg="#fdfdfd", font=("Meiryo", 11)).pack(pady=(10, 0))

    sort_var = tk.StringVar(value="id")

    # 並び順選択ラジオボタン（背景色付き）
    radio_frame = tk.Frame(sort_win, bg="#fdfdfd")
    radio_frame.pack(pady=5)
    tk.Radiobutton(radio_frame, text="🆔 ID順", variable=sort_var, value="id", font=("Meiryo", 10), bg="#fdfdfd", command=lambda: sort_and_display()).pack(anchor="w")
    tk.Radiobutton(radio_frame, text="📂 カテゴリ順", variable=sort_var, value="category", font=("Meiryo", 10), bg="#fdfdfd", command=lambda: sort_and_display()).pack(anchor="w")
    tk.Radiobutton(radio_frame, text="⏰ 投稿日時順", variable=sort_var, value="created_at", font=("Meiryo", 10), bg="#fdfdfd", command=lambda: sort_and_display()).pack(anchor="w")

    # スクロールバー付きテキストエリア
    text_frame = tk.Frame(sort_win)
    text_frame.pack(expand=True, fill="both", padx=10, pady=10)

    scrollbar = tk.Scrollbar(text_frame)
    scrollbar.pack(side="right", fill="y")

    text_area = tk.Text(
        text_frame,
        wrap="word",
        font=("Meiryo", 11),
        spacing3=6,
        bg="#ffffff",
        relief="groove",
        yscrollcommand=scrollbar.set
    )
    text_area.pack(expand=True, fill="both")
    scrollbar.config(command=text_area.yview)

    def sort_and_display():
        memos = load_memos()
        key = sort_var.get()

        if not memos:
            text_area.delete("1.0", tk.END)
            text_area.insert(tk.END, "📭 メモがありません。\n")
            return

        try:
            if key == "created_at":
                sorted_memos = sorted(memos, key=lambda m: datetime.strptime(m["created_at"], "%Y-%m-%d %H:%M"))
            else:
                sorted_memos = sorted(memos, key=lambda m: m[key])
        except Exception as e:
            text_area.delete("1.0", tk.END)
            text_area.insert(tk.END, f"❌ ソートエラー: {str(e)}\n")
            return

        text_area.delete("1.0", tk.END)
        for memo in sorted_memos:
            text_area.insert(tk.END, f"📝 ID: {memo['id']}\n", "bold")
            text_area.insert(tk.END, f"📂 カテゴリ: {memo['category']}\n")
            text_area.insert(tk.END, f"⏰ 投稿日時: {memo['created_at']}\n")
            text_area.insert(tk.END, f"{memo['content']}\n")
            text_area.insert(tk.END, "-" * 40 + "\n")

    sort_and_display()  # 初回表示

    def sort_and_display():
        print("🟢 表示ボタンが押された！")
        memos = load_memos()
        key = sort_var.get()

        if not memos:
            text_area.delete("1.0", tk.END)
            text_area.insert(tk.END, "📭 メモがありません。\n")
            return

        try:
            if key == "created_at":
                sorted_memos = sorted(
                    memos,
                    key=lambda m: datetime.strptime(m["created_at"], "%Y-%m-%d %H:%M")
                )
            else:
                sorted_memos = sorted(memos, key=lambda m: m[key])
        except Exception as e:
            text_area.delete("1.0", tk.END)
            text_area.insert(tk.END, f"❌ ソートエラー: {str(e)}\n")
            return

        text_area.delete("1.0", tk.END)
        for memo in sorted_memos:
            text_area.insert(tk.END, f"📝 ID: {memo['id']}\n")
            text_area.insert(tk.END, f"📂 カテゴリ: {memo['category']}\n")
            text_area.insert(tk.END, f"⏰ 投稿日時: {memo['created_at']}\n")
            text_area.insert(tk.END, f"{memo['content']}\n")
            text_area.insert(tk.END, "-" * 40 + "\n")

    tk.Button(sort_win, text="🔍 表示する", command=sort_and_display).pack(pady=5)

# ============ メイン画面構築 ============
root = tk.Tk()
root.title("📝 メモ追加")
root.geometry("420x480")
root.configure(bg="#fdfdfd")

memos = load_memos()
categories = sorted(set(m["category"] for m in memos))
category_var = tk.StringVar(value=categories[0] if categories else "")

tk.Label(root, text="📂 既存カテゴリ：", font=("Meiryo", 11), bg="#fdfdfd").pack(anchor="w", padx=10, pady=(10, 0))
category_menu = ttk.Combobox(root, textvariable=category_var, values=categories)
category_menu.pack(fill="x", padx=10)

tk.Label(root, text="🆕 新規カテゴリ：", font=("Meiryo", 11), bg="#fdfdfd").pack(anchor="w", padx=10, pady=(10, 0))
new_category_entry = tk.Entry(root, font=("Meiryo", 10))
new_category_entry.pack(fill="x", padx=10)

tk.Label(root, text="📝 メモ内容：", font=("Meiryo", 11), bg="#fdfdfd").pack(anchor="w", padx=10, pady=(10, 0))
memo_text = tk.Text(root, height=8, font=("Meiryo", 11), spacing3=6, bg="#ffffff", relief="groove")
memo_text.pack(fill="both", expand=True, padx=10, pady=(0, 5))

# ボタンたち
tk.Button(root, text="💾 追加する", font=("Meiryo", 11), command=add_memo).pack(pady=8)
tk.Button(root, text="📖 メモを表示", font=("Meiryo", 11), command=lambda: open_display_window()).pack(pady=3)
tk.Button(root, text="📂 カテゴリで表示", font=("Meiryo", 11), command=lambda: open_filter_window()).pack(pady=3)
tk.Button(root, text="🔽 並び替え表示", font=("Meiryo", 11), command=lambda: open_sort_window()).pack(pady=3)

root.mainloop()
