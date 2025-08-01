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
    
    def __init__(self, root, user_id=None):
        self.root = root
        self.user_id = user_id or "default"
        self.root.title(get_text('button_smash_window_title'))
        
        # 設定視窗關閉處理
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # 設定視窗置頂
        setup_window_topmost(self.root)
        background_color = f"#{config.COLORS['BACKGROUND'][0]:02x}{config.COLORS['BACKGROUND'][1]:02x}{config.COLORS['BACKGROUND'][2]:02x}"
        self.canvas = tk.Canvas(root, width=config.WINDOW_WIDTH, height=config.WINDOW_HEIGHT, bg=background_color)
        self.canvas.pack()

        # 測試狀態
        self.state = "waiting"  # waiting, testing, finished
        self.start_time = None
        self.test_duration = 10.0  # 10 秒測試時間
        self.click_count = 0
        self.timer_id = None
        self.click_timestamps = []  # 記錄每次點擊的時間戳
        self.button_pressed = False  # 防止重複觸發
        self.designated_button = None  # 指定的按鈕（第一次按下的按鈕）
        
        # 視覺元素
        self.circle_radius = 80
        self.circle_x = 600
        self.circle_y = 400
        
        # 創建圓形按鈕（根據會議回饋：初始為白底）
        button_default_color = f"#{config.COLORS['BUTTON_DEFAULT'][0]:02x}{config.COLORS['BUTTON_DEFAULT'][1]:02x}{config.COLORS['BUTTON_DEFAULT'][2]:02x}"
        text_color = f"#{config.COLORS['TEXT'][0]:02x}{config.COLORS['TEXT'][1]:02x}{config.COLORS['TEXT'][2]:02x}"
        self.circle = self.canvas.create_oval(
            self.circle_x - self.circle_radius, 
            self.circle_y - self.circle_radius,
            self.circle_x + self.circle_radius, 
            self.circle_y + self.circle_radius,
            fill=button_default_color, 
            outline=text_color, 
            width=3
        )
        
        # X 符號（初始隱藏）
        self.x_symbol = self.canvas.create_text(
            self.circle_x, self.circle_y,
            text="✕",
            font=("Arial", 48, "bold"),
            fill=text_color,
            state="hidden"
        )
        
        # 計時顯示
        self.timer_text = self.canvas.create_text(
            600, 200,
            text="",
            font=("Arial", 32),
            fill=text_color
        )
        
        # CPS 顯示
        primary_color = f"#{config.COLORS['PRIMARY'][0]:02x}{config.COLORS['PRIMARY'][1]:02x}{config.COLORS['PRIMARY'][2]:02x}"
        self.cps_text = self.canvas.create_text(
            600, 600,
            text="",
            font=("Arial", 24),
            fill=primary_color
        )

        # 指示文字
        background_color = f"#{config.COLORS['BACKGROUND'][0]:02x}{config.COLORS['BACKGROUND'][1]:02x}{config.COLORS['BACKGROUND'][2]:02x}"
        text_color = f"#{config.COLORS['TEXT'][0]:02x}{config.COLORS['TEXT'][1]:02x}{config.COLORS['TEXT'][2]:02x}"
        self.label = tk.Label(root,
                              text=get_text('gui_smash_instructions'),
                              font=("Arial", 20),
                              bg=background_color,
                              fg=text_color)
        self.label.place(relx=0.5, rely=0.1, anchor='center')

        # 開始按鈕
        button_default_color = f"#{config.COLORS['BUTTON_DEFAULT'][0]:02x}{config.COLORS['BUTTON_DEFAULT'][1]:02x}{config.COLORS['BUTTON_DEFAULT'][2]:02x}"
        self.start_button = tk.Button(root, 
                                      text=get_text('gui_start_test'), 
                                      font=("Arial", 24), 
                                      command=self.start_test,
                                      bg=button_default_color,
                                      fg=text_color)
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
        self.click_timestamps = []  # 清空點擊時間戳記錄
        self.designated_button = None  # 重置指定按鈕
        
        # 隱藏開始按鈕和說明文字
        self.start_button.place_forget()
        self.label.place_forget()
        
        # 重置視覺元素（根據會議回饋：使用白底，依靠 X 符號而非顏色）
        button_default_color = f"#{config.COLORS['BUTTON_DEFAULT'][0]:02x}{config.COLORS['BUTTON_DEFAULT'][1]:02x}{config.COLORS['BUTTON_DEFAULT'][2]:02x}"
        self.canvas.itemconfig(self.circle, fill=button_default_color)
        self.canvas.itemconfig(self.x_symbol, state="hidden")
        self.canvas.itemconfig(self.timer_text, text=get_text('gui_waiting_first_click'))
        self.canvas.itemconfig(self.cps_text, text="")
        
        print(get_text('button_smash_test_started'))

    def update_timer(self):
        """更新計時器顯示"""
        if self.state != "testing" or self.start_time is None:
            return
            
        elapsed = time.time() - self.start_time
        remaining = max(0, self.test_duration - elapsed)
        
        if remaining > 0:
            self.canvas.itemconfig(self.timer_text, 
                                   text=get_text('gui_remaining_time', time=remaining))
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
        
        # 儲存測試結果
        self.save_test_results(cps)
        
        # 顯示結果
        self.canvas.itemconfig(self.timer_text, text=get_text('gui_test_complete_smash'))
        self.canvas.itemconfig(self.cps_text, 
                               text=get_text('gui_smash_results', count=self.click_count, cps=cps, duration=self.test_duration))
        
        # 重置圓形和 X 符號（根據會議回饋：使用白底而非灰色）
        button_default_color = f"#{config.COLORS['BUTTON_DEFAULT'][0]:02x}{config.COLORS['BUTTON_DEFAULT'][1]:02x}{config.COLORS['BUTTON_DEFAULT'][2]:02x}"
        self.canvas.itemconfig(self.circle, fill=button_default_color)
        self.canvas.itemconfig(self.x_symbol, state="hidden")
        
        # 顯示重新開始按鈕
        background_color = f"#{config.COLORS['BACKGROUND'][0]:02x}{config.COLORS['BACKGROUND'][1]:02x}{config.COLORS['BACKGROUND'][2]:02x}"
        text_color = f"#{config.COLORS['TEXT'][0]:02x}{config.COLORS['TEXT'][1]:02x}{config.COLORS['TEXT'][2]:02x}"
        self.label.config(text=get_text('gui_smash_final', count=self.click_count, cps=cps),
                         bg=background_color, fg=text_color)
        self.label.place(relx=0.5, rely=0.1, anchor='center')
        self.start_button.place(relx=0.5, rely=0.85, anchor='center')
        
        print(get_text('button_smash_test_complete_msg'))
        print(get_text('button_smash_total_clicks', count=self.click_count))
        print(get_text('button_smash_test_time', duration=self.test_duration))
        print(f"🖱️ CPS (Clicks Per Second): {cps:.2f}")
        print(get_text('button_smash_cps_calculation', count=self.click_count, duration=self.test_duration, cps=cps))

    def save_test_results(self, cps):
        """儲存測試結果為 JSON 檔案"""
        # 準備儲存的測試參數
        parameters = {
            "metadata": {
                "test_version": "1.0",
                "data_format_version": "1.0",
                "description": "按鍵連擊速度測試，測試在固定時間內的最大點擊頻率",
                "data_definitions": {
                    "time_units": "test_duration以秒為單位",
                    "cps_calculation": "CPS = 總點擊數 ÷ 測試持續時間",
                    "timing_start": "第一次點擊開始計時，而非測試開始時計時",
                    "click_definition": "任意按鍵按下都計為一次點擊"
                }
            },
            "window_size": {
                "width": config.WINDOW_WIDTH,
                "height": config.WINDOW_HEIGHT
            },
            "test_duration_seconds": self.test_duration,
            "button_position": {
                "x": self.circle_x,
                "y": self.circle_y,
                "radius": self.circle_radius
            },
            "test_mechanics": {
                "timing_trigger": "第一次點擊開始計時",
                "duration_fixed": f"{self.test_duration}秒固定時間",
                "visual_feedback": "X符號顯示點擊，圓形保持白色",
                "accessibility": "依靠X符號而非顏色變化提供回饋"
            }
        }
        
        # 計算點擊間隔和節奏分析
        click_intervals = []
        if len(self.click_timestamps) > 1:
            for i in range(1, len(self.click_timestamps)):
                interval = self.click_timestamps[i]["relative_time_ms"] - self.click_timestamps[i-1]["relative_time_ms"]
                click_intervals.append(interval)
        
        avg_interval = sum(click_intervals) / len(click_intervals) if click_intervals else 0
        interval_variance = sum((x - avg_interval)**2 for x in click_intervals) / len(click_intervals) if click_intervals else 0

        # 準備儲存的指標數據
        metrics = {
            "total_clicks": self.click_count,
            "test_duration_seconds": self.test_duration,
            "clicks_per_second": cps,
            "performance_rating": self.get_performance_rating(cps),
            "click_timestamps": self.click_timestamps,
            "rhythm_analysis": {
                "click_intervals_ms": click_intervals,
                "average_interval_ms": avg_interval,
                "interval_variance": interval_variance,
                "rhythm_consistency": "低變異數表示節奏穩定" if interval_variance < 1000 else "高變異數表示節奏不穩定"
            },
            "temporal_distribution": {
                "first_second_clicks": len([c for c in self.click_timestamps if c["relative_time_ms"] <= 1000]),
                "last_second_clicks": len([c for c in self.click_timestamps if c["relative_time_ms"] >= 9000]),
                "middle_period_clicks": len([c for c in self.click_timestamps if 1000 < c["relative_time_ms"] < 9000])
            }
        }
        
        # 儲存結果
        save_test_result(
            user_id=self.user_id,
            test_name="button_smash",
            metrics=metrics,
            parameters=parameters
        )
        
        print("=" * 50)
        print(get_text('button_smash_test_statistics'))
        print(get_text('button_smash_total_clicks', count=self.click_count))
        print(get_text('button_smash_test_time', duration=self.test_duration))
        print(get_text('button_smash_click_rate', cps=cps))
        print(get_text('button_smash_performance_rating', rating=self.get_performance_rating(cps)))
        print("=" * 50)

    def get_performance_rating(self, cps):
        """根據 CPS 給出表現評級"""
        if cps >= 10:
            return get_text('button_smash_excellent')
        elif cps >= 8:
            return get_text('button_smash_good')
        elif cps >= 6:
            return get_text('button_smash_average')
        elif cps >= 4:
            return get_text('button_smash_needs_practice')
        else:
            return get_text('button_smash_beginner')

    def on_joycon_input(self, buttons, leftX, leftY, last_key_bit, last_key_down):
        """處理 Joy-Con 輸入"""
        
        # 如果在等待狀態，不處理手把輸入（開始測試只能用滑鼠）
        if self.state == "waiting":
            return
        
        # 如果不是按鍵事件，忽略
        if last_key_bit is None:
            return
        
        # 如果已經指定按鈕，檢查是否為同一按鈕
        if self.designated_button is not None and last_key_bit != self.designated_button:
            return  # 不是指定的按鈕，忽略
            
        if last_key_down:
            # 按鍵按下 - 如果是第一次按下，記錄為指定按鈕
            if self.designated_button is None:
                self.designated_button = last_key_bit
                print(get_text('button_smash_designated_button', button=last_key_bit))
            self.on_button_press()
        else:
            # 按鍵放開 - 只處理指定按鈕的放開事件
            if last_key_bit == self.designated_button:
                self.on_button_release()

    def on_button_press(self):
        """處理按鍵按下事件"""
        if self.button_pressed:
            return  # 避免重複觸發
            
        self.button_pressed = True
        
        # 在測試狀態才處理按鈕輸入，等待狀態只能用滑鼠點擊開始按鈕
        if self.state == "testing":
            # 如果是第一次點擊，開始計時
            if self.start_time is None:
                self.start_time = time.time()
                self.update_timer()
                print(get_text('button_smash_start_timing'))
            
            # 檢查是否還在測試時間內
            current_time = time.time()
            if self.start_time and (current_time - self.start_time) < self.test_duration:
                self.click_count += 1
                
                # 記錄點擊時間戳
                click_timestamp = {
                    "click_number": self.click_count,
                    "absolute_time": current_time,
                    "relative_time_ms": (current_time - self.start_time) * 1000
                }
                self.click_timestamps.append(click_timestamp)
                
                print(get_text('button_smash_click_record', count=self.click_count, time=click_timestamp['relative_time_ms']))
                
                # 視覺回饋：按下時顯示 X 符號（色盲友善設計）
                button_active_color = f"#{config.COLORS['BUTTON_ACTIVE'][0]:02x}{config.COLORS['BUTTON_ACTIVE'][1]:02x}{config.COLORS['BUTTON_ACTIVE'][2]:02x}"
                self.canvas.itemconfig(self.circle, fill=button_active_color)  # 使用色盲友善的按鈕啟動色
                self.canvas.itemconfig(self.x_symbol, state="normal")

    def on_button_release(self):
        """處理按鍵放開事件"""
        if not self.button_pressed:
            return
            
        self.button_pressed = False
        
        if self.state == "testing":
            # 視覺回饋：放開時恢復原色並隱藏 X（主要依靠形狀變化，而非顏色）
            button_default_color = f"#{config.COLORS['BUTTON_DEFAULT'][0]:02x}{config.COLORS['BUTTON_DEFAULT'][1]:02x}{config.COLORS['BUTTON_DEFAULT'][2]:02x}"
            self.canvas.itemconfig(self.circle, fill=button_default_color)
            self.canvas.itemconfig(self.x_symbol, state="hidden")

    def on_keyboard_press(self, event):
        """處理鍵盤按下事件（測試備用）"""
        # 只在測試狀態才處理鍵盤輸入
        if event.keysym == 'space' and self.state == "testing":  # 空白鍵
            self.on_button_press()

    def on_keyboard_release(self, event):
        """處理鍵盤放開事件（測試備用）"""
        # 只在測試狀態才處理鍵盤輸入
        if event.keysym == 'space' and self.state == "testing":  # 空白鍵
            self.on_button_release()

    def on_closing(self):
        """處理視窗關閉事件"""
        print("🔄 正在安全關閉應用程式...")
        
        # 停止測試
        self.state = "finished"
        
        # 取消任何待執行的計時器
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
        
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
    parser = argparse.ArgumentParser(description=get_text('button_smash_test_description'))
    parser.add_argument("--user", "-u", default=None, help=get_text('arg_user_id'))
    parser.add_argument("--age", type=int, default=None, help=get_text('arg_age'))
    parser.add_argument("--controller-freq", type=int, default=None, help=get_text('arg_controller_freq'))
    parser.add_argument("--test", action="store_true", help=get_text('button_smash_test_mode_help'))
    parser.add_argument("--english", action="store_true", help=get_text('arg_english'))
    args = parser.parse_args()

    # 如果沒有提供 user_id，則請求輸入
    user_id = args.user
    if not user_id and not args.test:
        user_id = input(get_text('user_id_input_prompt')).strip()
        if not user_id:
            user_id = "default"

    # 如果通過命令列參數提供了使用者資訊，直接設定到 config
    if args.age is not None and args.controller_freq is not None and not args.test:
        config.user_info = {
            "user_id": user_id,
            "age": args.age,
            "controller_usage_frequency": args.controller_freq,
            "controller_usage_frequency_description": "1=從來沒用過, 7=每天使用"
        }
        print(get_text('button_smash_user_info_loaded', user_id=user_id))
    elif not args.test:
        # 收集使用者基本資訊（如果尚未收集）
        collect_user_info_if_needed(user_id)

    root = tk.Tk()
    app = ButtonSmashTestApp(root, user_id)

    # 檢查是否有測試參數
    if args.test:
        # 測試模式：模擬點擊來驗證 CPS 計算
        print(get_text('button_smash_test_mode_verify'))
        
        # 模擬 25 次點擊，應該得到 2.5 CPS
        app.start_test()
        app.start_time = time.time()
        app.click_count = 25
        app.finish_test()
        
        print(get_text('button_smash_test_complete_verify'))
        root.destroy()
        sys.exit(0)

    # 設定手把輸入監聽
    # 使用新的遙控器管理系統 - 會自動使用已配對的遙控器
    app.listener = ControllerInput(button_callback=app.on_joycon_input,
                                   use_existing_controller=True)
    Thread(target=app.listener.run, daemon=True).start()

    try:
        root.mainloop()
    except KeyboardInterrupt:
        print(f"\n{get_text('button_smash_interrupt_signal')}")
    finally:
        # 確保清理資源
        if hasattr(app, 'listener') and app.listener:
            app.listener.stop()
        print(get_text('button_smash_test_end'))
