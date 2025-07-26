import tkinter as tk
import random
import time
import sys
import argparse
from pathlib import Path

# 添加父目錄到 Python 路徑以便導入共用模組
sys.path.append(str(Path(__file__).parent.parent))

from common import config
from common.utils import setup_window_topmost
from common.result_saver import save_test_result


class AccuracyDirectionTestApp:

    def __init__(self, root, user_id=None):
        self.root = root
        self.user_id = user_id or "default"
        self.root.title("按鍵準確度測試")
        
        # 設定視窗置頂
        setup_window_topmost(self.root)
        background_color = f"#{config.COLORS['BACKGROUND'][0]:02x}{config.COLORS['BACKGROUND'][1]:02x}{config.COLORS['BACKGROUND'][2]:02x}"
        self.canvas = tk.Canvas(root, width=config.WINDOW_WIDTH, height=config.WINDOW_HEIGHT, bg=background_color)
        self.canvas.pack()

        # 計算中心位置和方向按鈕位置
        center_x, center_y = config.WINDOW_WIDTH // 2, config.WINDOW_HEIGHT // 2
        button_distance = 150  # 按鈕距離中心的距離
        
        # 調整為正菱形排列（正方形旋轉45度），符合真實控制器外觀
        # 使用45度角的對角線距離來計算位置
        diagonal_distance = button_distance * 1.414  # sqrt(2) ≈ 1.414
        
        self.directions = {
            "up": {
                "pos": (center_x, center_y - diagonal_distance),
                "bit": None
            },
            "down": {
                "pos": (center_x, center_y + diagonal_distance),
                "bit": None
            },
            "left": {
                "pos": (center_x - diagonal_distance, center_y),
                "bit": None
            },
            "right": {
                "pos": (center_x + diagonal_distance, center_y),
                "bit": None
            },
        }

        self.circles = {}
        button_default_color = f"#{config.COLORS['BUTTON_DEFAULT'][0]:02x}{config.COLORS['BUTTON_DEFAULT'][1]:02x}{config.COLORS['BUTTON_DEFAULT'][2]:02x}"
        text_color = f"#{config.COLORS['TEXT'][0]:02x}{config.COLORS['TEXT'][1]:02x}{config.COLORS['TEXT'][2]:02x}"
        for dir, info in self.directions.items():
            x, y = info["pos"]
            self.circles[dir] = self.canvas.create_oval(x - 50,
                                                        y - 50,
                                                        x + 50,
                                                        y + 50,
                                                        fill=button_default_color,
                                                        outline=text_color,
                                                        width=3)
            # self.canvas.create_text(x, y, text=dir.upper(), font=("Arial", 16))

        self.label = tk.Label(root, text="請按亮起的方向鍵", font=("Arial", 32),
                             bg=background_color, fg=text_color)
        self.start_button = tk.Button(root,
                                      text="開始計算",
                                      font=("Arial", 24),
                                      command=self.start_measurement,
                                      bg=button_default_color,
                                      fg=text_color)
        self.reset()

    def reset(self):
        self.label.place(relx=0.5, rely=0.05, anchor='n')
        self.start_button.place(relx=0.5, rely=0.92, anchor='s')

        self.measuring = False
        self.current_target = None
        self.round_start_time = None
        self.score = 0
        self.total = 0
        self.response_times = []
        self.error_count = 0
        self.test_results = []  # 儲存詳細的測試結果
        self.next_round()

    def start_measurement(self):
        self.label.place_forget()  # 隱藏提示文字
        self.start_button.place_forget()  # 隱藏開始按鈕
        self.response_times.clear()
        self.total = 0
        self.score = 0
        self.error_count = 0
        self.measuring = True
        print("🔄 已重新開始計算！")

    def next_round(self):
        button_default_color = f"#{config.COLORS['BUTTON_DEFAULT'][0]:02x}{config.COLORS['BUTTON_DEFAULT'][1]:02x}{config.COLORS['BUTTON_DEFAULT'][2]:02x}"
        for cid in self.circles.values():
            self.canvas.itemconfig(cid, fill=button_default_color)
        delay = random.randint(1000, 3000)  # 毫秒，1 到 3 秒
        self.root.after(delay, self.start)

    def start(self):
        self.current_target = random.choice(list(self.directions.keys()))
        error_color = f"#{config.COLORS['ERROR'][0]:02x}{config.COLORS['ERROR'][1]:02x}{config.COLORS['ERROR'][2]:02x}"
        self.canvas.itemconfig(self.circles[self.current_target], fill=error_color)
        self.round_start_time = time.time()

    def on_joycon_input(self, buttons, leftX, leftY, last_key_bit,
                        last_key_down):
        if not last_key_down or last_key_bit is None:
            return

        for direction, info in self.directions.items():
            if info["bit"] == last_key_bit:
                response_time = time.time() - self.round_start_time

                if direction == self.current_target:
                    success_color = f"#{config.COLORS['SUCCESS'][0]:02x}{config.COLORS['SUCCESS'][1]:02x}{config.COLORS['SUCCESS'][2]:02x}"
                    self.canvas.itemconfig(self.circles[direction],
                                           fill=success_color)
                    # self.label.config(text="✅ 正確！")
                    correct = True
                    self.score += 1
                else:
                    neutral_color = f"#{config.COLORS['NEUTRAL'][0]:02x}{config.COLORS['NEUTRAL'][1]:02x}{config.COLORS['NEUTRAL'][2]:02x}"
                    self.canvas.itemconfig(self.circles[direction],
                                           fill=neutral_color)
                    # self.label.config(text=f"❌ 錯誤！正確是 {self.current_target.upper()}")
                    correct = False
                    self.error_count += 1

                self.total += 1

                if self.measuring:
                    if self.total > 5:
                        avg_time = sum(self.response_times) / len(
                            self.response_times)
                        error_rate = self.error_count / (self.total - 1)
                        
                        # 儲存測試結果
                        self.save_test_results(avg_time, error_rate)
                        
                        # 更新畫面上方 label
                        background_color = f"#{config.COLORS['BACKGROUND'][0]:02x}{config.COLORS['BACKGROUND'][1]:02x}{config.COLORS['BACKGROUND'][2]:02x}"
                        text_color = f"#{config.COLORS['TEXT'][0]:02x}{config.COLORS['TEXT'][1]:02x}{config.COLORS['TEXT'][2]:02x}"
                        self.label.config(
                            text=
                            f"測驗結束\n正確率：{(1-error_rate):.1%}｜平均反應時間：{avg_time:.3f} 秒",
                            bg=background_color, fg=text_color
                        )
                        print(
                            f"📊 平均反應時間：{avg_time:.3f} 秒｜錯誤率：{error_rate:.1%}")
                        self.reset()
                        break
                    if self.total > 1:  # 第 1 回合不記錄
                        # 記錄詳細的測試結果
                        self.test_results.append({
                            "trial_number": self.total - 1,
                            "target_direction": self.current_target,
                            "response_direction": direction,
                            "correct": correct,
                            "response_time_ms": response_time * 1000,
                            "response_time_seconds": response_time
                        })
                        
                        self.response_times.append(response_time)
                        # # 更新畫面上方 label
                        # self.label.config(
                        #     text=f"正確率：{(1-error_rate):.1%}｜平均反應時間：{avg_time:.3f} 秒"
                        # )
                        print(
                            f"🔘 回合 {self.total-1}：{'正確' if correct else '錯誤'}，反應時間 {response_time:.3f} 秒"
                        )
                    else:
                        print("👟 第 1 回合為熱身，不納入統計。")

                self.root.after(1000, self.next_round)  # 等待 1 秒後開始下一回合
                break

    def save_test_results(self, avg_time, error_rate):
        """儲存測試結果為 JSON 檔案"""
        if not self.test_results:
            print("⚠️ 無測試結果可儲存")
            return
        
        # 計算統計數據
        correct_count = sum(1 for t in self.test_results if t["correct"])
        total_trials = len(self.test_results)
        accuracy_percentage = (correct_count / total_trials) * 100
        
        # 準備儲存的測試參數
        parameters = {
            "window_size": {
                "width": config.WINDOW_WIDTH,
                "height": config.WINDOW_HEIGHT
            },
            "total_trials": 5,  # 第1回合是熱身，實際5回合
            "directions": list(self.directions.keys()),
            "response_delay_range_ms": [1000, 3000]
        }
        
        # 準備儲存的指標數據
        metrics = {
            "total_trials": total_trials,
            "correct_responses": correct_count,
            "incorrect_responses": total_trials - correct_count,
            "accuracy_percentage": accuracy_percentage,
            "error_rate": error_rate,
            "average_response_time_ms": avg_time * 1000,
            "average_response_time_seconds": avg_time,
            "trials": self.test_results
        }
        
        # 儲存結果
        save_test_result(
            user_id=self.user_id,
            test_name="button_accuracy",
            metrics=metrics,
            parameters=parameters
        )
        
        print("=" * 50)
        print("📊 測試結果統計")
        print(f"總回合數: {total_trials}")
        print(f"正確回合: {correct_count}")
        print(f"錯誤回合: {total_trials - correct_count}")
        print(f"正確率: {accuracy_percentage:.1f}%")
        print(f"平均反應時間: {avg_time:.3f} 秒")
        print("=" * 50)


if __name__ == "__main__":
    from threading import Thread
    from common.controller_input import ControllerInput

    # 解析命令列參數
    parser = argparse.ArgumentParser(description="Button Accuracy Test")
    parser.add_argument("--user", "-u", default=None, help="使用者 ID")
    args = parser.parse_args()

    # 如果沒有提供 user_id，則請求輸入
    user_id = args.user
    if not user_id:
        user_id = input("請輸入使用者 ID (例如: P1): ").strip()
        if not user_id:
            user_id = "default"

    root = tk.Tk()
    app = AccuracyDirectionTestApp(root, user_id)

    # 根據你的 Joy-Con 對應設定 bit 值
    app.directions["up"]["bit"] = 3
    app.directions["down"]["bit"] = 0
    app.directions["left"]["bit"] = 2
    app.directions["right"]["bit"] = 1

    # 使用新的遙控器管理系統 - 會自動使用已配對的遙控器
    listener = ControllerInput(button_callback=app.on_joycon_input,
                               use_existing_controller=True)
    Thread(target=listener.run, daemon=True).start()

    root.mainloop()
    print("🎮 CRT 反應時間測試結束")
