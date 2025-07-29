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
    設定視窗置頂並取得焦點
    適用於 tkinter 視窗
    """
    try:
        # 導入 config 來獲取正確的視窗大小
        from . import config
        
        # 設定視窗大小
        width = config.WINDOW_WIDTH
        height = config.WINDOW_HEIGHT
        
        # 先更新視窗以確保正確計算螢幕大小
        root.update_idletasks()
        
        # 計算螢幕中央位置
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        
        # 設定視窗大小和位置
        root.geometry(f'{width}x{height}+{x}+{y}')
        
        # 禁止調整視窗大小（確保維持固定大小）
        root.resizable(False, False)
        
        # 設定視窗置頂
        root.attributes('-topmost', True)
        
        # 讓視窗取得焦點
        root.focus_force()
        root.lift()
        
        print(f"🖥️ 視窗設定為：{width}x{height}，位置：({x}, {y})")
        
    except Exception as e:
        print(f"⚠️ 設定視窗置頂失敗: {e}")
        # 備用設定
        try:
            root.geometry('1200x800')
            root.resizable(False, False)
            root.attributes('-topmost', True)
            root.focus_force()
        except:
            print("⚠️ 備用視窗設定也失敗")


def setup_pygame_window_topmost():
    """
    設定 pygame 視窗置頂
    注意：pygame 的視窗置頂功能有限，主要依賴作業系統
    """
    try:
        import os
        # 在 macOS 上可以嘗試設定環境變數
        os.environ['SDL_VIDEO_WINDOW_POS'] = 'centered'
        print("🔝 已嘗試設定 pygame 視窗置頂")
    except Exception as e:
        print(f"⚠️ 設定 pygame 視窗置頂失敗: {e}")


def collect_user_info_if_needed(user_id):
    """
    如果尚未收集使用者資訊，則收集使用者的年齡和手把使用頻率
    用於直接執行單個測試時確保資料完整性
    """
    from . import config
    
    # 檢查是否已經有完整的使用者資訊
    if (hasattr(config, 'user_info') and config.user_info and 
        config.user_info.get('user_id') == user_id and
        config.user_info.get('age') is not None and
        config.user_info.get('controller_usage_frequency') is not None):
        # 資訊已完整，無需重新收集
        print(f"✅ 使用者 '{user_id}' 的資訊已存在，無需重複收集")
        return
    
    print(f"\n📝 為使用者 '{user_id}' 收集基本資訊以完善測試數據：")
    
    # 收集年齡
    while True:
        try:
            age_input = input("請輸入您的年齡: ").strip()
            age = int(age_input)
            if age > 0 and age < 150:  # 合理的年齡範圍
                break
            else:
                print("請輸入有效的年齡 (1-149)")
        except ValueError:
            print("請輸入數字")
    
    # 收集手把使用頻率
    print("\n🎮 手把使用頻率：")
    print("1 = 沒用過")
    print("2 = 有用過但沒有使用習慣") 
    print("3 = 有規律使用習慣")
    while True:
        try:
            freq_input = input("請選擇您的手把使用頻率 (1-3): ").strip()
            controller_usage_frequency = int(freq_input)
            if controller_usage_frequency in [1, 2, 3]:
                break
            else:
                print("請輸入 1、2 或 3")
        except ValueError:
            print("請輸入數字")
    
    # 更新 config 中的使用者資訊
    config.user_info = {
        "user_id": user_id,
        "age": age,
        "controller_usage_frequency": controller_usage_frequency,
        "controller_usage_frequency_description": "1=沒用過, 2=有用過但無習慣, 3=有規律使用"
    }
    
    print(f"✅ 使用者資訊已記錄：{user_id}, 年齡: {age}, 手把使用頻率: {controller_usage_frequency}\n")
