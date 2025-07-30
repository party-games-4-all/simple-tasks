# Simple Tasks - 手把測試應用程式

> English Version Below

Python 與 pygame 開發的遊戲手把測試應用程式，測試反應時間、精準度和協調能力，適用於遊戲研究與使用者體驗評估。

## 快速開始

### 系統需求
- Python 3.8+
- macOS 10.14+ 或 Linux
- 支援的遊戲手把 (Joy-Con、PlayStation、Xbox 等)

### 安裝與執行
```bash
# 安裝 uv (Python 套件管理工具)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone 專案
git clone https://github.com/party-games-4-all/simple-tasks
cd simple-tasks

# 執行程式 (自動安裝依賴)
uv run python main.py

# 如果想要以英文執行
uv run python main.py --english
```

## 測試項目

### Button 測試系列
1. **簡單反應時間測試** - 基礎反應速度測試
2. **預測反應時間測試** - 時間預測與視覺追蹤能力
3. **Button Smash 連打測試** - 快速連續點擊能力
4. **方向選擇反應測試** - 選擇性反應與準確度

### Analog 測試系列
5. **類比搖桿移動測試** - 基礎搖桿控制能力
6. **路徑追蹤測試** - 精確路徑追蹤與精細運動控制


## 專案結構

```
simple-tasks/
├── main.py                    # 主程式入口
├── tests/                     # 測試模組
│   ├── button_*_test.py      # Button 測試系列
│   └── analog_*_test.py      # Analog 測試系列
├── common/                    # 共用模組
│   ├── controller_input.py   # 手把輸入處理
│   ├── result_saver.py       # 結果儲存
│   └── trace_plot.py         # 軌跡圖生成
└── data/                      # 測試結果與圖表
    ├── results/[user_id]/     # JSON 結果
    └── images/                # PNG 軌跡圖
```

## 特色功能

- **色盲友善設計** - 藍橘配色，高對比度
- **模組化架構** - 獨立測試模組，易於擴充
- **自動結果儲存** - JSON 格式與視覺化圖表
- **多手把支援** - Joy-Con、PlayStation、Xbox 等

## 故障排除

### 手把連接問題
```bash
# 手把連接診斷
uv run python common/connection_test.py

# 常見解決方案
# - 確認手把已連接並配對
# - 重新配對藍牙裝置
# - 檢查驅動程式
```

### 系統相關問題
- macOS 可能需要：`brew install sdl2`
- Linux 可能需要：`apt install python3-tk`

---

# Simple Tasks - Gamepad Testing Application

A Python and pygame-based gamepad testing application suite for measuring reaction time, precision, and coordination skills, suitable for gaming research and user experience evaluation.

## Quick Start

### System Requirements
- Python 3.8+
- macOS 10.14+ or Linux
- Supported gamepad (Joy-Con, PlayStation, Xbox, etc.)

### Installation & Usage
```bash
# Install uv (Python package manager)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone repository
git clone https://github.com/party-games-4-all/simple-tasks
cd simple-tasks

# Run application (auto-install dependencies)
uv run python main.py --english
```

## Test Categories

### Button Test Series
1. **Simple Reaction Time Test** - Basic reaction speed measurement
2. **Prediction Countdown Test** - Time prediction and visual tracking ability
3. **Button Smash Test** - Rapid consecutive clicking ability
4. **Direction Selection Test** - Selective reaction and accuracy

### Analog Test Series
5. **Analog Stick Movement Test** - Basic joystick control ability
6. **Path Following Test** - Precise path tracking and fine motor control

### Execution Methods
```bash
# Interactive menu
uv run python main.py

# Run individual tests
uv run python tests/button_reaction_time_test.py --user P1
uv run python tests/analog_move_test.py --user P1

# Gamepad connection test
uv run python common/connection_test.py
```

## Project Structure

```
simple-tasks/
├── main.py                    # Main application entry
├── tests/                     # Test modules
│   ├── button_*_test.py      # Button test series
│   └── analog_*_test.py      # Analog test series
├── common/                    # Shared modules
│   ├── controller_input.py   # Gamepad input handling
│   ├── result_saver.py       # Result storage
│   └── trace_plot.py         # Trajectory plotting
└── data/                      # Test results and charts
    ├── results/[user_id]/     # JSON results
    └── images/                # PNG trajectory plots
```

## Key Features

- **Colorblind-Friendly Design** - Blue-orange color scheme with high contrast
- **Modular Architecture** - Independent test modules, easy to extend
- **Automatic Result Storage** - JSON format with visualization charts
- **Multi-Gamepad Support** - Joy-Con, PlayStation, Xbox, etc.

## Troubleshooting

### Gamepad Connection Issues
```bash
# Gamepad connection diagnosis
uv run python common/connection_test.py

# Common solutions:
# - Ensure gamepad is connected and paired
# - Re-pair Bluetooth device
# - Check driver installation
```

### System-Related Issues
- macOS may require: `brew install sdl2`
- Linux may require: `apt install python3-tk`

## Development

```bash
# Development mode
uv shell
python main.py

# Install development dependencies
uv add --dev pytest black flake8

# Code formatting and linting
black .
flake8 .
```

## Test Results

All test results are automatically saved in standardized JSON format with accompanying visualization charts for trajectory-based tests. Results are organized by user ID and timestamp for easy analysis and comparison.
