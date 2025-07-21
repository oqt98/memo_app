import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import json
import os

MEMO_FILE = "memo.json"

def load_memos():
    if not os.path.exists(MEMO_FILE):
        return []
    with open(MEMO_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_memos(memos):
    with open(MEMO_FILE, "w", encoding="utf-8") as f:
        json.dump(memos, f, ensure_ascii=False, indent=4)

def add_memo():
    global memos
    category = new_category_entry.get() or category_var.get()
    content = memo_text.get("1.0", "end").strip()
    if not content:
        messagebox.showwarning("⚠ 入力エラー", "メモ内容が空です。")
        return
    new_id = max([memo["id"] for memo in memos], default=0) + 1
    new_memo = {
        "id": new_id,
        "category": category,
        "content": content,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    memos.append(new_memo)
    save_memos(memos)
    memo_text.delete("1.0", "end")
    new_category_entry.delete(0, "end")
    refresh_category_menu()
    messagebox.showinfo("✅ 追加完了", "メモを追加しました")

def refresh_category_menu():
    categories = sorted(set(m["category"] for m in memos))
    category_menu["values"] = categories
    if categories:
        category_var.set(categories[0])

def refresh_display(frame):
    for widget in frame.winfo_children():
        widget.destroy()
    for memo in memos:
        entry = tk.Frame(frame, bg="white", pady=5)
        entry.pack(fill="x", padx=10)
        tk.Label(entry, text=f"🆔 ID: {memo['id']}", font=("Meiryo UI", 10, "bold"), bg="white").pack(anchor="w")
        tk.Label(entry, text=f"📂 カテゴリ: {memo['category']}", font=("Meiryo UI", 10), bg="white").pack(anchor="w")
        tk.Label(entry, text=f"⏰ 投稿日時: {memo['created_at']}", font=("Meiryo UI", 10), bg="white").pack(anchor="w")
        tk.Label(entry, text=memo["content"], font=("Meiryo UI", 10), bg="white", wraplength=650, justify="left").pack(anchor="w")
        tk.Label(entry, text="-"*60, bg="white").pack(anchor="w")

def delete_memo(delete_id, scrollable_frame, error_label):
    global memos
    try:
        delete_id = int(delete_id)
    except ValueError:
        error_label.config(text="⚠ 削除IDは数字で入力してください")
        return

    target = next((memo for memo in memos if memo["id"] == delete_id), None)
    if not target:
        error_label.config(text=f"⚠ ID {delete_id} のメモが見つかりません")
        return

    confirm = messagebox.askokcancel("削除確認", f"ID {delete_id} のメモを削除しますか？", icon="warning")
    if not confirm:
        error_label.config(text="キャンセルされました")
        return

    memos = [memo for memo in memos if memo["id"] != delete_id]
    save_memos(memos)
    error_label.config(text="")
    refresh_display(scrollable_frame)
    messagebox.showinfo("✅ 削除完了", f"ID {delete_id} のメモを削除しました")

def edit_memo(edit_id, new_category, new_content, scrollable_frame, error_label):
    global memos
    try:
        edit_id = int(edit_id)
    except ValueError:
        error_label.config(text="⚠ 編集IDは数字で入力してください")
        return

    for memo in memos:
        if memo["id"] == edit_id:
            if new_category:
                memo["category"] = new_category
            if new_content:
                memo["content"] = new_content
            save_memos(memos)
            error_label.config(text="✅ メモを更新しました")
            refresh_display(scrollable_frame)
            return

    error_label.config(text=f"⚠ ID {edit_id} のメモが見つかりません")

def open_display_window():
    global memos
    memos = load_memos()

    display_win = tk.Toplevel(root)
    display_win.title("📖 メモ一覧")
    display_win.geometry("700x700")
    display_win.configure(bg="#f9f9f9")

    main_frame = tk.Frame(display_win, bg="#f9f9f9")
    main_frame.pack(fill="both", expand=True)

    # 検索欄
    search_frame = tk.Frame(main_frame, bg="#f9f9f9")
    search_frame.pack(side="top", fill="x", pady=5)
    tk.Label(search_frame, text="🔍 キーワード検索：", font=("Meiryo UI", 10), bg="#f9f9f9").pack(side="left")
    search_entry = tk.Entry(search_frame)
    search_entry.pack(side="left", padx=5)
    tk.Button(search_frame, text="検索", command=lambda: search_memo(search_entry.get())).pack(side="left")

    # スクロール領域
    canvas_frame = tk.Frame(main_frame)
    canvas_frame.pack(fill="both", expand=True)

    canvas = tk.Canvas(canvas_frame, bg="#ffffff")
    scrollbar = tk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)

    scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)

    scrollable_frame = tk.Frame(canvas, bg="#ffffff")
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    scrollable_frame.bind("<Configure>", lambda event: canvas.configure(scrollregion=canvas.bbox("all")))

    refresh_display(scrollable_frame)

    # 下部操作欄
    control_frame = tk.Frame(main_frame, bg="#f9f9f9", pady=10)
    control_frame.pack(fill="x")
    error_label = tk.Label(control_frame, text="", fg="red", font=("Meiryo UI", 9), bg="#f9f9f9")
    error_label.grid(row=3, column=0, columnspan=4, sticky="w", padx=5, pady=2)

    # 削除
    tk.Label(control_frame, text="🗑 削除するID：", font=("Meiryo UI", 10), bg="#f9f9f9").grid(row=0, column=0, sticky="e")
    delete_id_entry = tk.Entry(control_frame, width=5)
    delete_id_entry.grid(row=0, column=1, sticky="w", padx=5)
    tk.Button(control_frame, text="🗑 削除", command=lambda: delete_memo(delete_id_entry.get(), scrollable_frame, error_label)).grid(row=0, column=2, padx=5)

    # 編集
    tk.Label(control_frame, text="✏ 編集ID：", font=("Meiryo UI", 10), bg="#f9f9f9").grid(row=1, column=0, sticky="e")
    edit_id_entry = tk.Entry(control_frame, width=5)
    edit_id_entry.grid(row=1, column=1, sticky="w", padx=5)
    tk.Label(control_frame, text="➡ 新カテゴリ：", font=("Meiryo UI", 10), bg="#f9f9f9").grid(row=1, column=2, sticky="e")
    new_category_entry = tk.Entry(control_frame, width=10)
    new_category_entry.grid(row=1, column=3, sticky="w", padx=5)

    tk.Label(control_frame, text="📝 新メモ内容：", font=("Meiryo UI", 10), bg="#f9f9f9").grid(row=2, column=0, sticky="ne")
    new_content_entry = tk.Entry(control_frame, width=60)
    new_content_entry.grid(row=2, column=1, columnspan=3, sticky="w", pady=5)

    tk.Button(control_frame, text="💾 更新", command=lambda: edit_memo(edit_id_entry.get(), new_category_entry.get(), new_content_entry.get(), scrollable_frame, error_label)).grid(row=2, column=4, padx=5)

def search_memo(keyword):
    filtered = [m for m in memos if keyword.lower() in m["content"].lower()]
    if not filtered:
        messagebox.showinfo("検索結果", "一致するメモはありませんでした。")
        return

    result_win = tk.Toplevel(root)
    result_win.title("🔍 検索結果")
    result_win.geometry("600x500")
    result_frame = tk.Frame(result_win, bg="white")
    result_frame.pack(fill="both", expand=True)

    for memo in filtered:
        frame = tk.Frame(result_frame, bg="white", pady=5)
        frame.pack(fill="x", padx=10)
        tk.Label(frame, text=f"🆔 ID: {memo['id']}", font=("Meiryo UI", 10, "bold"), bg="white").pack(anchor="w")
        tk.Label(frame, text=f"📂 カテゴリ: {memo['category']}", font=("Meiryo UI", 10), bg="white").pack(anchor="w")
        tk.Label(frame, text=f"⏰ 投稿日時: {memo['created_at']}", font=("Meiryo UI", 10), bg="white").pack(anchor="w")
        tk.Label(frame, text=memo["content"], font=("Meiryo UI", 10), bg="white", wraplength=550).pack(anchor="w")
        tk.Label(frame, text="-"*60, bg="white").pack(anchor="w")

def open_filter_window():
    filter_win = tk.Toplevel(root)
    filter_win.title("📂 カテゴリ別に表示")
    filter_win.geometry("520x500")
    filter_win.configure(bg="#fdfdfd")

    tk.Label(filter_win, text="📚 表示したいカテゴリを選んでください：", font=("Meiryo UI", 11), bg="#fdfdfd").pack(pady=(10, 0))

    memos = load_memos()
    categories = sorted(set(m["category"] for m in memos))
    category_var_local = tk.StringVar()
    category_combo = ttk.Combobox(filter_win, textvariable=category_var_local, values=categories, state="readonly", font=("Meiryo UI", 10))
    category_combo.pack(pady=5, padx=10, fill="x")
    category_combo.bind("<<ComboboxSelected>>", lambda event: filter_display())

    # スクロール付きテキストエリア
    text_frame = tk.Frame(filter_win)
    text_frame.pack(fill="both", padx=10, pady=10)  # expand=Falseに
    text_frame.configure(height=300)  # 👈 高さを制限してみる（調整可）

    scrollbar = tk.Scrollbar(text_frame)
    scrollbar.pack(side="right", fill="y")

    text_area = tk.Text(
        text_frame,
        wrap="word",
        font=("Meiryo UI", 11),
        spacing3=6,
        bg="#ffffff",
        relief="groove",
        yscrollcommand=scrollbar.set
    )
    text_area.pack(expand=True, fill="both")
    scrollbar.config(command=text_area.yview)

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

    tk.Button(filter_win, text="🔍 表示する", font=("Meiryo UI", 10), command=filter_display).pack(pady=5)


import tkinter as tk
from tkinter import ttk
from datetime import datetime
import json
import os

# 🔽 メモの読み込み関数（前提として存在）
def load_memos():
    if not os.path.exists("memo.json"):
        return []
    with open("memo.json", "r", encoding="utf-8") as f:
        return json.load(f)

# ⏰ 安全に日時をパースする関数（秒あり・秒なし両対応）
def parse_datetime_safe(dt_str):
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M"):
        try:
            return datetime.strptime(dt_str, fmt)
        except ValueError:
            continue
    raise ValueError(f"⚠️ 未対応フォーマット: {dt_str}")

# 🔽 並び替え表示ウィンドウ
def open_sort_window():
    sort_win = tk.Toplevel()
    sort_win.title("🔽 並び替えて表示")
    sort_win.geometry("520x500")
    sort_win.configure(bg="#fdfdfd")

    tk.Label(sort_win, text="📌 並び替え方法を選んでください：", bg="#fdfdfd", font=("Meiryo", 11)).pack(pady=(10, 0))

    sort_var = tk.StringVar(value="id")

    # 🔘 並び順選択ラジオボタン
    radio_frame = tk.Frame(sort_win, bg="#fdfdfd")
    radio_frame.pack(pady=5)
    tk.Radiobutton(radio_frame, text="🆔 ID順", variable=sort_var, value="id", font=("Meiryo", 10), bg="#fdfdfd", command=lambda: sort_and_display()).pack(anchor="w")
    tk.Radiobutton(radio_frame, text="📂 カテゴリ順", variable=sort_var, value="category", font=("Meiryo", 10), bg="#fdfdfd", command=lambda: sort_and_display()).pack(anchor="w")
    tk.Radiobutton(radio_frame, text="⏰ 投稿日時順", variable=sort_var, value="created_at", font=("Meiryo", 10), bg="#fdfdfd", command=lambda: sort_and_display()).pack(anchor="w")

    # 📄 スクロール付き表示欄
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

    # 🔄 並び替えて表示する処理
    def sort_and_display():
        memos = load_memos()
        key = sort_var.get()

        if not memos:
            text_area.delete("1.0", tk.END)
            text_area.insert(tk.END, "📭 メモがありません。\n")
            return

        try:
            if key == "created_at":
                sorted_memos = sorted(memos, key=lambda m: parse_datetime_safe(m["created_at"]))
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

    # 🔘 最初に1回表示
    sort_and_display()

    # 🔍 表示ボタン（必要なら）
    tk.Button(sort_win, text="🔍 表示する", font=("Meiryo", 10), command=sort_and_display).pack(pady=5)




# ========================= メイン画面 =========================
root = tk.Tk()
root.title("📝 メモ追加")
root.geometry("420x500")
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

# 🧩 ボタンを2列に並べるフレーム
button_frame = tk.Frame(root, bg="#fdfdfd")
button_frame.pack(pady=10)

# 左列のボタンたち
left_col = tk.Frame(button_frame, bg="#fdfdfd")
left_col.pack(side="left", padx=10)

tk.Button(left_col, text="💾 追加する", font=("Meiryo UI", 11), command=add_memo).pack(pady=3)
tk.Button(left_col, text="🔽 並び替え表示", font=("Meiryo UI", 11), command=open_sort_window).pack(pady=3)

# 右列のボタンたち
right_col = tk.Frame(button_frame, bg="#fdfdfd")
right_col.pack(side="left", padx=10)

tk.Button(right_col, text="📖 メモを表示", font=("Meiryo UI", 11), command=open_display_window).pack(pady=3)
tk.Button(right_col, text="📂 カテゴリで表示", font=("Meiryo UI", 11), command=open_filter_window).pack(pady=3)

root.mainloop()
