import tkinter as tk
import time
import sys
from pathlib import Path

# 添加父目錄到 Python 路徑以便導入共用模組
sys.path.append(str(Path(__file__).parent.parent))


class ButtonSmashTestApp:
    """
    Button Smash 快速點擊測試應用程式
    
    功能說明：
    - 測試玩家在 10 秒內的快速點擊能力
    - 從第一次點擊開始計時 10 秒
    - 計算 CPS (Clicks Per Second) = 總點擊數 ÷ 10
    - 使用色盲友善的視覺設計（主要依靠形狀變化而非顏色）
    - 支援 Joy-Con 手把和鍵盤輸入（空白鍵）
    
    視覺回饋：
    - 圓形按鈕：按下時顯示 X 符號，放開時隱藏
    - 顏色變化：按下時淺藍色，放開時白色（避免紅綠色盲問題）
    """
    
    def __init__(self, root):
        self.root = root
        self.root.title("Button Smash Test")
        self.canvas = tk.Canvas(root, width=1200, height=800, bg="white")
        self.canvas.pack()

        # 測試狀態
        self.state = "waiting"  # waiting, testing, finished
        self.start_time = None
        self.test_duration = 10.0  # 10 秒測試時間
        self.click_count = 0
        self.timer_id = None
        
        # 視覺元素
        self.circle_radius = 80
        self.circle_x = 600
        self.circle_y = 400
        
        # 創建圓形按鈕（根據會議回饋：初始為白底）
        self.circle = self.canvas.create_oval(
            self.circle_x - self.circle_radius, 
            self.circle_y - self.circle_radius,
            self.circle_x + self.circle_radius, 
            self.circle_y + self.circle_radius,
            fill="white", 
            outline="black", 
            width=3
        )
        
        # X 符號（初始隱藏）
        self.x_symbol = self.canvas.create_text(
            self.circle_x, self.circle_y,
            text="✕",
            font=("Arial", 48, "bold"),
            fill="black",
            state="hidden"
        )
        
        # 計時顯示
        self.timer_text = self.canvas.create_text(
            600, 200,
            text="",
            font=("Arial", 32),
            fill="black"
        )
        
        # CPS 顯示
        self.cps_text = self.canvas.create_text(
            600, 600,
            text="",
            font=("Arial", 24),
            fill="blue"
        )

        # 指示文字
        self.label = tk.Label(root,
                              text="按『開始測試』開始 10 秒快速點擊測試\n(可使用 Joy-Con 或空白鍵測試)",
                              font=("Arial", 20))
        self.label.place(relx=0.5, rely=0.1, anchor='center')

        # 開始按鈕
        self.start_button = tk.Button(root, 
                                      text="開始測試", 
                                      font=("Arial", 24), 
                                      command=self.start_test)
        self.start_button.place(relx=0.5, rely=0.85, anchor='center')
        
        # 按鍵狀態追蹤
        self.button_pressed = False
        
        # 綁定鍵盤事件作為測試備用（當沒有手把時）
        self.root.bind('<KeyPress>', self.on_keyboard_press)
        self.root.bind('<KeyRelease>', self.on_keyboard_release)
        self.root.focus_set()  # 確保視窗可以接收鍵盤事件

    def start_test(self):
        """開始測試"""
        self.state = "testing"
        self.start_time = None  # 將在第一次點擊時設定
        self.click_count = 0
        
        # 隱藏開始按鈕和說明文字
        self.start_button.place_forget()
        self.label.place_forget()
        
        # 重置視覺元素（根據會議回饋：使用白底，依靠 X 符號而非顏色）
        self.canvas.itemconfig(self.circle, fill="white")
        self.canvas.itemconfig(self.x_symbol, state="hidden")
        self.canvas.itemconfig(self.timer_text, text="等待第一次點擊...")
        self.canvas.itemconfig(self.cps_text, text="")
        
        print("🎮 Button Smash 測試開始！等待第一次點擊...")

    def update_timer(self):
        """更新計時器顯示"""
        if self.state != "testing" or self.start_time is None:
            return
            
        elapsed = time.time() - self.start_time
        remaining = max(0, self.test_duration - elapsed)
        
        if remaining > 0:
            self.canvas.itemconfig(self.timer_text, 
                                   text=f"剩餘時間: {remaining:.1f}s\n點擊次數: {self.click_count}")
            # 繼續更新計時器
            self.timer_id = self.root.after(100, self.update_timer)
        else:
            # 測試結束
            self.finish_test()

    def finish_test(self):
        """結束測試並顯示結果"""
        self.state = "finished"
        
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None
        
        # 計算 CPS (Clicks Per Second)
        cps = self.click_count / self.test_duration
        
        # 顯示結果
        self.canvas.itemconfig(self.timer_text, text="測試完成！")
        self.canvas.itemconfig(self.cps_text, 
                               text=f"總點擊數: {self.click_count}\nCPS: {cps:.2f}\n(點擊數 ÷ {self.test_duration} 秒)")
        
        # 重置圓形和 X 符號（根據會議回饋：使用白底而非灰色）
        self.canvas.itemconfig(self.circle, fill="white")
        self.canvas.itemconfig(self.x_symbol, state="hidden")
        
        # 顯示重新開始按鈕
        self.label.config(text=f"測試完成！總點擊: {self.click_count}, CPS: {cps:.2f}")
        self.label.place(relx=0.5, rely=0.1, anchor='center')
        self.start_button.place(relx=0.5, rely=0.85, anchor='center')
        
        print(f"🎯 測試完成！")
        print(f"📊 總點擊數: {self.click_count}")
        print(f"⏱️ 測試時間: {self.test_duration} 秒")
        print(f"🖱️ CPS (Clicks Per Second): {cps:.2f}")
        print(f"📈 計算方式: {self.click_count} ÷ {self.test_duration} = {cps:.2f}")

    def on_joycon_input(self, buttons, leftX, leftY, last_key_bit, last_key_down):
        """處理 Joy-Con 輸入"""
        
        # 如果不是按鍵事件，忽略
        if last_key_bit is None:
            return
            
        if last_key_down:
            # 按鍵按下
            self.on_button_press()
        else:
            # 按鍵放開
            self.on_button_release()

    def on_button_press(self):
        """處理按鍵按下事件"""
        if self.button_pressed:
            return  # 避免重複觸發
            
        self.button_pressed = True
        
        if self.state == "waiting":
            # 如果在等待狀態，開始測試
            self.start_test()
            return
        
        elif self.state == "testing":
            # 如果是第一次點擊，開始計時
            if self.start_time is None:
                self.start_time = time.time()
                self.update_timer()
                print("⏰ 開始計時！")
            
            # 檢查是否還在測試時間內
            if self.start_time and (time.time() - self.start_time) < self.test_duration:
                self.click_count += 1
                print(f"🖱️ 點擊 #{self.click_count}")
                
                # 視覺回饋：按下時顯示 X 符號（色盲友善設計）
                self.canvas.itemconfig(self.circle, fill="lightblue")  # 使用色盲友善的藍色
                self.canvas.itemconfig(self.x_symbol, state="normal")

    def on_button_release(self):
        """處理按鍵放開事件"""
        if not self.button_pressed:
            return
            
        self.button_pressed = False
        
        if self.state == "testing":
            # 視覺回饋：放開時恢復原色並隱藏 X（主要依靠形狀變化，而非顏色）
            self.canvas.itemconfig(self.circle, fill="white")
            self.canvas.itemconfig(self.x_symbol, state="hidden")

    def on_keyboard_press(self, event):
        """處理鍵盤按下事件（測試備用）"""
        if event.keysym == 'space':  # 空白鍵
            self.on_button_press()

    def on_keyboard_release(self, event):
        """處理鍵盤放開事件（測試備用）"""
        if event.keysym == 'space':  # 空白鍵
            self.on_button_release()


if __name__ == "__main__":
    from threading import Thread
    from common.controller_input import ControllerInput

    root = tk.Tk()
    app = ButtonSmashTestApp(root)

    # 檢查是否有測試參數
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        # 測試模式：模擬點擊來驗證 CPS 計算
        print("🧪 測試模式：驗證 CPS 計算...")
        
        # 模擬 25 次點擊，應該得到 2.5 CPS
        app.start_test()
        app.start_time = time.time()
        app.click_count = 25
        app.finish_test()
        
        print("✅ 測試完成")
        root.destroy()
        sys.exit(0)

    # 設定手把輸入監聽
    listener = ControllerInput(button_callback=app.on_joycon_input)
    Thread(target=listener.run, daemon=True).start()

    root.mainloop()
    print("🎮 Button Smash 測試結束")
