import pygame

# 初始化 pygame joystick 模組
pygame.init()
pygame.joystick.init()

# 偵測是否有連接手把
joystick_count = pygame.joystick.get_count()
print(f"Detected {joystick_count} controllers | 偵測到 {joystick_count} 支手把")

if joystick_count > 0:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    print(f"Using controller | 使用中手把：{joystick.get_name()}")

    try:
        # 持續讀取事件
        while True:
            for event in pygame.event.get():
                if event.type == pygame.JOYAXISMOTION:
                    print(f"Axis movement | 軸移動：{event.axis} -> {event.value}")
                elif event.type == pygame.JOYBUTTONDOWN:
                    print(f"Button pressed | 按下按鍵：{event.button}")
                elif event.type == pygame.JOYBUTTONUP:
                    print(f"Button released | 放開按鍵：{event.button}")
    except KeyboardInterrupt:
        print("🎮 Stopped controller event monitoring | 停止監聽手把事件")
    finally:
        pygame.quit()  # 確保退出時清理資源
else:
    print("No controllers detected | 未偵測到手把")
