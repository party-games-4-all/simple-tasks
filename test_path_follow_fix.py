#!/usr/bin/env python3
"""
測試路徑追蹤程式的修復 - 檢查關閉時是否會出現錯誤
"""
import subprocess
import sys
import time
import signal
import os

def test_path_follow_shutdown():
    """測試路徑追蹤程式的正常關閉"""
    print("🧪 開始測試路徑追蹤程式的關閉機制...")
    
    # 啟動測試程式
    try:
        # 使用 subprocess 啟動測試，模擬真實使用情況
        process = subprocess.Popen([
            sys.executable, "-m", "tests.analog_path_follow_test",
            "--user", "test_user",
            "--age", "25",
            "--controller-freq", "3"
        ], 
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE, 
        text=True,
        cwd=os.path.dirname(os.path.abspath(__file__))
        )
        
        print("✅ 程式已啟動，PID:", process.pid)
        
        # 等待程式初始化
        time.sleep(3)
        
        # 檢查程式是否正在運行
        if process.poll() is None:
            print("✅ 程式正在運行中")
            
            # 發送中斷信號來測試關閉
            print("📤 發送 SIGINT 信號...")
            process.send_signal(signal.SIGINT)
            
            # 等待程式關閉
            try:
                stdout, stderr = process.communicate(timeout=10)
                print("✅ 程式已正常關閉")
                
                # 檢查錯誤輸出
                if "video system not initialized" in stderr:
                    print("❌ 仍然出現 'video system not initialized' 錯誤")
                    print("錯誤輸出:", stderr)
                    return False
                elif "Fatal Python error" in stderr:
                    print("❌ 仍然出現致命錯誤")
                    print("錯誤輸出:", stderr)
                    return False
                else:
                    print("✅ 沒有檢測到 pygame 相關錯誤")
                    if stderr.strip():
                        print("⚠️ 有其他錯誤訊息:", stderr.strip())
                    return True
                    
            except subprocess.TimeoutExpired:
                print("⚠️ 程式關閉超時，強制終止")
                process.kill()
                return False
        else:
            print("❌ 程式啟動失敗")
            stdout, stderr = process.communicate()
            print("錯誤輸出:", stderr)
            return False
            
    except Exception as e:
        print(f"❌ 測試過程中發生錯誤: {e}")
        return False

if __name__ == "__main__":
    success = test_path_follow_shutdown()
    if success:
        print("\n🎉 測試通過！路徑追蹤程式的關閉機制已修復")
    else:
        print("\n😞 測試失敗，需要進一步修復")
    sys.exit(0 if success else 1)
