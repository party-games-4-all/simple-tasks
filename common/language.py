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
        'menu_analog_tests': "Analog 測試 (搖桿測試 - 由簡單到難):",
        'menu_simple_reaction': "簡單反應時間測試",
        'menu_prediction_reaction': "預測反應時間測試",
        'menu_button_smash': "Button Smash 連打測試",
        'menu_choice_reaction': "選擇反應測試",
        'menu_analog_move': "類比搖桿移動測試",
        'menu_path_follow': "路徑追蹤測試",
        'menu_exit': "退出",
        
        # Button Accuracy Test
        'button_accuracy_window_title': "按鍵準確度測試",
        'button_accuracy_warmup_test': "不計分測試",
        'button_accuracy_formal_test': "第 {}/10 次",
        'button_accuracy_ready_message': "準備好了嗎？",
        'button_accuracy_start_button': "開始",
        'button_accuracy_correct_feedback': "✅ 正確！",
        'button_accuracy_incorrect_feedback': "❌ 錯誤！正確是 {}",
        'button_accuracy_test_summary': "測驗結束 正確率：{:.1%}｜平均反應時間：{:.3f} 秒",
        'button_accuracy_statistics_output': "📊 平均反應時間：{:.3f} 秒｜錯誤率：{:.1%}",
        'button_accuracy_results_saved': "✅ 測試結果已自動儲存",
        'button_accuracy_warmup_feedback': "👟 熱身測試：{}，反應時間 {:.3f} 秒",
        'button_accuracy_formal_feedback': "🔘 回合 {}：{}，反應時間 {:.3f} 秒",
        'button_accuracy_correct': "正確",
        'button_accuracy_incorrect': "錯誤",
        'button_accuracy_warmup_passed': "✅ 熱身測試通過，開始正式測試",
        'button_accuracy_test_finished': "測試結束",
        'button_accuracy_test_end': "🎮 按鍵準確度測試結束",
        
        # Button Reaction Time Test
        'button_reaction_window_title': "反應時間測試",
        'button_reaction_test_description': "反應時間測試",
        'user_id_input_prompt': "請輸入使用者 ID (例如: P1): ",
        
        # Button Smash Test
        'button_smash_window_title': "Button Smash 連打測試",
        'button_smash_test_description': "Button Smash 連打測試",
        'button_smash_test_started': "🎮 Button Smash 測試開始！用手把按鈕開始第一次點擊...",
        'button_smash_test_complete_msg': "🎯 測試完成！",
        'button_smash_total_clicks': "📊 總點擊數: {count}",
        'button_smash_test_time': "⏱️ 測試時間: {duration} 秒",
        'button_smash_cps_calculation': "📈 計算方式: {count} ÷ {duration} = {cps:.2f}",
        'button_smash_test_statistics': "📊 測試結果統計",
        'button_smash_click_rate': "點擊率: {cps:.2f} CPS",
        'button_smash_performance_rating': "表現評級: {rating}",
        'button_smash_excellent': "優秀",
        'button_smash_good': "良好",
        'button_smash_average': "普通",
        'button_smash_needs_practice': "需要練習",
        'button_smash_beginner': "初學者",
        'button_smash_designated_button': "🎮 指定按鈕: {button}",
        'button_smash_start_timing': "⏰ 開始計時！",
        'button_smash_click_record': "🖱️ 點擊 #{count} (t={time:.1f}ms)",
        'button_smash_test_mode_help': "執行測試模式",
        'button_smash_user_info_loaded': "✅ 使用者 '{user_id}' 的資訊已從命令列參數載入",
        'button_smash_test_mode_verify': "🧪 測試模式：驗證 CPS 計算...",
        'button_smash_test_complete_verify': "✅ 測試完成",
        'button_smash_interrupt_signal': "🔄 接收到中斷信號，正在關閉...",
        'button_smash_test_end': "🎮 Button Smash 測試結束",
        
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
        
        # 控制器相關訊息
        'controller_unable_connect': "❌ 無法連接已選擇的遙控器，嘗試自動選擇...",
        'controller_no_pairing': "❌ 無法配對任何遙控器", 
        'controller_signal_received': "🔄 接收到信號 {signum}，正在安全關閉控制器...",
        'controller_no_gamepad': "❌ 未偵測到任何🎮手把",
        'controller_auto_connect': "🎮 自動連接遙控器：{name}",
        'controller_auto_connect_failed': "❌ 自動連接遙控器失敗：{error}",
        'controller_detected_count': "🎮 偵測到 {count} 支手把",
        'controller_detected': "🔍 偵測到手把：{name}",
        'controller_selected': "✅ 已選擇：{name}",
        'controller_none_selected': "❌ 沒有選擇任何手把",
        'controller_listening': "🎮 開始監聽手把事件... (Ctrl+C 中止)",
        'controller_axis_move': "軸移動：{axis} -> {value}",
        'controller_analog_error': "⚠️ 處理類比輸入時發生錯誤: {error}",
        'controller_button_press': "按下按鍵：{button}",
        'controller_button_press_error': "⚠️ 處理按鍵按下時發生錯誤: {error}",
        'controller_button_release': "放開按鍵：{button}",
        'controller_button_release_error': "⚠️ 處理按鍵放開時發生錯誤: {error}",
        'controller_event_error': "⚠️ 處理事件時發生錯誤: {error}",
        'controller_thread_error': "❌ 控制器執行緒發生嚴重錯誤: {error}",
        'controller_thread_ended': "🔄 控制器監聽執行緒已安全結束",
        'controller_listening_stopped': "🔄 控制器輸入監聽已停止",
        'controller_use_device': "要使用這個裝置嗎？(Y/n): ",
        'controller_not_selected_yet': "❌ 尚未選擇遙控器",
        'controller_not_exist': "❌ 遙控器 {index} 不存在，當前有 {count} 支手把",
        'controller_connected': "🎮 已連接遙控器：{name}",
                'controller_connect_failed': "❌ Failed to connect controller: {error}",
        
        # Trace plot related
        'trace_saved_in': "Session trace saved in",
        'trace_no_data': "Trial {index} has no recorded data",
        'trace_image_saved': "Saved",
        'trace_path_no_data': "Path {index} has no trace data",
        'trace_path_saved': "Saved path {index} trace diagram",
        
        # Reaction time test
        
        # 軌跡圖相關
        'trace_saved_in': "本次軌跡儲存在",
        'trace_no_data': "第 {index} 筆無紀錄資料",
        'trace_image_saved': "已儲存",
        'trace_path_no_data': "路徑 {index} 無軌跡資料",
        'trace_path_saved': "已儲存路徑 {index} 軌跡圖",
        
        # 反應時間測試
        'controller_in_use': "使用中手把",
        'controller_axis_move_debug': "軸移動：{axis} -> {value}",
        'controller_button_press_debug': "按下按鍵：{button}",
        'controller_button_release_debug': "放開按鍵：{button}",
        'controller_stop_listening': "🎮 停止監聽手把事件",
        'controller_no_gamepad_detected': "未偵測到手把",
        
        # 軌跡繪圖相關
        'trace_saved_in': "本次軌跡儲存在",
        'trace_no_data': "第 {index} 筆無紀錄資料",
        'trace_image_saved': "已儲存：{path}",
        'trace_no_path_data': "路徑 {index} 無軌跡資料",
        'trace_path_saved': "已儲存路徑 {index} 軌跡圖：{path}",
        
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
                # GUI Text - Analog Movement Test
        'gui_analog_instructions': "按『開始測試』後先進行暖身，然後正式測試 (僅使用左手搖桿操作)",
        'gui_test_complete_analog': "✅ 測驗完成",
        'gui_trial_number': "第 {trial} 次",
        'gui_warmup_complete': "暖身測試完成",
        
        # Analog Move Test specific messages
        'window_title_analog_move': "Joystick 移動目標測試",
        'trial_success': "✅ 第 {trial} 次成功",
        'trial_position': "🎯 位置：{position} ({size_type}-{distance_type})",
        'trial_time': "⏱ 用時：{time:.2f} 秒",
        'trial_distance': "📏 距離：{distance:.1f} px", 
        'trial_efficiency': "⚡ 單位距離時間：{efficiency:.4f} 秒/像素",
        'trial_average': "📊 平均時間：{avg_time:.2f} 秒，平均秒/像素：{avg_efficiency:.4f}",
        'warmup_complete_formal': "🎯 現在開始正式測試...",
        'warmup_complete_status': "暖身完成，開始正式測試",
        'saving_results': "⚠️ 無測試結果可儲存",
        'update_position_error': "⚠️ 更新玩家位置時發生錯誤: {error}",
        'closing_app_safely': "🔄 正在安全關閉應用程式...",
        'enter_user_id_prompt': "請輸入使用者 ID (例如: P1): ",
        'user_info_loaded_cli': "✅ 使用者 '{user_id}' 的資訊已從命令列參數載入",
        'interrupt_signal': "🔄 接收到中斷信號，正在關閉...",
        'fitts_law_test_end': "🎮 Fitt's Law 測試結束",
        'controller_usage_freq_desc': "1=從來沒用過, 7=每天使用",
        
        # Test summary messages
        'test_summary_title': "🎯 ISO9241 Analog Move Test - 測試完成總結",
        'test_summary_separator': "=" * 50,
        'test_summary_user': "👤 使用者：{user_id}",
        'test_summary_trials': "🎯 正式測試次數：{trials}",
        'test_summary_warmup': "🏃 包含暖身測試：是 (第0次不計入統計)",
        'test_summary_total_time': "⏱️ 總用時：{time:.2f} 秒",
        'test_summary_avg_time': "📊 平均用時：{time:.2f} 秒",
        'test_summary_avg_efficiency': "⚡ 平均效率：{efficiency:.4f} 秒/像素",
        'test_summary_standard': "🎪 測試標準：ISO9241 九點圓形指向測試",
        'test_summary_distances': "📏 長距離：{long} 像素，短距離：{short} 像素",
        'test_summary_combinations': "🎯 測試組合：長距離大小目標 + 短距離大小目標",
        'test_summary_analysis': "📈 各難度表現分析：",
        'difficulty_item': "  {difficulty}: {count} 次，平均 {avg_time:.0f} ms",
        'trace_image_saved_path': "軌跡圖片儲存在: {path}",
        
        # Analog Path Follow Test specific messages
        'window_title_path_follow': "🎮 Path Following 測試 (簡化版本)",
        'path_test_interrupted': "🔴 測試被中斷",
        'path_test_completed': "🎮 Path Following 測試結束",
        'path_total_time_format': "⏱ 總時間：{time:.2f} 秒",
        'path_off_path_time_format': "❌ 偏離路徑時間：{time:.2f} 秒", 
        'path_off_path_percentage_format': "📊 偏離比例：{percentage:.2f}%",
        'path_movement_type_format': "🔄 移動類型：{type}",
        'path_straight_segments_format': "📏 直線段落：{count} 個",
        'path_corner_segments_format': "🔄 轉彎段落：{count} 個",
        'path_total_paths_format': "🎯 總路徑數：{trials} (4條直線 + 8種L型)",
        'path_total_used_time_format': "⏱️ 總用時：{time:.2f} 秒",
        'path_avg_completion_time_format': "📊 平均完成時間：{time:.2f} 秒",
        'path_avg_accuracy_format': "🎯 平均路徑精確度：{accuracy:.1f}%",
        'path_user_format': "👤 使用者：{user_id}",
        
        # Button Prediction Countdown Test specific messages
        'window_title_prediction_countdown': "🎮 預測反應時間測試 - 遊戲化版本",
        'ball_launched': "🚀 發射第 {ball_number} 個球 (已發射: {launched}/{total})",
        'ball_missed': "⏰ 錯過了第 {ball_number} 個球！球繼續往右移動...",
        'all_balls_processed': "✅ 所有 {total} 顆球已處理完畢，結束測試",
        'button_press_check': "⚡ 按鍵時刻，檢查 {count} 個活躍球:",
        'ball_elapsed_time': "  球 {number}: 經過時間 {elapsed:.2f}s",
        'current_best_choice': "    -> 目前最佳選擇 (評分: {score:.4f})",
        'relaxed_condition_search': "  第一輪未找到，放寬條件...",
        'ball_elapsed_relaxed': "  球 {number} (放寬): 經過時間 {elapsed:.2f}s",
        'relaxed_best_choice': "    -> 放寬條件下最佳選擇",
        'no_suitable_ball': "⚠️ 沒有找到適合的球！",
        'ball_hit': "🎯 擊中球 {number} (經過時間: {elapsed:.2f}s)",
        'feedback_perfect': "🎯 完美！",
        'feedback_great': "👍 很好！",
        'feedback_good': "👌 不錯！",
        'feedback_practice': "💪 再練習一下！",
        'timing_too_fast': "快了",
        'timing_too_slow': "慢了",
        'ball_feedback_format': "球 {number}: {feedback} {direction} {accuracy:.0f} 毫秒",
        'test_completing': "🎮 測試完成！正在輸出結果...",
        'final_statistics': "📊 最終統計結果：",
        'total_trials_count': "總測試次數: {count}",
        'successful_responses': "成功響應: {count}",
        'missed_responses': "錯過響應: {count}",
        'success_rate_percent': "成功率: {rate:.1f}%",
        'average_error_ms': "平均誤差: {error:.1f} ms",
        'all_missed_warning': "⚠️ 所有測試皆未按下按鈕",
        'results_saved_success': "✅ 結果已成功儲存到 JSON 檔案",
        'missed_ball_feedback': "錯過",
        'save_result_success': "💾 測試結果已成功儲存！",
        'save_result_error': "❌ 儲存結果時發生錯誤: {error}",
        'detailed_test_statistics': "📊 詳細測試結果統計",
        'user_id_label': "使用者 ID: {user_id}",
        'minimum_error_ms': "最小誤差: {error:.1f} ms",
        'maximum_error_ms': "最大誤差: {error:.1f} ms",
        'prediction_test_end': "🎮 預測反應時間測試結束",
        
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
        'path_horizontal_straight': "水平直線",
        'path_vertical_straight': "垂直直線",
        'path_corner_turns': "L型轉彎",
        'path_stats_format': "{name}: {count} 條，平均時間 {time:.2f}s，精確度 {accuracy:.1f}%",
        
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
        
        # Controller related messages
        'controller_unable_connect': "❌ Unable to connect selected controller, trying auto-select...",
        'controller_no_pairing': "❌ Unable to pair any controller",
        'controller_signal_received': "🔄 Received signal {signum}, safely closing controller...",
        'controller_no_gamepad': "❌ No 🎮 gamepad detected",
        'controller_auto_connect': "🎮 Auto-connected controller: {name}",
        'controller_auto_connect_failed': "❌ Auto-connect controller failed: {error}",
        'controller_detected_count': "🎮 Detected {count} gamepad(s)",
        'controller_detected': "🔍 Detected gamepad: {name}",
        'controller_selected': "✅ Selected: {name}",
        'controller_none_selected': "❌ No gamepad selected",
        'controller_listening': "🎮 Start listening gamepad events... (Ctrl+C to stop)",
        'controller_axis_move': "Axis move: {axis} -> {value}",
        'controller_analog_error': "⚠️ Error processing analog input: {error}",
        'controller_button_press': "Button pressed: {button}",
        'controller_button_press_error': "⚠️ Error processing button press: {error}",
        'controller_button_release': "Button released: {button}",
        'controller_button_release_error': "⚠️ Error processing button release: {error}",
        'controller_event_error': "⚠️ Error processing event: {error}",
        'controller_thread_error': "❌ Controller thread critical error: {error}",
        'controller_thread_ended': "🔄 Controller listening thread ended safely",
        'controller_listening_stopped': "🔄 Controller input listening stopped",
        'controller_use_device': "Use this device? (Y/n): ",
        'controller_not_selected_yet': "❌ No controller selected yet",
        'controller_not_exist': "❌ Controller {index} does not exist, currently {count} gamepad(s) available",
        'controller_connected': "🎮 Connected controller: {name}",
        'controller_connect_failed': "❌ Failed to connect controller: {error}",
        'controller_in_use': "Controller in use",
        'controller_axis_move_debug': "Axis move: {axis} -> {value}",
        'controller_button_press_debug': "Button pressed: {button}",
        'controller_button_release_debug': "Button released: {button}",
        'controller_stop_listening': "🎮 Stop listening gamepad events",
        'controller_no_gamepad_detected': "No gamepad detected",
        
        # Trace plotting related
        'trace_saved_in': "Session trace saved in",
        'trace_no_data': "No recorded data for trial {index}",
        'trace_image_saved': "Saved: {path}",
        'trace_no_path_data': "No trace data for path {index}",
        'trace_path_saved': "Saved path {index} trace diagram: {path}",
        
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
        'gui_trial_number': "Trial {trial}",
        'gui_warmup_complete': "Warmup test completed",
        
        # Analog Move Test specific messages
        'window_title_analog_move': "Joystick Movement Target Test",
        'trial_success': "✅ Trial {trial} completed successfully",
        'trial_position': "🎯 Position: {position} ({size_type}-{distance_type})",
        'trial_time': "⏱ Time: {time:.2f} seconds",
        'trial_distance': "📏 Distance: {distance:.1f} px",
        'trial_efficiency': "⚡ Time per unit distance: {efficiency:.4f} s/px",
        'trial_average': "📊 Average time: {avg_time:.2f}s, average s/px: {avg_efficiency:.4f}",
        'warmup_complete_formal': "🎯 Starting formal test now...",
        'warmup_complete_status': "Warmup complete, starting formal test",
        'saving_results': "⚠️ No test results to save",
        'update_position_error': "⚠️ Error updating player position: {error}",
        'closing_app_safely': "🔄 Safely closing application...",
        'enter_user_id_prompt': "Enter user ID (e.g., P1): ",
        'user_info_loaded_cli': "✅ User '{user_id}' information loaded from command line parameters",
        'interrupt_signal': "🔄 Received interrupt signal, closing...",
        'fitts_law_test_end': "🎮 Fitt's Law Test Completed",
        'controller_usage_freq_desc': "1=Never used, 7=Daily use",
        
        # Test summary messages
        'test_summary_title': "🎯 ISO9241 Analog Move Test - Test Summary",
        'test_summary_separator': "=" * 50,
        'test_summary_user': "👤 User: {user_id}",
        'test_summary_trials': "🎯 Formal test trials: {trials}",
        'test_summary_warmup': "🏃 Includes warmup test: Yes (Trial 0 not counted in statistics)",
        'test_summary_total_time': "⏱️ Total time: {time:.2f} seconds",
        'test_summary_avg_time': "📊 Average time: {time:.2f} seconds",
        'test_summary_avg_efficiency': "⚡ Average efficiency: {efficiency:.4f} s/px",
        'test_summary_standard': "🎪 Test standard: ISO9241 nine-point circular pointing test",
        'test_summary_distances': "📏 Long distance: {long} pixels, short distance: {short} pixels",
        'test_summary_combinations': "🎯 Test combinations: Long/short distance with large/small targets",
        'test_summary_analysis': "📈 Performance analysis by difficulty:",
        'difficulty_item': "  {difficulty}: {count} trials, average {avg_time:.0f} ms",
        'trace_image_saved_path': "Trace images saved in: {path}",
        
        # Analog Path Follow Test specific messages
        'window_title_path_follow': "🎮 Path Following Test (Simplified Version)",
        'path_test_interrupted': "🔴 Test interrupted",
        'path_test_completed': "🎮 Path Following Test Completed",
        'path_total_time_format': "⏱ Total time: {time:.2f} seconds",
        'path_off_path_time_format': "❌ Off-path time: {time:.2f} seconds",
        'path_off_path_percentage_format': "📊 Off-path percentage: {percentage:.2f}%", 
        'path_movement_type_format': "🔄 Movement type: {type}",
        'path_straight_segments_format': "📏 Straight segments: {count}",
        'path_corner_segments_format': "🔄 Corner segments: {count}",
        'path_total_paths_format': "🎯 Total paths: {trials} (4 straight + 8 L-shaped)",
        'path_total_used_time_format': "⏱️ Total time used: {time:.2f} seconds",
        'path_avg_completion_time_format': "📊 Average completion time: {time:.2f} seconds",
        'path_avg_accuracy_format': "🎯 Average path accuracy: {accuracy:.1f}%",
        'path_user_format': "👤 User: {user_id}",
        
        # Button Prediction Countdown Test specific messages
        'window_title_prediction_countdown': "🎮 Prediction Reaction Time Test - Gamified Version",
        'ball_launched': "🚀 Launched ball {ball_number} (launched: {launched}/{total})",
        'ball_missed': "⏰ Missed ball {ball_number}! Ball continues moving right...",
        'all_balls_processed': "✅ All {total} balls processed, ending test",
        'button_press_check': "⚡ Button press moment, checking {count} active balls:",
        'ball_elapsed_time': "  Ball {number}: elapsed time {elapsed:.2f}s",
        'current_best_choice': "    -> Current best choice (score: {score:.4f})",
        'relaxed_condition_search': "  First round not found, relaxing conditions...",
        'ball_elapsed_relaxed': "  Ball {number} (relaxed): elapsed time {elapsed:.2f}s",
        'relaxed_best_choice': "    -> Best choice under relaxed conditions",
        'no_suitable_ball': "⚠️ No suitable ball found!",
        'ball_hit': "🎯 Hit ball {number} (elapsed time: {elapsed:.2f}s)",
        'feedback_perfect': "🎯 Perfect!",
        'feedback_great': "👍 Great!",
        'feedback_good': "👌 Good!",
        'feedback_practice': "💪 Keep practicing!",
        'timing_too_fast': "too fast",
        'timing_too_slow': "too slow",
        'ball_feedback_format': "Ball {number}: {feedback} {direction} {accuracy:.0f} milliseconds",
        'test_completing': "🎮 Test completed! Outputting results...",
        'final_statistics': "📊 Final statistics:",
        'total_trials_count': "Total trials: {count}",
        'successful_responses': "Successful responses: {count}",
        'missed_responses': "Missed responses: {count}",
        'success_rate_percent': "Success rate: {rate:.1f}%",
        'average_error_ms': "Average error: {error:.1f} ms",
        'all_missed_warning': "⚠️ All tests missed - no button pressed",
        'results_saved_success': "✅ Results successfully saved to JSON file",
        'missed_ball_feedback': "Missed",
        'save_result_success': "💾 Test results successfully saved!",
        'save_result_error': "❌ Error occurred while saving results: {error}",
        'detailed_test_statistics': "📊 Detailed Test Result Statistics",
        'user_id_label': "User ID: {user_id}",
        'minimum_error_ms': "Minimum error: {error:.1f} ms",
        'maximum_error_ms': "Maximum error: {error:.1f} ms",
        'prediction_test_end': "🎮 Prediction Reaction Time Test Completed",
        
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
        'path_horizontal_straight': "Horizontal straight",
        'path_vertical_straight': "Vertical straight",
        'path_corner_turns': "L-shaped turns",
        'path_stats_format': "{name}: {count} paths, avg time {time:.2f}s, accuracy {accuracy:.1f}%",
        
        # Statistics Display
        'stats_total_trials': "Total trials: {count}",
        'stats_correct_trials': "Correct trials: {count}",
        'stats_incorrect_trials': "Incorrect trials: {count}",
        'stats_accuracy_percentage': "Accuracy: {percentage:.1f}%",
        'stats_average_time': "Average reaction time: {time:.3f} seconds",
        'stats_avg_reaction_time_ms': "Average reaction time: {time:.1f} ms",
        'stats_min_reaction_time_ms': "Fastest reaction time: {time:.1f} ms",
        'stats_max_reaction_time_ms': "Slowest reaction time: {time:.1f} ms",
        
        # Button Accuracy Test
        'button_accuracy_window_title': "Button Accuracy Test",
        'button_accuracy_warmup_test': "Practice Test",
        'button_accuracy_formal_test': "Round {}/10",
        'button_accuracy_ready_message': "Are you ready?",
        'button_accuracy_start_button': "Start",
        'button_accuracy_correct_feedback': "✅ Correct!",
        'button_accuracy_incorrect_feedback': "❌ Incorrect! Correct answer is {}",
        'button_accuracy_test_summary': "Test Complete\nAccuracy: {:.1%}｜Average Response Time: {:.3f} sec",
        'button_accuracy_statistics_output': "📊 Average Response Time: {:.3f} sec｜Error Rate: {:.1%}",
        'button_accuracy_results_saved': "✅ Test results automatically saved",
        'button_accuracy_warmup_feedback': "👟 Practice: {}, Response Time {:.3f} sec",
        'button_accuracy_formal_feedback': "🔘 Round {}: {}, Response Time {:.3f} sec",
        'button_accuracy_correct': "Correct",
        'button_accuracy_incorrect': "Incorrect",
        'button_accuracy_warmup_passed': "✅ Warmup test passed, starting formal test",
        'button_accuracy_test_finished': "Test Finished",
        'button_accuracy_test_end': "🎮 Button Accuracy Test Completed",
        
        # Button Reaction Time Test
        'button_reaction_window_title': "Reaction Time Test",
        'button_reaction_test_description': "Button Reaction Time Test",
        'user_id_input_prompt': "Enter user ID (e.g., P1): ",
        
        # Button Smash Test
        'button_smash_window_title': "Button Smash Test",
        'button_smash_test_description': "Button Smash Test",
        'button_smash_test_started': "🎮 Button Smash test started! Use controller button to start first click...",
        'button_smash_test_complete_msg': "🎯 Test complete!",
        'button_smash_total_clicks': "📊 Total clicks: {count}",
        'button_smash_test_time': "⏱️ Test time: {duration} seconds",
        'button_smash_cps_calculation': "📈 Calculation: {count} ÷ {duration} = {cps:.2f}",
        'button_smash_test_statistics': "📊 Test Results Statistics",
        'button_smash_click_rate': "Click rate: {cps:.2f} CPS",
        'button_smash_performance_rating': "Performance rating: {rating}",
        'button_smash_excellent': "Excellent",
        'button_smash_good': "Good",
        'button_smash_average': "Average",
        'button_smash_needs_practice': "Needs Practice",
        'button_smash_beginner': "Beginner",
        'button_smash_designated_button': "🎮 Designated button: {button}",
        'button_smash_start_timing': "⏰ Start timing!",
        'button_smash_click_record': "🖱️ Click #{count} (t={time:.1f}ms)",
        'button_smash_test_mode_help': "Run test mode",
        'button_smash_user_info_loaded': "✅ User '{user_id}' information loaded from command line parameters",
        'button_smash_test_mode_verify': "🧪 Test mode: Verifying CPS calculation...",
        'button_smash_test_complete_verify': "✅ Test complete",
        'button_smash_interrupt_signal': "🔄 Received interrupt signal, shutting down...",
        'button_smash_test_end': "🎮 Button Smash test ended",
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
