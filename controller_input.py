import pygame

pygame.init()
pygame.joystick.init()

class ControllerInput:
    def __init__(self, button_callback=None, analog_callback=None):

        self.joystick = None
        self.leftX = 0
        self.leftY = 0
        self.buttons = 0

        self.button_callback = button_callback
        self.analog_callback = analog_callback

        self.detect_joycon()

    def detect_joycon(self):
        count = pygame.joystick.get_count()
        print(f"🎮 偵測到 {count} 支手把")

        if count == 0:
            print("❌ 未偵測到任何🎮手把")
            return

        for i in range(count):
            j = pygame.joystick.Joystick(i)
            j.init()
            print(f"🔍 偵測到手把：{j.get_name()}")
            confirm = input("要使用這個裝置嗎？(Y/n): ").strip().lower()
            if confirm == "y" or confirm == "":
                self.joystick = j
                print(f"✅ 已選擇：{j.get_name()}")
                return
            else:
                j.quit()

        print("❌ 沒有選擇任何手把")

    def run(self):
        if self.joystick is None:
            return

        print("🎮 開始監聽手把事件... (Ctrl+C 中止)")
        while True:
            for event in pygame.event.get():
                last_key_bit = None
                last_key_down = None

                if event.type == pygame.JOYAXISMOTION:
                    print(f"軸移動：{event.axis} -> {event.value}")
                    axis = event.axis
                    val = round(event.value, 3)

                    if axis == 0:
                        self.leftX = val
                    elif axis == 1:
                        self.leftY = val

                    if self.analog_callback:
                        self.analog_callback(
                            buttons=self.buttons,
                            leftX=self.leftX,
                            leftY=self.leftY,
                            last_key_bit=axis,
                            last_key_down=True
                        )

                elif event.type == pygame.JOYBUTTONDOWN:
                    print(f"按下按鍵：{event.button}")
                    self.buttons |= (1 << event.button)
                    last_key_bit = event.button
                    last_key_down = True

                    if self.button_callback:
                        self.button_callback(
                            buttons=self.buttons,
                            leftX=self.leftX,
                            leftY=self.leftY,
                            last_key_bit=last_key_bit,
                            last_key_down=last_key_down
                        )

                elif event.type == pygame.JOYBUTTONUP:
                    print(f"放開按鍵：{event.button}")
                    self.buttons &= ~(1 << event.button)
                    last_key_bit = event.button
                    last_key_down = False

                    if self.button_callback:
                        self.button_callback(
                            buttons=self.buttons,
                            leftX=self.leftX,
                            leftY=self.leftY,
                            last_key_bit=last_key_bit,
                            last_key_down=last_key_down
                        )

if __name__ == "__main__":
    # 初始化手把輸入
    controller = ControllerInput()

    # 開始監聽手把事件
    controller.run()