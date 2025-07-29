# 多語言支援實作指南

這個指南說明如何為現有的測試檔案添加多語言支援。

## 步驟 1: 匯入語言模組

在檔案頂部添加語言模組的匯入：

```python
from common.language import set_language, get_text
```

## 步驟 2: 設定語言檢查

在 `if __name__ == "__main__":` 區塊的開始添加：

```python
# 檢查是否有 --english 參數來提前設定語言
if '--english' in sys.argv:
    set_language('en')
else:
    set_language('zh')
```

## 步驟 3: 更新 ArgumentParser

更新命令列參數說明：

```python
parser.add_argument("--user", "-u", default=None, help=get_text('arg_user_id'))
parser.add_argument("--age", type=int, default=None, help=get_text('arg_age'))
parser.add_argument("--controller-freq", type=int, default=None, help=get_text('arg_controller_freq'))
parser.add_argument("--english", action="store_true", help=get_text('arg_english'))
```

## 步驟 4: 替換 print 語句

將所有硬編碼的中文文字替換為 `get_text()` 調用：

```python
# 舊的方式
print("🔄 已開始反應時間測試系列！")

# 新的方式
print(get_text('reaction_test_started'))
```

## 步驟 5: 添加新的語言鍵值

如果需要新的文字，在 `common/language.py` 中添加對應的中英文鍵值對。

## 現有的語言鍵值

以下是已經在 `language.py` 中定義的常用鍵值：

### 通用訊息
- `test_restart`: "🔄 已重新開始計算！" / "🔄 Restarted calculation!"
- `test_results_saved`: "✅ 測試結果已自動儲存" / "✅ Test results saved automatically"
- `no_results_to_save`: "⚠️ 無測試結果可儲存" / "⚠️ No test results to save"
- `closing_app`: "🔄 正在安全關閉應用程式..." / "🔄 Safely closing application..."
- `test_statistics`: "📊 測試結果統計" / "📊 Test Result Statistics"
- `received_interrupt`: "🔄 接收到中斷信號，正在關閉..." / "🔄 Received interrupt signal, closing..."

### 反應時間測試
- `reaction_test_started`: "🔄 已開始反應時間測試系列！" / "🔄 Started reaction time test series!"
- `too_fast_restart`: "太快了！重新開始第 {trial} 次測試" / "Too fast! Restarting trial {trial}"
- `reaction_time_result`: "🔘 第 {trial} 次：反應時間 {time:.3f} 秒" / "🔘 Trial {trial}: Reaction time {time:.3f} seconds"
- `average_reaction_time`: "📊 平均反應時間：{time:.3f} 秒" / "📊 Average reaction time: {time:.3f} seconds"

### 命令列參數說明
- `arg_user_id`: "使用者 ID" / "User ID"
- `arg_age`: "使用者年齡" / "User age"
- `arg_controller_freq`: "手把使用頻率 (1-7)" / "Controller usage frequency (1-7)"
- `arg_english`: "使用英文介面" / "Use English interface"

## 使用範例

```python
# 在您的測試檔案中
if __name__ == "__main__":
    # 檢查是否有 --english 參數
    if '--english' in sys.argv:
        set_language('en')
    else:
        set_language('zh')
    
    # 建立 ArgumentParser
    parser = argparse.ArgumentParser(description="Your Test Name")
    parser.add_argument("--english", action="store_true", help=get_text('arg_english'))
    
    # 在程式中使用多語言文字
    print(get_text('test_restart'))
    print(get_text('reaction_time_result', trial=1, time=0.523))
```

## 測試

測試中文版本：
```bash
uv run python tests/your_test.py --help
```

測試英文版本：
```bash
uv run python tests/your_test.py --english --help
```
