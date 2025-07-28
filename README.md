# Simple Tasks - 手把測試應用程式

這是一個使用 Python 和 pygame 開發的手把測試應用程式集合，用於測試使用者的反應時間、精準度和協調能力。包含多種從簡單到複雜的互動測試，適用於遊戲研究、使用者體驗測試和能力評估。

## 前置需求

在開始使用之前，請確保您的系統已安裝以下軟體：

### 必要系統需求
- **Python 3.8 或更高版本**
- **macOS 10.14+ 或 Linux** (Windows 可能需要額外設定)
- **支援的遊戲手把** (Joy-Con、PlayStation 控制器、Xbox 控制器等)

### 安裝 uv (強烈推薦)
uv 是一個高效能的 Python 套件管理工具，提供快速的依賴安裝和環境管理：

```bash
# macOS 和 Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# 或使用 Homebrew (macOS)
brew install uv

# 或使用 pip
pip install uv
```

安裝後請重新啟動終端機，或執行：
```bash
source ~/.bashrc  # Linux
source ~/.zshrc   # macOS (如果使用 zsh)
```

### 驗證安裝
```bash
uv --version
```

## 快速開始

1. **Clone 專案並進入目錄**
   ```bash
   git clone <your-repo-url>
   cd simple-tasks
   ```

2. **連接手把裝置**
   - 確保手把已正確連接到電腦
   - 對於 Joy-Con：確保已透過藍牙配對
   - 對於其他手把：確保驅動程式已安裝

3. **執行程式**
   ```bash
   # uv 會自動建立虛擬環境並安裝所有依賴
   uv run python main.py
   ```

## 專案架構

本專案採用模組化架構，方便維護與擴充：

```
simple-tasks/
├── main.py                         # 主控程式 - 互動式測試選單
├── pyproject.toml                  # 專案配置和依賴管理
├── uv.lock                        # 依賴版本鎖定檔案
├── README.md                      # 專案說明文件
├── tests/                         # 測試模組目錄
│   ├── __init__.py               # Python 套件初始化
│   ├── button_reaction_time_test.py    # 簡單反應時間測試
│   ├── button_prediction_countdown_test.py # 預測反應時間測試  
│   ├── button_smash_test.py       # Button Smash 連打測試
│   ├── button_accuracy_test.py    # 方向選擇反應測試
│   ├── analog_move_test.py        # 類比搖桿移動測試
│   └── analog_path_follow_test.py # 路徑追蹤測試
├── common/                        # 共用模組
│   ├── __init__.py               # Python 套件初始化
│   ├── config.py                 # 全域配置設定
│   ├── controller_input.py       # 手把輸入處理核心
│   ├── connection_test.py        # 手把連接測試工具
│   ├── result_saver.py           # 測試結果儲存模組
│   ├── trace_plot.py             # 軌跡圖表生成工具
│   └── utils.py                  # 通用工具函式
├── data/                         # 資料儲存目錄
│   ├── results/                  # 測試結果 (JSON 格式)
│   │   └── [user_id]/           # 各使用者的測試結果
│   └── images/                   # 圖片輸出 (軌跡圖等)
│       ├── analog_move/          # 移動測試軌跡圖
│       └── analog_path_trace/    # 路徑追蹤軌跡圖
├── docs/                         # 開發文件
└── __pycache__/                  # Python 編譯快取 (自動生成)
```

## 執行測試

### 互動式執行
```bash
uv run python main.py
```

### 執行單一測試
每個測試都可以獨立執行，並支援指定使用者 ID：

```bash
# 手把連接測試
uv run python common/connection_test.py --user P1

# Button 測試系列
uv run python tests/button_reaction_time_test.py --user P1
uv run python tests/button_prediction_countdown_test.py --user P1
uv run python tests/button_smash_test.py --user P1
uv run python tests/button_accuracy_test.py --user P1

# Analog Stick 測試系列
uv run python tests/analog_move_test.py --user P1
uv run python tests/analog_path_follow_test.py --user P1
```

如果不提供 `--user` 參數，程式會要求您輸入使用者 ID。

### 執行完整測試套件
```bash
# 執行所有測試 (從主選單選擇選項 8)
uv run python main.py
```

進入互動選單後選擇選項 8 即可依序執行所有測試。

**注意**：目前選項 8 (執行完整測試套件) 的功能需要手動依序執行各個測試。未來版本將會加入自動化腳本。

## 測試說明

本應用程式包含 8 種不同類型的測試，從簡單到複雜循序漸進，全面評估使用者的反應能力和操作技巧。

### Button 測試系列 (按鈕測試)

按照難度由簡單到困難的順序排列：

#### 1. 簡單反應時間測試 (`button_reaction_time_test.py`)
- **目的**：測試基礎反應速度
- **操作**：當畫面顯示提示時立即按下任意按鈕
- **測量指標**：反應時間（毫秒）
- **測試次數**：10 次試驗
- **說明**：這是最基本的反應速度測試，評估大腦接收視覺訊號並做出反應的時間

#### 2. 預測反應時間測試 (`button_prediction_countdown_test.py`)
- **目的**：測試預測和時間感知能力
- **操作**：觀察移動的球，在它到達目標區域的瞬間按下按鈕
- **測量指標**：預測準確度、提前/延遲時間
- **設計特色**：參考 Mario Party 遊戲機制，球移動時間為 1200ms
- **說明**：評估玩家在動態情境中的視覺追蹤和時間預測能力

#### 3. Button Smash 連打測試 (`button_smash_test.py`)
- **目的**：測試快速連續點擊能力
- **操作**：在 10 秒內盡可能快速地重複按下按鈕
- **測量指標**：CPS (Clicks Per Second)、總點擊數
- **視覺回饋**：按鈕按下時顯示 X 符號和顏色變化
- **說明**：評估玩家的肌肉協調性和持續操作能力

#### 4. 方向選擇反應測試 (`button_accuracy_test.py`)
- **目的**：測試選擇性反應和準確度
- **操作**：根據畫面指示按下對應方向的按鈕（上下左右）
- **測量指標**：準確率、反應時間、錯誤率
- **測試次數**：20 次試驗
- **說明**：評估認知處理能力和精確操作技巧

### Analog 測試系列 (搖桿測試)

按照難度由簡單到困難的順序排列：

#### 5. 類比搖桿移動測試 (`analog_move_test.py`)
- **目的**：測試基礎搖桿控制能力
- **操作**：使用搖桿將游標移動到隨機出現的目標圓圈內
- **測量指標**：移動時間、移動距離、軌跡效率
- **視覺輸出**：產生移動軌跡圖，顯示玩家的移動路徑
- **說明**：評估基本的搖桿操作技巧和手眼協調能力

#### 6. 路徑追蹤測試 (`analog_path_follow_test.py`)
- **目的**：測試精確路徑追蹤能力
- **操作**：沿著指定路徑從起點移動到終點，不能偏離路徑
- **測量指標**：完成時間、路徑偏離次數、偏離距離
- **路徑類型**：直線路徑、S 型曲線路徑
- **說明**：評估精細運動控制和路徑規劃能力

### 手把連接測試 (`connection_test.py`)
- **目的**：驗證手把連接狀態
- **功能**：檢測已連接的手把裝置、顯示按鈕和搖桿輸入狀態
- **說明**：在進行正式測試前確保手把正常工作

## 測試結果

### 資料儲存結構
所有測試結果以統一格式儲存，便於後續分析和比較：

**JSON 結果檔案**
- 儲存位置：`data/results/[user_id]/`
- 格式：每個測試產生一個 JSON 檔案
- 內容包含：使用者 ID、測試名稱、時間戳記、詳細測試指標

**視覺化圖片**
- 儲存位置：`data/images/[test_type]/[user_id]/[timestamp]/`
- Analog Stick 測試會產生軌跡圖，顯示：
  - 玩家移動路徑
  - 目標區域
  - 按鍵點擊位置
  - 路徑偏離情況

### 支援的資料格式
- **JSON**：數值資料、統計結果、時間戳記
- **PNG**：軌跡圖、路徑圖、視覺化結果

這種結構化的資料儲存方式便於：
- 跨使用者的資料比較分析
- 自動化資料處理和統計
- 長期的研究資料保存

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

### 手把連接問題
- **手把無法偵測**：
  - 確認手把已正確連接並配對
  - 嘗試重新連接手把或重新配對藍牙
  - 檢查系統是否識別手把裝置 (系統設定 → 控制器)
  - 執行 `uv run python common/connection_test.py` 進行連接診斷

- **Joy-Con 特定問題**：
  - 確保 Joy-Con 電池電量充足
  - 嘗試關閉並重新開啟 Joy-Con (按住同步按鈕)
  - 在 macOS 中可能需要重新配對藍牙裝置

- **其他手把問題**：
  - PS4/PS5 控制器：確認驅動程式已安裝
  - Xbox 控制器：確認已連接或配對成功
  - 通用 USB 手把：檢查 USB 連接和相容性

### 程式執行問題
- **Python 版本錯誤**：
  - 確認 Python 版本為 3.8 或更高
  - 使用 `python3 --version` 檢查版本

- **pygame 相關錯誤**：
  - macOS 可能需要安裝額外套件：`brew install sdl2`
  - 若出現音效錯誤，程式已設定忽略音效輸出

- **tkinter 顯示問題**：
  - macOS：確認已安裝 Tkinter：`python3 -m tkinter`
  - Linux：可能需要安裝 `python3-tk`

### uv 相關問題
- **uv 安裝失敗**：
  - 確認網路連接正常
  - 嘗試使用 pip 安裝：`pip install uv`
  - 檢查系統權限，可能需要 sudo

- **虛擬環境問題**：
  - 確認 uv 已正確安裝：`uv --version`
  - 清除快取：`uv cache clean`
  - 重新建立環境：刪除 `.venv` 資料夾後重新執行 `uv run`

- **依賴安裝問題**：
  - 檢查 `pyproject.toml` 檔案完整性
  - 嘗試手動安裝：`uv add pygame matplotlib`

### 測試結果問題
- **無法儲存結果**：
  - 檢查 `data/` 目錄權限
  - 確認硬碟空間充足
  - 檢查檔案系統是否支援檔名中的時間戳記格式

- **圖片無法生成**：
  - 確認 matplotlib 正確安裝
  - 檢查 `data/images/` 目錄權限
  - 確認系統支援 PNG 格式輸出

### 效能問題
- **程式運行緩慢**：
  - 關閉其他佔用系統資源的應用程式
  - 確認系統記憶體充足
  - 嘗試降低顯示解析度 (修改 `config.py` 中的視窗大小)

- **畫面卡頓**：
  - 檢查系統 CPU 使用率
  - 確認顯示卡驅動程式為最新版本

### 獲取幫助
如果問題仍未解決，請：
1. 檢查錯誤訊息的完整內容
2. 確認系統環境 (作業系統版本、Python 版本等)
3. 嘗試在不同環境下執行測試

## 開發

如果要修改或擴展程式：

```bash
# 進入開發模式（啟動虛擬環境）
uv shell

# 之後可以直接使用 python 指令
python main.py

# 安裝開發依賴
uv add --dev pytest black flake8

# 執行程式碼格式化
black .

# 執行語法檢查
flake8 .
```

### 開發建議
- **新增測試**：參考現有測試模組的結構和設計模式
- **修改配置**：所有可調整參數都在 `common/config.py` 中
- **新增功能**：遵循現有的模組化架構
- **測試變更**：先使用 `connection_test.py` 確保手把功能正常

## 檔案說明

### 主程式檔案

#### `main.py`
- **功能**：應用程式主入口點
- **特色**：提供互動式選單系統，可選擇執行單一測試或完整測試套件
- **使用方式**：直接執行可進入選單模式，也可以命令列參數方式執行

#### `pyproject.toml`
- **功能**：專案配置檔案 (Python 標準)
- **內容**：定義專案依賴 (pygame, matplotlib)、Python 版本需求等
- **重要性**：uv 會根據此檔案自動管理虛擬環境和依賴安裝

### 測試模組 (`tests/` 目錄)

所有測試模組都遵循統一的設計模式：
- 支援 `--user` 命令列參數指定使用者 ID
- 自動儲存測試結果為 JSON 格式
- 使用色盲友善的視覺設計
- 支援手把和鍵盤輸入 (作為備用)

#### `button_reaction_time_test.py`
- **測試類型**：簡單反應時間測試
- **UI 框架**：tkinter
- **輸入方式**：任意按鈕/鍵盤空白鍵
- **結果檔案**：`button_reaction_time_YYYYMMDD_HHMMSS.json`

#### `button_prediction_countdown_test.py`
- **測試類型**：預測反應時間測試
- **特殊功能**：動畫球移動、預測時間計算
- **遊戲化設計**：參考 Mario Party 機制
- **結果檔案**：`button_prediction_countdown_YYYYMMDD_HHMMSS.json`

#### `button_smash_test.py`
- **測試類型**：快速連打測試
- **計時機制**：從第一次點擊開始計時 10 秒
- **視覺回饋**：即時顯示點擊計數和 CPS
- **結果檔案**：`button_smash_YYYYMMDD_HHMMSS.json`

#### `button_accuracy_test.py`
- **測試類型**：方向選擇反應測試
- **按鈕排列**：菱形排列模擬真實手把配置
- **評估指標**：準確率、平均反應時間
- **結果檔案**：`button_accuracy_YYYYMMDD_HHMMSS.json`

#### `analog_move_test.py`
- **測試類型**：搖桿移動測試
- **圖形輸出**：自動產生移動軌跡圖
- **測量指標**：移動效率、軌跡分析
- **結果檔案**：JSON + PNG 軌跡圖

#### `analog_path_follow_test.py`
- **測試類型**：路徑追蹤測試
- **路徑類型**：直線路徑、S 型曲線路徑
- **圖形輸出**：路徑追蹤軌跡圖，顯示偏離情況
- **結果檔案**：JSON + PNG 軌跡圖

### 共用模組 (`common/` 目錄)

#### `config.py`
- **功能**：全域配置設定
- **內容**：
  - 測試時間設定 (如連打測試的 10 秒限制)
  - 視窗尺寸設定 (1200x800)
  - 色盲友善配色方案 (藍色/橘色組合)
  - 反應時間相關參數
- **設計原則**：集中管理所有可調整參數，便於維護

#### `controller_input.py`
- **功能**：手把輸入處理核心模組
- **特色**：
  - 自動偵測並連接可用的手把裝置
  - 統一的按鈕和搖桿事件處理
  - 支援多種手把類型 (Joy-Con、PlayStation、Xbox 等)
  - 提供除錯模式便於開發測試
- **重要性**：所有測試的手把輸入都依賴此模組

#### `connection_test.py`
- **功能**：手把連接診斷工具
- **用途**：
  - 檢測已連接的手把裝置
  - 即時顯示按鈕和搖桿輸入狀態
  - 手把功能驗證
- **建議**：執行正式測試前先使用此工具確認手把正常

#### `result_saver.py`
- **功能**：測試結果儲存管理
- **特色**：
  - 統一的 JSON 格式儲存
  - 自動建立使用者專屬目錄
  - 時間戳記檔案命名
  - 標準化的資料結構
- **資料結構**：包含使用者 ID、測試名稱、時間戳記、詳細測試指標

#### `trace_plot.py`
- **功能**：軌跡圖表生成工具
- **支援圖表類型**：
  - 移動軌跡圖 (analog_move_test)
  - 路徑追蹤圖 (analog_path_follow_test)
  - 路徑追蹤軌跡圖 (analog_path_follow_test)
- **圖表特色**：高解析度 PNG 輸出、清晰的視覺標示
- **使用技術**：matplotlib

#### `utils.py`
- **功能**：通用工具函式庫
- **包含功能**：數學計算、資料處理、檔案操作等輔助函式
- **設計原則**：避免重複程式碼，提供可重用的工具函式

### 資料目錄 (`data/`)

#### `results/[user_id]/`
- **功能**：儲存各使用者的測試結果
- **檔案格式**：JSON
- **命名規則**：`[測試名稱]_YYYYMMDD_HHMMSS.json`
- **資料保存**：長期研究資料保存，便於統計分析

#### `images/[test_type]/[user_id]/[timestamp]/`
- **功能**：儲存視覺化圖表
- **檔案格式**：PNG
- **圖表類型**：
  - `analog_move/`：移動測試軌跡圖
  - `analog_path_trace/`：路徑追蹤軌跡圖

### 開發文件 (`docs/`)
- **內容**：專案開發過程中的會議記錄、技術文件
- **用途**：記錄設計決策和開發進度