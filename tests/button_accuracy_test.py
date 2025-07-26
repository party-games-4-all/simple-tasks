import tkinter as tk
import random
import time
import sys
from pathlib import Path

# 添加父目錄到 Python 路徑以便導入共用模組
sys.path.append(str(Path(__file__).parent.parent))

from common import config


class AccuracyDirectionTestApp:

    def __init__(self, root):
        self.root = root
        self.root.title("按鍵準確度測試")
        background_color = f"#{config.COLORS['BACKGROUND'][0]:02x}{config.COLORS['BACKGROUND'][1]:02x}{config.COLORS['BACKGROUND'][2]:02x}"
        self.canvas = tk.Canvas(root, width=config.WINDOW_WIDTH, height=config.WINDOW_HEIGHT, bg=background_color)
        self.canvas.pack()

        # 計算中心位置和方向按鈕位置
        center_x, center_y = config.WINDOW_WIDTH // 2, config.WINDOW_HEIGHT // 2
        button_distance = 200  # 按鈕距離中心的距離
        
        self.directions = {
            "up": {
                "pos": (center_x, center_y - button_distance),
                "bit": None
            },
            "down": {
                "pos": (center_x, center_y + button_distance),
                "bit": None
            },
            "left": {
                "pos": (center_x - button_distance, center_y),
                "bit": None
            },
            "right": {
                "pos": (center_x + button_distance, center_y),
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


if __name__ == "__main__":
    from threading import Thread
    from common.controller_input import ControllerInput

    root = tk.Tk()
    app = AccuracyDirectionTestApp(root)

    # 根據你的 Joy-Con 對應設定 bit 值
    app.directions["up"]["bit"] = 3
    app.directions["down"]["bit"] = 0
    app.directions["left"]["bit"] = 2
    app.directions["right"]["bit"] = 1

    listener = ControllerInput(button_callback=app.on_joycon_input)
    Thread(target=listener.run, daemon=True).start()

    root.mainloop()
    print("🎮 CRT 反應時間測試結束")
