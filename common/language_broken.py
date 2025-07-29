"""
多語言支援模組
支援中文（繁體）和英文介面
"""

# 語言配置
LANGUAGES = {
    'zh': {
        # 主選單
        'menu_title': "手把測試應用程式",
        'menu_connection_test': "手把連接測試",
        'menu_button_tests': "Button 測試 (按鈕測試 - 由簡單到難):",
        'menu_analog_tests': "Analog 測試 (搖桿測試 - 由簡單到難)        'gui_trial_number': "Trial {trial}",
        'gui_warmup_complete': "Warmup test completed",
        
        # Analog Path Follow Test
        'path_data_saved': "Session data saved to",
        'path_all_complete': "All path tests completed",
        'path_reached_end': "Reached endpoint",
        'path_total_time': "Total time",
        'path_off_path_time': "Off-path time",
        'path_off_path_percentage': "Off-path percentage",
        'path_movement_type': "Movement type",
        'path_straight_segments': "Straight segments",
        'path_corner_segments': "Corner segments",
        'path_test_start': "Test started! Please follow the path",
        'path_no_results': "No test results to save",
        'path_test_summary': "Analog Path Follow Test - Test Summary",
        'path_user': "User",
        'path_total_paths': "Total paths",
        'path_total_used_time': "Total time used",
        'path_avg_completion_time': "Average completion time",
        'path_avg_accuracy': "Average path accuracy",
        'path_basic_analysis': "Basic path type performance analysis:",
        'path_detailed_analysis': "Detailed movement type analysis:",
        
        # Statistics display        'menu_simple_reaction': "簡單反應時間測試",
        'menu_prediction_reaction': "預測反應時間測試",
        'menu_button_smash': "Button Smash 連打測試",
        'menu_choice_reaction': "選擇反應測試",
        'menu_analog_move': "類比搖桿移動測試",
        'menu_path_follow': "路徑追蹤測試",
        'menu_exit': "退出",
        
        # 通用訊息
        'controller_initializing': "🎮 正在初始化遙控器...",
        'controller_failed': "❌ 無法選擇遙控器，某些測試可能無法正常運行",
        'controller_failed_continue': "您仍然可以進入測試選單，但建議先解決遙控器連接問題",
        'controller_success': "🎮 遙控器選擇成功！已選擇：{name}",
        'enter_user_id': "請輸入使用者ID (預設: test_user): ",
        'user_info_recorded': "✅ 使用者資訊已記錄：{user_id}, 年齡: {age}, 手把使用頻率: {frequency}",
        'choose_test': "請選擇測試項目 (0-9): ",
        'invalid_option': "請輸入有效的選項 (0-9)",
        'enter_number': "請輸入數字",
        'program_interrupted': "程式已中斷",
        'press_enter': "按 Enter 繼續...",
        'thank_you': "感謝使用！",
        'running_full_suite': "執行完整測試套件 (使用者: {user_id})...",
        'running_test': "執行測試 {num}...",
        'invalid_test_number': "無效的測試編號",
        
        # 使用者資訊收集
        'user_info_title': "📝 請提供一些基本資訊以協助數據分析：",
        'user_info_exists': "✅ 使用者 '{user_id}' 的資訊已存在，無需重複收集",
        'user_info_supplement': "📝 為使用者 '{user_id}' 收集基本資訊以完善測試數據：",
        'enter_age': "請輸入您的年齡: ",
        'valid_age': "請輸入有效的年齡 (1-149)",
        'controller_frequency_title': "🎮 手把使用頻率：",
        'controller_frequency_desc': "包含 Nintendo Wii / Switch、PS / Xbox 系列家機、掌機、遊樂場街機等",
        'controller_frequency_scale': "1=從來沒用過  2  3  4  5  6  7=每天使用",
        'enter_frequency': "請選擇您的手把使用頻率 (1-7): ",
        'valid_frequency': "請輸入 1-7 之間的數字",
        'user_info_from_cli': "✅ 使用者 '{user_id}' 的資訊已從命令列參數載入",
        
        # 測試共用訊息
        'test_restart': "🔄 已重新開始計算！",
        'test_results_saved': "✅ 測試結果已自動儲存",
        'no_results_to_save': "⚠️ 無測試結果可儲存",
        'closing_app': "🔄 正在安全關閉應用程式...",
        'test_statistics': "📊 測試結果統計",
        'received_interrupt': "🔄 接收到中斷信號，正在關閉...",
        
        # 反應時間測試
        'reaction_test_started': "🔄 已開始反應時間測試系列！",
        'too_fast_restart': "太快了！重新開始第 {trial} 次測試",
        'reaction_time_result': "🔘 第 {trial} 次：反應時間 {time:.3f} 秒",
        'average_reaction_time': "📊 平均反應時間：{time:.3f} 秒",
        'avg_reaction_time_ms': "平均反應時間: {time:.1f} ms",
        'min_reaction_time_ms': "最快反應時間: {time:.1f} ms",
        'max_reaction_time_ms': "最慢反應時間: {time:.1f} ms",
        'reaction_test_end': "🎮 SRT 反應時間測試結束",
        
        # 準確度測試
        'warmup_failed': "❌ 熱身測試答錯，請重新開始熱身測試",
        'warmup_result': "👟 熱身測試：{'正確' if correct else '錯誤'}，反應時間 {time:.3f} 秒",
        'warmup_passed': "✅ 熱身測試通過，開始正式測試",
        'total_trials': "總回合數: {count}",
        'correct_trials': "正確回合: {count}",
        'incorrect_trials': "錯誤回合: {count}",
        'accuracy_percentage': "正確率: {percentage:.1f}%",
        'average_time': "平均反應時間: {time:.3f} 秒",
        
        # 命令列參數說明
        'arg_user_id': "使用者 ID",
        'arg_age': "使用者年齡",
        'arg_controller_freq': "手把使用頻率 (1-7)",
        'arg_english': "使用英文介面",
        
        # 視窗設定
        'window_setup_success': "🖥️ 視窗設定為：{width}x{height}，位置：({x}, {y})",
        'window_setup_failed': "⚠️ 設定視窗置頂失敗: {error}",
        'pygame_window_topmost': "🔝 已嘗試設定 pygame 視窗置頂",
        'pygame_window_failed': "⚠️ 設定 pygame 視窗置頂失敗: {error}",
        
        # GUI 文字 - 按鈕準確度測試
        'gui_press_direction': "請按亮起的方向鍵",
        'gui_start_calculation': "開始計算",
        'gui_restart': "重新開始",
        'gui_warmup_failed_restart': "❌ 熱身測試答錯，請重新開始熱身測試",
        'gui_warmup_passed': "✅ 熱身測試通過，開始正式測試",
        
        # GUI 文字 - 反應時間測試
        'gui_click_start_test': "請按『開始測試』按鈕開始測試",
        'gui_start_test': "開始測試",
        'gui_test_complete_reaction': "測試完成！\n平均反應時間：{time:.3f} 秒\n請按『開始測試』重新開始。",
        
        # GUI 文字 - 預測反應測試
        'gui_ready_prediction': "準備好了嗎？請在球到達灰色圓圈時按下按鈕！",
        'gui_test_complete_saved': "測試完成！結果已儲存。點擊重新開始",
        'gui_restart_test': "重新開始",
        
        # GUI 文字 - 快速點擊測試
        'gui_smash_instructions': "用滑鼠按『開始測試』開始 10 秒快速點擊測試\n測試開始後請用手把同一個按鈕進行點擊\n(也可使用空白鍵作為備用)",
        'gui_waiting_first_click': "等待手把第一次點擊...",
        'gui_remaining_time': "剩餘時間: {time:.1f}s",
        'gui_test_complete_smash': "測試完成！",
        'gui_smash_results': "總點擊數: {count}\nCPS: {cps:.2f}\n(點擊數 ÷ {duration} 秒)",
        'gui_smash_final': "測試完成！總點擊: {count}, CPS: {cps:.2f}",
        
        # GUI 文字 - 搖桿移動測試  
        'gui_analog_instructions': "按『開始測試』後先進行暖身，然後正式測試 (僅使用左手搖桿操作)",
        'gui_test_complete_analog': "✅ 測驗完成",
        'gui_trial_number': "第 {trial} 次",
        'gui_warmup_complete': "暖身測試完成",
        
        # Analog Path Follow Test
        'path_data_saved': "本次資料儲存於",
        'path_all_complete': "所有路徑測試完成",
        'path_reached_end': "到達終點",
        'path_total_time': "總時間",
        'path_off_path_time': "偏離路徑時間",
        'path_off_path_percentage': "偏離比例",
        'path_movement_type': "移動類型",
        'path_straight_segments': "直線段落",
        'path_corner_segments': "轉彎段落",
        'path_test_start': "開始測試！請沿著路徑前進",
        'path_no_results': "無測試結果可儲存",
        'path_test_summary': "Analog Path Follow Test - 測試完成總結",
        'path_user': "使用者",
        'path_total_paths': "總路徑數",
        'path_total_used_time': "總用時",
        'path_avg_completion_time': "平均完成時間",
        'path_avg_accuracy': "平均路徑精確度",
        'path_basic_analysis': "基本路徑類型表現分析：",
        'path_detailed_analysis': "詳細移動類型分析：",
        
        # 統計顯示
        'stats_total_trials': "總回合數: {count}",
        'stats_correct_trials': "正確回合: {count}",
        'stats_incorrect_trials': "錯誤回合: {count}",
        'stats_accuracy_percentage': "正確率: {percentage:.1f}%",
        'stats_average_time': "平均反應時間: {time:.3f} 秒",
        'stats_avg_reaction_time_ms': "平均反應時間: {time:.1f} ms",
        'stats_min_reaction_time_ms': "最快反應時間: {time:.1f} ms",
        'stats_max_reaction_time_ms': "最慢反應時間: {time:.1f} ms",
    },
    
    'en': {
        # Main menu
        'menu_title': "Controller Testing Application",
        'menu_connection_test': "Controller Connection Test",
        'menu_button_tests': "Button Tests (Simple to Complex):",
        'menu_analog_tests': "Analog Tests (Simple to Complex):",
        'menu_simple_reaction': "Simple Reaction Time Test",
        'menu_prediction_reaction': "Prediction Reaction Time Test",
        'menu_button_smash': "Button Smash Test",
        'menu_choice_reaction': "Choice Reaction Test",
        'menu_analog_move': "Analog Stick Movement Test",
        'menu_path_follow': "Path Following Test",
        'menu_exit': "Exit",
        
        # Common messages
        'controller_initializing': "🎮 Initializing controller...",
        'controller_failed': "❌ Unable to select controller, some tests may not work properly",
        'controller_failed_continue': "You can still access the test menu, but we recommend fixing the controller connection first",
        'controller_success': "🎮 Controller selected successfully! Selected: {name}",
        'enter_user_id': "Enter user ID (default: test_user): ",
        'user_info_recorded': "✅ User information recorded: {user_id}, Age: {age}, Controller usage: {frequency}",
        'choose_test': "Choose a test item (0-9): ",
        'invalid_option': "Please enter a valid option (0-9)",
        'enter_number': "Please enter a number",
        'program_interrupted': "Program interrupted",
        'press_enter': "Press Enter to continue...",
        'thank_you': "Thank you for using!",
        'running_full_suite': "Running full test suite (user: {user_id})...",
        'running_test': "Running test {num}...",
        'invalid_test_number': "Invalid test number",
        
        # User information collection
        'user_info_title': "📝 Please provide some basic information to help with data analysis:",
        'user_info_exists': "✅ User '{user_id}' information already exists, no need to collect again",
        'user_info_supplement': "📝 Collecting basic information for user '{user_id}' to complete test data:",
        'enter_age': "Enter your age: ",
        'valid_age': "Please enter a valid age (1-149)",
        'controller_frequency_title': "🎮 Controller usage frequency:",
        'controller_frequency_desc': "Including Nintendo Wii/Switch, PS/Xbox consoles, handhelds, arcade machines, etc.",
        'controller_frequency_scale': "1=Never used  2  3  4  5  6  7=Daily use",
        'enter_frequency': "Choose your controller usage frequency (1-7): ",
        'valid_frequency': "Please enter a number between 1-7",
        'user_info_from_cli': "✅ User '{user_id}' information loaded from command line parameters",
        
        # Test common messages
        'test_restart': "🔄 Restarted calculation!",
        'test_results_saved': "✅ Test results saved automatically",
        'no_results_to_save': "⚠️ No test results to save",
        'closing_app': "🔄 Safely closing application...",
        'test_statistics': "📊 Test Result Statistics",
        'received_interrupt': "🔄 Received interrupt signal, closing...",
        
        # Reaction time test
        'reaction_test_started': "🔄 Started reaction time test series!",
        'too_fast_restart': "Too fast! Restarting trial {trial}",
        'reaction_time_result': "🔘 Trial {trial}: Reaction time {time:.3f} seconds",
        'average_reaction_time': "📊 Average reaction time: {time:.3f} seconds",
        'avg_reaction_time_ms': "Average reaction time: {time:.1f} ms",
        'min_reaction_time_ms': "Fastest reaction time: {time:.1f} ms",
        'max_reaction_time_ms': "Slowest reaction time: {time:.1f} ms",
        'reaction_test_end': "🎮 SRT Reaction Time Test Completed",
        
        # Accuracy test
        'warmup_failed': "❌ Warmup test failed, please restart warmup",
        'warmup_result': "👟 Warmup test: {'Correct' if correct else 'Incorrect'}, reaction time {time:.3f} seconds",
        'warmup_passed': "✅ Warmup test passed, starting formal test",
        'total_trials': "Total trials: {count}",
        'correct_trials': "Correct trials: {count}",
        'incorrect_trials': "Incorrect trials: {count}",
        'accuracy_percentage': "Accuracy: {percentage:.1f}%",
        'average_time': "Average reaction time: {time:.3f} seconds",
        
        # Command line argument descriptions
        'arg_user_id': "User ID",
        'arg_age': "User age",
        'arg_controller_freq': "Controller usage frequency (1-7)",
        'arg_english': "Use English interface",
        
        # Window setup
        'window_setup_success': "🖥️ Window set to: {width}x{height}, position: ({x}, {y})",
        'window_setup_failed': "⚠️ Failed to set window topmost: {error}",
        'pygame_window_topmost': "🔝 Attempted to set pygame window topmost",
        'pygame_window_failed': "⚠️ Failed to set pygame window topmost: {error}",
        
        # GUI Text - Button Accuracy Test
        'gui_press_direction': "Press the highlighted direction key",
        'gui_start_calculation': "Start Test",
        'gui_restart': "Restart",
        'gui_warmup_failed_restart': "❌ Warmup test failed, please restart warmup",
        'gui_warmup_passed': "✅ Warmup test passed, starting formal test",
        
        # GUI Text - Reaction Time Test
        'gui_click_start_test': "Click 'Start Test' button to begin",
        'gui_start_test': "Start Test",
        'gui_test_complete_reaction': "Test Complete!\nAverage reaction time: {time:.3f} seconds\nClick 'Start Test' to restart.",
        
        # GUI Text - Prediction Reaction Test
        'gui_ready_prediction': "Ready? Press the button when the ball reaches the gray circle!",
        'gui_test_complete_saved': "Test complete! Results saved. Click to restart",
        'gui_restart_test': "Restart",
        
        # GUI Text - Button Smash Test
        'gui_smash_instructions': "Use mouse to click 'Start Test' for 10-second rapid clicking test\nAfter test starts, use the same controller button to click\n(Space bar can be used as backup)",
        'gui_waiting_first_click': "Waiting for first controller input...",
        'gui_remaining_time': "Time remaining: {time:.1f}s",
        'gui_test_complete_smash': "Test Complete!",
        'gui_smash_results': "Total clicks: {count}\nCPS: {cps:.2f}\n(Clicks ÷ {duration} seconds)",
        'gui_smash_final': "Test complete! Total clicks: {count}, CPS: {cps:.2f}",
        
        # GUI Text - Analog Movement Test
        'gui_analog_instructions': "Click 'Start Test' for warmup first, then formal test (use left stick only)",
        'gui_test_complete_analog': "✅ Test Complete",
        'gui_trial_number': "Trial {count}",
        'gui_warmup_complete': "Warmup complete, starting formal test",
        
        # Statistics Display
        'stats_total_trials': "Total trials: {count}",
        'stats_correct_trials': "Correct trials: {count}",
        'stats_incorrect_trials': "Incorrect trials: {count}",
        'stats_accuracy_percentage': "Accuracy: {percentage:.1f}%",
        'stats_average_time': "Average reaction time: {time:.3f} seconds",
        'stats_avg_reaction_time_ms': "Average reaction time: {time:.1f} ms",
        'stats_min_reaction_time_ms': "Fastest reaction time: {time:.1f} ms",
        'stats_max_reaction_time_ms': "Slowest reaction time: {time:.1f} ms",
    }
}

# 目前語言設定 (預設為中文)
current_language = 'zh'

def set_language(language_code):
    """設定目前使用的語言"""
    global current_language
    if language_code in LANGUAGES:
        current_language = language_code
    else:
        print(f"Warning: Language '{language_code}' not supported, using default 'zh'")

def get_text(key, **kwargs):
    """
    取得當前語言的文字
    
    Args:
        key: 文字鍵值
        **kwargs: 格式化參數
        
    Returns:
        格式化後的文字字串
    """
    try:
        text = LANGUAGES[current_language].get(key, key)
        if kwargs:
            return text.format(**kwargs)
        return text
    except (KeyError, ValueError) as e:
        # 如果格式化失敗，回傳原始鍵值
        print(f"Warning: Text formatting failed for key '{key}': {e}")
        return key

def get_current_language():
    """取得目前語言代碼"""
    return current_language

def is_english():
    """檢查是否為英文模式"""
    return current_language == 'en'

def is_chinese():
    """檢查是否為中文模式"""
    return current_language == 'zh'
