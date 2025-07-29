# Simple Tasks - Controller Testing Application

This is a collection of controller testing applications developed using Python and pygame, designed to test users' reaction time, accuracy, and coordination abilities. It includes various interactive tests ranging from simple to complex, suitable for gaming research, user experience testing, and ability assessment.

## Prerequisites

Before getting started, please ensure your system has the following software installed:

### System Requirements
- **Python 3.8 or higher**
- **macOS 10.14+ or Linux** (Windows may require additional setup)
- **Supported game controllers** (Joy-Con, PlayStation controllers, Xbox controllers, etc.)

### Installing uv (Highly Recommended)
uv is a high-performance Python package management tool that provides fast dependency installation and environment management:

```bash
# macOS and Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Or using Homebrew (macOS)
brew install uv

# Or using pip
pip install uv
```

After installation, please restart your terminal or run:
```bash
source ~/.bashrc  # Linux
source ~/.zshrc   # macOS (if using zsh)
```

### Verify Installation
```bash
uv --version
```

## Quick Start

1. **Clone the project and enter the directory**
   ```bash
   git clone <your-repo-url>
   cd simple-tasks
   ```

2. **Connect your controller**
   - Ensure the controller is properly connected to your computer
   - For Joy-Con: Ensure it's paired via Bluetooth
   - For other controllers: Ensure drivers are installed

3. **Run the application**
   ```bash
   # uv will automatically create a virtual environment and install all dependencies
   uv run python main.py
   ```

## Project Architecture

This project uses a modular architecture for easy maintenance and expansion:

```
simple-tasks/
├── main.py                         # Main program - Interactive test menu
├── pyproject.toml                  # Project configuration and dependency management
├── uv.lock                        # Dependency version lock file
├── README.md                      # Project documentation
├── tests/                         # Test modules directory
│   ├── __init__.py               # Python package initialization
│   ├── button_reaction_time_test.py    # Simple reaction time test
│   ├── button_prediction_countdown_test.py # Prediction reaction time test  
│   ├── button_smash_test.py       # Button smash rapid-click test
│   ├── button_accuracy_test.py    # Direction choice reaction test
│   ├── analog_move_test.py        # Analog stick movement test
│   └── analog_path_follow_test.py # Path following test
├── common/                        # Shared modules
│   ├── __init__.py               # Python package initialization
│   ├── config.py                 # Global configuration settings
│   ├── controller_input.py       # Controller input processing core
│   ├── connection_test.py        # Controller connection test tool
│   ├── result_saver.py           # Test result saving module
│   ├── trace_plot.py             # Trajectory chart generation tool
│   └── utils.py                  # Common utility functions
├── data/                         # Data storage directory
│   ├── results/                  # Test results (JSON format)
│   │   └── [user_id]/           # Test results for each user
│   └── images/                   # Image output (trajectory plots, etc.)
│       ├── analog_move/          # Movement test trajectory plots
│       └── analog_path_trace/    # Path following trajectory plots
├── docs/                         # Development documentation
└── __pycache__/                  # Python compiled cache (auto-generated)
```

## Running Tests

### Interactive Execution
```bash
uv run python main.py
```

### Running Individual Tests
Each test can be run independently and supports specifying a user ID:

```bash
# Controller connection test
uv run python common/connection_test.py --user P1

# Button test series
uv run python tests/button_reaction_time_test.py --user P1
uv run python tests/button_prediction_countdown_test.py --user P1
uv run python tests/button_smash_test.py --user P1
uv run python tests/button_accuracy_test.py --user P1

# Analog Stick test series
uv run python tests/analog_move_test.py --user P1
uv run python tests/analog_path_follow_test.py --user P1
```

If you don't provide the `--user` parameter, the program will prompt you to enter a user ID.

### Running Complete Test Suite
```bash
# Run all tests (select option 8 from main menu)
uv run python main.py
```

After entering the interactive menu, select option 8 to run all tests sequentially.

**Note**: Currently option 8 (run complete test suite) requires manually running each test in sequence. Automated scripts will be added in future versions.

## Test Descriptions

This application includes 8 different types of tests, progressively arranged from simple to complex, comprehensively evaluating users' reaction abilities and operational skills.

### Button Test Series

Arranged in order of difficulty from simple to complex:

#### 1. Simple Reaction Time Test (`button_reaction_time_test.py`)
- **Purpose**: Test basic reaction speed
- **Operation**: Press any button immediately when the screen shows a prompt
- **Metrics**: Reaction time (milliseconds)
- **Trials**: 10 tests
- **Description**: This is the most basic reaction speed test, evaluating the time for the brain to receive visual signals and react

#### 2. Prediction Reaction Time Test (`button_prediction_countdown_test.py`)
- **Purpose**: Test prediction and time perception abilities
- **Operation**: Watch the moving ball and press the button at the moment it reaches the target area
- **Metrics**: Prediction accuracy, early/late timing
- **Design Feature**: Based on Mario Party game mechanics, ball movement time is 1200ms
- **Description**: Evaluates players' visual tracking and time prediction abilities in dynamic situations

#### 3. Button Smash Test (`button_smash_test.py`)
- **Purpose**: Test rapid consecutive clicking ability
- **Operation**: Press buttons as quickly as possible repeatedly within 10 seconds
- **Metrics**: CPS (Clicks Per Second), total clicks
- **Visual Feedback**: Button shows X symbol and color change when pressed
- **Description**: Evaluates players' muscle coordination and sustained operation ability

#### 4. Direction Choice Reaction Test (`button_accuracy_test.py`)
- **Purpose**: Test selective reaction and accuracy
- **Operation**: Press the corresponding direction button (up, down, left, right) according to screen instructions
- **Metrics**: Accuracy rate, reaction time, error rate
- **Trials**: 20 tests
- **Description**: Evaluates cognitive processing ability and precise operation skills

### Analog Test Series

Arranged in order of difficulty from simple to complex:

#### 5. Analog Stick Movement Test (`analog_move_test.py`)
- **Purpose**: Test basic joystick control ability
- **Operation**: Use the joystick to move the cursor to randomly appearing target circles
- **Metrics**: Movement time, movement distance, trajectory efficiency
- **Visual Output**: Generates movement trajectory plots showing the player's movement path
- **Description**: Evaluates basic joystick operation skills and hand-eye coordination

#### 6. Path Following Test (`analog_path_follow_test.py`)
- **Purpose**: Test precise path tracking ability
- **Operation**: Move along specified paths from start to end without deviating from the path
- **Metrics**: Completion time, path deviation count, deviation distance
- **Path Types**: Straight line paths, S-curve paths
- **Description**: Evaluates fine motor control and path planning abilities

### Controller Connection Test (`connection_test.py`)
- **Purpose**: Verify controller connection status
- **Function**: Detect connected controller devices, display button and joystick input status
- **Description**: Ensure the controller is working properly before conducting formal tests

## Test Results

### Data Storage Structure
All test results are stored in a unified format for easy subsequent analysis and comparison:

**JSON Result Files**
- Storage Location: `data/results/[user_id]/`
- Format: Each test generates one JSON file
- Contents Include: User ID, test name, timestamp, detailed test metrics

**Visualization Images**
- Storage Location: `data/images/[test_type]/[user_id]/[timestamp]/`
- Analog Stick tests generate trajectory plots showing:
  - Player movement paths
  - Target areas
  - Button click positions
  - Path deviation conditions

### Supported Data Formats
- **JSON**: Numerical data, statistical results, timestamps
- **PNG**: Trajectory plots, path diagrams, visualization results

This structured data storage approach facilitates:
- Cross-user data comparison and analysis
- Automated data processing and statistics
- Long-term research data preservation

## Design Features

### Color-Blind Friendly Design
- Uses blue/orange color scheme, friendly to color-blind users
- Avoids direct red-green color combinations
- Uses high contrast design to improve recognizability
- Combines text labels and icon symbols, not relying solely on color for information

### Modular Architecture
- Each test module is independent, facilitating maintenance and expansion
- Common modules are centrally managed to avoid code duplication
- Unified JSON data format facilitates subsequent analysis

### Accessibility Design
- Clear interaction prompts and countdown timers
- Supports multiple input methods
- Consistent operation procedures

## Controller Setup

The program will automatically detect connected controller devices. On first run, please:

1. Ensure the controller is properly connected to the computer
2. Run any test program
3. Select the controller device to use

## Advantages of Using uv

- **Fast Startup**: uv automatically manages Python versions and virtual environments
- **Fast Installation**: Package installation 10-100 times faster than pip
- **Automatic Dependency Management**: Automatically installs correct dependency versions based on `pyproject.toml`
- **Cross-Platform Consistency**: Ensures consistent behavior across different systems

## Common uv Commands
```bash
# Install specific packages
uv add pygame matplotlib

# Update all dependencies
uv lock --upgrade

# Remove a package
uv remove package_name

# Check current environment
uv pip list

# Clear cache
uv cache clean
```

## Development Information

### Adding New Tests
To add new test types:
1. Create new test files in the `tests/` directory
2. Follow existing module structure and naming conventions
3. Update the main menu in `main.py`
4. Ensure JSON output format follows existing standards

### Data Analysis
- All test results are stored in JSON format for easy programmatic processing
- Timestamp format: `YYYYMMDD_HHMMSS`
- Cross-user data analysis scripts can be added to the `scripts/` directory

## Troubleshooting

### Controller Connection Issues
- **Joy-Con not detected**:
  - First time use: Press the sync button to enter pairing mode
  - Ensure Bluetooth is enabled and Joy-Con shows up in Bluetooth settings
  - Try closing and reopening Joy-Con (hold sync button)
  - On macOS, may need to re-pair Bluetooth device

- **Other controller issues**:
  - PS4/PS5 controllers: Confirm drivers are installed
  - Xbox controllers: Confirm connection or successful pairing
  - Generic USB controllers: Check USB connection and compatibility

### Program Execution Issues
- **Python version error**:
  - Confirm Python version is 3.8 or higher
  - Use `python3 --version` to check version

- **pygame related errors**:
  - macOS may require additional packages: `brew install sdl2`
  - If audio errors occur, program is configured to ignore audio output

- **tkinter display issues**:
  - macOS: Confirm Tkinter is installed: `python3 -m tkinter`
  - Linux: May need to install `python3-tk`

### uv Related Issues
- **uv installation failure**:
  - Confirm network connection is normal
  - Try installing with pip: `pip install uv`
  - Check system permissions, may need sudo

- **Virtual environment issues**:
  - Confirm uv is properly installed: `uv --version`
  - Clear cache: `uv cache clean`
  - Recreate environment: Delete `.venv` folder then re-run `uv run`

- **Dependency installation issues**:
  - Check `pyproject.toml` file integrity
  - Try manual installation: `uv add pygame matplotlib`

### Test Result Issues
- **Cannot save results**:
  - Check `data/` directory permissions
  - Confirm sufficient disk space
  - Check if file system supports timestamp format in filenames

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

- **Cannot generate images**:
  - Confirm matplotlib is properly installed
  - Check `data/images/` directory permissions
  - Confirm system supports PNG format output

### Performance Issues
- **Program running slowly**:
  - Close other applications consuming system resources
  - Confirm sufficient system memory
  - Try reducing display resolution (modify window size in `config.py`)

- **Screen stuttering**:
  - Check system CPU usage
  - Confirm graphics card drivers are up to date

### Getting Help
If issues persist, please:
1. Check the complete error message content
2. Confirm system environment (OS version, Python version, etc.)
3. Try running tests in different environments

## Development

To modify or extend the program:

```bash
# Enter development mode (activate virtual environment)
uv shell

# Then you can directly use python commands
python main.py

# Install development dependencies
uv add --dev pytest black flake8

# Run code formatting
black .

# Run syntax checking
flake8 .
```

### Development Recommendations
- **Adding Tests**: Reference the structure and design patterns of existing test modules
- **Modifying Configuration**: All adjustable parameters are in `common/config.py`
- **Adding Features**: Follow the existing modular architecture
- **Testing Changes**: First use `connection_test.py` to ensure controller functionality is normal

## File Descriptions

### Main Program Files

#### `main.py`
- **Function**: Application main entry point
- **Features**: Provides interactive menu system, can select single test or complete test suite execution
- **Usage**: Direct execution enters menu mode, can also be executed with command line parameters

#### `pyproject.toml`
- **Function**: Project configuration file (Python standard)
- **Contents**: Defines project dependencies (pygame, matplotlib), Python version requirements, etc.
- **Importance**: uv automatically manages virtual environments and dependency installation based on this file

### Test Modules (`tests/` directory)

All test modules follow a unified design pattern:
- Support `--user` command line parameter to specify user ID
- Automatically save test results in JSON format
- Use color-blind friendly visual design
- Support controller and keyboard input (as backup)

#### `button_reaction_time_test.py`
- **Test Type**: Simple reaction time test
- **UI Framework**: tkinter
- **Input Method**: Any button/keyboard spacebar
- **Result File**: `button_reaction_time_YYYYMMDD_HHMMSS.json`

#### `button_prediction_countdown_test.py`
- **Test Type**: Prediction reaction time test
- **Special Features**: Animated ball movement, prediction time calculation
- **Gamified Design**: References Mario Party mechanics
- **Result File**: `button_prediction_countdown_YYYYMMDD_HHMMSS.json`

#### `button_smash_test.py`
- **Test Type**: Rapid clicking test
- **Timing Mechanism**: Starts timing from first click for 10 seconds
- **Visual Feedback**: Real-time display of click count and CPS
- **Result File**: `button_smash_YYYYMMDD_HHMMSS.json`

#### `button_accuracy_test.py`
- **Test Type**: Direction choice reaction test
- **Button Layout**: Diamond arrangement simulating real controller configuration
- **Evaluation Metrics**: Accuracy rate, average reaction time
- **Result File**: `button_accuracy_YYYYMMDD_HHMMSS.json`

#### `analog_move_test.py`
- **Test Type**: Joystick movement test
- **Graphical Output**: Automatically generates movement trajectory plots
- **Measurement Metrics**: Movement efficiency, trajectory analysis
- **Result Files**: JSON + PNG trajectory plot

#### `analog_path_follow_test.py`
- **Test Type**: Path tracking test
- **Path Types**: Straight line paths, S-curve paths
- **Graphical Output**: Path tracking trajectory plot showing deviation conditions
- **Result Files**: JSON + PNG trajectory plot

### Common Modules (`common/` directory)

#### `config.py`
- **Function**: Global configuration settings
- **Contents**:
  - Test timing settings (such as 10-second limit for clicking test)
  - Window size settings (1200x800)
  - Color-blind friendly color scheme (blue/orange combination)
  - Reaction time related parameters
- **Design Principles**: Centrally manage all adjustable parameters for easy maintenance

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
- **Function**: Store visualization charts
- **File Format**: PNG
- **Chart Types**:
  - `analog_move/`: Movement test trajectory plots
  - `analog_path_trace/`: Path tracking trajectory plots

### Development Documentation (`docs/`)
- **Contents**: Meeting records and technical documents from the project development process
- **Purpose**: Record design decisions and development progress

## License

This project is released under the MIT License. See the `LICENSE` file for details.

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Submit a pull request

## Acknowledgments

Special thanks to all contributors and the research team that helped develop this testing framework.

---

*For more technical details and development documentation, please refer to the `docs/` directory.*