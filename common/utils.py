def get_directional_offset(dx, dy, offset):
    """根據主方向決定 offset 應該加在哪一軸"""
    if abs(dx) > abs(dy):
        # 水平為主：偏移 x
        return (offset if dx >= 0 else -offset), 0
    else:
        # 垂直為主：偏移 y
        return 0, (offset if dy >= 0 else -offset)


def setup_window_topmost(root):
    """
工具函式模組
包含視窗設定、使用者資訊收集等共用功能
"""
import tkinter as tk
from . import config
from .language import get_text

def setup_window_topmost(root):
    """
    設定視窗置頂並取得焦點
    將視窗設定為指定大小、置於螢幕中央、設定為置頂並取得焦點
    """
    try:
        # 從 config 獲取視窗尺寸
        width = config.WINDOW_WIDTH
        height = config.WINDOW_HEIGHT
        
        # 計算螢幕中央位置
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        
        # 設定視窗大小和位置
        root.geometry(f'{width}x{height}+{x}+{y}')
        
        # 禁止調整視窗大小（確保維持固定大小）
        root.resizable(False, False)
        
        # 設定視窗置頂
        root.attributes('-topmost', True)
        
        # 讓視窗取得焦點
        root.focus_force()
        root.lift()
        
        print(get_text('window_setup_success', width=width, height=height, x=x, y=y))
        
    except Exception as e:
        print(get_text('window_setup_failed', error=e))
        # 備用設定
        try:
            root.geometry('1200x800')
            root.resizable(False, False)
            root.attributes('-topmost', True)
            root.focus_force()
        except:
            pass  # 如果連備用設定都失敗，就使用預設設定


def setup_pygame_window_topmost():
    """
    設定 pygame 視窗置頂
    注意：pygame 的視窗置頂功能有限，主要依賴作業系統
    """
    try:
        import os
        # 在 macOS 上可以嘗試設定環境變數
        os.environ['SDL_VIDEO_WINDOW_POS'] = 'centered'
        print(get_text('pygame_window_topmost'))
    except Exception as e:
        print(get_text('pygame_window_failed', error=e))


def collect_user_info_if_needed(user_id):
    """
    收集使用者基本資訊（如果尚未收集）
    包括年齡和手把使用頻率
    """
    
    # 檢查是否已經有完整的使用者資訊
    if (hasattr(config, 'user_info') and config.user_info and 
        config.user_info.get('user_id') == user_id and
        config.user_info.get('age') is not None and
        config.user_info.get('controller_usage_frequency') is not None):
        # 資訊已完整，無需重新收集
        print(get_text('user_info_exists', user_id=user_id))
        return
    
    # 判斷是否為首次收集（從 main.py 呼叫）或補充收集（從個別測試呼叫）
    if not hasattr(config, 'user_info') or not config.user_info:
        print(f"\n{get_text('user_info_title')}")
    else:
        print(f"\n{get_text('user_info_supplement', user_id=user_id)}")
    
    # 收集年齡
    while True:
        try:
            age_input = input(get_text('enter_age')).strip()
            age = int(age_input)
            if age > 0 and age < 150:  # 合理的年齡範圍
                break
            else:
                print(get_text('valid_age'))
        except ValueError:
            print(get_text('enter_number'))
    
    # 收集手把使用頻率
    print(f"\n{get_text('controller_frequency_title')}")
    print(get_text('controller_frequency_desc'))
    print(get_text('controller_frequency_scale'))
    while True:
        try:
            freq_input = input(get_text('enter_frequency')).strip()
            controller_usage_frequency = int(freq_input)
            if controller_usage_frequency in [1, 2, 3, 4, 5, 6, 7]:
                break
            else:
                print(get_text('valid_frequency'))
        except ValueError:
            print(get_text('enter_number'))
    
    # 更新 config 中的使用者資訊
    config.user_info = {
        "user_id": user_id,
        "age": age,
        "controller_usage_frequency": controller_usage_frequency,
        "controller_usage_frequency_description": "1=從來沒用過, 7=每天使用"  # 保持原始說明在 JSON 中
    }
    
    print(f"\n{get_text('user_info_recorded', user_id=user_id, age=age, frequency=controller_usage_frequency)}")
