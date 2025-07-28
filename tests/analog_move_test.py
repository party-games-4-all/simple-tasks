import tkinter as tk
import random
import time
from threading import Thread
import sys
from pathlib import Path

# 添加父目錄到 Python 路徑以便導入共用模組
sys.path.append(str(Path(__file__).parent.parent))

from common import config
from common.result_saver import save_test_result
from common.trace_plot import init_trace_output_folder, output_move_trace
from common.utils import setup_window_topmost


class JoystickTargetTestApp:

    def __init__(self, root, user_id=None):
        self.root = root
        self.user_id = user_id or "default"
        self.root.title("Joystick 移動目標測試")
        
        # 設定視窗置頂
        setup_window_topmost(self.root)
        
        self.canvas_width = config.WINDOW_WIDTH
        self.canvas_height = config.WINDOW_HEIGHT
        background_color = f"#{config.COLORS['BACKGROUND'][0]:02x}{config.COLORS['BACKGROUND'][1]:02x}{config.COLORS['BACKGROUND'][2]:02x}"
        self.canvas = tk.Canvas(root,
                                width=self.canvas_width,
                                height=self.canvas_height,
                                bg=background_color)
        self.canvas.pack()

        text_color = f"#{config.COLORS['TEXT'][0]:02x}{config.COLORS['TEXT'][1]:02x}{config.COLORS['TEXT'][2]:02x}"
        self.label = tk.Label(root,
                              text="按『開始測試』後先進行暖身，然後正式測試",
                              font=("Arial", 24),
                              bg=background_color,
                              fg=text_color)
        self.label.place(relx=0.5, rely=0.02, anchor='n')

        button_default_color = f"#{config.COLORS['BUTTON_DEFAULT'][0]:02x}{config.COLORS['BUTTON_DEFAULT'][1]:02x}{config.COLORS['BUTTON_DEFAULT'][2]:02x}"
        self.start_button = tk.Button(root,
                                      text="開始測試",
                                      font=("Arial", 24),
                                      command=self.start_test,
                                      bg=button_default_color,
                                      fg=text_color)
        self.start_button.place(relx=0.5, rely=0.95, anchor='s')

        # self.target_radius = 30
        self.player_radius = 10

        self.target = None
        self.player = None

        self.start_time = None
        self.has_moved = False
        self.total_time = 0
        self.success_count = 0
        self.testing = False
        self.total_efficiency = 0  # 用來計算時間 / 距離
        
        # 記錄所有測試結果用於 JSON 儲存
        self.test_results = []

        self.player_x = self.canvas_width // 2
        self.player_y = self.canvas_height // 2

        self.target_x = 0
        self.target_y = 0

        self.leftX = 0
        self.leftY = 0

        self.trace_points = []  # 當前軌跡
        self.press_trace = []
        self.output_dir = init_trace_output_folder("analog_move", self.user_id)

        # ISO9241 標準九點圓形測試設計
        # 從中心點 (600, 400) 距離 300 像素的圓周上設置 9 個點
        # 每個點相隔 40 度 (360/9)
        self.center_x = self.canvas_width // 2  # 600
        self.center_y = self.canvas_height // 2  # 400
        self.distance = 300  # 長距離
        self.short_distance = 100  # 短距離
        
        # 生成 9 個長距離圓周點的座標
        import math
        self.circle_points = []
        for i in range(9):
            angle = i * (360 / 9) * math.pi / 180  # 轉換為弧度
            x = self.center_x + self.distance * math.cos(angle)
            y = self.center_y + self.distance * math.sin(angle)
            self.circle_points.append((x, y))
        
        # 生成 9 個短距離圓周點的座標
        self.short_circle_points = []
        for i in range(9):
            angle = i * (360 / 9) * math.pi / 180  # 轉換為弧度
            x = self.center_x + self.short_distance * math.cos(angle)
            y = self.center_y + self.short_distance * math.sin(angle)
            self.short_circle_points.append((x, y))
        
        # 測試序列：從位置1開始，到對面順時針的下一個位置
        # 位置編號：0=右(0°), 1=右下(40°), 2=下右(80°), 3=下左(120°), 4=左下(160°), 
        #          5=左(200°), 6=左上(240°), 7=上左(280°), 8=上右(320°)
        self.test_sequence = [1, 6, 2, 7, 3, 8, 4, 0, 5]  # 從1開始，每次跳到對面順時針下一個
        
        # 固定目標組合：增加第零次測試 + 先測試所有大目標，再測試所有小目標
        self.fixed_targets = []
        
        # 第零次測試：移動到最後一個位置（不計入正式結果）
        last_pos_index = self.test_sequence[-1]  # 最後一個位置
        x, y = self.circle_points[last_pos_index]
        self.fixed_targets.append({
            "x": x,
            "y": y,
            "radius": 30,  # 使用中等大小的目標
            "sequence_index": 0,
            "position_index": last_pos_index,
            "size_type": "warmup",
            "is_warmup": True
        })
        
        # 先添加大目標 (radius=50) - 完整的9個位置 (長距離)
        for i, pos_index in enumerate(self.test_sequence):
            x, y = self.circle_points[pos_index]
            self.fixed_targets.append({
                "x": x,
                "y": y,
                "radius": 50,
                "sequence_index": i + 1,
                "position_index": pos_index,
                "size_type": "large",
                "is_warmup": False,
                "distance_type": "long"
            })
        
        # 再添加小目標 (radius=20) - 完整的9個位置 (長距離)
        for i, pos_index in enumerate(self.test_sequence):
            x, y = self.circle_points[pos_index]
            self.fixed_targets.append({
                "x": x,
                "y": y,
                "radius": 20,
                "sequence_index": i + 1,
                "position_index": pos_index,
                "size_type": "small",
                "is_warmup": False,
                "distance_type": "long"
            })
        
        # 添加短距離大目標 (radius=50) - 完整的9個位置 (短距離)
        for i, pos_index in enumerate(self.test_sequence):
            x, y = self.short_circle_points[pos_index]
            self.fixed_targets.append({
                "x": x,
                "y": y,
                "radius": 50,
                "sequence_index": i + 1,
                "position_index": pos_index,
                "size_type": "large",
                "is_warmup": False,
                "distance_type": "short"
            })
        
        # 添加短距離小目標 (radius=20) - 完整的9個位置 (短距離)
        for i, pos_index in enumerate(self.test_sequence):
            x, y = self.short_circle_points[pos_index]
            self.fixed_targets.append({
                "x": x,
                "y": y,
                "radius": 20,
                "sequence_index": i + 1,
                "position_index": pos_index,
                "size_type": "small",
                "is_warmup": False,
                "distance_type": "short"
            })
        
        # 不打亂順序，保持測試的一致性

        self.spawn_target()
        Thread(target=self.player_loop, daemon=True).start()

    def player_loop(self):
        while True:
            if self.testing:
                self.update_player_position()
            time.sleep(0.016)  # 約 60fps

    def start_test(self):
        if self.success_count >= len(self.fixed_targets):
            self.label.config(text="✅ 測驗完成")
            return

        self.testing = True
        self.total_time = 0
        self.label.config(text="")
        self.start_button.place_forget()  # 隱藏按鈕
        self.spawn_target()
        self.has_moved = False  # 重設第一次移動判定

    def spawn_target(self):
        self.canvas.delete("all")

        # 只在第一次測試時重置玩家位置到中心點
        if self.success_count == 0:
            self.player_x = self.center_x
            self.player_y = self.center_y

        if self.success_count >= len(self.fixed_targets):
            self.label.config(text="✅ 測驗完成")
            return

        target_index = self.success_count
        target_info = self.fixed_targets[target_index]
        self.target_x = target_info["x"]
        self.target_y = target_info["y"]
        self.target_radius = target_info["radius"]

        # 計算從當前位置到目標的實際距離
        self.initial_distance = ((self.player_x - self.target_x)**2 +
                                 (self.player_y - self.target_y)**2)**0.5

        target_color = f"#{config.COLORS['TARGET'][0]:02x}{config.COLORS['TARGET'][1]:02x}{config.COLORS['TARGET'][2]:02x}"
        self.target = self.canvas.create_oval(
            self.target_x - self.target_radius,
            self.target_y - self.target_radius,
            self.target_x + self.target_radius,
            self.target_y + self.target_radius,
            fill=target_color)
        primary_color = f"#{config.COLORS['PRIMARY'][0]:02x}{config.COLORS['PRIMARY'][1]:02x}{config.COLORS['PRIMARY'][2]:02x}"
        self.player = self.canvas.create_oval(
            self.player_x - self.player_radius,
            self.player_y - self.player_radius,
            self.player_x + self.player_radius,
            self.player_y + self.player_radius,
            fill=primary_color)

    def update_player_position(self):
        # 將 -1 ~ 1 值轉換為 -13 ~ +13 的速度
        dx = (self.leftX) * 13
        dy = (self.leftY) * 13

        self.player_x += dx
        self.player_y += dy

        # 限制在畫布內
        self.player_x = max(
            self.player_radius,
            min(self.canvas_width - self.player_radius, self.player_x))
        self.player_y = max(
            self.player_radius,
            min(self.canvas_height - self.player_radius, self.player_y))

        self.canvas.coords(self.player, self.player_x - self.player_radius,
                           self.player_y - self.player_radius,
                           self.player_x + self.player_radius,
                           self.player_y + self.player_radius)

        if self.testing:
            self.trace_points.append((self.player_x, self.player_y))

    def on_joycon_input(self, buttons, leftX, leftY, last_key_bit,
                        last_key_down):
        self.leftX = leftX
        self.leftY = leftY

        # 如果第一次移動，開始計時
        if not self.has_moved and (leftX != 0 or leftY != 0):
            self.start_time = time.time()
            self.has_moved = True

    def on_joycon_button(self, buttons, leftX, leftY, last_key_bit,
                         last_key_down):
        # 若按下任一按鍵（例如 A 鍵），進行位置判定
        if not last_key_down:
            return  # 只處理按下事件（不處理放開）

        if not self.testing:
            return

        # 以 1 號鍵為例，可視需要調整
        if last_key_bit != 1:  # 你可以改成任意你想用的按鍵編號
            return

        self.press_trace.append((self.player_x, self.player_y))

        distance = ((self.player_x - self.target_x)**2 +
                    (self.player_y - self.target_y)**2)**0.5
        if distance <= self.target_radius:
            elapsed = time.time() - self.start_time
            self.success_count += 1

            # 獲取當前目標資訊
            current_target_info = self.fixed_targets[self.success_count - 1]
            
            # 判斷是否為暖身測試
            is_warmup = current_target_info.get("is_warmup", False)
            
            if not is_warmup:
                # 只有非暖身測試才計入統計
                efficiency = elapsed / self.initial_distance
                self.total_time += elapsed
                self.total_efficiency += efficiency

                formal_count = self.success_count - 1  # 扣除暖身測試
                avg_time = self.total_time / formal_count if formal_count > 0 else 0
                avg_efficiency = self.total_efficiency / formal_count if formal_count > 0 else 0

                # 記錄起始位置以便軌跡輸出
                start_position = (self.trace_points[0] if self.trace_points else (self.player_x, self.player_y))

                # 記錄單次測試結果
                trial_result = {
                    "trial_number": formal_count,
                    "target_x": self.target_x,
                    "target_y": self.target_y,
                    "target_radius": self.target_radius,
                    "initial_distance": self.initial_distance,
                    "completion_time_ms": elapsed * 1000,  # 轉換為毫秒
                    "efficiency_s_per_px": efficiency,
                    "trace_points_count": len(self.trace_points),
                    "press_points_count": len(self.press_trace),
                    "sequence_index": current_target_info.get("sequence_index", 0),
                    "position_index": current_target_info.get("position_index", 0),
                    "size_type": current_target_info.get("size_type", "unknown"),
                    "distance_type": current_target_info.get("distance_type", "unknown")
                }
                self.test_results.append(trial_result)

                print(f"✅ 第 {formal_count} 次成功")
                print(f"🎯 位置：{current_target_info.get('position_index', 'N/A')} ({current_target_info.get('size_type', 'N/A')}-{current_target_info.get('distance_type', 'N/A')})")
                print(f"⏱ 用時：{elapsed:.2f} 秒")
                print(f"📏 距離：{self.initial_distance:.1f} px")
                print(f"⚡ 單位距離時間：{efficiency:.4f} 秒/像素")
                print(f"📊 平均時間：{avg_time:.2f} 秒，平均秒/像素：{avg_efficiency:.4f}")
                self.label.config(text=(f"第 {formal_count} 次"))
            else:
                # 暖身測試
                print(f"🏃 暖身測試完成")
                print(f"⏱ 用時：{elapsed:.2f} 秒")
                print(f"📏 距離：{self.initial_distance:.1f} px")
                print(f"🎯 現在開始正式測試...")
                self.label.config(text="暖身完成，開始正式測試")
                
            self.testing = False
            
            # 輸出軌跡圖（包括暖身測試）
            if not is_warmup:
                # 正式測試使用實際的測試編號
                start_position = (self.trace_points[0] if self.trace_points else (self.player_x, self.player_y))
                output_move_trace(
                    trace_points=self.trace_points,
                    start=start_position,
                    target=(self.target_x, self.target_y),
                    radius=self.target_radius,
                    player_radius=self.player_radius,
                    press_points=self.press_trace,
                    index=formal_count,  # 使用正式測試編號
                    output_dir=self.output_dir
                )
            else:
                # 暖身測試使用特殊編號
                start_position = (self.trace_points[0] if self.trace_points else (self.player_x, self.player_y))
                output_move_trace(
                    trace_points=self.trace_points,
                    start=start_position,
                    target=(self.target_x, self.target_y),
                    radius=self.target_radius,
                    player_radius=self.player_radius,
                    press_points=self.press_trace,
                    index=0,  # 暖身測試編號為0
                    output_dir=self.output_dir
                )
            
            self.trace_points = []  # 清空以便下次測試
            self.press_trace = []
            
            # 如果測試完成，儲存 JSON 結果
            if self.success_count >= len(self.fixed_targets):
                self.save_test_results()
            
            time.sleep(1)  # 等待 1 秒後再開始下一個目標
            self.start_test()  # 重新開始測試

    def save_test_results(self):
        """儲存測試結果為 JSON 檔案"""
        if not self.test_results:
            print("⚠️ 無測試結果可儲存")
            return
        
        # 計算總體統計
        total_trials = len(self.test_results)
        avg_time = self.total_time / total_trials
        avg_efficiency = self.total_efficiency / total_trials
        
        # 分析不同難度的表現 - 基於新的ISO9241九點測試 (四種組合)
        long_large_trials = [t for t in self.test_results if t["target_radius"] == 50 and t.get("distance_type", "long") == "long"]
        long_small_trials = [t for t in self.test_results if t["target_radius"] == 20 and t.get("distance_type", "long") == "long"]
        short_large_trials = [t for t in self.test_results if t["target_radius"] == 50 and t.get("distance_type", "short") == "short"]
        short_small_trials = [t for t in self.test_results if t["target_radius"] == 20 and t.get("distance_type", "short") == "short"]
        
        # 準備儲存的測試參數
        parameters = {
            "window_size": {
                "width": self.canvas_width,
                "height": self.canvas_height
            },
            "player_radius": self.player_radius,
            "movement_speed_multiplier": 13,
            "total_targets": len(self.fixed_targets),
            "formal_test_count": len(self.fixed_targets) - 1,  # 扣除暖身測試
            "has_warmup": True,
            "iso9241_config": {
                "standard": "ISO9241多方向指向測試",
                "center_point": [self.center_x, self.center_y],
                "long_circle_radius": self.distance,
                "short_circle_radius": self.short_distance,
                "total_positions": 9,
                "angle_separation": 40,  # 度
                "target_sizes": [20, 50],  # 像素
                "distance_types": ["long", "short"],  # 距離類型
                "test_sequence": self.test_sequence,
                "warmup_target_size": 30,  # 暖身測試目標大小
                "test_combinations": {
                    "long_large": f"距離{self.distance}px，目標50px",
                    "long_small": f"距離{self.distance}px，目標20px", 
                    "short_large": f"距離{self.short_distance}px，目標50px",
                    "short_small": f"距離{self.short_distance}px，目標20px"
                }
            }
        }
        
        # 準備儲存的指標數據
        metrics = {
            "total_trials": total_trials,
            "total_time_seconds": self.total_time,
            "average_time_seconds": avg_time,
            "average_efficiency_s_per_px": avg_efficiency,
            "trials": self.test_results,
            "difficulty_analysis": {
                "long_large_d300_w50": {
                    "count": len(long_large_trials),
                    "avg_time_ms": sum(t["completion_time_ms"] for t in long_large_trials) / len(long_large_trials) if long_large_trials else 0,
                    "description": "ISO9241九點圓形測試 - 長距離大目標 (半徑50px, 距離300px)"
                },
                "long_small_d300_w20": {
                    "count": len(long_small_trials),
                    "avg_time_ms": sum(t["completion_time_ms"] for t in long_small_trials) / len(long_small_trials) if long_small_trials else 0,
                    "description": "ISO9241九點圓形測試 - 長距離小目標 (半徑20px, 距離300px)"
                },
                "short_large_d100_w50": {
                    "count": len(short_large_trials),
                    "avg_time_ms": sum(t["completion_time_ms"] for t in short_large_trials) / len(short_large_trials) if short_large_trials else 0,
                    "description": "ISO9241九點圓形測試 - 短距離大目標 (半徑50px, 距離100px)"
                },
                "short_small_d100_w20": {
                    "count": len(short_small_trials),
                    "avg_time_ms": sum(t["completion_time_ms"] for t in short_small_trials) / len(short_small_trials) if short_small_trials else 0,
                    "description": "ISO9241九點圓形測試 - 短距離小目標 (半徑20px, 距離100px)"
                }
            },
            "iso9241_info": {
                "standard": "ISO9241多方向指向測試",
                "total_positions": 9,
                "long_circle_radius": self.distance,
                "short_circle_radius": self.short_distance,
                "test_sequence": self.test_sequence,
                "position_angles": [i * 40 for i in range(9)]  # 每個位置的角度
            }
        }
        
        # 儲存結果
        save_test_result(
            user_id=self.user_id,
            test_name="analog_move",
            metrics=metrics,
            parameters=parameters,
            image_files=[f"軌跡圖片儲存在: {self.output_dir}"]
        )
        
        print("=" * 50)
        print("🎯 ISO9241 Analog Move Test - 測試完成總結")
        print("=" * 50)
        print(f"👤 使用者：{self.user_id}")
        print(f"🎯 正式測試次數：{total_trials}")
        print(f"🏃 包含暖身測試：是 (第0次不計入統計)")
        print(f"⏱️ 總用時：{self.total_time:.2f} 秒")
        print(f"📊 平均用時：{avg_time:.2f} 秒")
        print(f"⚡ 平均效率：{avg_efficiency:.4f} 秒/像素")
        print(f"🎪 測試標準：ISO9241 九點圓形指向測試")
        print(f"📏 長距離：{self.distance} 像素，短距離：{self.short_distance} 像素")
        print(f"🎯 測試組合：長距離大小目標 + 短距離大小目標")
        print("")
        print("📈 各難度表現分析：")
        for difficulty, data in metrics["difficulty_analysis"].items():
            if data["count"] > 0:
                print(f"  {difficulty}: {data['count']} 次，平均 {data['avg_time_ms']:.0f} ms")
        print("=" * 50)


if __name__ == "__main__":
    import argparse
    from threading import Thread
    from common.controller_input import ControllerInput

    # 解析命令列參數
    parser = argparse.ArgumentParser(description="Analog Move Test")
    parser.add_argument("--user", "-u", default=None, help="使用者 ID")
    args = parser.parse_args()

    # 如果沒有提供 user_id，則請求輸入
    user_id = args.user
    if not user_id:
        user_id = input("請輸入使用者 ID (例如: P1): ").strip()
        if not user_id:
            user_id = "default"

    root = tk.Tk()
    app = JoystickTargetTestApp(root, user_id)

    # 使用新的遙控器管理系統 - 會自動使用已配對的遙控器
    # 使用新的遙控器管理系統 - 會自動使用已配對的遙控器
    listener = ControllerInput(analog_callback=app.on_joycon_input,
                               button_callback=app.on_joycon_button,
                               use_existing_controller=True)
    Thread(target=listener.run, daemon=True).start()

    root.mainloop()
    print("🎮 Fitt's Law 測試結束")
