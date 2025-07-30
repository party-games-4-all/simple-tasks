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
from common.utils import setup_window_topmost, collect_user_info_if_needed
from common.language import set_language, get_text


class ReactionTestApp:
    """簡單的反應時間測試應用程式"""
    def __init__(self, root, user_id=None):
        self.root = root
        self.user_id = user_id or "default"
        self.root.title(get_text('button_reaction_window_title'))
        
        # 設定視窗關閉處理
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # 設定視窗置頂
        setup_window_topmost(self.root)
        
        self.canvas = tk.Canvas(root, width=config.WINDOW_WIDTH, height=config.WINDOW_HEIGHT, 
                               bg=f"#{config.COLORS['BACKGROUND'][0]:02x}{config.COLORS['BACKGROUND'][1]:02x}{config.COLORS['BACKGROUND'][2]:02x}")
        self.canvas.pack()

        self.state = "waiting"  # 初始狀態
        self.start_time = None
        self.after_id = None
        self.reaction_times = []
        self.test_results = []  # 儲存詳細的測試結果
        self.measuring = False  # 是否在測試中
        self.waiting_for_input = False  # 是否等待輸入
        self.current_trial = 0  # 當前測試次數
        self.total_trials = 10  # 總測試次數

        # 中央圓形（先畫成預設按鈕顏色）
        center_x, center_y = config.WINDOW_WIDTH // 2, config.WINDOW_HEIGHT // 2
        circle_size = 50  # 半徑
        button_default_color = f"#{config.COLORS['BUTTON_DEFAULT'][0]:02x}{config.COLORS['BUTTON_DEFAULT'][1]:02x}{config.COLORS['BUTTON_DEFAULT'][2]:02x}"
        text_color = f"#{config.COLORS['TEXT'][0]:02x}{config.COLORS['TEXT'][1]:02x}{config.COLORS['TEXT'][2]:02x}"
        self.circle = self.canvas.create_oval(center_x - circle_size, center_y - circle_size, 
                                            center_x + circle_size, center_y + circle_size, 
                                            fill=button_default_color, outline=text_color, width=3)

        self.label = tk.Label(root,
                              text=get_text('gui_click_start_test'),
                              font=("Arial", 24),
                              bg=f"#{config.COLORS['BACKGROUND'][0]:02x}{config.COLORS['BACKGROUND'][1]:02x}{config.COLORS['BACKGROUND'][2]:02x}",
                              fg=text_color)
        self.label.place(relx=0.5, rely=0.2, anchor='center')

        self.progress_label = tk.Label(root, text="", font=("Arial", 24),
                                      bg=f"#{config.COLORS['BACKGROUND'][0]:02x}{config.COLORS['BACKGROUND'][1]:02x}{config.COLORS['BACKGROUND'][2]:02x}",
                                      fg=text_color)

        self.start_button = tk.Button(root, text=get_text('gui_start_test'), font=("Arial", 24), command=self.start_test_series,
                                     bg=f"#{config.COLORS['BUTTON_DEFAULT'][0]:02x}{config.COLORS['BUTTON_DEFAULT'][1]:02x}{config.COLORS['BUTTON_DEFAULT'][2]:02x}",
                                     fg=f"#{config.COLORS['TEXT'][0]:02x}{config.COLORS['TEXT'][1]:02x}{config.COLORS['TEXT'][2]:02x}")
        self.start_button.place(relx=0.5, rely=0.8, anchor='center')

    def start_test_series(self):
        """開始整個測試系列"""
        self.label.place_forget()  # 隱藏提示文字
        self.start_button.place_forget()  # 隱藏開始按鈕
        # self.progress_label.place(relx=0.5, rely=0.05, anchor='n')  # 顯示進度標籤（已註解以提升專注度）
        
        self.measuring = True
        self.current_trial = 0
        self.reaction_times.clear()
        self.test_results.clear()
        
        print(get_text('reaction_test_started'))
        # 開始第一次測試
        self.next_trial()

    def next_trial(self):
        """開始下一次測試"""
        if not self.measuring:
            return
            
        self.current_trial += 1
        
        # 檢查是否已完成所有測試
        if self.current_trial > self.total_trials:
            return
        
        # 更新進度顯示（註解化以提升專注度）
        # progress_text = f"第 {self.current_trial}/{self.total_trials} 次"
        # background_color = f"#{config.COLORS['BACKGROUND'][0]:02x}{config.COLORS['BACKGROUND'][1]:02x}{config.COLORS['BACKGROUND'][2]:02x}"
        # text_color = f"#{config.COLORS['TEXT'][0]:02x}{config.COLORS['TEXT'][1]:02x}{config.COLORS['TEXT'][2]:02x}"
        # self.progress_label.config(text=progress_text, bg=background_color, fg=text_color)
        
        # 重置圓形顏色
        button_default_color = f"#{config.COLORS['BUTTON_DEFAULT'][0]:02x}{config.COLORS['BUTTON_DEFAULT'][1]:02x}{config.COLORS['BUTTON_DEFAULT'][2]:02x}"
        self.canvas.itemconfig(self.circle, fill=button_default_color)
        
        self.state = "waiting_to_start"  # 新狀態：等待開始
        self.waiting_for_input = False
        
        # 等待1秒後進入準備階段
        self.root.after(1000, self.enter_ready_state)
    
    def enter_ready_state(self):
        """進入準備狀態"""
        if not self.measuring:
            return
        self.state = "ready"
        self.set_random_timer()

    def start_test(self):
        """開始單次測試（已廢棄，保留以避免錯誤）"""
        pass

    def set_random_timer(self):
        delay = random.randint(1000, 3000)  # 隨機延遲 1~3 秒
        self.after_id = self.root.after(delay, self.turn_red)

    def turn_red(self):
        error_color = f"#{config.COLORS['ERROR'][0]:02x}{config.COLORS['ERROR'][1]:02x}{config.COLORS['ERROR'][2]:02x}"
        self.canvas.itemconfig(self.circle, fill=error_color)  # 使用色盲友善的錯誤顏色
        # self.label.config(text="快按 Joy-Con！", font=("Arial", 32))
        self.state = "go"
        self.waiting_for_input = True
        self.start_time = time.time()

    def on_joycon_input(self, buttons, leftX, leftY, last_key_bit, last_key_down):
        if not last_key_down:
            return  # 只處理按下事件（不處理放開）

        # 如果不在測試狀態，忽略輸入
        if not self.measuring:
            return

        if self.state == "waiting_to_start":
            # 在等待開始階段，完全忽略輸入
            return

        elif self.state == "ready":
            # 在準備狀態按鈕被按下，表示太早
            print(get_text('too_fast_restart', trial=self.current_trial))
            if self.after_id:
                self.root.after_cancel(self.after_id)
            # 重新開始當前測試（不改變 current_trial）
            self.current_trial -= 1  # 因為 next_trial 會 +1，所以這裡先 -1
            self.next_trial()

        elif self.state == "go" and self.waiting_for_input:
            # 正確的反應
            self.waiting_for_input = False  # 立即設定為不等待輸入
            reaction_time = time.time() - self.start_time
            self.reaction_times.append(reaction_time)
            
            # 記錄詳細的測試結果
            self.test_results.append({
                "trial_number": self.current_trial,
                "reaction_time_ms": reaction_time * 1000,
                "reaction_time_seconds": reaction_time
            })
            
            print(get_text('reaction_time_result', trial=self.current_trial, time=reaction_time))
            success_color = f"#{config.COLORS['SUCCESS'][0]:02x}{config.COLORS['SUCCESS'][1]:02x}{config.COLORS['SUCCESS'][2]:02x}"
            self.canvas.itemconfig(self.circle, fill=success_color)
            self.state = "completed_trial"  # 新狀態：完成測試

            if self.current_trial < self.total_trials:
                # 等待1秒後開始下一次測試
                self.root.after(1000, self.next_trial)
            else:
                # 測試完成
                avg_time = sum(self.reaction_times) / len(self.reaction_times)
                print(get_text('average_reaction_time', time=avg_time))
                
                # 儲存測試結果
                self.save_test_results()
                
                # 顯示結果並重置
                self.show_completion(avg_time)

    def show_completion(self, avg_time):
        """顯示測試完成結果"""
        self.measuring = False
        self.state = "waiting"  # 重置狀態
        self.waiting_for_input = False
        self.current_trial = 0  # 重置測試次數
        # self.progress_label.place_forget()  # 隱藏進度標籤（已註解因為不再顯示）
        
        text_color = f"#{config.COLORS['TEXT'][0]:02x}{config.COLORS['TEXT'][1]:02x}{config.COLORS['TEXT'][2]:02x}"
        background_color = f"#{config.COLORS['BACKGROUND'][0]:02x}{config.COLORS['BACKGROUND'][1]:02x}{config.COLORS['BACKGROUND'][2]:02x}"
        
        self.label.config(
            text=get_text('gui_test_complete_reaction', time=avg_time), 
            font=("Arial", 20),
            bg=background_color, 
            fg=text_color
        )
        self.label.place(relx=0.5, rely=0.2, anchor='center')
        self.start_button.place(relx=0.5, rely=0.8, anchor='center')

    def save_test_results(self):
        """儲存測試結果為 JSON 檔案"""
        if not self.test_results:
            print(get_text('no_results_to_save'))
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
            "total_trials": 10,
            "stimulus_delay_range_ms": [1000, 3000],
            "test_procedure": {
                "wait_signal": "圓形顯示為白色",
                "go_signal": "圓形變為紅色",
                "response_window": "刺激出現後無時間限制",
                "inter_trial_interval_ms": 1000,
                "premature_response_handling": "重新開始當前測試"
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
        print(get_text('test_statistics'))
        print(get_text('avg_reaction_time_ms', time=avg_reaction_time_ms))
        print(get_text('min_reaction_time_ms', time=min_reaction_time_ms))
        print(get_text('max_reaction_time_ms', time=max_reaction_time_ms))
        print("=" * 50)

    def on_closing(self):
        """處理視窗關閉事件"""
        print(get_text('closing_app'))
        
        # 停止測試
        self.measuring = False
        
        # 取消任何待執行的計時器
        if self.after_id:
            self.root.after_cancel(self.after_id)
        
        # 停止控制器執行緒（如果存在）
        if hasattr(self, 'listener') and self.listener:
            self.listener.stop()
        
        # 關閉視窗
        self.root.quit()
        self.root.destroy()


if __name__ == "__main__":
    from threading import Thread
    from common.controller_input import ControllerInput

    # 檢查是否有 --english 參數來提前設定語言
    if '--english' in sys.argv:
        set_language('en')
    else:
        set_language('zh')

    # 解析命令列參數
    parser = argparse.ArgumentParser(description=get_text('button_reaction_test_description'))
    parser.add_argument("--user", "-u", default=None, help=get_text('arg_user_id'))
    parser.add_argument("--age", type=int, default=None, help=get_text('arg_age'))
    parser.add_argument("--controller-freq", type=int, default=None, help=get_text('arg_controller_freq'))
    parser.add_argument("--english", action="store_true", help=get_text('arg_english'))
    args = parser.parse_args()

    # 如果沒有提供 user_id，則請求輸入
    user_id = args.user
    if not user_id:
        user_id = input(get_text('user_id_input_prompt')).strip()
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
        print(get_text('user_info_from_cli', user_id=user_id))
    else:
        # 收集使用者基本資訊（如果尚未收集）
        collect_user_info_if_needed(user_id)

    root = tk.Tk()
    app = ReactionTestApp(root, user_id)

    # 使用新的遙控器管理系統 - 會自動使用已配對的遙控器
    app.listener = ControllerInput(button_callback=app.on_joycon_input, use_existing_controller=True)
    Thread(target=app.listener.run, daemon=True).start()

    try:
        root.mainloop()
    except KeyboardInterrupt:
        print(f"\n{get_text('received_interrupt')}")
    finally:
        # 確保清理資源
        if hasattr(app, 'listener') and app.listener:
            app.listener.stop()
        print(get_text('reaction_test_end'))
