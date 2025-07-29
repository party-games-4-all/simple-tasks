import tkinter as tk
import random
import time
import sys
import argparse
from pathlib import Path

# 添加父目錄到 Python 路徑以便導入共用模組
sys.path.append(str(Path(__file__).parent.parent))

from common import config
from common.result_saver import save_test_result
from common.utils import setup_window_topmost


class ReactionTestApp:
    """簡單的反應時間測試應用程式"""
    def __init__(self, root, user_id=None):
        self.root = root
        self.user_id = user_id or "default"
        self.root.title("Reaction Test | 反應測試")
        
        # 設定視窗置頂
        setup_window_topmost(self.root)
        
        self.canvas = tk.Canvas(root, width=config.WINDOW_WIDTH, height=config.WINDOW_HEIGHT, 
                               bg=f"#{config.COLORS['BACKGROUND'][0]:02x}{config.COLORS['BACKGROUND'][1]:02x}{config.COLORS['BACKGROUND'][2]:02x}")
        self.canvas.pack()

        self.state = "waiting"
        self.start_time = None
        self.after_id = None
        self.reaction_times = []
        self.test_results = []  # 儲存詳細的測試結果

        # 中央圓形（先畫成預設按鈕顏色）
        center_x, center_y = config.WINDOW_WIDTH // 2, config.WINDOW_HEIGHT // 2
        circle_size = 50  # 半徑
        button_default_color = f"#{config.COLORS['BUTTON_DEFAULT'][0]:02x}{config.COLORS['BUTTON_DEFAULT'][1]:02x}{config.COLORS['BUTTON_DEFAULT'][2]:02x}"
        text_color = f"#{config.COLORS['TEXT'][0]:02x}{config.COLORS['TEXT'][1]:02x}{config.COLORS['TEXT'][2]:02x}"
        self.circle = self.canvas.create_oval(center_x - circle_size, center_y - circle_size, 
                                            center_x + circle_size, center_y + circle_size, 
                                            fill=button_default_color, outline=text_color, width=3)

        self.label = tk.Label(root,
                              text="Press 'Start Test' button to begin | 請按『開始測試』按鈕開始測試",
                              font=("Arial", 24),
                              bg=f"#{config.COLORS['BACKGROUND'][0]:02x}{config.COLORS['BACKGROUND'][1]:02x}{config.COLORS['BACKGROUND'][2]:02x}",
                              fg=text_color)
        self.label.place(relx=0.5, rely=0.2, anchor='center')

        self.start_button = tk.Button(root, text="Start Test | 開始測試", font=("Arial", 24), command=self.start_test,
                                     bg=f"#{config.COLORS['BUTTON_DEFAULT'][0]:02x}{config.COLORS['BUTTON_DEFAULT'][1]:02x}{config.COLORS['BUTTON_DEFAULT'][2]:02x}",
                                     fg=f"#{config.COLORS['TEXT'][0]:02x}{config.COLORS['TEXT'][1]:02x}{config.COLORS['TEXT'][2]:02x}")
        self.start_button.place(relx=0.5, rely=0.8, anchor='center')

    def start_test(self):
        self.state = "ready"
        self.start_button.place_forget()  # 隱藏開始按鈕
        self.label.place_forget()
        # self.label.config(text="準備中...")
        # self.canvas.config(bg="white")
        button_default_color = f"#{config.COLORS['BUTTON_DEFAULT'][0]:02x}{config.COLORS['BUTTON_DEFAULT'][1]:02x}{config.COLORS['BUTTON_DEFAULT'][2]:02x}"
        self.canvas.itemconfig(self.circle, fill=button_default_color)
        # self.root.after(3000, self.set_random_timer)
        self.set_random_timer()

    def set_random_timer(self):
        delay = random.randint(1000, 3000)  # 隨機延遲 1~3 秒
        self.after_id = self.root.after(delay, self.turn_red)

    def turn_red(self):
        error_color = f"#{config.COLORS['ERROR'][0]:02x}{config.COLORS['ERROR'][1]:02x}{config.COLORS['ERROR'][2]:02x}"
        self.canvas.itemconfig(self.circle, fill=error_color)  # 使用色盲友善的錯誤顏色
        # self.label.config(text="快按 Joy-Con！", font=("Arial", 32))
        self.state = "go"
        self.start_time = time.time()

    def on_joycon_input(self, buttons, leftX, leftY, last_key_bit, last_key_down):
        if not last_key_down:
            return  # 只處理按下事件（不處理放開）

        if self.state == "waiting":
            self.start_test()

        elif self.state == "ready":
            # self.label.config(text="太快了！再試一次。", font=("Arial", 24))
            # self.canvas.config(bg="white")
            if self.after_id:
                self.root.after_cancel(self.after_id)
            background_color = f"#{config.COLORS['BACKGROUND'][0]:02x}{config.COLORS['BACKGROUND'][1]:02x}{config.COLORS['BACKGROUND'][2]:02x}"
            self.canvas.itemconfig(self.circle, fill=background_color)
            self.state = "waiting"
            print(f"Too fast! Try again. | 太快了！再試一次。")

        elif self.state == "go":
            reaction_time = time.time() - self.start_time
            self.reaction_times.append(reaction_time)
            
            # 記錄詳細的測試結果
            self.test_results.append({
                "trial_number": len(self.test_results) + 1,
                "reaction_time_ms": reaction_time * 1000,
                "reaction_time_seconds": reaction_time
            })
            
            # self.label.config(text=f"反應時間：{reaction_time:.3f} 秒。請再按一次開始", font=("Arial", 24))
            print(f"Reaction time | 反應時間：{reaction_time:.3f} seconds | 秒")
            success_color = f"#{config.COLORS['SUCCESS'][0]:02x}{config.COLORS['SUCCESS'][1]:02x}{config.COLORS['SUCCESS'][2]:02x}"
            self.canvas.itemconfig(self.circle, fill=success_color)
            self.state = "waiting"

            if len(self.reaction_times) < 5:
                # self.root.after(2000, self.start_test)  # 2 秒後開始下一次測試
                pass
            else:
                avg_time = sum(self.reaction_times) / len(self.reaction_times)
                print(f"Average reaction time | 平均反應時間：{avg_time:.3f} seconds | 秒")
                
                # 儲存測試結果
                self.save_test_results()
                
                self.reaction_times.clear()
                text_color = f"#{config.COLORS['TEXT'][0]:02x}{config.COLORS['TEXT'][1]:02x}{config.COLORS['TEXT'][2]:02x}"
                background_color = f"#{config.COLORS['BACKGROUND'][0]:02x}{config.COLORS['BACKGROUND'][1]:02x}{config.COLORS['BACKGROUND'][2]:02x}"
                self.label.config(text="Test completed! Press 'Start Test' to restart. | 測試完成！請按『開始測試』重新開始。", font=("Arial", 24),
                                bg=background_color, fg=text_color)
                self.label.place(relx=0.5, rely=0.2, anchor='center')
                self.start_button.place(relx=0.5, rely=0.8, anchor='center')

    def save_test_results(self):
        """儲存測試結果為 JSON 檔案"""
        if not self.test_results:
            print("⚠️ No test results to save | 無測試結果可儲存")
            return
        
        # 計算統計數據
        reaction_times_ms = [t["reaction_time_ms"] for t in self.test_results]
        avg_reaction_time_ms = sum(reaction_times_ms) / len(reaction_times_ms)
        min_reaction_time_ms = min(reaction_times_ms)
        max_reaction_time_ms = max(reaction_times_ms)
        
        # 準備儲存的測試參數
        parameters = {
            "metadata": {
                "test_version": "1.0",
                "data_format_version": "1.0",
                "description": "簡單反應時間測試，測試對視覺刺激的基本反應速度",
                "data_definitions": {
                    "time_units": "reaction_time以秒為單位，reaction_time_ms以毫秒為單位",
                    "reaction_time_definition": "從紅色刺激出現到使用者按下任意按鍵的時間",
                    "stimulus_description": "圓形從白色變為紅色作為GO信號",
                    "premature_response": "在刺激出現前按鍵視為無效，需重新測試"
                }
            },
            "window_size": {
                "width": config.WINDOW_WIDTH,
                "height": config.WINDOW_HEIGHT
            },
            "total_trials": 5,
            "stimulus_delay_range_ms": [1000, 3000],
            "test_procedure": {
                "wait_signal": "圓形顯示為白色",
                "go_signal": "圓形變為紅色",
                "response_window": "刺激出現後無時間限制",
                "inter_trial_interval": "使用者控制，按鍵開始下一回合"
            }
        }
        
        # 準備儲存的指標數據
        metrics = {
            "total_trials": len(self.test_results),
            "average_reaction_time_ms": avg_reaction_time_ms,
            "minimum_reaction_time_ms": min_reaction_time_ms,
            "maximum_reaction_time_ms": max_reaction_time_ms,
            "trials": self.test_results
        }
        
        # 儲存結果
        save_test_result(
            user_id=self.user_id,
            test_name="button_reaction_time",
            metrics=metrics,
            parameters=parameters
        )
        
        print("=" * 50)
        print("📊 測試結果統計")
        print(f"平均反應時間: {avg_reaction_time_ms:.1f} ms")
        print(f"最快反應時間: {min_reaction_time_ms:.1f} ms")
        print(f"最慢反應時間: {max_reaction_time_ms:.1f} ms")
        print("=" * 50)


if __name__ == "__main__":
    from threading import Thread
    from common.controller_input import ControllerInput

    # 解析命令列參數
    parser = argparse.ArgumentParser(description="Button Reaction Time Test")
    parser.add_argument("--user", "-u", default=None, help="User ID | 使用者 ID")
    args = parser.parse_args()

    # 如果沒有提供 user_id，則請求輸入
    user_id = args.user
    if not user_id:
        user_id = input("Please enter User ID (e.g.: P1) | 請輸入使用者 ID (例如: P1): ").strip()
        if not user_id:
            user_id = "default"

    root = tk.Tk()
    app = ReactionTestApp(root, user_id)

    # 使用新的遙控器管理系統 - 會自動使用已配對的遙控器
    # 使用新的遙控器管理系統 - 會自動使用已配對的遙控器
    listener = ControllerInput(button_callback=app.on_joycon_input, use_existing_controller=True)
    Thread(target=listener.run, daemon=True).start()

    root.mainloop()
    print("🎮 SRT Reaction Time Test Complete | SRT 反應時間測試結束")
