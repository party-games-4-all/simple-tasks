#!/usr/bin/env python3
"""
測試新的遙控器管理系統
"""
import sys
from pathlib import Path

# 添加 common 模組到 Python 路徑
sys.path.append(str(Path(__file__).parent / "common"))

from common.controller_manager import controller_manager

def test_controller_manager():
    """測試遙控器管理器"""
    print("🎮 測試遙控器管理系統")
    print("=" * 50)
    
    # 測試1: 配對遙控器
    print("📡 正在配對遙控器...")
    controller = controller_manager.setup_controller()
    
    if controller:
        print(f"✅ 遙控器配對成功：{controller.get_name()}")
        
        # 測試2: 檢查遙控器狀態
        print(f"🔍 遙控器準備狀態：{controller_manager.is_controller_ready()}")
        
        # 測試3: 取得遙控器實例
        same_controller = controller_manager.get_controller()
        print(f"🔗 取得相同實例：{same_controller == controller}")
        
        # 測試4: 重複配對應該使用同一個遙控器
        print("🔄 測試重複配對...")
        controller2 = controller_manager.setup_controller()
        print(f"🔗 使用相同遙控器：{controller2 == controller}")
        
        print("=" * 50)
        print("✅ 遙控器管理系統測試完成")
        
    else:
        print("❌ 遙控器配對失敗")
        print("請確認遙控器已正確連接")

if __name__ == "__main__":
    test_controller_manager()
