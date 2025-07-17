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
python main.py
```

## 可用的測試程式

### 1. 手把連接測試
```bash
uv run python test/connection-test.py
```
測試手把是否正確連接並顯示輸入事件。

### 2. 簡單反應時間測試 (SRT)
```bash
uv run python button_reaction-time.py
```
測試對紅色圓形出現的反應時間。

### 3. 可預測反應時間測試 (TP)
```bash
uv run python button_reaction-countdown.py
```
測試對移動球體到達目標位置的預測反應能力。

### 4. 選擇反應時間測試 (CRT)
```bash
uv run python button_accuracy.py
```
測試對不同方向指示的選擇反應準確度和速度。

### 5. 類比搖桿移動測試
```bash
uv run python analog_move.py
```
測試使用類比搖桿移動到目標位置的精準度（Fitts' Law）。

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

- [`controller_input.py`](controller_input.py) - 手把輸入處理核心模組
- [`main.py`](main.py) - 基本手把輸入測試
- [`button_reaction-time.py`](button_reaction-time.py) - 簡單反應時間測試
- [`button_reaction-countdown.py`](button_reaction-countdown.py) - 預測反應時間測試
- [`button_accuracy.py`](button_accuracy.py) - 按鍵準確度測試
- [`analog_move.py`](analog_move.py) - 類比搖桿移動測試
- [`test/connection-test.py`](test/connection-test.py) - 手把連接診斷工具