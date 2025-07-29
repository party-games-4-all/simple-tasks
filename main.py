"""
主控程式 - 手把測試應用程式
可以選擇執行單一測試或完整測試套件
"""
import sys
import os
import argparse
from pathlib import Path

# 添加 common 模組到 Python 路徑
sys.path.append(str(Path(__file__).parent / "common"))

from common.controller_input import ControllerInput
from common.controller_manager import controller_manager
from common import config
from common.utils import collect_user_info_if_needed
from common.language import set_language, get_text

def show_menu():
    """顯示測試選單"""
    print("\n" + "="*50)
    print(f"0. {get_text('menu_connection_test')}")
    print("")
    print(get_text('menu_button_tests'))
    print(f"1. {get_text('menu_simple_reaction')}")
    print(f"2. {get_text('menu_prediction_reaction')}")
    print(f"3. {get_text('menu_button_smash')}")
    print(f"4. {get_text('menu_choice_reaction')}")
    print("")
    print(get_text('menu_analog_tests'))
    print(f"5. {get_text('menu_analog_move')}")
    print(f"6. {get_text('menu_path_follow')}")
    print("")
    print(f"9. {get_text('menu_exit')}")
    print("="*50)

def run_single_test(test_num, user_id="test_user", age=None, controller_usage_frequency=None, use_english=False):
    """執行單一測試"""
    # 建構基本命令
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
        command = test_commands[test_num]
        
        # 如果有使用者資訊，加入命令列參數
        if age is not None:
            command += f" --age {age}"
        if controller_usage_frequency is not None:
            command += f" --controller-freq {controller_usage_frequency}"
        
        # 如果使用英文，加入 --english 參數
        if use_english:
            command += " --english"
            
        print(f"\n{get_text('running_test', num=test_num)}")
        os.system(command)
    else:
        print(get_text('invalid_test_number'))

def main():
    """主函式"""
    # 檢查是否有 --english 參數來提前設定語言
    if '--english' in sys.argv:
        set_language('en')
    else:
        set_language('zh')
    
    # 解析命令列參數
    parser = argparse.ArgumentParser(description=get_text('menu_title'))
    parser.add_argument("--english", action="store_true", help=get_text('arg_english'))
    args = parser.parse_args()
    
    if len(sys.argv) > 1 and not args.english:
        # 如果有其他命令列參數（非語言參數），直接執行手把輸入測試
        controller = ControllerInput()
        controller.run()
        return
    
    # 在開始測試之前先選擇遙控器
    print(get_text('controller_initializing'))
    controller_selected = controller_manager.setup_controller()
    if not controller_selected:
        print(get_text('controller_failed'))
        print(get_text('controller_failed_continue'))
        input(f"\n{get_text('press_enter')}")
    else:
        info = controller_manager.get_selected_controller_info()
        print(get_text('controller_success', name=info['name']))
    
    # 互動式選單模式
    user_id = input(get_text('enter_user_id')).strip()
    if not user_id:
        user_id = "test_user"
    
    # 收集使用者基本資訊（使用 utils 中的共用函數）
    collect_user_info_if_needed(user_id)
    
    # 從 config 取得收集到的資訊
    age = config.user_info.get('age')
    controller_usage_frequency = config.user_info.get('controller_usage_frequency')
    
    print(f"\n{get_text('user_info_recorded', user_id=user_id, age=age, frequency=controller_usage_frequency)}")
    
    while True:
        show_menu()
        try:
            choice = int(input(f"\n{get_text('choose_test')}"))
            
            if choice == 9:
                print(get_text('thank_you'))
                break
            elif choice == 8:
                print(f"\n{get_text('running_full_suite', user_id=user_id)}")
                os.system(f"./run_all_tests.sh {user_id}")
            elif 0 <= choice <= 6:
                run_single_test(choice, user_id, age, controller_usage_frequency, args.english)
            else:
                print(get_text('invalid_option'))
                
        except ValueError:
            print(get_text('enter_number'))
        except KeyboardInterrupt:
            print(f"\n\n{get_text('program_interrupted')}")
            break
        
        input(f"\n{get_text('press_enter')}")

if __name__ == "__main__":
    main()