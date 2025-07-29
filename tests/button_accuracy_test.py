import tkinter as tk
import random
import time
import sys
import argparse
from pathlib import Path

# 添加父目錄到 Python 路徑以便導入共用模組
sys.path.append(str(Path(__file__).parent.parent))

from common import config
from common.utils import setup_window_topmost, collect_user_info_if_needed
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
        self.progress_label = tk.Label(root, text="", font=("Arial", 24),
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
        self.progress_label.place_forget()  # 隱藏進度標籤
        self.start_button.place(relx=0.5, rely=0.92, anchor='s')

        self.measuring = False
        self.current_target = None
        self.round_start_time = None
        self.waiting_for_input = False  # 新增：等待輸入狀態
        self.score = 0
        self.total = 0
        self.response_times = []
        self.error_count = 0
        self.test_results = []  # 儲存詳細的測試結果
        # 重置所有按鈕顏色
        button_default_color = f"#{config.COLORS['BUTTON_DEFAULT'][0]:02x}{config.COLORS['BUTTON_DEFAULT'][1]:02x}{config.COLORS['BUTTON_DEFAULT'][2]:02x}"
        for cid in self.circles.values():
            self.canvas.itemconfig(cid, fill=button_default_color)

    def start_measurement(self):
        self.label.place_forget()  # 隱藏提示文字
        self.start_button.place_forget()  # 隱藏開始按鈕
        self.progress_label.place(relx=0.5, rely=0.05, anchor='n')  # 顯示進度標籤
        
        # 完整重置測試狀態
        self.response_times.clear()
        self.test_results.clear()
        self.total = 0
        self.score = 0
        self.error_count = 0
        self.measuring = True
        self.current_target = None
        self.round_start_time = None
        self.waiting_for_input = False
        
        # 重置所有按鈕顏色
        button_default_color = f"#{config.COLORS['BUTTON_DEFAULT'][0]:02x}{config.COLORS['BUTTON_DEFAULT'][1]:02x}{config.COLORS['BUTTON_DEFAULT'][2]:02x}"
        for cid in self.circles.values():
            self.canvas.itemconfig(cid, fill=button_default_color)
        
        print("🔄 已重新開始計算！")
        
        # 開始第一回合（熱身測試）
        self.next_round()

    def next_round(self):
        if not self.measuring:
            return
        button_default_color = f"#{config.COLORS['BUTTON_DEFAULT'][0]:02x}{config.COLORS['BUTTON_DEFAULT'][1]:02x}{config.COLORS['BUTTON_DEFAULT'][2]:02x}"
        for cid in self.circles.values():
            self.canvas.itemconfig(cid, fill=button_default_color)
        
        # 更新進度顯示 - 在等待期間就顯示下一輪的進度
        if self.total == 0:
            progress_text = "不計分測試"
        elif self.total >= 1 and self.total <= 10:
            progress_text = f"第 {self.total}/10 次"
        else:
            progress_text = "測試結束"
        
        background_color = f"#{config.COLORS['BACKGROUND'][0]:02x}{config.COLORS['BACKGROUND'][1]:02x}{config.COLORS['BACKGROUND'][2]:02x}"
        text_color = f"#{config.COLORS['TEXT'][0]:02x}{config.COLORS['TEXT'][1]:02x}{config.COLORS['TEXT'][2]:02x}"
        self.progress_label.config(text=progress_text, bg=background_color, fg=text_color)
        
        delay = random.randint(1000, 3000)  # 毫秒，1 到 3 秒
        self.root.after(delay, self.start)

    def start(self):
        self.current_target = random.choice(list(self.directions.keys()))
        error_color = f"#{config.COLORS['ERROR'][0]:02x}{config.COLORS['ERROR'][1]:02x}{config.COLORS['ERROR'][2]:02x}"
        self.canvas.itemconfig(self.circles[self.current_target], fill=error_color)
        self.round_start_time = time.time()
        self.waiting_for_input = True  # 設定等待輸入狀態

    def on_joycon_input(self, buttons, leftX, leftY, last_key_bit,
                        last_key_down):
        if not last_key_down or last_key_bit is None:
            return
        
        # 如果不在測試狀態或沒有開始計時或不等待輸入，忽略輸入
        if not self.measuring or self.round_start_time is None or not self.waiting_for_input:
            return

        for direction, info in self.directions.items():
            if info["bit"] == last_key_bit:
                # 立即設定為不等待輸入，防止重複觸發
                self.waiting_for_input = False
                
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
                    # 檢查是否為熱身測試且答錯
                    if self.total == 1 and not correct:
                        print("❌ 熱身測試答錯，請重新開始熱身測試")
                        self.total = 0  # 重設計數器，重新開始熱身
                        self.root.after(1000, self.next_round)  # 等待 1 秒後重新開始熱身
                        return  # 直接返回，不要繼續執行
                    
                    if self.total == 11:  # 熱身1次 + 正式測試10次 = 總共11次
                        avg_time = sum(self.response_times) / len(
                            self.response_times)
                        error_rate = self.error_count / (self.total - 1)
                        
                        # 儲存測試結果
                        self.save_test_results(avg_time, error_rate)
                        
                        # 設定為測試完成狀態
                        self.measuring = False
                        self.waiting_for_input = False
                        
                        # 更新畫面上方 label
                        background_color = f"#{config.COLORS['BACKGROUND'][0]:02x}{config.COLORS['BACKGROUND'][1]:02x}{config.COLORS['BACKGROUND'][2]:02x}"
                        text_color = f"#{config.COLORS['TEXT'][0]:02x}{config.COLORS['TEXT'][1]:02x}{config.COLORS['TEXT'][2]:02x}"
                        self.progress_label.place_forget()  # 隱藏進度標籤
                        self.label.place(relx=0.5, rely=0.05, anchor='n')  # 顯示結果標籤
                        self.label.config(
                            text=
                            f"測驗結束\n正確率：{(1-error_rate):.1%}｜平均反應時間：{avg_time:.3f} 秒",
                            bg=background_color, fg=text_color
                        )
                        
                        # 重新顯示開始按鈕，讓使用者可以重新開始測試
                        self.start_button.config(text="重新開始")
                        self.start_button.place(relx=0.5, rely=0.92, anchor='s')
                        
                        print(
                            f"📊 平均反應時間：{avg_time:.3f} 秒｜錯誤率：{error_rate:.1%}")
                        print("✅ 測試結果已自動儲存")
                        return  # 直接返回，不要繼續執行下一回合
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
                    elif self.total == 1:  # 第 1 回合是熱身
                        print(f"👟 熱身測試：{'正確' if correct else '錯誤'}，反應時間 {response_time:.3f} 秒")
                        if correct:
                            print("✅ 熱身測試通過，開始正式測試")

                    # 只有在測試還沒結束且還在測試狀態時才安排下一回合
                    if self.measuring:  # 只有在測試狀態時才繼續
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
            "metadata": {
                "test_version": "1.0",
                "data_format_version": "1.0",
                "description": "方向按鍵準確度測試，測試使用者對方向指示的反應準確度",
                "data_definitions": {
                    "time_units": "response_time以秒為單位，response_time_ms以毫秒為單位",
                    "response_time_definition": "從方向指示出現到使用者按下按鍵的時間",
                    "accuracy_definition": "正確按下目標方向按鍵的比例",
                    "warmup_excluded": "第1回合為熱身，不計入統計"
                }
            },
            "window_size": {
                "width": config.WINDOW_WIDTH,
                "height": config.WINDOW_HEIGHT
            },
            "total_trials": 10,  # 第1回合是熱身，實際10回合
            "directions": list(self.directions.keys()),
            "response_delay_range_ms": [1000, 3000],
            "test_flow": {
                "warmup_trials": 1,
                "formal_trials": 10,
                "inter_trial_interval_ms": 1000,
                "stimulus_randomization": "方向隨機出現"
            }
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
    parser.add_argument("--age", type=int, default=None, help="使用者年齡")
    parser.add_argument("--controller-freq", type=int, default=None, help="手把使用頻率 (1-7)")
    args = parser.parse_args()

    # 如果沒有提供 user_id，則請求輸入
    user_id = args.user
    if not user_id:
        user_id = input("請輸入使用者 ID (例如: P1): ").strip()
        if not user_id:
            user_id = "default"

    # 如果通過命令列參數提供了使用者資訊，直接設定到 config
    if args.age is not None and args.controller_freq is not None:
        config.user_info = {
            "user_id": user_id,
            "age": args.age,
            "controller_usage_frequency": args.controller_freq,
            "controller_usage_frequency_description": "1=從來沒用過, 7=每天使用"
        }
        print(f"✅ 使用者 '{user_id}' 的資訊已從命令列參數載入")
    else:
        # 收集使用者基本資訊（如果尚未收集）
        collect_user_info_if_needed(user_id)

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
