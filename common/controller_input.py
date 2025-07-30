import pygame
import os
import signal
import sys
from .controller_manager import controller_manager
from .language import get_text

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
os.environ['SDL_VIDEODRIVER'] = 'dummy'

pygame.init()
pygame.joystick.init()

DEBUG = False  # 設定為 True 以啟用除錯輸出


class ControllerInput:

    def __init__(self, button_callback=None, analog_callback=None, use_existing_controller=True):
        self.leftX = 0
        self.leftY = 0
        self.buttons = 0
        self.running = True  # 添加運行狀態標記

        self.button_callback = button_callback
        self.analog_callback = analog_callback
        
        # 註冊 signal handler 來處理程式意外關閉
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)

        # 自動配對遙控器（使用已選擇的遙控器或自動選擇第一個）
        if use_existing_controller and controller_manager.is_controller_selected():
            # 使用已選擇的遙控器
            self.joystick = controller_manager.create_controller()
            if self.joystick is None:
                print(get_text('controller_unable_connect'))
                self.joystick = self._auto_select_controller()
        else:
            # 自動選擇第一個可用的遙控器
            self.joystick = self._auto_select_controller()
        
        if self.joystick is None:
            print(get_text('controller_no_pairing'))

    def _signal_handler(self, signum, frame):
        """處理系統信號，確保正常關閉"""
        print(get_text('controller_signal_received', signum=signum))
        self.stop()
        sys.exit(0)

    def _auto_select_controller(self):
        """自動選擇第一個可用的遙控器"""
        count = pygame.joystick.get_count()
        
        if count == 0:
            print(get_text('controller_no_gamepad'))
            return None
        
        # 自動選擇第一個遙控器
        try:
            j = pygame.joystick.Joystick(0)
            j.init()
            print(get_text('controller_auto_connect', name=j.get_name()))
            return j
        except Exception as e:
            print(get_text('controller_auto_connect_failed', error=e))
            return None

    def detect_joycon(self):
        count = pygame.joystick.get_count()
        print(get_text('controller_detected_count', count=count))

        if count == 0:
            print(get_text('controller_no_gamepad'))
            return

        for i in range(count):
            j = pygame.joystick.Joystick(i)
            j.init()
            print(get_text('controller_detected', name=j.get_name()))
            confirm = input(get_text('controller_use_device')).strip().lower()
            if confirm == "y" or confirm == "":
                self.joystick = j
                print(get_text('controller_selected', name=j.get_name()))
                return
            else:
                j.quit()

        print(get_text('controller_none_selected'))

    @staticmethod
    def setup_controller():
        """
        靜態方法：配對並返回遙控器實例
        用於在主程式啟動時一次性配對遙控器
        """
        count = pygame.joystick.get_count()
        print(get_text('controller_detected_count', count=count))

        if count == 0:
            print(get_text('controller_no_gamepad'))
            return None

        for i in range(count):
            j = pygame.joystick.Joystick(i)
            j.init()
            print(get_text('controller_detected', name=j.get_name()))
            confirm = input(get_text('controller_use_device')).strip().lower()
            if confirm == "y" or confirm == "":
                print(get_text('controller_selected', name=j.get_name()))
                return j
            else:
                j.quit()

        print(get_text('controller_none_selected'))
        return None

    def run(self):
        if self.joystick is None:
            return

        print(get_text('controller_listening'))
        try:
            while self.running:
                try:
                    # 檢查是否還有有效的事件系統
                    if not pygame.get_init():
                        break
                        
                    for event in pygame.event.get():
                        if not self.running:  # 再次檢查運行狀態
                            break
                        
                        # 處理 pygame 關閉事件
                        if event.type == pygame.QUIT:
                            self.running = False
                            break
                        
                        last_key_bit = None
                        last_key_down = None

                        if event.type == pygame.JOYAXISMOTION:
                            axis = event.axis
                            val = round(event.value, 4)
                            last_key_down = True
                            if abs(val) < 0.15:
                                val = 0
                                last_key_down = False

                            if axis == 0:
                                self.leftX = val
                            elif axis == 1:
                                self.leftY = val
                            else:
                                continue

                            if DEBUG:
                                print(get_text('controller_axis_move', axis=event.axis, value=round(event.value, 4)))

                            if self.analog_callback:
                                try:
                                    self.analog_callback(buttons=self.buttons,
                                                         leftX=self.leftX,
                                                         leftY=self.leftY,
                                                         last_key_bit=axis,
                                                         last_key_down=last_key_down)
                                except Exception as e:
                                    if self.running:  # 只在仍在運行時報告錯誤
                                        print(get_text('controller_analog_error', error=e))

                        elif event.type == pygame.JOYBUTTONDOWN:
                            if DEBUG:
                                print(get_text('controller_button_press', button=event.button))
                            self.buttons |= (1 << event.button)
                            last_key_bit = event.button
                            last_key_down = True

                            if self.button_callback:
                                try:
                                    self.button_callback(buttons=self.buttons,
                                                         leftX=self.leftX,
                                                         leftY=self.leftY,
                                                         last_key_bit=last_key_bit,
                                                         last_key_down=last_key_down)
                                except Exception as e:
                                    if self.running:  # 只在仍在運行時報告錯誤
                                        print(get_text('controller_button_press_error', error=e))

                        elif event.type == pygame.JOYBUTTONUP:
                            if DEBUG:
                                print(get_text('controller_button_release', button=event.button))
                            self.buttons &= ~(1 << event.button)
                            last_key_bit = event.button
                            last_key_down = False

                            if self.button_callback:
                                try:
                                    self.button_callback(buttons=self.buttons,
                                                         leftX=self.leftX,
                                                         leftY=self.leftY,
                                                         last_key_bit=last_key_bit,
                                                         last_key_down=last_key_down)
                                except Exception as e:
                                    if self.running:  # 只在仍在運行時報告錯誤
                                        print(get_text('controller_button_release_error', error=e))
                
                except Exception as e:
                    if self.running:  # 只在仍在運行時報告錯誤
                        print(get_text('controller_event_error', error=e))
                    
        except Exception as e:
            if self.running:
                print(get_text('controller_thread_error', error=e))
        finally:
            # 確保清理 pygame 資源
            try:
                if hasattr(self, 'joystick') and self.joystick:
                    self.joystick.quit()
            except Exception:
                pass  # 忽略清理過程中的錯誤
            print(get_text('controller_thread_ended'))

    def stop(self):
        """停止控制器輸入監聽"""
        self.running = False
        
        # 清理 pygame 資源
        try:
            if hasattr(self, 'joystick') and self.joystick:
                self.joystick.quit()
                self.joystick = None
        except Exception:
            pass  # 忽略清理過程中的錯誤
        
        # 清理 pygame - 但不完全關閉，避免其他地方還在使用
        try:
            pygame.joystick.quit()
            # 不調用 pygame.quit()，讓主程式決定何時關閉
        except Exception:
            pass  # 忽略清理過程中的錯誤
            
        print(get_text('controller_listening_stopped'))

    def __del__(self):
        """析構函數，確保資源釋放"""
        try:
            self.stop()
        except Exception:
            pass


if __name__ == "__main__":
    # 初始化手把輸入
    controller = ControllerInput()

    # 開始監聽手把事件
    controller.run()
