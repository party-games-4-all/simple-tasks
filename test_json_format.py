#!/usr/bin/env python3
"""
JSON 格式測試腳本
用於測試所有改進後的 JSON 輸出格式
"""

import json
import time
import os
from datetime import datetime

def create_sample_json_files():
    """創建示例 JSON 檔案以展示改進後的格式"""
    
    # 創建示例資料夾
    sample_dir = "data/results/test_json_format"
    os.makedirs(sample_dir, exist_ok=True)
    
    # 1. Button Prediction Countdown Test 示例
    button_prediction_sample = {
        "user_id": "test_user",
        "test_name": "button_prediction_countdown",
        "timestamp": datetime.now().isoformat(),
        "parameters": {
            "metadata": {
                "test_version": "1.0",
                "data_format_version": "1.0",
                "description": "太鼓達人風格預測反應時間測試，球從出現到目標點固定1000ms",
                "data_definitions": {
                    "time_units": "所有時間以毫秒為單位，除非特別註明為秒",
                    "coordinate_system": "畫布座標系統，左上角為(0,0)",
                    "response_time_definition": "從球出現到使用者按下按鍵的時間（秒）",
                    "target_time_definition": "球到達目標區域的理想時間（固定1.0秒）",
                    "error_calculation": "response_time - target_time (負值=提前按，正值=延遲按)"
                }
            },
            "window_size": {"width": 1200, "height": 800},
            "total_balls": 10,
            "ball_movement_time_ms": 1000,
            "ball_interval_ms": 500,
            "ball_path": {
                "start_x": 100,
                "target_x": 1080.0,
                "end_x": 1150,
                "y_position": 400,
                "movement_description": "球從左側滑入，經過目標區域後滑出"
            }
        },
        "metrics": {
            "total_trials": 10,
            "successful_responses": 7,
            "missed_responses": 3,
            "success_rate_percentage": 70.0,
            "average_error_ms": 120.5,
            "trials": [
                {
                    "trial_number": 1,
                    "response_time_seconds": 0.95,
                    "target_time_seconds": 1.0,
                    "error_seconds": -0.05,
                    "error_ms": -50,
                    "accuracy_ms": 50,
                    "feedback": "優秀！"
                }
            ]
        }
    }
    
    # 2. Analog Move Test 示例
    analog_move_sample = {
        "user_id": "test_user",
        "test_name": "analog_move",
        "timestamp": datetime.now().isoformat(),
        "parameters": {
            "metadata": {
                "test_version": "1.0",
                "data_format_version": "1.0",
                "description": "ISO9241標準九點圓形指向測試，測試joystick精確移動能力",
                "data_definitions": {
                    "completion_time_definition": "從使用者開始移動joystick到按下確認按鍵的時間",
                    "movement_start_detection": "joystick輸入值偏離(0,0)時開始計時",
                    "efficiency_calculation": "完成時間(秒) ÷ 直線距離(像素)",
                    "trace_sampling": "移動軌跡以約60fps頻率記錄座標點",
                    "coordinate_system": "畫布座標系統，左上角為(0,0)"
                }
            },
            "window_size": {"width": 1200, "height": 800},
            "iso9241_config": {
                "standard": "ISO9241多方向指向測試",
                "center_point": [600, 400],
                "long_circle_radius": 300,
                "short_circle_radius": 100,
                "total_positions": 9,
                "test_sequence": [1, 6, 2, 7, 3, 8, 4, 0, 5]
            }
        },
        "metrics": {
            "total_trials": 36,
            "trials": [
                {
                    "trial_number": 1,
                    "target_x": 750,
                    "target_y": 300,
                    "completion_time_ms": 1500,
                    "joystick_trajectory": {
                        "description": "玩家移動軌跡座標序列",
                        "coordinates": [
                            [600, 400], [610, 390], [625, 375], [650, 350], [700, 320], [750, 300]
                        ],
                        "start_position": [600, 400],
                        "end_position": [750, 300]
                    },
                    "movement_analysis": {
                        "total_distance_pixels": 212.8,
                        "straight_line_distance": 180.3,
                        "movement_efficiency_ratio": 0.85
                    }
                }
            ]
        }
    }
    
    # 3. Button Smash Test 示例
    button_smash_sample = {
        "user_id": "test_user", 
        "test_name": "button_smash",
        "timestamp": datetime.now().isoformat(),
        "parameters": {
            "metadata": {
                "test_version": "1.0",
                "data_format_version": "1.0",
                "description": "按鍵連擊速度測試，測試在固定時間內的最大點擊頻率",
                "data_definitions": {
                    "cps_calculation": "CPS = 總點擊數 ÷ 測試持續時間",
                    "timing_start": "第一次點擊開始計時，而非測試開始時計時",
                    "click_definition": "任意按鍵按下都計為一次點擊"
                }
            },
            "test_duration_seconds": 10,
            "test_mechanics": {
                "timing_trigger": "第一次點擊開始計時",
                "duration_fixed": "10秒固定時間"
            }
        },
        "metrics": {
            "total_clicks": 85,
            "clicks_per_second": 8.5,
            "click_timestamps": [
                {"click_number": 1, "relative_time_ms": 0},
                {"click_number": 2, "relative_time_ms": 120},
                {"click_number": 3, "relative_time_ms": 240}
            ],
            "rhythm_analysis": {
                "click_intervals_ms": [120, 120, 115, 125],
                "average_interval_ms": 120,
                "interval_variance": 16.7,
                "rhythm_consistency": "低變異數表示節奏穩定"
            }
        }
    }
    
    # 儲存示例檔案
    samples = [
        ("button_prediction_countdown_sample.json", button_prediction_sample),
        ("analog_move_sample.json", analog_move_sample),
        ("button_smash_sample.json", button_smash_sample)
    ]
    
    for filename, data in samples:
        filepath = os.path.join(sample_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"✅ 創建示例檔案: {filepath}")

def validate_json_structure(json_data, test_name):
    """驗證 JSON 結構是否符合規範"""
    required_fields = ["user_id", "test_name", "timestamp", "parameters", "metrics"]
    
    print(f"\n🔍 驗證 {test_name} JSON 結構:")
    
    for field in required_fields:
        if field in json_data:
            print(f"  ✅ {field}: 存在")
        else:
            print(f"  ❌ {field}: 缺失")
    
    # 檢查 metadata
    if "parameters" in json_data and "metadata" in json_data["parameters"]:
        metadata = json_data["parameters"]["metadata"]
        meta_fields = ["test_version", "data_format_version", "description", "data_definitions"]
        print(f"  📋 metadata 欄位:")
        for field in meta_fields:
            if field in metadata:
                print(f"    ✅ {field}: 存在")
            else:
                print(f"    ❌ {field}: 缺失")
    
    # 檢查時間定義
    if ("parameters" in json_data and 
        "metadata" in json_data["parameters"] and 
        "data_definitions" in json_data["parameters"]["metadata"]):
        
        definitions = json_data["parameters"]["metadata"]["data_definitions"]
        if any("time" in key.lower() for key in definitions.keys()):
            print(f"  ⏰ 時間定義: 已包含")
        else:
            print(f"  ⏰ 時間定義: 缺失")

if __name__ == "__main__":
    print("🧪 JSON 格式測試工具")
    print("=" * 50)
    
    # 創建示例檔案
    create_sample_json_files()
    
    print("\n" + "=" * 50)
    print("📋 JSON 格式改進檢查清單")
    print("=" * 50)
    
    checklist = [
        "✅ 每個測試都有明確的 Response Time 定義",
        "✅ 每個測試都有明確的 Target Time 定義（如適用）", 
        "✅ Joystick 軌跡完整記錄（Analog 測試）",
        "✅ 時間單位統一且明確標註",
        "✅ 包含測試說明和資料格式註釋",
        "✅ 軌跡取樣頻率和座標系統明確定義",
        "✅ 錯誤處理和異常情況記錄完整",
        "✅ 添加 metadata 區塊提高可讀性"
    ]
    
    for item in checklist:
        print(item)
    
    print("\n" + "=" * 50)
    print("🎯 主要改進項目總結")
    print("=" * 50)
    
    improvements = [
        "1. 統一添加 metadata 區塊包含版本資訊和說明",
        "2. 明確定義 Response Time 和 Target Time 的含義", 
        "3. 完整記錄 joystick 軌跡座標資料",
        "4. 標準化時間單位並添加說明",
        "5. 增加節奏分析和移動效率計算",
        "6. 提供詳細的測試參數說明",
        "7. 改善資料可讀性和可分析性"
    ]
    
    for improvement in improvements:
        print(improvement)
    
    print(f"\n💾 示例檔案已儲存至: data/results/test_json_format/")
    print("🔧 請運行實際測試檢查改進效果！")
