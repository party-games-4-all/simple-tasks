"""
預測反應時間測試 - 太鼓達人風格版本

根據 20250727 會議反饋進行調整：
- 球從出現到目標點固定為 1000ms (1秒整)
- 球與球之間間隔 500ms (0.5秒)
- 一次出現 10 個球，實現連續性測試效果
- 類似太鼓達人的節奏遊戲體驗
- 多個球可以同時在畫面上移動
- 玩家可以按任意順序擊中球，系統會自動選擇最適合的球
- 效能優化：使用主線程動畫，支援多球同時動畫

設計理念：
測試玩家在連續節拍下的預測反應能力，
模擬真實音樂遊戲中的多目標追蹤和時間預測能力。
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

        self.BALL_INTERVAL = 500  # 500ms - 球與球之間的間隔時間（0.5秒）
        self.CUE_VIEWING_TIME = 1000  # 1000ms - 球從出現到目標點的時間（1秒整）
        self.FRAME_INTERVAL = 16  # 約60FPS更新頻率 (1000ms/60 ≈ 16.7ms)

        self.ball_radius = 30
        self.start_x = 100
        self.target_x = config.WINDOW_WIDTH * 0.7  # 目標判定位置移動到偏向中間（原本0.9改為0.7）
        self.end_x = config.WINDOW_WIDTH - 50  # 球移動到畫面最右邊（留一點邊距）
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
        self.total_balls = 10  # 改為一次出現10個球
        self.balls_launched = 0  # 記錄已發射的球數
        self.active_balls = []  # 儲存所有活躍的球

        self.ball = None
        self.ball_start_time = None
        self.ball_timer_id = None
        self.next_ball_id = None
        self.ball_active = False
        self.animation_id = None  # 用於動畫循環的ID

    def start_test(self):
        self.start_button.place_forget()
        self.label.place_forget()
        self.balls_launched = 0

        self.ball = None
        self.ball_start_time = None
        self.ball_timer_id = None
        self.next_ball_id = None
        self.ball_active = False
        self.animation_id = None
        self.active_balls = []
        self.reaction_results.clear()
        self.test_results.clear()  # 清空詳細結果
        self.schedule_all_balls()
        self.animate_all_balls()

    def schedule_all_balls(self):
        """安排所有10個球的出現時間"""
        for i in range(self.total_balls):
            delay = i * self.BALL_INTERVAL  # 每個球間隔0.5秒出現
            self.root.after(delay, lambda ball_num=i+1: self.launch_ball(ball_num))

    def launch_ball(self, ball_number):
        """發射一個新球"""
        primary_color = f"#{config.COLORS['PRIMARY'][0]:02x}{config.COLORS['PRIMARY'][1]:02x}{config.COLORS['PRIMARY'][2]:02x}"
        ball_obj = self.canvas.create_oval(
            self.start_x - self.ball_radius, self.y_pos - self.ball_radius,
            self.start_x + self.ball_radius, self.y_pos + self.ball_radius,
            fill=primary_color, tags=f"ball_{ball_number}"
        )
        
        ball_data = {
            'id': ball_obj,
            'number': ball_number,
            'start_time': time.time(),
            'active': True,
            'hit': False
        }
        self.active_balls.append(ball_data)
        self.balls_launched += 1
        print(f"🚀 發射第 {ball_number} 個球 (已發射: {self.balls_launched}/{self.total_balls})")

    def animate_all_balls(self):
        """同時動畫所有活躍的球"""
        current_time = time.time()
        balls_to_remove = []
        
        for ball_data in self.active_balls:
            if not ball_data['active']:
                continue
                
            elapsed = current_time - ball_data['start_time']
            
            # 計算球的位置：前1秒從start_x移動到target_x，之後繼續移動到end_x
            if elapsed <= 1.0:
                # 前1秒：從起點移動到目標點
                progress = elapsed  # 0到1秒的進度
                x = self.start_x + (self.target_x - self.start_x) * progress
            else:
                # 超過1秒：從目標點繼續移動到終點
                extra_time = elapsed - 1.0
                # 計算從目標點到終點需要的時間（假設保持相同速度）
                remaining_distance = self.end_x - self.target_x
                target_distance = self.target_x - self.start_x
                remaining_time_needed = remaining_distance / target_distance  # 按比例計算剩餘時間
                
                if extra_time <= remaining_time_needed:
                    extra_progress = extra_time / remaining_time_needed
                    x = self.target_x + (self.end_x - self.target_x) * extra_progress
                else:
                    x = self.end_x  # 已經到達終點

            # 更新球的位置
            self.canvas.coords(ball_data['id'],
                x - self.ball_radius, self.y_pos - self.ball_radius,
                x + self.ball_radius, self.y_pos + self.ball_radius
            )

            # 檢查是否錯過目標點（球經過目標位置但沒被擊中）
            # 當球超過目標位置一定距離後標記為錯過
            if elapsed >= 1.25 and ball_data['active'] and not ball_data['hit']:
                # 標記為錯過，但不立即移除，讓球繼續移動
                if not ball_data.get('missed', False):  # 避免重複記錄
                    ball_data['missed'] = True
                    print(f"⏰ 錯過了第 {ball_data['number']} 個球！球繼續往右移動...")
                    self.reaction_results.append(None)

            # 當球完全跑出畫面右邊時才移除
            if x > self.end_x + self.ball_radius:
                ball_data['active'] = False
                self.canvas.delete(ball_data['id'])
                balls_to_remove.append(ball_data)
        
        # 移除已完成的球
        for ball_data in balls_to_remove:
            self.active_balls.remove(ball_data)

        # 檢查是否所有球都已被處理完畢（擊中或錯過）
        all_balls_launched = (self.balls_launched >= self.total_balls)
        all_balls_processed = (len(self.reaction_results) >= self.total_balls)
        
        if all_balls_launched and all_balls_processed:
            print(f"✅ 所有 {self.total_balls} 顆球已處理完畢，結束測試")
            self.finish_test()
            return

        # 繼續動畫循環
        self.animation_id = self.root.after(self.FRAME_INTERVAL, self.animate_all_balls)

    def register_press(self):
        """處理按鍵，找到最接近目標位置的球"""
        if not self.active_balls:
            return
            
        now = time.time()
        best_ball = None
        best_score = float('inf')
        
        print(f"⚡ 按鍵時刻，檢查 {len(self.active_balls)} 個活躍球:")
        
        # 找到最合適的球，優先考慮最接近理想擊中時間的球
        for ball_data in self.active_balls:
            if not ball_data['active'] or ball_data['hit'] or ball_data.get('missed', False):
                continue
                
            elapsed = now - ball_data['start_time']
            target_time = 1.0  # 1秒整到達目標位置
            
            print(f"  球 {ball_data['number']}: 經過時間 {elapsed:.2f}s")
            
            # 只考慮在合理時間範圍內的球（0.5秒到1.3秒之間）
            if 0.5 <= elapsed <= 1.3:
                # 計算綜合評分：優先考慮接近1.0秒的球
                # 使用平方來放大差異，讓更接近的球獲得更高優先級
                time_penalty = (elapsed - target_time) ** 2
                
                # 如果球已經超過目標時間太多，增加懲罰
                if elapsed > 1.1:
                    time_penalty *= 2  # 對於太晚的球增加懲罰
                
                if time_penalty < best_score:
                    best_score = time_penalty
                    best_ball = ball_data
                    print(f"    -> 目前最佳選擇 (評分: {time_penalty:.4f})")
        
        if best_ball is None:
            # 放寬條件再試一次，但更嚴格
            print("  第一輪未找到，放寬條件...")
            for ball_data in self.active_balls:
                if not ball_data['active'] or ball_data['hit'] or ball_data.get('missed', False):
                    continue
                    
                elapsed = now - ball_data['start_time']
                print(f"  球 {ball_data['number']} (放寬): 經過時間 {elapsed:.2f}s")
                
                # 緊急情況下只考慮0.7到1.2秒的球
                if 0.7 <= elapsed <= 1.2:
                    time_penalty = (elapsed - 1.0) ** 2
                    if time_penalty < best_score:
                        best_score = time_penalty
                        best_ball = ball_data
                        print(f"    -> 放寬條件下最佳選擇")
        
        if best_ball is None:
            print("⚠️ 沒有找到適合的球！")
            return
            
        # 處理擊中的球
        elapsed = now - best_ball['start_time']
        target_time = 1.0  # 1秒整到達目標位置
        error = elapsed - target_time  # 計算按下的誤差時間
        
        best_ball['active'] = False
        best_ball['hit'] = True
        self.canvas.delete(best_ball['id'])
        
        print(f"🎯 擊中球 {best_ball['number']} (經過時間: {elapsed:.2f}s)")
        
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
        print(f"球 {best_ball['number']}: {feedback} {direction} {accuracy_ms:.0f} 毫秒")
        
        # 記錄詳細的測試結果
        self.test_results.append({
            "trial_number": best_ball['number'],
            "response_time_seconds": elapsed,
            "target_time_seconds": target_time,
            "error_seconds": error,
            "error_ms": error * 1000,
            "accuracy_ms": accuracy_ms,
            "feedback": feedback
        })
        
        self.reaction_results.append(error)

    def finish_test(self):
        # 清理所有剩餘的球
        for ball_data in self.active_balls:
            self.canvas.delete(ball_data['id'])
        self.active_balls.clear()
        
        # 取消動畫循環
        if self.animation_id:
            self.root.after_cancel(self.animation_id)
            self.animation_id = None
            
        # 計算並顯示統計結果
        valid_errors = [abs(e) for e in self.reaction_results if e is not None]
        
        print("\n" + "=" * 50)
        print("🎮 測試完成！正在輸出結果...")
        print("=" * 50)
        
        if valid_errors:
            avg_error_ms = (sum(valid_errors) / len(valid_errors)) * 1000
            
            # 立即儲存測試結果到 JSON 檔案
            self.save_test_results(avg_error_ms, valid_errors)
            
            print(f"📊 最終統計結果：")
            print(f"總測試次數: {self.total_balls}")
            print(f"成功響應: {len(valid_errors)}")
            print(f"錯過響應: {self.total_balls - len(valid_errors)}")
            print(f"成功率: {(len(valid_errors) / self.total_balls) * 100:.1f}%")
            print(f"平均誤差: {avg_error_ms:.1f} ms")
        else:
            print("⚠️ 所有測試皆未按下按鈕")
            # 即使沒有成功響應也要儲存結果
            self.save_test_results(0, [])
        
        print("=" * 50)
        print("✅ 結果已成功儲存到 JSON 檔案")
        print("=" * 50)
        
        # 顯示重新開始界面
        self.label.place(relx=0.5, rely=0.2, anchor='center')
        self.label.config(text="測試完成！結果已儲存。點擊重新開始")
        
        background_color = f"#{config.COLORS['BACKGROUND'][0]:02x}{config.COLORS['BACKGROUND'][1]:02x}{config.COLORS['BACKGROUND'][2]:02x}"
        text_color = f"#{config.COLORS['TEXT'][0]:02x}{config.COLORS['TEXT'][1]:02x}{config.COLORS['TEXT'][2]:02x}"
        button_default_color = f"#{config.COLORS['BUTTON_DEFAULT'][0]:02x}{config.COLORS['BUTTON_DEFAULT'][1]:02x}{config.COLORS['BUTTON_DEFAULT'][2]:02x}"
        
        self.start_button = tk.Button(self.root, text="重新開始", font=("Arial", 24), command=self.start_test,
                                     bg=button_default_color, fg=text_color)
        self.start_button.place(relx=0.5, rely=0.8, anchor='center')

    def save_test_results(self, avg_error_ms, valid_errors):
        """儲存測試結果為 JSON 檔案"""
        
        # 計算統計數據
        success_count = len(valid_errors)
        missed_count = self.total_balls - success_count
        success_rate = (success_count / self.total_balls) * 100 if self.total_balls > 0 else 0
        min_error_ms = min(valid_errors) * 1000 if valid_errors else 0
        max_error_ms = max(valid_errors) * 1000 if valid_errors else 0
        
        # 確保 test_results 包含所有球的資訊（包括錯過的）
        processed_balls = set(result["trial_number"] for result in self.test_results)
        for i in range(1, self.total_balls + 1):
            if i not in processed_balls:
                # 為錯過的球添加記錄
                self.test_results.append({
                    "trial_number": i,
                    "response_time_seconds": None,
                    "target_time_seconds": 1.0,
                    "error_seconds": None,
                    "error_ms": None,
                    "accuracy_ms": None,
                    "feedback": "錯過"
                })
        
        # 按球號排序
        self.test_results.sort(key=lambda x: x["trial_number"])
        
        # 準備儲存的測試參數
        parameters = {
            "window_size": {
                "width": config.WINDOW_WIDTH,
                "height": config.WINDOW_HEIGHT
            },
            "total_balls": self.total_balls,
            "ball_movement_time_ms": self.CUE_VIEWING_TIME,
            "ball_interval_ms": self.BALL_INTERVAL,
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
            "missed_responses": missed_count,
            "success_rate_percentage": success_rate,
            "average_error_ms": avg_error_ms,
            "minimum_error_ms": min_error_ms,
            "maximum_error_ms": max_error_ms,
            "trials": self.test_results
        }
        
        # 儲存結果
        try:
            save_test_result(
                user_id=self.user_id,
                test_name="button_prediction_countdown",
                metrics=metrics,
                parameters=parameters
            )
            print(f"💾 測試結果已成功儲存！")
        except Exception as e:
            print(f"❌ 儲存結果時發生錯誤: {e}")
        
        print("=" * 50)
        print("📊 詳細測試結果統計")
        print(f"使用者 ID: {self.user_id}")
        print(f"總測試次數: {self.total_balls}")
        print(f"成功響應: {success_count}")
        print(f"錯過響應: {missed_count}")
        print(f"成功率: {success_rate:.1f}%")
        if valid_errors:
            print(f"平均誤差: {avg_error_ms:.1f} ms")
            print(f"最小誤差: {min_error_ms:.1f} ms")
            print(f"最大誤差: {max_error_ms:.1f} ms")
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