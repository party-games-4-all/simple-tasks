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
from common.utils import setup_window_topmost, collect_user_info_if_needed
from common.result_saver import save_test_result
from common.language import set_language, get_text

class CountdownReactionTestApp:

    def __init__(self, root, user_id=None):
        self.root = root
        self.user_id = user_id or "default"
        self.root.title(get_text('window_title_prediction_countdown'))
        
        # 設定視窗關閉處理
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
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
        target_color = f"#{config.COLORS['NEUTRAL'][0]:02x}{config.COLORS['NEUTRAL'][1]:02x}{config.COLORS['NEUTRAL'][2]:02x}"
        self.gray_circle = self.canvas.create_oval(
            self.target_x - self.ball_radius, self.y_pos - self.ball_radius,
            self.target_x + self.ball_radius, self.y_pos + self.ball_radius,
            fill=target_color, outline="")

        background_color = f"#{config.COLORS['BACKGROUND'][0]:02x}{config.COLORS['BACKGROUND'][1]:02x}{config.COLORS['BACKGROUND'][2]:02x}"
        text_color = f"#{config.COLORS['TEXT'][0]:02x}{config.COLORS['TEXT'][1]:02x}{config.COLORS['TEXT'][2]:02x}"
        self.label = tk.Label(root, text=get_text('gui_ready_prediction'), font=("Arial", 24),
                             bg=background_color, fg=text_color)
        self.label.place(relx=0.5, rely=0.2, anchor='center')

        button_default_color = f"#{config.COLORS['BUTTON_DEFAULT'][0]:02x}{config.COLORS['BUTTON_DEFAULT'][1]:02x}{config.COLORS['BUTTON_DEFAULT'][2]:02x}"
        self.start_button = tk.Button(root, text=get_text('gui_start_test'), font=("Arial", 24), command=self.start_test,
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
        print(get_text('ball_launched', 
                      ball_number=ball_number, 
                      launched=self.balls_launched, 
                      total=self.total_balls))

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
                    print(get_text('ball_missed', ball_number=ball_data['number']))
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
            print(get_text('all_balls_processed', total=self.total_balls))
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
        
        print(get_text('button_press_check', count=len(self.active_balls)))
        
        # 找到最合適的球，優先考慮最接近理想擊中時間的球
        for ball_data in self.active_balls:
            if not ball_data['active'] or ball_data['hit'] or ball_data.get('missed', False):
                continue
                
            elapsed = now - ball_data['start_time']
            target_time = 1.0  # 1秒整到達目標位置
            
            print(get_text('ball_elapsed_time', number=ball_data['number'], elapsed=elapsed))
            
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
                    print(get_text('current_best_choice', score=time_penalty))
        
        if best_ball is None:
            # 放寬條件再試一次，但更嚴格
            print(get_text('relaxed_condition_search'))
            for ball_data in self.active_balls:
                if not ball_data['active'] or ball_data['hit'] or ball_data.get('missed', False):
                    continue
                    
                elapsed = now - ball_data['start_time']
                print(get_text('ball_elapsed_relaxed', number=ball_data['number'], elapsed=elapsed))
                
                # 緊急情況下只考慮0.7到1.2秒的球
                if 0.7 <= elapsed <= 1.2:
                    time_penalty = (elapsed - 1.0) ** 2
                    if time_penalty < best_score:
                        best_score = time_penalty
                        best_ball = ball_data
                        print(get_text('relaxed_best_choice'))
        
        if best_ball is None:
            print(get_text('no_suitable_ball'))
            return
            
        # 處理擊中的球
        elapsed = now - best_ball['start_time']
        target_time = 1.0  # 1秒整到達目標位置
        error = elapsed - target_time  # 計算按下的誤差時間
        
        best_ball['active'] = False
        best_ball['hit'] = True
        self.canvas.delete(best_ball['id'])
        
        print(get_text('ball_hit', number=best_ball['number'], elapsed=elapsed))
        
        # 更友善的反饋訊息
        accuracy_ms = abs(error) * 1000
        feedback = ""
        if accuracy_ms < 50:
            feedback = get_text('feedback_perfect')
        elif accuracy_ms < 100:
            feedback = get_text('feedback_great')
        elif accuracy_ms < 200:
            feedback = get_text('feedback_good')
        else:
            feedback = get_text('feedback_practice')
            
        direction = get_text('timing_too_fast') if error < 0 else get_text('timing_too_slow')
        print(get_text('ball_feedback_format', 
                      number=best_ball['number'], 
                      feedback=feedback, 
                      direction=direction, 
                      accuracy=accuracy_ms))
        
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
        print(get_text('test_completing'))
        print("=" * 50)
        
        if valid_errors:
            avg_error_ms = (sum(valid_errors) / len(valid_errors)) * 1000
            
            # 立即儲存測試結果到 JSON 檔案
            self.save_test_results(avg_error_ms, valid_errors)
            
            print(get_text('final_statistics'))
            print(get_text('total_trials_count', count=self.total_balls))
            print(get_text('successful_responses', count=len(valid_errors)))
            print(get_text('missed_responses', count=self.total_balls - len(valid_errors)))
            print(get_text('success_rate_percent', rate=(len(valid_errors) / self.total_balls) * 100))
            print(get_text('average_error_ms', error=avg_error_ms))
        else:
            print(get_text('all_missed_warning'))
            # 即使沒有成功響應也要儲存結果
            self.save_test_results(0, [])
        
        print("=" * 50)
        print(get_text('results_saved_success'))
        print("=" * 50)
        
        # 顯示重新開始界面
        self.label.place(relx=0.5, rely=0.2, anchor='center')
        self.label.config(text=get_text('gui_test_complete_saved'))
        
        background_color = f"#{config.COLORS['BACKGROUND'][0]:02x}{config.COLORS['BACKGROUND'][1]:02x}{config.COLORS['BACKGROUND'][2]:02x}"
        text_color = f"#{config.COLORS['TEXT'][0]:02x}{config.COLORS['TEXT'][1]:02x}{config.COLORS['TEXT'][2]:02x}"
        button_default_color = f"#{config.COLORS['BUTTON_DEFAULT'][0]:02x}{config.COLORS['BUTTON_DEFAULT'][1]:02x}{config.COLORS['BUTTON_DEFAULT'][2]:02x}"
        
        self.start_button = tk.Button(self.root, text=get_text('gui_restart_test'), font=("Arial", 24), command=self.start_test,
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
                    "feedback": get_text('missed_ball_feedback')
                })
        
        # 按球號排序
        self.test_results.sort(key=lambda x: x["trial_number"])
        
        # 準備儲存的測試參數
        parameters = {
            "metadata": {
                "test_version": "1.0",
                "data_format_version": "1.0", 
                "description": "太鼓達人風格預測反應時間測試，球從出現到目標點固定1000ms",
                "data_definitions": {
                    "time_units": "所有時間以毫秒為單位，除非特別註明為秒",
                    "coordinate_system": "畫布座標系統，左上角為(0,0)",
                    "response_time_definition": "從球出現到使用者按下按鍵的時間（秒）",
                    "target_time_definition": "球到達目標區域的理想時間（固定1.0秒）",
                    "error_calculation": "response_time - target_time (負值=提前按，正值=延遲按)"
                }
            },
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
                "y_position": self.y_pos,
                "movement_description": "球從左側滑入，經過目標區域後滑出"
            },
            "timing_definitions": {
                "ball_spawn_to_target": "球從出現到到達目標線的時間（1000ms）",
                "continuous_mode": "多個球可同時在畫面上，間隔500ms生成"
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
            print(get_text('save_result_success'))
        except Exception as e:
            print(get_text('save_result_error', error=e))
        
        print("=" * 50)
        print(get_text('detailed_test_statistics'))
        print(get_text('user_id_label', user_id=self.user_id))
        print(get_text('total_trials_count', count=self.total_balls))
        print(get_text('successful_responses', count=success_count))
        print(get_text('missed_responses', count=missed_count))
        print(get_text('success_rate_percent', rate=success_rate))
        if valid_errors:
            print(get_text('average_error_ms', error=avg_error_ms))
            print(get_text('minimum_error_ms', error=min_error_ms))
            print(get_text('maximum_error_ms', error=max_error_ms))
        print("=" * 50)

    # ← Joy-Con 按鍵會呼叫這個函數
    def on_joycon_input(self, buttons, leftX, leftY, last_key_bit, last_key_down):
        if last_key_down:
            self.register_press()

    def on_closing(self):
        """處理視窗關閉事件"""
        print(get_text('closing_app_safely'))
        
        # 停止測試
        self.game_state = "finished"
        
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
    parser = argparse.ArgumentParser(description="Button Prediction Countdown Test")
    parser.add_argument("--user", "-u", default=None, help=get_text('arg_user_id'))
    parser.add_argument("--age", type=int, default=None, help=get_text('arg_age'))
    parser.add_argument("--controller-freq", type=int, default=None, help=get_text('arg_controller_freq'))
    parser.add_argument("--english", action="store_true", help=get_text('arg_english'))
    args = parser.parse_args()

    # 如果沒有提供 user_id，則請求輸入
    user_id = args.user
    if not user_id:
        user_id = input(get_text('enter_user_id_prompt')).strip()
        if not user_id:
            user_id = "default"

    # 如果通過命令列參數提供了使用者資訊，直接設定到 config
    if args.age is not None and args.controller_freq is not None:
        config.user_info = {
            "user_id": user_id,
            "age": args.age,
            "controller_usage_frequency": args.controller_freq,
            "controller_usage_frequency_description": get_text('controller_usage_freq_desc')
        }
        print(get_text('user_info_loaded_cli', user_id=user_id))
    else:
        # 收集使用者基本資訊（如果尚未收集）
        collect_user_info_if_needed(user_id)

    root = tk.Tk()
    app = CountdownReactionTestApp(root, user_id)

    # 使用新的遙控器管理系統 - 會自動使用已配對的遙控器
    app.listener = ControllerInput(button_callback=app.on_joycon_input,
                                   use_existing_controller=True)
    Thread(target=app.listener.run, daemon=True).start()

    try:
        root.mainloop()
    except KeyboardInterrupt:
        print(get_text('interrupt_signal'))
    finally:
        # 確保清理資源
        if hasattr(app, 'listener') and app.listener:
            app.listener.stop()
        print(get_text('prediction_test_end'))