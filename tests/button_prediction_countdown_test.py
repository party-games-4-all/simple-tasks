import tkinter as tk
import time
import threading

class CountdownReactionTestApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Reaction Test")
        CANVAS_WIDTH = 1600
        CANVAS_HEIGHT = 800
        self.canvas = tk.Canvas(root, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bg='white')
        self.canvas.pack()

        self.PERIOD = 800  # 1500ms
        self.CUE_VIEWING_TIME = 250  # 250ms
        self.SCREEN_UPDATE_INTERVAL = 10  # 每5ms更新一次畫面

        self.ball_radius = 30
        self.start_x = 100
        self.end_x = CANVAS_WIDTH * 0.9
        self.y_pos = 400

        self.gray_x0 = self.end_x - self.ball_radius
        self.gray_x1 = self.end_x + self.ball_radius
        # self.canvas.create_rectangle(self.gray_x0, 0, self.gray_x1, CANVAS_HEIGHT, fill="lightgray", outline="")
        # 在 __init__ 中新增灰色圓形（與球一樣大小）放在 end_x 處
        self.gray_circle = self.canvas.create_oval(
            self.end_x - self.ball_radius, self.y_pos - self.ball_radius,
            self.end_x + self.ball_radius, self.y_pos + self.ball_radius,
            fill="lightgray", outline="")

        self.label = tk.Label(root, text="請按『開始測試』按鈕開始測試", font=("Arial", 24))
        self.label.place(relx=0.5, rely=0.2, anchor='center')

        self.start_button = tk.Button(root, text="開始測試", font=("Arial", 24), command=self.start_test)
        self.start_button.place(relx=0.5, rely=0.8, anchor='center')

        self.reaction_results = []
        self.total_balls = 5
        self.current_ball_index = 0

        self.ball = None
        self.ball_start_time = None
        self.ball_timer_id = None
        self.next_ball_id = None
        self.ball_active = False

    def start_test(self):
        self.start_button.place_forget()
        self.label.place_forget()
        self.current_ball_index = 0

        self.ball = None
        self.ball_start_time = None
        self.ball_timer_id = None
        self.next_ball_id = None
        self.ball_active = False
        self.reaction_results.clear()
        self.schedule_next_ball()

    def schedule_next_ball(self):
        if self.current_ball_index >= self.total_balls:
            return
        self.next_ball_id = self.root.after(self.PERIOD, self.launch_ball)

    def launch_ball(self):
        self.current_ball_index += 1
        self.schedule_next_ball()
        self.canvas.delete("ball")
        self.ball = self.canvas.create_oval(
            self.start_x - self.ball_radius, self.y_pos - self.ball_radius,
            self.start_x + self.ball_radius, self.y_pos + self.ball_radius,
            fill="red", tags="ball"
        )
        self.ball_start_time = time.time()
        self.ball_active = True
        thread = threading.Thread(target=self.move_ball_thread, daemon=True)
        thread.start()

    def move_ball_thread(self):
        while self.ball_active:
            elapsed = (time.time() - self.ball_start_time)
            progress = min(elapsed / (self.CUE_VIEWING_TIME / 1000), 1.0)
            x = self.start_x + (self.end_x - self.start_x) * progress

            # 更新畫面必須在主線程進行
            self.root.after(0, self.canvas.coords,
                self.ball,
                x - self.ball_radius, self.y_pos - self.ball_radius,
                x + self.ball_radius, self.y_pos + self.ball_radius
            )

            if progress >= 1.0:
                break

        time.sleep(self.SCREEN_UPDATE_INTERVAL / 1000.0)  # 換算成秒

    def register_press(self):
        if not self.ball_active:
            return
        now = time.time()
        elapsed = now - self.ball_start_time
        error = elapsed - self.CUE_VIEWING_TIME / 1000  # 計算按下的誤差時間
        self.ball_active = False
        self.canvas.delete("ball")
        if self.ball_timer_id:
            self.root.after_cancel(self.ball_timer_id)
        print(f"{'快了' if error < 0 else '慢了'} {abs(error):.3f} 秒")
        self.reaction_results.append(error)
        if self.current_ball_index >= self.total_balls:
            self.finish_test()

    def finish_test(self):
        self.canvas.delete("ball")
        self.label.place(relx=0.5, rely=0.2, anchor='center')
        self.label.config(text="測試完成，請按『開始測試』重新開始")
        self.start_button.place(relx=0.5, rely=0.8, anchor='center')
        self.start_button = tk.Button(root, text="開始測試", font=("Arial", 24), command=self.start_test)
        valid_errors = [abs(e) for e in self.reaction_results if e is not None]
        if valid_errors:
            avg_error = sum(valid_errors) / len(valid_errors)
            print(f"五次誤差平均（絕對值）：{avg_error:.3f} 秒")
        else:
            print("五次皆未按")

    # ← Joy-Con 按鍵會呼叫這個函數
    def on_joycon_input(self, buttons, leftX, leftY, last_key_bit, last_key_down):
        if last_key_down:
            self.register_press()

if __name__ == "__main__":
    from threading import Thread
    from common.controller_input import ControllerInput

    root = tk.Tk()
    app = CountdownReactionTestApp(root)

    listener = ControllerInput(button_callback=app.on_joycon_input)
    Thread(target=listener.run, daemon=True).start()

    root.mainloop()
    print("🎮 TP 可預測反應時間測試結束")