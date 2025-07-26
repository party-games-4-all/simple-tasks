#!/usr/bin/env python3
"""
批量更新測試文件腳本
- 添加視窗置頂功能
- 使用新的遙控器管理系統
"""
import os
import re
from pathlib import Path

def update_test_file(file_path):
    """更新單一測試文件"""
    print(f"正在更新：{file_path}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # 1. 添加 utils 導入（如果沒有的話）
    if 'from common.utils import' not in content:
        if 'from common import config' in content:
            content = content.replace(
                'from common import config',
                'from common import config\nfrom common.utils import setup_window_topmost'
            )
        elif 'from common.result_saver import' in content:
            content = content.replace(
                'from common.result_saver import save_test_result',
                'from common.result_saver import save_test_result\nfrom common.utils import setup_window_topmost'
            )
    
    # 2. 在 __init__ 方法中添加視窗置頂設定（針對 tkinter 應用）
    if 'tk.Tk()' in content or 'tkinter' in content:
        # 尋找 self.root.title 之後添加置頂設定
        title_pattern = r'(self\.root\.title\([^)]+\))'
        if re.search(title_pattern, content):
            replacement = r'\1\n        \n        # 設定視窗置頂\n        setup_window_topmost(self.root)'
            content = re.sub(title_pattern, replacement, content)
    
    # 3. 更新 ControllerInput 使用方式
    # 尋找 ControllerInput( 的實例化
    controller_pattern = r'listener = ControllerInput\((.*?)\)'
    def replace_controller(match):
        args = match.group(1)
        if 'use_existing_controller=True' not in args:
            if args.strip():
                return f'listener = ControllerInput({args},\n                               use_existing_controller=True)'
            else:
                return 'listener = ControllerInput(use_existing_controller=True)'
        return match.group(0)
    
    content = re.sub(controller_pattern, replace_controller, content, flags=re.DOTALL)
    
    # 4. 添加遙控器管理系統的註釋說明
    comment_pattern = r'(listener = ControllerInput\([^)]*\))'
    replacement = r'# 使用新的遙控器管理系統 - 會自動使用已配對的遙控器\n    \1'
    content = re.sub(comment_pattern, replacement, content)
    
    # 只有在內容有變更時才寫入檔案
    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ 已更新：{file_path}")
        return True
    else:
        print(f"⚪ 無需更新：{file_path}")
        return False

def main():
    """主函數"""
    tests_dir = Path(__file__).parent / "tests"
    
    # 取得所有 Python 測試文件（排除 __init__.py）
    test_files = [f for f in tests_dir.glob("*.py") if f.name != "__init__.py"]
    
    print(f"🔄 開始批量更新 {len(test_files)} 個測試文件...")
    print("=" * 50)
    
    updated_count = 0
    for test_file in test_files:
        if update_test_file(test_file):
            updated_count += 1
    
    print("=" * 50)
    print(f"✅ 更新完成！共更新了 {updated_count}/{len(test_files)} 個文件")
    
    if updated_count > 0:
        print("\n🎮 更新內容包括：")
        print("   - 添加視窗置頂功能")
        print("   - 使用新的遙控器管理系統")
        print("   - 避免重複配對遙控器")

if __name__ == "__main__":
    main()
