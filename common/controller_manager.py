"""
遙控器管理器 - 用於在程式生命週期中共享遙控器實例
"""
import pygame
import os
from .language import get_text

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
            print(get_text('controller_selected', name=self._selected_controller_name))
            return True
        
        # 重新掃描遙控器
        pygame.joystick.quit()
        pygame.joystick.init()
        
        count = pygame.joystick.get_count()
        print(get_text('controller_detected_count', count=count))
        
        if count == 0:
            print(get_text('controller_no_gamepad'))
            return False
        
        for i in range(count):
            j = pygame.joystick.Joystick(i)
            j.init()
            controller_name = j.get_name()
            print(get_text('controller_detected', name=controller_name))
            confirm = input(get_text('controller_use_device')).strip().lower()
            if confirm == "y" or confirm == "":
                # 只記錄選擇，不保持連接
                self._selected_controller_index = i
                self._selected_controller_name = controller_name
                print(get_text('controller_selected', name=controller_name))
                j.quit()  # 立即斷開連接
                return True
            else:
                j.quit()
        
        print(get_text('controller_none_selected'))
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
            print(get_text('controller_not_selected_yet'))
            return None
        
        # 確保 pygame joystick 已初始化
        if not pygame.joystick.get_init():
            pygame.joystick.init()
        
        count = pygame.joystick.get_count()
        if count <= self._selected_controller_index:
            print(get_text('controller_not_exist', index=self._selected_controller_index, count=count))
            return None
        
        try:
            j = pygame.joystick.Joystick(self._selected_controller_index)
            j.init()
            print(get_text('controller_connected', name=j.get_name()))
            return j
        except Exception as e:
            print(get_text('controller_connect_failed', error=e))
            return None
    
    def reset(self):
        """重置選擇狀態"""
        self._selected_controller_index = None
        self._selected_controller_name = None


# 建立全域實例
controller_manager = ControllerManager()
