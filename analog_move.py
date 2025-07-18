import tkinter as tk
import random
import time
from threading import Thread

class JoystickTargetTestApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Joystick 移動目標測試")
        self.canvas_width = 1200
        self.canvas_height = 800
        self.canvas = tk.Canvas(root, width=self.canvas_width, height=self.canvas_height, bg='white')
        self.canvas.pack()

        self.label = tk.Label(root, text="按『開始測試』後用搖桿移動到紅圈", font=("Arial", 24))
        self.label.place(relx=0.5, rely=0.02, anchor='n')

        self.start_button = tk.Button(root, text="開始測試", font=("Arial", 24), command=self.start_test)
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

        self.player_x = self.canvas_width // 2
        self.player_y = self.canvas_height // 2

        self.target_x = 0
        self.target_y = 0

        self.leftX = 0
        self.leftY = 0

        # 固定目標組合
        self.fixed_targets = [
            # D=100 W=20
            {"x": 670, "y": 330, "radius": 20},  # 右上
            {"x": 530, "y": 330, "radius": 20},  # 左上
            {"x": 530, "y": 470, "radius": 20},  # 左下
            {"x": 670, "y": 470, "radius": 20},  # 右下
            # D=100 W=50
            {"x": 670, "y": 330, "radius": 50},  # 右上
            {"x": 530, "y": 330, "radius": 50},  # 左上
            {"x": 530, "y": 470, "radius": 50},  # 左下
            {"x": 670, "y": 470, "radius": 50},  # 右下
            # D=400 W=20
            {"x": 882, "y": 118, "radius": 20},  # 右上
            {"x": 318, "y": 118, "radius": 20},  # 左上
            {"x": 318, "y": 682, "radius": 20},  # 左下
            {"x": 882, "y": 682, "radius": 20},  # 右下
            # D=400 W=50
            {"x": 882, "y": 118, "radius": 50},  # 右上
            {"x": 318, "y": 118, "radius": 50},  # 左上
            {"x": 318, "y": 682, "radius": 50},  # 左下
            {"x": 882, "y": 682, "radius": 50},  # 右下
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
        self.initial_distance = ((self.player_x - self.target_x) ** 2 + (self.player_y - self.target_y) ** 2) ** 0.5

        self.target = self.canvas.create_oval(
            self.target_x - self.target_radius, self.target_y - self.target_radius,
            self.target_x + self.target_radius, self.target_y + self.target_radius,
            fill="red"
        )
        self.player = self.canvas.create_oval(
            self.player_x - self.player_radius, self.player_y - self.player_radius,
            self.player_x + self.player_radius, self.player_y + self.player_radius,
            fill="blue"
        )

    def update_player_position(self):
        # 將 -1 ~ 1 值轉換為 -13 ~ +13 的速度
        dx = (self.leftX) * 13
        dy = (self.leftY) * 13

        self.player_x += dx
        self.player_y += dy

        # 限制在畫布內
        self.player_x = max(self.player_radius, min(self.canvas_width - self.player_radius, self.player_x))
        self.player_y = max(self.player_radius, min(self.canvas_height - self.player_radius, self.player_y))

        self.canvas.coords(
            self.player,
            self.player_x - self.player_radius, self.player_y - self.player_radius,
            self.player_x + self.player_radius, self.player_y + self.player_radius
        )

    def on_joycon_input(self, buttons, leftX, leftY, last_key_bit, last_key_down):
        self.leftX = leftX
        self.leftY = leftY

        # 如果第一次移動，開始計時
        if not self.has_moved and (leftX != 0 or leftY != 0):
            self.start_time = time.time()
            self.has_moved = True

    def on_joycon_button(self, buttons, leftX, leftY, last_key_bit, last_key_down):
        # 若按下任一按鍵（例如 A 鍵），進行位置判定
        if not last_key_down:
            return  # 只處理按下事件（不處理放開）

        # 以 1 號鍵為例，可視需要調整
        if last_key_bit != 1:  # 你可以改成任意你想用的按鍵編號
            return

        if not self.testing:
            return

        distance = ((self.player_x - self.target_x) ** 2 + (self.player_y - self.target_y) ** 2) ** 0.5
        if distance <= self.target_radius:
            elapsed = time.time() - self.start_time
            self.success_count += 1

            efficiency = elapsed / self.initial_distance
            self.total_time += elapsed
            self.total_efficiency += efficiency

            avg_time = self.total_time / (self.success_count)
            avg_efficiency = self.total_efficiency / (self.success_count)

            print(f"✅ 第 {self.success_count} 次成功")
            print(f"⏱ 用時：{elapsed:.2f} 秒")
            print(f"📏 初始距離：{self.initial_distance:.1f} px")
            print(f"⚡ 單位距離時間：{efficiency:.4f} 秒/像素")
            print(f"📊 平均時間：{avg_time:.2f} 秒，平均秒/像素：{avg_efficiency:.4f}")
            self.label.config(
                text=(
                    f"第 {self.success_count} 次"
                )
            )
            self.testing = False
            time.sleep(1)  # 等待 1 秒後再開始下一個目標
            self.start_test()  # 重新開始測試

if __name__ == "__main__":
    from threading import Thread
    from controller_input import ControllerInput

    root = tk.Tk()
    app = JoystickTargetTestApp(root)

    listener = ControllerInput(analog_callback=app.on_joycon_input, button_callback=app.on_joycon_button)
    Thread(target=listener.run, daemon=True).start()

    root.mainloop()
    print("🎮 Fitt's Law 測試結束")
