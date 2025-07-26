#!/usr/bin/env python3
"""
測試視窗設置
"""
import tkinter as tk
import sys
from pathlib import Path

# 添加 common 模組到 Python 路徑
sys.path.append(str(Path(__file__).parent / "common"))

from common import config
from common.utils import setup_window_topmost

def test_window_setup():
    """測試視窗設置"""
    print("🖥️ 測試視窗設置...")
    print(f"配置中的視窗大小：{config.WINDOW_WIDTH}x{config.WINDOW_HEIGHT}")
    
    root = tk.Tk()
    root.title("視窗大小測試")
    
    # 使用我們的視窗設置函數
    setup_window_topmost(root)
    
    # 創建一個 Canvas 來測試
    canvas = tk.Canvas(root, 
                      width=config.WINDOW_WIDTH, 
                      height=config.WINDOW_HEIGHT,
                      bg='lightblue')
    canvas.pack()
    
    # 在 Canvas 中央顯示文字
    canvas.create_text(config.WINDOW_WIDTH//2, config.WINDOW_HEIGHT//2,
                      text=f"視窗大小測試\n{config.WINDOW_WIDTH}x{config.WINDOW_HEIGHT}",
                      font=("Arial", 24),
                      fill="black")
    
    # 顯示實際視窗大小
    def show_actual_size():
        actual_width = root.winfo_width()
        actual_height = root.winfo_height()
        print(f"實際視窗大小：{actual_width}x{actual_height}")
        canvas.create_text(config.WINDOW_WIDTH//2, config.WINDOW_HEIGHT//2 + 100,
                          text=f"實際大小：{actual_width}x{actual_height}",
                          font=("Arial", 16),
                          fill="red")
    
    # 5秒後檢查實際大小
    root.after(1000, show_actual_size)
    
    # 10秒後自動關閉
    root.after(10000, root.destroy)
    
    print("視窗已開啟，將顯示10秒後自動關閉...")
    root.mainloop()

if __name__ == "__main__":
    test_window_setup()
