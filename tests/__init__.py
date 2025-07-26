"""
Tests package
包含所有手把測試模組
"""

# 可以在這裡匯入所有測試模組，方便統一調用
from ..common import connection_test
from . import button_reaction_time_test
from . import button_prediction_countdown_test
from . import button_accuracy_test
from . import button_smash_test
from . import analog_move_test
from . import analog_path_follow_test
from . import analog_path_obstacle_test

__all__ = [
    'connection_test',
    'button_reaction_time_test', 
    'button_prediction_countdown_test',
    'button_accuracy_test',
    'button_smash_test',
    'analog_move_test',
    'analog_path_follow_test',
    'analog_path_obstacle_test'
]
