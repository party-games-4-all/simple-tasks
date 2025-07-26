"""
Tests package
包含所有手把測試模組
"""

# 可以在這裡匯入所有測試模組，方便統一調用
from . import connection_test
from . import button_reaction_time  
from . import prediction_reaction_test
from . import choice_accuracy_test
from . import analog_move_test
from . import path_follow_test

__all__ = [
    'connection_test',
    'button_reaction_time', 
    'prediction_reaction_test',
    'choice_accuracy_test', 
    'analog_move_test',
    'path_follow_test'
]
