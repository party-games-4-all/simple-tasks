"""
主控程式 - 手把測試應用程式
可以選擇執行單一測試或完整測試套件
"""
import sys
import os
from pathlib import Path

# 添加 common 模組到 Python 路徑
sys.path.append(str(Path(__file__).parent / "common"))

from common.controller_input import ControllerInput
from common.controller_manager import controller_manager
from common import config

def show_menu():
    """顯示測試選單"""
    print("\n" + "="*50)
    print("0. 手把連接測試")
    print("")
    print("Button 測試 (按鈕測試 - 由簡單到難):")
    print("1. 簡單反應時間測試")
    print("2. 預測反應時間測試") 
    print("3. Button Smash 連打測試")
    print("4. 選擇反應測試")
    print("")
    print("Analog 測試 (搖桿測試 - 由簡單到難):")
    print("5. 類比搖桿移動測試")
    print("6. 路徑追蹤測試")
    print("")
    print("9. 退出")
    print("="*50)

def run_single_test(test_num, user_id="test_user"):
    """執行單一測試"""
    test_commands = {
        0: f"uv run python common/connection_test.py --user {user_id}",
        1: f"uv run python tests/button_reaction_time_test.py --user {user_id}",
        2: f"uv run python tests/button_prediction_countdown_test.py --user {user_id}",
        3: f"uv run python tests/button_smash_test.py --user {user_id}",
        4: f"uv run python tests/button_accuracy_test.py --user {user_id}",
        5: f"uv run python tests/analog_move_test.py --user {user_id}",
        6: f"uv run python tests/analog_path_follow_test.py --user {user_id}",
    }
    
    if test_num in test_commands:
        print(f"\n執行測試 {test_num}...")
        os.system(test_commands[test_num])
    else:
        print("無效的測試編號")

def main():
    """主函式"""
    if len(sys.argv) > 1:
        # 如果有命令列參數，直接執行手把輸入測試
        controller = ControllerInput()
        controller.run()
        return
    
    # 在開始測試之前先選擇遙控器
    print("🎮 正在初始化遙控器...")
    controller_selected = controller_manager.setup_controller()
    if not controller_selected:
        print("❌ 無法選擇遙控器，某些測試可能無法正常運行")
        print("您仍然可以進入測試選單，但建議先解決遙控器連接問題")
        input("\n按 Enter 繼續...")
    else:
        info = controller_manager.get_selected_controller_info()
        print(f"🎮 遙控器選擇成功！已選擇：{info['name']}")
    
    # 互動式選單模式
    user_id = input("請輸入使用者ID (預設: test_user): ").strip()
    if not user_id:
        user_id = "test_user"
    
    # 收集使用者基本資訊
    print("\n📝 請提供一些基本資訊以協助數據分析：")
    
    # 年齡
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
    
    # 手把使用頻率
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
    
    # 將使用者資訊存到 config 中供其他模組使用
    config.user_info = {
        "user_id": user_id,
        "age": age,
        "controller_usage_frequency": controller_usage_frequency,
        "controller_usage_frequency_description": "1=沒用過, 2=有用過但無習慣, 3=有規律使用"
    }
    
    print(f"\n✅ 使用者資訊已記錄：{user_id}, 年齡: {age}, 手把使用頻率: {controller_usage_frequency}")
    
    while True:
        show_menu()
        try:
            choice = int(input("\n請選擇測試項目 (0-9): "))
            
            if choice == 9:
                print("感謝使用！")
                break
            elif choice == 8:
                print(f"\n執行完整測試套件 (使用者: {user_id})...")
                os.system(f"./run_all_tests.sh {user_id}")
            elif 0 <= choice <= 6:
                run_single_test(choice, user_id)
            else:
                print("請輸入有效的選項 (0-9)")
                
        except ValueError:
            print("請輸入數字")
        except KeyboardInterrupt:
            print("\n\n程式已中斷")
            break
        
        input("\n按 Enter 繼續...")

if __name__ == "__main__":
    main()