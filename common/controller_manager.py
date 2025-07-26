"""
遙控器管理器 - 用於在程式生命週期中共享遙控器實例
"""
import pygame
import os

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

# 確保 pygame 已初始化
if not pygame.get_init():
    pygame.init()
if not pygame.joystick.get_init():
    pygame.joystick.init()


class ControllerManager:
    """全域遙控器管理器"""
    
    _instance = None
    _controller = None
    _is_initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ControllerManager, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        # 避免重複初始化
        if not self._is_initialized:
            self._is_initialized = True
    
    def setup_controller(self, force_setup=False):
        """
        配對遙控器（只在第一次調用或強制設定時執行）
        """
        if self._controller is not None and not force_setup:
            print(f"🎮 使用已配對的遙控器：{self._controller.get_name()}")
            return self._controller
        
        # 重新掃描遙控器
        pygame.joystick.quit()
        pygame.joystick.init()
        
        count = pygame.joystick.get_count()
        print(f"🎮 偵測到 {count} 支手把")
        
        if count == 0:
            print("❌ 未偵測到任何🎮手把")
            return None
        
        for i in range(count):
            j = pygame.joystick.Joystick(i)
            j.init()
            print(f"🔍 偵測到手把：{j.get_name()}")
            confirm = input("要使用這個裝置嗎？(Y/n): ").strip().lower()
            if confirm == "y" or confirm == "":
                self._controller = j
                print(f"✅ 已選擇：{j.get_name()}")
                return self._controller
            else:
                j.quit()
        
        print("❌ 沒有選擇任何手把")
        return None
    
    def get_controller(self):
        """取得已配對的遙控器實例"""
        return self._controller
    
    def is_controller_ready(self):
        """檢查遙控器是否已配對且可用"""
        return self._controller is not None and self._controller.get_init()
    
    def reset(self):
        """重置遙控器狀態（用於重新配對）"""
        if self._controller:
            self._controller.quit()
        self._controller = None


# 建立全域實例
controller_manager = ControllerManager()
