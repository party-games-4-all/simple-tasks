#!/usr/bin/env python3
"""
測試視窗設置 (無 pygame)
"""
import tkinter as tk
import sys
from pathlib import Path

# 添加 common 模組到 Python 路徑
sys.path.append(str(Path(__file__).parent / "common"))

# 設置視窗配置
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800

def setup_window_topmost_simple(root):
    """
    簡化版本的視窗設定
    """
    try:
        # 設定視窗大小
        width = WINDOW_WIDTH
        height = WINDOW_HEIGHT
        
        # 計算螢幕中央位置
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        
        # 設定視窗大小和位置
        root.geometry(f'{width}x{height}+{x}+{y}')
        
        # 設定視窗置頂
        root.attributes('-topmost', True)
        
        # 讓視窗取得焦點
        root.focus_force()
        root.lift()
        
        # 設定最小視窗大小以防止意外縮小
        root.minsize(width, height)
        
        print(f"🖥️ 視窗設定為：{width}x{height}，位置：({x}, {y})")
        
    except Exception as e:
        print(f"⚠️ 設定視窗失敗: {e}")

def test_window_setup():
    """測試視窗設置"""
    print("🖥️ 測試視窗設置...")
    print(f"預期視窗大小：{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
    
    root = tk.Tk()
    root.title("視窗大小測試")
    
    # 使用我們的視窗設置函數
    setup_window_topmost_simple(root)
    
    # 創建一個 Canvas 來測試
    canvas = tk.Canvas(root, 
                      width=WINDOW_WIDTH, 
                      height=WINDOW_HEIGHT,
                      bg='lightblue')
    canvas.pack()
    
    # 在 Canvas 中央顯示文字
    canvas.create_text(WINDOW_WIDTH//2, WINDOW_HEIGHT//2,
                      text=f"視窗大小測試\n{WINDOW_WIDTH}x{WINDOW_HEIGHT}",
                      font=("Arial", 24),
                      fill="black")
    
    # 顯示實際視窗大小
    def show_actual_size():
        actual_width = root.winfo_width()
        actual_height = root.winfo_height()
        print(f"實際視窗大小：{actual_width}x{actual_height}")
        canvas.create_text(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 100,
                          text=f"實際大小：{actual_width}x{actual_height}",
                          font=("Arial", 16),
                          fill="red")
    
    # 1秒後檢查實際大小
    root.after(1000, show_actual_size)
    
    # 按下任意鍵關閉
    def close_window(event):
        root.destroy()
    
    root.bind('<Key>', close_window)
    root.focus_set()
    
    canvas.create_text(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 200,
                      text="按任意鍵關閉視窗",
                      font=("Arial", 14),
                      fill="gray")
    
    print("視窗已開啟，按任意鍵關閉...")
    root.mainloop()

if __name__ == "__main__":
    test_window_setup()
