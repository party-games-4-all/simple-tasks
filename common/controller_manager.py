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
    _selected_controller_index = None  # 儲存已選擇的控制器索引
    _selected_controller_name = None   # 儲存已選擇的控制器名稱
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
        選擇遙控器（只記錄選擇，不實際連接）
        """
        if self._selected_controller_index is not None and not force_setup:
            print(f"🎮 已選擇遙控器：{self._selected_controller_name}")
            return True
        
        # 重新掃描遙控器
        pygame.joystick.quit()
        pygame.joystick.init()
        
        count = pygame.joystick.get_count()
        print(f"🎮 偵測到 {count} 支手把")
        
        if count == 0:
            print("❌ 未偵測到任何🎮手把")
            return False
        
        for i in range(count):
            j = pygame.joystick.Joystick(i)
            j.init()
            controller_name = j.get_name()
            print(f"🔍 偵測到手把：{controller_name}")
            confirm = input("要使用這個裝置嗎？(Y/n): ").strip().lower()
            if confirm == "y" or confirm == "":
                # 只記錄選擇，不保持連接
                self._selected_controller_index = i
                self._selected_controller_name = controller_name
                print(f"✅ 已選擇：{controller_name}")
                j.quit()  # 立即斷開連接
                return True
            else:
                j.quit()
        
        print("❌ 沒有選擇任何手把")
        return False
    
    def get_selected_controller_info(self):
        """取得已選擇的遙控器資訊"""
        return {
            'index': self._selected_controller_index,
            'name': self._selected_controller_name
        }
    
    def is_controller_selected(self):
        """檢查是否已選擇遙控器"""
        return self._selected_controller_index is not None
    
    def create_controller(self):
        """為測試程式建立新的遙控器實例"""
        if self._selected_controller_index is None:
            print("❌ 尚未選擇遙控器")
            return None
        
        # 確保 pygame joystick 已初始化
        if not pygame.joystick.get_init():
            pygame.joystick.init()
        
        count = pygame.joystick.get_count()
        if count <= self._selected_controller_index:
            print(f"❌ 遙控器 {self._selected_controller_index} 不存在，當前有 {count} 支手把")
            return None
        
        try:
            j = pygame.joystick.Joystick(self._selected_controller_index)
            j.init()
            print(f"🎮 已連接遙控器：{j.get_name()}")
            return j
        except Exception as e:
            print(f"❌ 連接遙控器失敗：{e}")
            return None
    
    def reset(self):
        """重置選擇狀態"""
        self._selected_controller_index = None
        self._selected_controller_name = None


# 建立全域實例
controller_manager = ControllerManager()
