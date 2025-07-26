# Simple Tasks - 手把測試應用程式

這是一個使用 Python 和 pygame 開發的手把測試應用程式集合，包含多種反應時間和精準度測試。

## 系統需求

- Python 3.8+
- macOS 或 Linux 系統
- 支援的遊戲手把（如 Joy-Con、Xbox 控制器等）

## 安裝與設定

### 使用 uv（推薦）

1. **安裝 uv**
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. **Clone 專案**
   ```bash
   git clone <your-repo-url>
   cd simple-tasks
   ```

3. **使用 uv 安裝依賴並執行**
   ```bash
   # uv 會自動建立虛擬環境並安裝依賴
   uv run main.py
   ```

### 傳統方式

如果您偏好使用傳統的 pip 方式：

```bash
# 建立虛擬環境
python -m venv venv

# 啟動虛擬環境
source venv/bin/activate

# 安裝依賴
pip install pygame

# 執行程式
uv run python main.py
```

## 專案架構

本專案採用模組化架構，方便維護與擴充：

```
project/
├── tests/                          # 測試模組目錄
│   ├── connection_test.py          # 手把連接測試
│   ├── reaction_time_test.py       # 簡單反應時間測試
│   ├── prediction_reaction_test.py # 預測反應時間測試
│   ├── choice_accuracy_test.py     # 選擇反應測試
│   ├── analog_move_test.py         # 類比搖桿移動測試
│   └── path_follow_test.py         # 路徑追蹤測試
├── common/                         # 共用模組
│   ├── controller_input.py         # 手把輸入處理核心
│   ├── utils.py                    # 工具函式
│   └── config.py                   # 參數設定
├── data/                           # 資料目錄
│   ├── results/                    # 測試結果（JSON 格式）
│   └── images/                     # 圖片輸出（軌跡圖等）
├── main.py                         # 主控程式
├── run_all_tests.sh               # 一鍵執行所有測試
└── README.md
```

## 執行測試

### 互動式執行
```bash
uv run python main.py
```
啟動互動式選單，可選擇執行單一測試或完整測試套件。

### 執行完整測試套件
```bash
./run_all_tests.sh <使用者ID>
```
按順序執行所有測試項目，並將結果儲存到 `data/results/<使用者ID>/` 目錄。

### 執行單一測試
```bash
# 手把連接測試
uv run python tests/connection_test.py

# 簡單反應時間測試
uv run python tests/reaction_time_test.py

# 預測反應時間測試  
uv run python tests/prediction_reaction_test.py

# 選擇反應測試
uv run python tests/choice_accuracy_test.py

# 類比搖桿移動測試
uv run python tests/analog_move_test.py

# 路徑追蹤測試
uv run python tests/path_follow_test.py
```

## 測試說明

### 1. 手把連接測試
測試手把是否正確連接並顯示輸入事件。

### 2. 簡單反應時間測試 (SRT)
測試對紅色圓形出現的反應時間。

### 3. 預測反應時間測試 (TP)
測試對移動球體到達目標位置的預測反應能力。

### 4. 選擇反應時間測試 (CRT)
測試對不同方向指示的選擇反應準確度和速度。

### 5. 類比搖桿移動測試
測試使用類比搖桿移動到目標位置的精準度（Fitts' Law）。

### 6. 路徑追蹤測試
測試沿指定路徑移動的能力和精準度。

## 測試結果

所有測試結果以 JSON 格式儲存在 `data/results/` 目錄下，包含：
- 使用者 ID
- 測試名稱
- 時間戳記
- 詳細測試指標（反應時間、準確度、點擊次數等）

部分測試（如路徑追蹤）會在 `data/images/` 目錄產生視覺化軌跡圖。

## 設計特色

### 色盲友善設計
- 採用藍色/橘色配色組合，對色盲使用者友善
- 避免紅綠色直接搭配
- 使用高對比度設計，提升可辨識性
- 結合文字標籤和圖示符號，不僅依賴顏色傳達資訊

### 模組化架構
- 各測試模組獨立，便於維護和擴充
- 共用模組集中管理，避免重複程式碼
- 統一的 JSON 資料格式，便於後續分析

### 無障礙設計
- 清楚的互動提示和倒數計時
- 支援多種輸入方式
- 一致的操作流程

## 手把設定

程式會自動偵測連接的手把裝置。第一次執行時，請：

1. 確保手把已正確連接到電腦
2. 執行任一測試程式
3. 選擇要使用的手把裝置

## 使用 uv 的優勢

- **快速啟動**：uv 會自動管理 Python 版本和虛擬環境
- **快速安裝**：比 pip 快 10-100 倍的套件安裝速度
- **自動依賴管理**：根據 `pyproject.toml` 自動安裝正確的依賴版本
- **跨平台一致性**：確保在不同系統上的一致行為

## 常用 uv 指令

```bash
# 執行特定檔案
uv run python <filename>.py

# 安裝額外套件
uv add <package-name>

# 移除套件
uv remove <package-name>

# 更新所有依賴
uv lock --upgrade

# 顯示已安裝的套件
uv pip list
```

## 故障排除

### 手把無法偵測
- 確認手把已正確連接並配對
- 嘗試重新連接手把
- 檢查系統是否識別手把裝置

### uv 相關問題
- 確認 uv 已正確安裝：`uv --version`
- 清除快取：`uv cache clean`
- 重新建立環境：刪除 `.venv` 資料夾後重新執行 `uv run`

## 開發

如果要修改或擴展程式：

```bash
# 進入開發模式（啟動虛擬環境）
uv shell

# 之後可以直接使用 python 指令
python main.py
```

## 檔案說明

### 核心檔案
- [`main.py`](main.py) - 主控程式，提供互動式選單
- [`run_all_tests.sh`](run_all_tests.sh) - 一鍵執行所有測試的腳本

### 共用模組 (common/)
- [`controller_input.py`](common/controller_input.py) - 手把輸入處理核心
- [`utils.py`](common/utils.py) - 工具函式
- [`config.py`](common/config.py) - 參數設定和色盲友善配色

### 測試模組 (tests/)
- [`connection_test.py`](tests/connection_test.py) - 手把連接診斷工具
- [`reaction_time_test.py`](tests/reaction_time_test.py) - 簡單反應時間測試
- [`prediction_reaction_test.py`](tests/prediction_reaction_test.py) - 預測反應時間測試
- [`choice_accuracy_test.py`](tests/choice_accuracy_test.py) - 選擇反應測試
- [`analog_move_test.py`](tests/analog_move_test.py) - 類比搖桿移動測試
- [`path_follow_test.py`](tests/path_follow_test.py) - 路徑追蹤測試