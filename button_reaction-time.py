import tkinter as tk
import random
import time


class ReactionTestApp:
    """簡單的反應時間測試應用程式"""
    def __init__(self, root):
        self.root = root
        self.root.title("Reaction Test")
        self.canvas = tk.Canvas(root, width=1200, height=800, bg="white")
        self.canvas.pack()

        self.state = "waiting"
        self.start_time = None
        self.after_id = None
        self.reaction_times = []

        # 中央圓形（先畫成灰色）
        self.circle = self.canvas.create_oval(550, 350, 650, 450, fill="gray", outline="black", width=3)

        self.label = tk.Label(root,
                              text="請按『開始測試』按鈕開始測試",
                              font=("Arial", 24))
        self.label.place(relx=0.5, rely=0.2, anchor='center')

        self.start_button = tk.Button(root, text="開始測試", font=("Arial", 24), command=self.start_test)
        self.start_button.place(relx=0.5, rely=0.8, anchor='center')

    def start_test(self):
        self.state = "ready"
        self.start_button.place_forget()  # 隱藏開始按鈕
        self.label.place_forget()
        # self.label.config(text="準備中...")
        # self.canvas.config(bg="white")
        self.canvas.itemconfig(self.circle, fill="gray")
        # self.root.after(3000, self.set_random_timer)
        self.set_random_timer()

    def set_random_timer(self):
        delay = random.randint(1000, 3000)  # 隨機延遲 1~3 秒
        self.after_id = self.root.after(delay, self.turn_red)

    def turn_red(self):
        self.canvas.itemconfig(self.circle, fill="red")  # 只改變圓形顏色
        # self.label.config(text="快按 Joy-Con！", font=("Arial", 32))
        self.state = "go"
        self.start_time = time.time()

    def on_joycon_input(self, buttons, leftX, leftY, last_key_bit, last_key_down):
        if not last_key_down:
            return  # 只處理按下事件（不處理放開）

        if self.state == "waiting":
            self.start_test()

        elif self.state == "ready":
            # self.label.config(text="太快了！再試一次。", font=("Arial", 24))
            # self.canvas.config(bg="white")
            if self.after_id:
                self.root.after_cancel(self.after_id)
            self.canvas.itemconfig(self.circle, fill="white")
            self.state = "waiting"
            print(f"太快了！再試一次。")

        elif self.state == "go":
            reaction_time = time.time() - self.start_time
            self.reaction_times.append(reaction_time)
            # self.label.config(text=f"反應時間：{reaction_time:.3f} 秒。請再按一次開始", font=("Arial", 24))
            print(f"反應時間：{reaction_time:.3f} 秒")
            self.canvas.itemconfig(self.circle, fill="green")
            self.state = "waiting"

            if len(self.reaction_times) < 5:
                # self.root.after(2000, self.start_test)  # 2 秒後開始下一次測試
                pass
            else:
                avg_time = sum(self.reaction_times) / len(self.reaction_times)
                print(f"平均反應時間：{avg_time:.3f} 秒")
                self.reaction_times.clear()
                self.label.config(text="測試完成！請按『開始測試』重新開始。", font=("Arial", 24))
                self.label.place(relx=0.5, rely=0.2, anchor='center')
                self.start_button.place(relx=0.5, rely=0.8, anchor='center')


if __name__ == "__main__":
    from threading import Thread
    from controller_input import ControllerInput

    root = tk.Tk()
    app = ReactionTestApp(root)

    # 把所有輸入都交給 app 處理（不過濾按鍵）
    listener = ControllerInput(button_callback=app.on_joycon_input)
    Thread(target=listener.run, daemon=True).start()

    root.mainloop()
    print("🎮 Joy-Con 反應時間測試結束")
