"""
測試結果儲存模組
用於統一儲存 JSON 格式的測試結果
"""

import json
import os
from datetime import datetime
from pathlib import Path
from common import config


def save_test_result(user_id, test_name, metrics, parameters=None, image_files=None):
    """
    儲存測試結果為 JSON 檔案
    
    Args:
        user_id: 使用者 ID
        test_name: 測試名稱
        metrics: 測試指標數據
        parameters: 測試參數（可選）
        image_files: 相關圖片檔案名稱列表（可選）
    
    Returns:
        str: 儲存的檔案路徑
    """
    # 建立時間戳記
    timestamp = datetime.now().isoformat()
    
    # 建立結果資料結構
    result_data = {
        "user_id": user_id,
        "test_name": test_name,
        "timestamp": timestamp,
        "parameters": parameters or {},
        "metrics": metrics
    }
    
    # 如果有圖片檔案，加入記錄
    if image_files:
        result_data["image_files"] = image_files
    
    # 建立儲存目錄
    result_dir = Path(config.RESULTS_DIR) / user_id
    result_dir.mkdir(parents=True, exist_ok=True)
    
    # 建立帶有時間戳記的檔案名稱以避免覆蓋
    timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = result_dir / f"{test_name}_{timestamp_str}.json"
    
    # 寫入 JSON 檔案
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(result_data, f, indent=2, ensure_ascii=False)
    
    print(f"📄 測試結果已儲存：{file_path}")
    return str(file_path)


def load_test_result(user_id, test_name):
    """
    載入測試結果 JSON 檔案（載入最新的檔案）
    
    Args:
        user_id: 使用者 ID
        test_name: 測試名稱
    
    Returns:
        dict: 測試結果資料，若檔案不存在則返回 None
    """
    user_dir = Path(config.RESULTS_DIR) / user_id
    
    if not user_dir.exists():
        return None
    
    # 尋找符合模式的檔案 (test_name_YYYYMMDD_HHMMSS.json)
    pattern = f"{test_name}_*.json"
    matching_files = list(user_dir.glob(pattern))
    
    if not matching_files:
        return None
    
    # 取得最新的檔案（按檔案名稱排序，最後一個就是最新的）
    latest_file = sorted(matching_files)[-1]
    
    with open(latest_file, 'r', encoding='utf-8') as f:
        return json.load(f)


def get_user_test_results(user_id):
    """
    取得使用者的所有測試結果檔案
    
    Args:
        user_id: 使用者 ID
    
    Returns:
        list: 測試結果檔案路徑列表
    """
    user_dir = Path(config.RESULTS_DIR) / user_id
    
    if not user_dir.exists():
        return []
    
    return [str(f) for f in user_dir.glob("*.json")]


def get_test_result_files(user_id, test_name):
    """
    取得使用者特定測試的所有結果檔案
    
    Args:
        user_id: 使用者 ID
        test_name: 測試名稱
    
    Returns:
        list: 測試結果檔案路徑列表，按時間順序排序
    """
    user_dir = Path(config.RESULTS_DIR) / user_id
    
    if not user_dir.exists():
        return []
    
    # 尋找符合模式的檔案 (test_name_YYYYMMDD_HHMMSS.json)
    pattern = f"{test_name}_*.json"
    matching_files = list(user_dir.glob(pattern))
    
    # 按檔案名稱排序（時間戳記順序）
    return [str(f) for f in sorted(matching_files)]
