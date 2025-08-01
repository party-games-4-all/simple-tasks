import pygame
import sys
import os
from pathlib import Path

# 支持相對導入和直接執行
try:
    from .language import get_text
except ImportError:
    # 當直接執行時，添加父目錄到路徑
    sys.path.append(str(Path(__file__).parent.parent))
    from common.language import get_text

# 初始化 pygame joystick 模組
pygame.init()
pygame.joystick.init()

# 偵測是否有連接手把
joystick_count = pygame.joystick.get_count()
print(get_text('controller_detected_count', count=joystick_count))

if joystick_count > 0:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    print(f"{get_text('controller_in_use')}：{joystick.get_name()}")

    try:
        # 持續讀取事件
        while True:
            for event in pygame.event.get():
                if event.type == pygame.JOYAXISMOTION:
                    print(get_text('controller_axis_move_debug', axis=event.axis, value=event.value))
                elif event.type == pygame.JOYBUTTONDOWN:
                    print(get_text('controller_button_press_debug', button=event.button))
                elif event.type == pygame.JOYBUTTONUP:
                    print(get_text('controller_button_release_debug', button=event.button))
    except KeyboardInterrupt:
        print(get_text('controller_stop_listening'))
    finally:
        pygame.quit()  # 確保退出時清理資源
else:
    print(get_text('controller_no_gamepad_detected'))
