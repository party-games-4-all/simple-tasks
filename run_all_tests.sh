#!/bin/bash
# 用法: ./run_all_tests.sh <使用者ID>
USER_ID=$1

# 若未提供參數，提示用法並退出
if [ -z "$USER_ID" ]; then
  echo "用法: $0 <使用者ID>"
  exit 1
fi

# 建立結果輸出目錄 (以使用者ID命名) 
OUTPUT_DIR="data/results/$USER_ID"
IMAGE_DIR="data/images/$USER_ID"
mkdir -p "$OUTPUT_DIR" "$IMAGE_DIR"

echo "開始執行所有測試 (使用者: $USER_ID)..."

# 1. 手把連接測試
echo "1. 執行手把連接測試..."
uv run python tests/connection_test.py --user $USER_ID --out "$OUTPUT_DIR/connection.json"
echo "手把連接測試完成。結果已儲存至 $OUTPUT_DIR/connection.json"
echo ""

# 2. 簡單反應時間測試 (紅圈出現反應)
echo "2. 執行簡單反應時間測試..."
uv run python tests/reaction_time_test.py --user $USER_ID --out "$OUTPUT_DIR/reaction_time.json"
echo "簡單反應時間測試完成。結果已儲存至 $OUTPUT_DIR/reaction_time.json"
echo ""

# 3. 預測反應時間測試 (倒數計時球體)
echo "3. 執行預測反應時間測試..."
uv run python tests/prediction_reaction_test.py --user $USER_ID --out "$OUTPUT_DIR/prediction_reaction.json"
echo "預測反應時間測試完成。結果已儲存至 $OUTPUT_DIR/prediction_reaction.json"
echo ""

# 4. 選擇反應/按鍵準確度測試
echo "4. 執行選擇反應測試..."
uv run python tests/choice_accuracy_test.py --user $USER_ID --out "$OUTPUT_DIR/choice_accuracy.json"
echo "選擇反應測試完成。結果已儲存至 $OUTPUT_DIR/choice_accuracy.json"
echo ""

# 5. 類比搖桿移動精準度測試
echo "5. 執行類比搖桿移動測試..."
uv run python tests/analog_move_test.py --user $USER_ID --out "$OUTPUT_DIR/analog_move.json"
echo "類比搖桿移動測試完成。結果已儲存至 $OUTPUT_DIR/analog_move.json"
echo ""

# 6. 路徑追蹤測試
echo "6. 執行路徑追蹤測試..."
uv run python tests/path_follow_test.py --user $USER_ID --out "$OUTPUT_DIR/path_follow.json" \
                                  --image_dir "$IMAGE_DIR"
echo "路徑追蹤測試完成。結果已儲存至 $OUTPUT_DIR/path_follow.json，軌跡圖儲存於 $IMAGE_DIR/"
echo ""

echo "所有測試皆完成！請查看 $OUTPUT_DIR 以取得結果。"
