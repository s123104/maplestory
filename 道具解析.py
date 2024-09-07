import tkinter as tk
import re
import json
import os

# 定義 JSON 檔案路徑
json_file_dir = '/Users/azlife.eth/code/MS'
json_file_path = os.path.join(json_file_dir, 'items.json')

# 如果 JSON 檔案不存在，創建一個空的 JSON 檔案
if not os.path.exists(json_file_path):
    os.makedirs(json_file_dir, exist_ok=True)
    with open(json_file_path, 'w', encoding='utf-8') as json_file:
        json.dump({}, json_file, ensure_ascii=False, indent=4)

# 從 JSON 檔案中讀取現有的資料
def load_json():
    with open(json_file_path, 'r', encoding='utf-8') as json_file:
        return json.load(json_file)

# 將更新後的資料寫回 JSON 檔案
def save_json(data):
    with open(json_file_path, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)

# 更新處理狀態顯示
def update_status(message, color):
    status_label.config(text=message, fg=color)

# 解析輸入的道具名稱，並更新到 JSON
def process_input():
    input_text = text_area.get("1.0", tk.END).strip()
    
    # 使用正則表達式來解析道具名稱
    pattern = r'([\u4e00-\u9fa5a-zA-Z0-9]+)\s+[\d.]+%'
    item_names = re.findall(pattern, input_text)
    
    # 去除重複的道具名稱並排序
    unique_items = sorted(set(item_names))

    # 讀取現有的 JSON 資料
    items_dict = load_json()

    # 計算新增的道具數量
    new_items = {item for item in unique_items if item not in items_dict}
    new_items_count = len(new_items)

    # 將新的道具加入字典，確保不重複
    for item in new_items:
        items_dict[item] = {"aliases": []}

    # 保存更新後的 JSON 資料
    save_json(items_dict)

    # 顯示處理結果
    if new_items_count > 0:
        message = f"新增了 {new_items_count} 個道具。"
        update_status(message, 'green')
    else:
        update_status("所有道具已存在。", 'red')

    # 打印處理結果
    print(f"處理結果: 新增了 {new_items_count} 個道具。")
    print("更新後的 JSON 資料：")
    with open(json_file_path, 'r', encoding='utf-8') as json_file:
        print(json_file.read())

# 貼上按鈕功能
def paste_text():
    text_area.delete("1.0", tk.END)
    text_area.insert(tk.END, root.clipboard_get())

# 清空文本區域
def clear_text():
    text_area.delete("1.0", tk.END)
    update_status("文本區已清空。", 'white')

# 建立 UI 窗口
root = tk.Tk()
root.title("道具處理工具")

# 置頂功能
root.attributes("-topmost", True)

button_frame = tk.Frame(root)
button_frame.pack(pady=10)

paste_button = tk.Button(button_frame, text="貼上", command=paste_text)
paste_button.grid(row=0, column=0, padx=5)

clear_button = tk.Button(button_frame, text="清空", command=clear_text)
clear_button.grid(row=0, column=1, padx=5)

# 設置 UI 元件
text_area = tk.Text(root, height=15, width=50)
text_area.pack(pady=10)

process_button = tk.Button(root, text="處理", command=process_input, width=20, height=2)
process_button.pack(pady=10)

status_label = tk.Label(root, text="", font=("Arial", 12))
status_label.pack(pady=10)

# 運行主循環
root.mainloop()