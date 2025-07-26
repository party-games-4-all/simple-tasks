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
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FULLSCREEN = False

# 色盲友善配色
COLORS = {
    'BACKGROUND': (30, 30, 30),      # 深灰色背景
    'PRIMARY': (0, 120, 255),        # 藍色 - 色盲友善主色
    'SECONDARY': (255, 140, 0),      # 橘色 - 色盲友善次色
    'SUCCESS': (0, 150, 255),        # 藍色變體 - 成功
    'ERROR': (255, 100, 100),        # 紅色 - 錯誤（高對比度）
    'TEXT': (255, 255, 255),         # 白色文字
    'TARGET': (255, 165, 0),         # 橘色 - 目標顏色
    'PATH': (100, 149, 237),         # 淺藍色 - 路徑顏色
}

# 類比搖桿設定
ANALOG_DEADZONE = 0.1
ANALOG_SENSITIVITY = 1.0

# 路徑追蹤設定
PATH_WIDTH = 40
PATH_CORNER_TOLERANCE = 20
PATH_OUT_OF_BOUNDS_TOLERANCE = 10

# 檔案路徑設定
DATA_DIR = "data"
RESULTS_DIR = "data/results"
IMAGES_DIR = "data/images"

# 日誌設定
LOG_LEVEL = "INFO"
DEBUG_MODE = False
