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
from common import config

def show_menu():
    """顯示測試選單"""
    print("\n" + "="*50)
    print("手把測試應用程式")
    print("="*50)
    print("1. 手把連接測試")
    print("2. 簡單反應時間測試")
    print("3. 預測反應時間測試") 
    print("4. 選擇反應測試")
    print("5. 類比搖桿移動測試")
    print("6. 路徑追蹤測試")
    print("7. 執行完整測試套件")
    print("0. 退出")
    print("="*50)

def run_single_test(test_num, user_id="test_user"):
    """執行單一測試"""
    test_commands = {
        1: f"uv run python tests/connection_test.py --user {user_id}",
        2: f"uv run python tests/reaction_time_test.py --user {user_id}",
        3: f"uv run python tests/prediction_reaction_test.py --user {user_id}",
        4: f"uv run python tests/choice_accuracy_test.py --user {user_id}",
        5: f"uv run python tests/analog_move_test.py --user {user_id}",
        6: f"uv run python tests/path_follow_test.py --user {user_id}",
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
    
    # 互動式選單模式
    user_id = input("請輸入使用者ID (預設: test_user): ").strip()
    if not user_id:
        user_id = "test_user"
    
    while True:
        show_menu()
        try:
            choice = int(input("\n請選擇測試項目 (0-7): "))
            
            if choice == 0:
                print("感謝使用！")
                break
            elif choice == 7:
                print(f"\n執行完整測試套件 (使用者: {user_id})...")
                os.system(f"./run_all_tests.sh {user_id}")
            elif 1 <= choice <= 6:
                run_single_test(choice, user_id)
            else:
                print("請輸入有效的選項 (0-7)")
                
        except ValueError:
            print("請輸入數字")
        except KeyboardInterrupt:
            print("\n\n程式已中斷")
            break
        
        input("\n按 Enter 繼續...")

if __name__ == "__main__":
    main()