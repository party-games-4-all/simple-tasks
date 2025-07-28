"""
共用配置設定文件
"""

# 測試時間設定（秒）
BUTTON_SMASH_DURATION = 5
REACTION_TIME_TRIALS = 10
CHOICE_ACCURACY_TRIALS = 20

# 反應時間設定（毫秒）
REACTION_TIME_MIN_INTERVAL = 1000
REACTION_TIME_MAX_INTERVAL = 3000
REACTION_TIME_TIMEOUT = 2000

# 顯示設定
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
FULLSCREEN = False

# 色盲友善配色
COLORS = {
    'BACKGROUND': (255, 255, 255),   # 白色背景 - 提高對比度
    'PRIMARY': (0, 120, 255),        # 藍色 - 色盲友善主色（玩家顏色）
    'SECONDARY': (255, 140, 0),      # 橘色 - 色盲友善次色
    'SUCCESS': (0, 150, 255),        # 藍色變體 - 成功
    'ERROR': (255, 100, 100),        # 紅色 - 錯誤（高對比度）
    'TEXT': (0, 0, 0),               # 黑色文字 - 適配白色背景
    'TARGET': (255, 100, 100),       # 紅色 - 目標顏色
    'PATH': (128, 128, 128),         # 中性灰色 - 路徑顏色（與玩家藍色形成對比）
    'BUTTON_DEFAULT': (240, 240, 240),  # 淺灰色 - 按鈕預設狀態
    'BUTTON_ACTIVE': (200, 200, 200),   # 深灰色 - 按鈕按下狀態
    'NEUTRAL': (128, 128, 128),      # 中性灰色
}

# 類比搖桿設定
ANALOG_DEADZONE = 0.1
ANALOG_SENSITIVITY = 1.0

# 路徑追蹤設定
PATH_WIDTH = 80  # 道路拓寬一倍，從 40 增加到 80
PATH_CORNER_TOLERANCE = 20
PATH_OUT_OF_BOUNDS_TOLERANCE = 10

# 檔案路徑設定
DATA_DIR = "data"
RESULTS_DIR = "data/results"
IMAGES_DIR = "data/images"

# 日誌設定
LOG_LEVEL = "INFO"
DEBUG_MODE = False
