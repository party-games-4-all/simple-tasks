from controller_input import ControllerInput

if __name__ == "__main__":
    # 初始化手把輸入
    controller = ControllerInput()

    # 開始監聽手把事件
    controller.run()