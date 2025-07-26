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
                              text="按『開始測試』後用搖桿移動到紅圈",
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

        # 固定目標組合
        self.fixed_targets = [
            # D=100 W=20
            {
                "x": 670,
                "y": 330,
                "radius": 20
            },  # 右上
            {
                "x": 530,
                "y": 330,
                "radius": 20
            },  # 左上
            {
                "x": 530,
                "y": 470,
                "radius": 20
            },  # 左下
            {
                "x": 670,
                "y": 470,
                "radius": 20
            },  # 右下
            # D=100 W=50
            {
                "x": 670,
                "y": 330,
                "radius": 50
            },  # 右上
            {
                "x": 530,
                "y": 330,
                "radius": 50
            },  # 左上
            {
                "x": 530,
                "y": 470,
                "radius": 50
            },  # 左下
            {
                "x": 670,
                "y": 470,
                "radius": 50
            },  # 右下
            # D=400 W=20
            {
                "x": 882,
                "y": 118,
                "radius": 20
            },  # 右上
            {
                "x": 318,
                "y": 118,
                "radius": 20
            },  # 左上
            {
                "x": 318,
                "y": 682,
                "radius": 20
            },  # 左下
            {
                "x": 882,
                "y": 682,
                "radius": 20
            },  # 右下
            # D=400 W=50
            {
                "x": 882,
                "y": 118,
                "radius": 50
            },  # 右上
            {
                "x": 318,
                "y": 118,
                "radius": 50
            },  # 左上
            {
                "x": 318,
                "y": 682,
                "radius": 50
            },  # 左下
            {
                "x": 882,
                "y": 682,
                "radius": 50
            },  # 右下
        ]
        random.shuffle(self.fixed_targets)

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

        # 重置玩家位置
        self.player_x = self.canvas_width // 2
        self.player_y = self.canvas_height // 2

        if self.success_count >= len(self.fixed_targets):
            self.label.config(text="✅ 測驗完成")
            return

        target_index = (self.success_count) % len(self.fixed_targets)
        target_info = self.fixed_targets[target_index]
        self.target_x = target_info["x"]
        self.target_y = target_info["y"]
        self.target_radius = target_info["radius"]

        # 計算初始距離
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

            efficiency = elapsed / self.initial_distance
            self.total_time += elapsed
            self.total_efficiency += efficiency

            avg_time = self.total_time / (self.success_count)
            avg_efficiency = self.total_efficiency / (self.success_count)

            # 記錄單次測試結果
            trial_result = {
                "trial_number": self.success_count,
                "target_x": self.target_x,
                "target_y": self.target_y,
                "target_radius": self.target_radius,
                "initial_distance": self.initial_distance,
                "completion_time_ms": elapsed * 1000,  # 轉換為毫秒
                "efficiency_s_per_px": efficiency,
                "trace_points_count": len(self.trace_points),
                "press_points_count": len(self.press_trace)
            }
            self.test_results.append(trial_result)

            print(f"✅ 第 {self.success_count} 次成功")
            print(f"⏱ 用時：{elapsed:.2f} 秒")
            print(f"📏 初始距離：{self.initial_distance:.1f} px")
            print(f"⚡ 單位距離時間：{efficiency:.4f} 秒/像素")
            print(f"📊 平均時間：{avg_time:.2f} 秒，平均秒/像素：{avg_efficiency:.4f}")
            self.label.config(text=(f"第 {self.success_count} 次"))
            self.testing = False
            output_move_trace(
                trace_points=self.trace_points,
                start=(self.canvas_width // 2, self.canvas_height // 2),
                target=(self.target_x, self.target_y),
                radius=self.target_radius,
                player_radius=self.player_radius,   # ✅ 傳入實際玩家半徑
                press_points=self.press_trace,
                index=self.success_count,
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
        
        # 分析不同難度的表現
        d100_w20_trials = [t for t in self.test_results if t["initial_distance"] <= 150 and t["target_radius"] == 20]
        d100_w50_trials = [t for t in self.test_results if t["initial_distance"] <= 150 and t["target_radius"] == 50]
        d400_w20_trials = [t for t in self.test_results if t["initial_distance"] > 150 and t["target_radius"] == 20]
        d400_w50_trials = [t for t in self.test_results if t["initial_distance"] > 150 and t["target_radius"] == 50]
        
        # 準備儲存的測試參數
        parameters = {
            "window_size": {
                "width": self.canvas_width,
                "height": self.canvas_height
            },
            "player_radius": self.player_radius,
            "movement_speed_multiplier": 13,
            "total_targets": len(self.fixed_targets)
        }
        
        # 準備儲存的指標數據
        metrics = {
            "total_trials": total_trials,
            "total_time_seconds": self.total_time,
            "average_time_seconds": avg_time,
            "average_efficiency_s_per_px": avg_efficiency,
            "trials": self.test_results,
            "difficulty_analysis": {
                "d100_w20": {
                    "count": len(d100_w20_trials),
                    "avg_time_ms": sum(t["completion_time_ms"] for t in d100_w20_trials) / len(d100_w20_trials) if d100_w20_trials else 0
                },
                "d100_w50": {
                    "count": len(d100_w50_trials),
                    "avg_time_ms": sum(t["completion_time_ms"] for t in d100_w50_trials) / len(d100_w50_trials) if d100_w50_trials else 0
                },
                "d400_w20": {
                    "count": len(d400_w20_trials),
                    "avg_time_ms": sum(t["completion_time_ms"] for t in d400_w20_trials) / len(d400_w20_trials) if d400_w20_trials else 0
                },
                "d400_w50": {
                    "count": len(d400_w50_trials),
                    "avg_time_ms": sum(t["completion_time_ms"] for t in d400_w50_trials) / len(d400_w50_trials) if d400_w50_trials else 0
                }
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
        print("🎯 Analog Move Test - 測試完成總結")
        print("=" * 50)
        print(f"👤 使用者：{self.user_id}")
        print(f"🎯 總試驗次數：{total_trials}")
        print(f"⏱️ 總用時：{self.total_time:.2f} 秒")
        print(f"📊 平均用時：{avg_time:.2f} 秒")
        print(f"⚡ 平均效率：{avg_efficiency:.4f} 秒/像素")
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
