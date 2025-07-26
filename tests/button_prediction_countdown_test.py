"""
預測反應時間測試 - 遊戲化版本

根據 20250721 會議反饋進行調整：
- 將球移動時間從 250ms 增加到 1200ms，更符合實際 Party Game 節奏
- 增加球與球之間的間隔時間到 2000ms
- 參考 Mario Party 等遊戲的時間設計，讓玩家能夠進行視覺追蹤和預測
- 改進使用者體驗：更友善的反饋訊息和遊戲化介面
- 測試目標：評估玩家在類似真實遊戲情境下的預測能力
- 效能優化：使用主線程動畫取代多線程，減少掉幀問題

設計理念：
不再測試底層的反應速度，而是測試玩家在實際遊戲情境中
結合視覺追蹤和時間預測的綜合能力表現。
"""

import tkinter as tk
import time
import sys
import argparse
from pathlib import Path

# 添加父目錄到 Python 路徑以便導入共用模組
sys.path.append(str(Path(__file__).parent.parent))

from common import config
from common.utils import setup_window_topmost
from common.result_saver import save_test_result

class CountdownReactionTestApp:

    def __init__(self, root, user_id=None):
        self.root = root
        self.user_id = user_id or "default"
        self.root.title("🎮 預測反應時間測試 - 遊戲化版本")
        
        # 設定視窗置頂
        setup_window_topmost(self.root)
        background_color = f"#{config.COLORS['BACKGROUND'][0]:02x}{config.COLORS['BACKGROUND'][1]:02x}{config.COLORS['BACKGROUND'][2]:02x}"
        self.canvas = tk.Canvas(root, width=config.WINDOW_WIDTH, height=config.WINDOW_HEIGHT, bg=background_color)
        self.canvas.pack()

        self.PERIOD = 2000  # 2000ms - 增加球與球之間的間隔時間
        self.CUE_VIEWING_TIME = 1200  # 1200ms - 大幅增加球移動時間，參考 Mario Party 等遊戲節奏
        self.FRAME_INTERVAL = 16  # 約60FPS更新頻率 (1000ms/60 ≈ 16.7ms)

        self.ball_radius = 30
        self.start_x = 100
        self.end_x = config.WINDOW_WIDTH  # 球移動到畫面最右邊（留一點邊距）
        self.target_x = config.WINDOW_WIDTH * 0.9  # 目標判定位置（灰色圓圈位置）
        self.y_pos = config.WINDOW_HEIGHT // 2  # 使用畫面中央

        self.gray_x0 = self.target_x - self.ball_radius
        self.gray_x1 = self.target_x + self.ball_radius
        # self.canvas.create_rectangle(self.gray_x0, 0, self.gray_x1, config.WINDOW_HEIGHT, fill="lightgray", outline="")
        # 在 __init__ 中新增灰色圓形（與球一樣大小）放在 target_x 處
        target_color = f"#{config.COLORS['TARGET'][0]:02x}{config.COLORS['TARGET'][1]:02x}{config.COLORS['TARGET'][2]:02x}"
        self.gray_circle = self.canvas.create_oval(
            self.target_x - self.ball_radius, self.y_pos - self.ball_radius,
            self.target_x + self.ball_radius, self.y_pos + self.ball_radius,
            fill=target_color, outline="")

        background_color = f"#{config.COLORS['BACKGROUND'][0]:02x}{config.COLORS['BACKGROUND'][1]:02x}{config.COLORS['BACKGROUND'][2]:02x}"
        text_color = f"#{config.COLORS['TEXT'][0]:02x}{config.COLORS['TEXT'][1]:02x}{config.COLORS['TEXT'][2]:02x}"
        self.label = tk.Label(root, text="準備好了嗎？請在球到達灰色圓圈時按下按鈕！", font=("Arial", 24),
                             bg=background_color, fg=text_color)
        self.label.place(relx=0.5, rely=0.2, anchor='center')

        button_default_color = f"#{config.COLORS['BUTTON_DEFAULT'][0]:02x}{config.COLORS['BUTTON_DEFAULT'][1]:02x}{config.COLORS['BUTTON_DEFAULT'][2]:02x}"
        self.start_button = tk.Button(root, text="開始測試", font=("Arial", 24), command=self.start_test,
                                     bg=button_default_color, fg=text_color)
        self.start_button.place(relx=0.5, rely=0.8, anchor='center')

        self.reaction_results = []
        self.test_results = []  # 儲存詳細的測試結果
        self.total_balls = 8  # 增加測試次數以獲得更穩定的數據
        self.current_ball_index = 0

        self.ball = None
        self.ball_start_time = None
        self.ball_timer_id = None
        self.next_ball_id = None
        self.ball_active = False
        self.animation_id = None  # 用於動畫循環的ID

    def start_test(self):
        self.start_button.place_forget()
        self.label.place_forget()
        self.current_ball_index = 0

        self.ball = None
        self.ball_start_time = None
        self.ball_timer_id = None
        self.next_ball_id = None
        self.ball_active = False
        self.animation_id = None
        self.reaction_results.clear()
        self.test_results.clear()  # 清空詳細結果
        self.schedule_next_ball()

    def schedule_next_ball(self):
        if self.current_ball_index >= self.total_balls:
            return
        self.next_ball_id = self.root.after(self.PERIOD, self.launch_ball)

    def launch_ball(self):
        self.current_ball_index += 1
        self.schedule_next_ball()
        self.canvas.delete("ball")
        primary_color = f"#{config.COLORS['PRIMARY'][0]:02x}{config.COLORS['PRIMARY'][1]:02x}{config.COLORS['PRIMARY'][2]:02x}"
        self.ball = self.canvas.create_oval(
            self.start_x - self.ball_radius, self.y_pos - self.ball_radius,
            self.start_x + self.ball_radius, self.y_pos + self.ball_radius,
            fill=primary_color, tags="ball"  # 改為藍色，避免與目標區域混淆
        )
        self.ball_start_time = time.time()
        self.ball_active = True
        self.animate_ball()  # 使用主線程動畫而非多線程

    def animate_ball(self):
        """在主線程中進行動畫更新，避免掉幀問題"""
        if not self.ball_active:
            return
            
        elapsed = (time.time() - self.ball_start_time)
        progress = min(elapsed / (self.CUE_VIEWING_TIME / 1000), 1.0)
        x = self.start_x + (self.end_x - self.start_x) * progress

        # 更新球的位置
        self.canvas.coords(self.ball,
            x - self.ball_radius, self.y_pos - self.ball_radius,
            x + self.ball_radius, self.y_pos + self.ball_radius
        )

        # 如果動畫還沒結束，繼續下一幀
        if progress < 1.0 and self.ball_active:
            self.animation_id = self.root.after(self.FRAME_INTERVAL, self.animate_ball)
        elif progress >= 1.0:
            # 球移動到最右邊，如果還沒被按下則視為錯過
            if self.ball_active:
                self.ball_active = False
                self.canvas.delete("ball")
                print("⏰ 錯過了！球已經移動到最右邊")
                self.reaction_results.append(None)
                if self.current_ball_index >= self.total_balls:
                    self.finish_test()

    def register_press(self):
        if not self.ball_active:
            return
        now = time.time()
        elapsed = now - self.ball_start_time
        
        # 計算球在目標位置的理論時間（而非終點時間）
        target_progress = (self.target_x - self.start_x) / (self.end_x - self.start_x)
        target_time = target_progress * (self.CUE_VIEWING_TIME / 1000)
        error = elapsed - target_time  # 計算按下的誤差時間
        
        self.ball_active = False
        self.canvas.delete("ball")
        
        # 取消動畫循環
        if self.animation_id:
            self.root.after_cancel(self.animation_id)
            self.animation_id = None
            
        if self.ball_timer_id:
            self.root.after_cancel(self.ball_timer_id)
        
        # 更友善的反饋訊息
        accuracy_ms = abs(error) * 1000
        feedback = ""
        if accuracy_ms < 50:
            feedback = "🎯 完美！"
        elif accuracy_ms < 100:
            feedback = "👍 很好！"
        elif accuracy_ms < 200:
            feedback = "👌 不錯！"
        else:
            feedback = "💪 再練習一下！"
            
        direction = "快了" if error < 0 else "慢了"
        print(f"{feedback} {direction} {accuracy_ms:.0f} 毫秒")
        
        # 記錄詳細的測試結果
        self.test_results.append({
            "trial_number": self.current_ball_index,
            "response_time_seconds": elapsed,
            "target_time_seconds": target_time,
            "error_seconds": error,
            "error_ms": error * 1000,
            "accuracy_ms": accuracy_ms,
            "feedback": feedback
        })
        
        self.reaction_results.append(error)
        if self.current_ball_index >= self.total_balls:
            self.finish_test()

    def finish_test(self):
        self.canvas.delete("ball")
        self.label.place(relx=0.5, rely=0.2, anchor='center')
        self.label.config(text="測試完成！您的表現很棒！點擊重新開始")
        self.start_button.place(relx=0.5, rely=0.8, anchor='center')
        self.start_button = tk.Button(root, text="重新開始", font=("Arial", 24), command=self.start_test)
        
        # 計算並顯示統計結果
        valid_errors = [abs(e) for e in self.reaction_results if e is not None]
        if valid_errors:
            avg_error_ms = (sum(valid_errors) / len(valid_errors)) * 1000
            
            # 儲存測試結果
            self.save_test_results(avg_error_ms, valid_errors)
            
            print(f"\n🎮 測試完成統計：")
            print(f"平均誤差：{avg_error_ms:.0f} 毫秒")
            print(f"成功次數：{len(valid_errors)}/{self.total_balls}")
        else:
            print("所有測試皆未按下按鈕，請再試一次！")

    def save_test_results(self, avg_error_ms, valid_errors):
        """儲存測試結果為 JSON 檔案"""
        if not self.test_results:
            print("⚠️ 無測試結果可儲存")
            return
        
        # 計算統計數據
        success_count = len(valid_errors)
        success_rate = (success_count / self.total_balls) * 100
        min_error_ms = min(valid_errors) * 1000 if valid_errors else 0
        max_error_ms = max(valid_errors) * 1000 if valid_errors else 0
        
        # 準備儲存的測試參數
        parameters = {
            "window_size": {
                "width": config.WINDOW_WIDTH,
                "height": config.WINDOW_HEIGHT
            },
            "total_balls": self.total_balls,
            "ball_movement_time_ms": self.CUE_VIEWING_TIME,
            "interval_between_balls_ms": self.PERIOD,
            "ball_path": {
                "start_x": self.start_x,
                "target_x": self.target_x,
                "end_x": self.end_x,
                "y_position": self.y_pos
            }
        }
        
        # 準備儲存的指標數據
        metrics = {
            "total_trials": self.total_balls,
            "successful_responses": success_count,
            "missed_responses": self.total_balls - success_count,
            "success_rate_percentage": success_rate,
            "average_error_ms": avg_error_ms,
            "minimum_error_ms": min_error_ms,
            "maximum_error_ms": max_error_ms,
            "trials": self.test_results
        }
        
        # 儲存結果
        save_test_result(
            user_id=self.user_id,
            test_name="button_prediction_countdown",
            metrics=metrics,
            parameters=parameters
        )
        
        print("=" * 50)
        print("📊 測試結果統計")
        print(f"總測試次數: {self.total_balls}")
        print(f"成功響應: {success_count}")
        print(f"錯過響應: {self.total_balls - success_count}")
        print(f"成功率: {success_rate:.1f}%")
        print(f"平均誤差: {avg_error_ms:.1f} ms")
        print("=" * 50)

    # ← Joy-Con 按鍵會呼叫這個函數
    def on_joycon_input(self, buttons, leftX, leftY, last_key_bit, last_key_down):
        if last_key_down:
            self.register_press()

if __name__ == "__main__":
    from threading import Thread
    from common.controller_input import ControllerInput

    # 解析命令列參數
    parser = argparse.ArgumentParser(description="Button Prediction Countdown Test")
    parser.add_argument("--user", "-u", default=None, help="使用者 ID")
    args = parser.parse_args()

    # 如果沒有提供 user_id，則請求輸入
    user_id = args.user
    if not user_id:
        user_id = input("請輸入使用者 ID (例如: P1): ").strip()
        if not user_id:
            user_id = "default"

    root = tk.Tk()
    app = CountdownReactionTestApp(root, user_id)

    # 使用新的遙控器管理系統 - 會自動使用已配對的遙控器
    listener = ControllerInput(button_callback=app.on_joycon_input,
                               use_existing_controller=True)
    Thread(target=listener.run, daemon=True).start()

    root.mainloop()
    print("🎮 預測反應時間測試結束")