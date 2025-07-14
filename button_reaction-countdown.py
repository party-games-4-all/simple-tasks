import tkinter as tk
import time
import threading

class CountdownReactionTestApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Reaction Test with Countdown")
        CANVAS_WIDTH = 1200
        CANVAS_HEIGHT = 800
        self.canvas = tk.Canvas(root, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bg='white')
        self.canvas.pack()

        self.state = "waiting"  # waiting, countdown, go
        self.start_time = None
        self.after_id = None

        self.state_lock = threading.Lock()
        self.reaction_times = []
        self.early_press_times = []

        self.P = 2000  # 總等待時間 (ms)
        self.interval = 10  # 更新間隔
        self.steps = self.P // self.interval
        self.step_count = 0

        self.ball_radius = 30
        self.start_x = 100
        self.end_x = CANVAS_WIDTH * 0.9
        self.y_pos = 400

        self.label = tk.Label(root,
                              text="請按『開始測試』按鈕開始測試",
                              font=("Arial", 24))
        self.label.place(relx=0.5, rely=0.2, anchor='center')

        self.start_button = tk.Button(root, text="開始測試", font=("Arial", 24), command=self.start_test)
        self.start_button.place(relx=0.5, rely=0.8, anchor='center')

        # 畫選擇區域（灰色）
        gray_zone_width = self.ball_radius
        self.gray_x0 = self.end_x - gray_zone_width
        self.gray_x1 = self.end_x + self.ball_radius
        self.canvas.create_rectangle(
            self.gray_x0, 0,
            self.gray_x1, CANVAS_HEIGHT,
            fill="lightgray", outline=""
        )

    def start_test(self):
        self.start_button.place_forget()
        self.label.place_forget()

        self.ball = self.canvas.create_oval(
            self.start_x - self.ball_radius, self.y_pos - self.ball_radius,
            self.start_x + self.ball_radius, self.y_pos + self.ball_radius,
            fill="red"
        )

        with self.state_lock:
            self.state = "countdown"

        self.animate_ball()

    def animate_ball(self):
        progress = self.step_count / self.steps
        x = self.start_x + (self.end_x - self.start_x) * progress

        self.canvas.coords(
            self.ball,
            x - self.ball_radius, self.y_pos - self.ball_radius,
            x + self.ball_radius, self.y_pos + self.ball_radius
        )

        self.step_count += 1
        if self.step_count < self.steps:
            self.after_id = self.root.after(self.interval, self.animate_ball)
        else:
            with self.state_lock:
                self.state = "go"
            self.start_time = time.time()

    def on_joycon_input(self, buttons, leftX, leftY, last_key_bit, last_key_down):
        if not last_key_down:
            return

        with self.state_lock:
            current_state = self.state

        if current_state == "waiting":
            self.start_test()

        elif current_state == "countdown":
            time_early = (self.steps - self.step_count) * self.interval / 1000.0
            self.early_press_times.append(time_early)
            print(f"快了 {time_early:.3f} 秒")
            self.label.place(relx=0.5, rely=0.2, anchor='center')
            self.label.config(text=f"快了 {time_early:.3f} 秒。\n請再按一次開始", font=("Arial", 24))
            if self.after_id:
                self.root.after_cancel(self.after_id)
            with self.state_lock:
                self.state = "waiting"
            self.canvas.config(bg="white")

        elif current_state == "go":
            reaction_time = time.time() - self.start_time
            self.reaction_times.append(reaction_time)
            self.label.config(
                text=f"反應時間：{reaction_time:.3f} 秒。\n請再按一次開始",
                font=("Arial", 24))
            print(f"反應時間：{reaction_time:.3f} 秒")
            with self.state_lock:
                self.state = "waiting"
            self.canvas.config(bg="white")

        if len(self.reaction_times) + len(self.early_press_times) < 10:
            pass
        else:
            avg_time = sum(self.reaction_times) / len(self.reaction_times)
            avg_early_time = sum(self.early_press_times) / len(self.early_press_times)
            print(f"晚按次數：{len(self.reaction_times)}，平均時間：{avg_time:.3f} 秒")
            print(f"快按次數：{len(self.early_press_times)}，快按秒數：{avg_early_time} 秒")
            self.reaction_times.clear()
            self.early_press_times.clear()
            self.label.config(text="測試完成！請按『開始測試』重新開始。", font=("Arial", 24))
            self.start_button.place(relx=0.5, rely=0.8, anchor='center')

if __name__ == "__main__":
    from threading import Thread
    from controller_input import ControllerInput

    root = tk.Tk()
    app = CountdownReactionTestApp(root)

    listener = ControllerInput(button_callback=app.on_joycon_input)
    Thread(target=listener.run, daemon=True).start()

    root.mainloop()