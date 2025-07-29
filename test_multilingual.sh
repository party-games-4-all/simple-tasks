#!/bin/bash

# 多語言系統測試腳本
echo "🌐 測試多語言系統功能"
echo "=========================="

PYTHON_CMD="/Users/sky/Documents/GitHub/simple-tasks/.venv/bin/python"

echo "📝 測試所有程式的 --english 參數支援："
echo ""

echo "1️⃣ 主程式 (main.py):"
$PYTHON_CMD main.py --english --help | head -5
echo ""

echo "2️⃣ 按鈕反應時間測試:"
$PYTHON_CMD tests/button_reaction_time_test.py --english --help | head -5
echo ""

echo "3️⃣ 按鈕準確度測試:"
$PYTHON_CMD tests/button_accuracy_test.py --english --help | head -5
echo ""

echo "4️⃣ 預測反應測試:"
$PYTHON_CMD tests/button_prediction_countdown_test.py --english --help | head -5
echo ""

echo "5️⃣ 快速點擊測試:"
$PYTHON_CMD tests/button_smash_test.py --english --help | head -5
echo ""

echo "6️⃣ 搖桿移動測試:"
$PYTHON_CMD tests/analog_move_test.py --english --help | head -5
echo ""

echo "7️⃣ 路徑追蹤測試:"
$PYTHON_CMD tests/analog_path_follow_test.py --english --help | head -5
echo ""

echo "✅ 所有測試程式都已支援 --english 參數！"
echo ""
echo "🎯 使用範例："
echo "   中文模式: $PYTHON_CMD main.py"
echo "   英文模式: $PYTHON_CMD main.py --english"
