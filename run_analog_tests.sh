#!/bin/bash
# 用法: ./run_analog_tests.sh <使用者ID>

USER_ID=$1

# 若未提供參數，提示用法並退出
if [ -z "$USER_ID" ]; then
  echo "用法: $0 <使用者ID>"
  echo "範例: $0 P1"
  exit 1
fi

# 建立結果輸出目錄 (以使用者ID命名) 
OUTPUT_DIR="data/results/$USER_ID"
IMAGE_DIR="data/images/$USER_ID"
mkdir -p "$OUTPUT_DIR" "$IMAGE_DIR"

echo "開始執行所有 Analog Stick 測試 (使用者: $USER_ID)..."

# 1. 類比搖桿移動精準度測試 (Fitts' Law)
echo "🎯 開始類比搖桿移動精準度測試..."
python3 tests/analog_move_test.py --user "$USER_ID"
echo "類比搖桿移動測試完成。"

# 短暫延遲
sleep 2

# 2. 路徑追蹤測試
echo "🛤️ 開始路徑追蹤測試..."
python3 tests/analog_path_follow_test.py --user "$USER_ID"
echo "路徑追蹤測試完成。"

# 短暫延遲
sleep 2

# 3. 路徑追蹤測試 (障礙物版本 - 簡化)
echo "🚧 開始路徑追蹤測試 (障礙物版本)..."
python3 tests/analog_path_obstacle_test.py --user "$USER_ID"
echo "路徑追蹤測試 (障礙物版本) 完成。"

echo ""
echo "✅ 所有 Analog Stick 測試皆完成！"
echo "📂 圖片輸出位置: data/images/*/$(echo $USER_ID)/*"
echo "📊 結果輸出位置: $OUTPUT_DIR (如果有 JSON 輸出的話)"
echo ""
echo "圖片檔案結構："
find data/images -name "*.png" -path "*/$USER_ID/*" | head -10
if [ $(find data/images -name "*.png" -path "*/$USER_ID/*" | wc -l) -gt 10 ]; then
    echo "... (更多圖片檔案)"
fi
