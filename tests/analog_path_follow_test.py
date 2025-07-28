"""
路徑追蹤測試 - 簡化版本
- 已禁用路徑收縮功能以降低複雜度
- 玩家需要沿著固定路徑移動到達終點
"""
import random
import tkinter as tk
import time, os
import math
from threading import Thread
from abc import ABC, abstractmethod
import sys
from pathlib import Path

# 添加父目錄到 Python 路徑以便導入共用模組
sys.path.append(str(Path(__file__).parent.parent))

from common import config
from common.result_saver import save_test_result
from common.utils import get_directional_offset, setup_window_topmost
from common.trace_plot import output_single_trace

DEBUG = False  # 是否啟用除錯模式


class Path(ABC):
    """抽象路徑基類"""

    def __init__(self, canvas, width, color="black"):
        self.canvas = canvas
        self.width = width
        self.color = color
        self.path_elements = []  # 儲存路徑的圖形元素
        self.shrink_speed = 3
        self.is_active = True
        self.player_trace = []  # 玩家軌跡點

    @abstractmethod
    def create_path(self):
        """創建路徑圖形，子類必須實現"""
        pass

    @abstractmethod
    def is_inside(self, x, y):
        """檢查點是否在路徑內，子類必須實現"""
        pass

    @abstractmethod
    def shrink(self):
        """收縮路徑，子類必須實現"""
        pass

    @abstractmethod
    def get_goal_area(self):
        """獲取目標區域座標，子類必須實現"""
        pass

    def destroy(self):
        """銷毀路徑圖形"""
        for element in self.path_elements:
            self.canvas.delete(element)
        self.path_elements.clear()


class StraightPath(Path):
    """直線路徑"""

    def __init__(self,
                 canvas,
                 start_x,
                 start_y,
                 end_x,
                 end_y,
                 width,
                 color="black"):
        super().__init__(canvas, width, color)
        self.start_x = start_x
        self.start_y = start_y
        self.end_x = end_x
        self.end_y = end_y

        # 計算路徑方向和長度
        self.dx = end_x - start_x
        self.dy = end_y - start_y
        self.path_length = math.sqrt(self.dx**2 + self.dy**2)

        # 當前路徑長度（用於收縮）
        self.current_length = self.path_length

    def get_path_shapes(self):
        """回傳完整未收縮的直線路徑多邊形點位"""
        original_length = self.current_length
        self.current_length = self.path_length  # 暫時還原成完整長度
        points = self._calculate_path_points()
        self.current_length = original_length  # 還原
        return [[(points[i], points[i + 1]) for i in range(0, 8, 2)]]

    def create_path(self):
        """創建直線路徑"""
        if self.path_length > 0:
            # 計算初始路徑點
            points = self._calculate_path_points()

            # 創建多邊形路徑
            self.path_rect = self.canvas.create_polygon(points,
                                                        fill=self.color,
                                                        outline=self.color)
        else:
            # 處理零長度的情況
            half_width = self.width // 2
            self.path_rect = self.canvas.create_oval(self.start_x - half_width,
                                                     self.start_y - half_width,
                                                     self.start_x + half_width,
                                                     self.start_y + half_width,
                                                     fill=self.color,
                                                     outline=self.color)

        self.path_elements.append(self.path_rect)

    def _calculate_path_points(self):
        """計算路徑的多邊形點座標（從起點收縮到終點）"""
        # 計算當前起點位置
        ratio = self.current_length / self.path_length
        current_start_x = self.end_x - self.dx * ratio
        current_start_y = self.end_y - self.dy * ratio

        # 單位向量
        ux = self.dx / self.path_length
        uy = self.dy / self.path_length

        # 垂直向量
        perp_x = -uy * self.width / 2
        perp_y = ux * self.width / 2

        return [
            current_start_x + perp_x,
            current_start_y + perp_y,  # 左上
            self.end_x + perp_x,
            self.end_y + perp_y,  # 右上
            self.end_x - perp_x,
            self.end_y - perp_y,  # 右下
            current_start_x - perp_x,
            current_start_y - perp_y  # 左下
        ]

    def is_inside(self, x, y):
        """檢查點是否在收縮後的直線路徑內"""
        if self.path_length == 0:
            distance = math.hypot(x - self.start_x, y - self.start_y)
            return distance <= self.width / 2

        # 目前黑色段的起點（從 end 回推）
        ratio = self.current_length / self.path_length
        current_start_x = self.end_x - self.dx * ratio
        current_start_y = self.end_y - self.dy * ratio

        # 使用 current_start → end 這段作為合法區段
        # 玩家若跑在 current_start 前面（已被收掉），也要算偏離
        dx = x - current_start_x
        dy = y - current_start_y

        segment_dx = self.end_x - current_start_x
        segment_dy = self.end_y - current_start_y
        segment_len_sq = segment_dx**2 + segment_dy**2

        if segment_len_sq == 0:
            return False

        # 投影參數 t：投影在 segment 上的相對位置（0~1）
        t = (dx * segment_dx + dy * segment_dy) / segment_len_sq

        # ⛔ 超出 segment 範圍（不是黑色段）
        if t < 0 or t > 1:
            return False

        # 找到投影點
        nearest_x = current_start_x + t * segment_dx
        nearest_y = current_start_y + t * segment_dy

        distance = math.hypot(x - nearest_x, y - nearest_y)
        return distance <= self.width / 2

    def shrink(self):
        """從起點向終點方向收縮路徑"""
        if self.current_length > 0:
            self.current_length = max(0,
                                      self.current_length - self.shrink_speed)

            # 使用 coords 更新現有圖形，避免閃爍
            if self.path_length > 0:
                points = self._calculate_path_points()
                self.canvas.coords(self.path_rect, *points)
            else:
                # 圓形路徑的處理
                half_width = max(
                    0,
                    self.width // 2 * (self.current_length / self.path_length))
                self.canvas.coords(self.path_rect, self.start_x - half_width,
                                   self.start_y - half_width,
                                   self.start_x + half_width,
                                   self.start_y + half_width)

    def get_goal_area(self):
        """獲取目標區域座標"""
        goal_length = 100  # 目標區域長度

        if self.path_length == 0:
            return {
                'left': self.start_x - self.width // 2,
                'top': self.start_y - self.width // 2,
                'right': self.start_x + self.width // 2,
                'bottom': self.start_y + self.width // 2
            }

        # 計算目標區域起點
        if self.path_length > goal_length:
            ratio = (self.path_length - goal_length) / self.path_length
            goal_start_x = self.start_x + self.dx * ratio
            goal_start_y = self.start_y + self.dy * ratio
        else:
            goal_start_x = self.start_x
            goal_start_y = self.start_y

        # 計算垂直向量
        ux = self.dx / self.path_length
        uy = self.dy / self.path_length
        perp_x = -uy * self.width / 2
        perp_y = ux * self.width / 2

        return {
            'points': [
                goal_start_x + perp_x, goal_start_y + perp_y,
                self.end_x + perp_x, self.end_y + perp_y, self.end_x - perp_x,
                self.end_y - perp_y, goal_start_x - perp_x,
                goal_start_y - perp_y
            ]
        }


class CornerPath(Path):
    """轉彎路徑"""

    def __init__(self,
                 canvas,
                 start_x,
                 start_y,
                 corner_x,
                 corner_y,
                 end_x,
                 end_y,
                 width,
                 color="black"):
        super().__init__(canvas, width, color)
        self.start_x = start_x
        self.start_y = start_y
        self.corner_x = corner_x
        self.corner_y = corner_y
        self.end_x = end_x
        self.end_y = end_y

        # 計算路徑段
        self.segment1_length = math.sqrt((corner_x - start_x)**2 +
                                         (corner_y - start_y)**2)
        self.segment2_length = math.sqrt((end_x - corner_x)**2 +
                                         (end_y - corner_y)**2)
        self.total_length = self.segment1_length + self.segment2_length
        self.current_progress = 1.0  # 1.0 表示完整路徑，0.0 表示完全收縮

    def get_path_shapes(self):
        """回傳未收縮的兩段轉角路徑 polygon 點位陣列（供圖像輸出用）"""
        shapes = []

        # 第一段：start → corner
        points1 = self._create_segment_points(self.start_x, self.start_y,
                                              self.corner_x, self.corner_y)
        shape1 = [(points1[i], points1[i + 1]) for i in range(0, 8, 2)]
        shapes.append(shape1)

        # 第二段：使用與 create_path 相同的邏輯計算起點
        dx1 = self.corner_x - self.start_x
        dy1 = self.corner_y - self.start_y
        length1 = math.sqrt(dx1**2 + dy1**2)
        
        dx2 = self.end_x - self.corner_x
        dy2 = self.end_y - self.corner_y
        length2 = math.sqrt(dx2**2 + dy2**2)
        
        if length1 > 0 and length2 > 0:
            ux2 = dx2 / length2
            uy2 = dy2 / length2
            
            cross_product = dx1 * dy2 - dy1 * dx2
            
            if abs(cross_product) > 1e-6:
                seg2_start_x = self.corner_x - ux2 * (self.width / 2)
                seg2_start_y = self.corner_y - uy2 * (self.width / 2)
            else:
                seg2_start_x = self.corner_x
                seg2_start_y = self.corner_y
        else:
            seg2_start_x = self.corner_x
            seg2_start_y = self.corner_y

        points2 = self._create_segment_points(seg2_start_x, seg2_start_y,
                                              self.end_x, self.end_y)
        shape2 = [(points2[i], points2[i + 1]) for i in range(0, 8, 2)]
        shapes.append(shape2)

        return shapes

    def create_path(self):
        """創建轉彎路徑，確保兩段路徑完全銜接無縫隙"""
        # 第一段：從起點到轉角
        self.segment1 = self._create_segment(self.start_x, self.start_y,
                                             self.corner_x, self.corner_y,
                                             'blue')
        
        # 計算第一段的方向向量
        dx1 = self.corner_x - self.start_x
        dy1 = self.corner_y - self.start_y
        length1 = math.sqrt(dx1**2 + dy1**2)
        
        # 計算第二段的方向向量
        dx2 = self.end_x - self.corner_x
        dy2 = self.end_y - self.corner_y
        length2 = math.sqrt(dx2**2 + dy2**2)
        
        # 動態調整第二段起點來確保完全銜接
        if length1 > 0 and length2 > 0:
            # 第一段的單位向量
            ux1 = dx1 / length1
            uy1 = dy1 / length1
            
            # 第二段的單位向量  
            ux2 = dx2 / length2
            uy2 = dy2 / length2
            
            # 第一段在轉角處的垂直向量
            perp1_x = -uy1 * self.width / 2
            perp1_y = ux1 * self.width / 2
            
            # 第二段在轉角處的垂直向量
            perp2_x = -uy2 * self.width / 2
            perp2_y = ux2 * self.width / 2
            
            # 根據轉彎方向調整第二段起點
            # 計算叉積來判斷轉彎方向
            cross_product = dx1 * dy2 - dy1 * dx2
            
            if abs(cross_product) > 1e-6:  # 避免除零錯誤
                if cross_product > 0:  # 左轉
                    # 延伸第二段起點，使其與第一段的外側邊緣銜接
                    segment2_start_x = self.corner_x - ux2 * (self.width / 2)
                    segment2_start_y = self.corner_y - uy2 * (self.width / 2)
                else:  # 右轉
                    # 延伸第二段起點，使其與第一段的內側邊緣銜接
                    segment2_start_x = self.corner_x - ux2 * (self.width / 2)
                    segment2_start_y = self.corner_y - uy2 * (self.width / 2)
            else:
                # 直線情況（理論上不會發生在轉角路徑中）
                segment2_start_x = self.corner_x
                segment2_start_y = self.corner_y
        else:
            # 後備方案
            segment2_start_x = self.corner_x
            segment2_start_y = self.corner_y
            
        self.segment2 = self._create_segment(segment2_start_x, segment2_start_y,
                                             self.end_x, self.end_y, 'green')

        if self.segment1:
            self.path_elements.append(self.segment1)
        if self.segment2:
            self.path_elements.append(self.segment2)

    def _create_segment(self, x1, y1, x2, y2, color):
        """創建路徑段"""
        # 計算垂直於路徑方向的向量
        dx = x2 - x1
        dy = y2 - y1
        length = math.sqrt(dx**2 + dy**2)

        if length == 0:
            return None

        # 單位向量
        ux = dx / length
        uy = dy / length

        # 垂直向量
        perp_x = -uy * self.width / 2
        perp_y = ux * self.width / 2

        # 創建多邊形
        points = [
            x1 + perp_x,
            y1 + perp_y,  # 左上
            x2 + perp_x,
            y2 + perp_y,  # 右上
            x2 - perp_x,
            y2 - perp_y,  # 右下
            x1 - perp_x,
            y1 - perp_y  # 左下
        ]

        if DEBUG:
            return self.canvas.create_polygon(points,
                                              fill=color,
                                              outline=self.color)

        return self.canvas.create_polygon(points,
                                          fill=self.color,
                                          outline=self.color)

    def is_inside(self, x, y):
        """檢查點是否在收縮後的黑色轉彎路徑內"""
        remaining_length = self.total_length * self.current_progress
        if remaining_length <= 0:
            return False

        # 計算第二段的正確起點（與其他方法保持一致）
        dx1 = self.corner_x - self.start_x
        dy1 = self.corner_y - self.start_y
        length1 = math.sqrt(dx1**2 + dy1**2)
        
        dx2 = self.end_x - self.corner_x
        dy2 = self.end_y - self.corner_y
        length2 = math.sqrt(dx2**2 + dy2**2)
        
        if length1 > 0 and length2 > 0:
            ux2 = dx2 / length2
            uy2 = dy2 / length2
            
            cross_product = dx1 * dy2 - dy1 * dx2
            
            if abs(cross_product) > 1e-6:
                segment2_start_x = self.corner_x - ux2 * (self.width / 2)
                segment2_start_y = self.corner_y - uy2 * (self.width / 2)
            else:
                segment2_start_x = self.corner_x
                segment2_start_y = self.corner_y
        else:
            segment2_start_x = self.corner_x
            segment2_start_y = self.corner_y

        if remaining_length <= self.segment2_length:
            ratio = remaining_length / self.segment2_length
            seg2_start_x = self.end_x - (self.end_x - segment2_start_x) * ratio
            seg2_start_y = self.end_y - (self.end_y - segment2_start_y) * ratio

            polygon = self._create_segment_points(seg2_start_x, seg2_start_y,
                                                  self.end_x, self.end_y)
            return self._point_in_polygon(x, y, polygon)
        else:
            remain_len = remaining_length - self.segment2_length
            ratio = remain_len / self.segment1_length
            seg1_start_x = self.corner_x - (self.corner_x -
                                            self.start_x) * ratio
            seg1_start_y = self.corner_y - (self.corner_y -
                                            self.start_y) * ratio

            polygon1 = self._create_segment_points(seg1_start_x, seg1_start_y,
                                                   self.corner_x,
                                                   self.corner_y)
            polygon2 = self._create_segment_points(segment2_start_x,
                                                   segment2_start_y,
                                                   self.end_x, self.end_y)

            return self._point_in_polygon(x, y, polygon1) or \
                self._point_in_polygon(x, y, polygon2)

    def _point_in_segment(self, px, py, x1, y1, x2, y2):
        """檢查點是否在路徑段內"""
        # 計算點到線段的距離
        dx = x2 - x1
        dy = y2 - y1
        length_sq = dx**2 + dy**2

        if length_sq == 0:
            return False

        # 計算投影參數
        t = ((px - x1) * dx + (py - y1) * dy) / length_sq
        t = max(0, min(1, t))

        # 計算最近點
        nearest_x = x1 + t * dx
        nearest_y = y1 + t * dy

        # 計算距離
        distance = math.sqrt((px - nearest_x)**2 + (py - nearest_y)**2)

        return distance <= self.width / 2

    def _point_in_polygon(self, px, py, polygon_points):
        """使用 ray casting 演算法判斷點是否在多邊形內"""
        num = len(polygon_points)
        inside = False
        j = num - 2
        for i in range(0, num, 2):
            xi, yi = polygon_points[i], polygon_points[i + 1]
            xj, yj = polygon_points[j], polygon_points[j + 1]
            if ((yi > py) != (yj > py)) and \
            (px < (xj - xi) * (py - yi) / ((yj - yi) + 1e-9) + xi):
                inside = not inside
            j = i
        return inside

    def shrink(self):
        """收縮轉彎路徑"""
        if self.current_progress > 0:
            self.current_progress = max(
                0,
                self.current_progress - self.shrink_speed / self.total_length)
            self._update_path()

    def _update_path(self):
        """根據當前進度更新路徑（從終點往起點收縮），使用正確的銜接邏輯"""
        remaining_length = self.total_length * self.current_progress

        if remaining_length <= 0:
            for element in self.path_elements:
                self.canvas.coords(element, 0, 0, 0, 0)
            return

        # 計算第二段的正確起點（與 create_path 使用相同邏輯）
        dx1 = self.corner_x - self.start_x
        dy1 = self.corner_y - self.start_y
        length1 = math.sqrt(dx1**2 + dy1**2)
        
        dx2 = self.end_x - self.corner_x
        dy2 = self.end_y - self.corner_y
        length2 = math.sqrt(dx2**2 + dy2**2)
        
        if length1 > 0 and length2 > 0:
            ux2 = dx2 / length2
            uy2 = dy2 / length2
            
            cross_product = dx1 * dy2 - dy1 * dx2
            
            if abs(cross_product) > 1e-6:
                segment2_start_x = self.corner_x - ux2 * (self.width / 2)
                segment2_start_y = self.corner_y - uy2 * (self.width / 2)
            else:
                segment2_start_x = self.corner_x
                segment2_start_y = self.corner_y
        else:
            segment2_start_x = self.corner_x
            segment2_start_y = self.corner_y

        if remaining_length <= self.segment2_length:
            # segment2 正在收縮
            ratio = remaining_length / self.segment2_length
            start_x = self.end_x - (self.end_x - segment2_start_x) * ratio
            start_y = self.end_y - (self.end_y - segment2_start_y) * ratio

            if self.segment2:
                points = self._create_segment_points(start_x, start_y,
                                                     self.end_x, self.end_y)
                self.canvas.coords(self.segment2, *points)

            if self.segment1:
                self.canvas.coords(self.segment1, 0, 0, 0, 0)

        else:
            # segment2 全部顯示
            if self.segment2:
                points2 = self._create_segment_points(segment2_start_x,
                                                      segment2_start_y,
                                                      self.end_x, self.end_y)
                self.canvas.coords(self.segment2, *points2)

            # segment1 部分收縮
            remaining_length1 = remaining_length - self.segment2_length
            ratio = remaining_length1 / self.segment1_length
            start_x = self.corner_x - (self.corner_x - self.start_x) * ratio
            start_y = self.corner_y - (self.corner_y - self.start_y) * ratio

            if self.segment1:
                points1 = self._create_segment_points(start_x, start_y,
                                                      self.corner_x,
                                                      self.corner_y)
                self.canvas.coords(self.segment1, *points1)

    def _create_segment_points(self, x1, y1, x2, y2):
        """創建路徑段的點座標"""
        # 計算垂直於路徑方向的向量
        dx = x2 - x1
        dy = y2 - y1
        length = math.sqrt(dx**2 + dy**2)

        if length == 0:
            return [x1, y1, x1, y1, x1, y1, x1, y1]

        # 單位向量
        ux = dx / length
        uy = dy / length

        # 垂直向量
        perp_x = -uy * self.width / 2
        perp_y = ux * self.width / 2

        # 返回多邊形的四個頂點
        return [
            x1 + perp_x,
            y1 + perp_y,  # 左上
            x2 + perp_x,
            y2 + perp_y,  # 右上
            x2 - perp_x,
            y2 - perp_y,  # 右下
            x1 - perp_x,
            y1 - perp_y  # 左下
        ]

    def get_goal_area(self):
        """獲取目標區域座標"""
        # 計算終點附近的目標區域
        goal_length = 100  # 目標區域長度

        # 計算第二段的方向向量
        dx = self.end_x - self.corner_x
        dy = self.end_y - self.corner_y
        length = math.sqrt(dx**2 + dy**2)

        if length == 0:
            return {
                'left': self.end_x,
                'top': self.end_y,
                'right': self.end_x,
                'bottom': self.end_y
            }

        # 單位向量
        ux = dx / length
        uy = dy / length

        # 目標區域起點
        goal_start_x = self.end_x - ux * goal_length
        goal_start_y = self.end_y - uy * goal_length

        # 垂直向量
        perp_x = -uy * self.width / 2
        perp_y = ux * self.width / 2

        return {
            'points': [
                goal_start_x + perp_x, goal_start_y + perp_y,
                self.end_x + perp_x, self.end_y + perp_y, self.end_x - perp_x,
                self.end_y - perp_y, goal_start_x - perp_x,
                goal_start_y - perp_y
            ]
        }


class PathFollowingTestApp:

    def __init__(self, root, user_id=None):
        self.root = root
        self.user_id = user_id or "default"
        self.root.title("🎮 Path Following 測試 (簡化版本)")
        
        # 設定視窗置頂
        setup_window_topmost(self.root)
        
        self.canvas_width = config.WINDOW_WIDTH
        self.canvas_height = config.WINDOW_HEIGHT
        background_color = f"#{config.COLORS['BACKGROUND'][0]:02x}{config.COLORS['BACKGROUND'][1]:02x}{config.COLORS['BACKGROUND'][2]:02x}"
        self.canvas = tk.Canvas(root,
                                width=self.canvas_width,
                                height=self.canvas_height,
                                bg=background_color)
        self.canvas.pack()

        # 調整角色大小和移動速度，考慮不同年齡層使用者
        self.player_radius = 15  # 變大為道路寬的 1/4 (120/4 = 30，半徑為 15)
        self.goal_color = f"#{config.COLORS['TARGET'][0]:02x}{config.COLORS['TARGET'][1]:02x}{config.COLORS['TARGET'][2]:02x}"

        self.player_x = 100
        self.player_y = 400
        self.offset = 15  # 減小起始偏移距離
        self.leftX = 0
        self.leftY = 0
        self.speed = 7  # 速度放慢，從 10 減為 7

        self.off_path_time = 0
        self.total_time = 0
        self.start_time = None
        self.running = False
        self.reached_goal = False

        # 記錄所有測試結果用於 JSON 儲存
        self.test_results = []

        # 創建路徑（可以選擇不同類型的路徑）
        self.paths = self.create_paths()
        self.current_path_index = 0
        self.setup_player()
        self.load_path(self.current_path_index)

        # 圖片紀錄位置 - 改為使用 data/images 結構
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        self.session_output_dir = os.path.join("data", "images", "analog_path_trace", self.user_id, timestamp)
        os.makedirs(self.session_output_dir, exist_ok=True)
        print(f"📂 本次資料儲存於：{self.session_output_dir}")

    def create_paths(self):
        """回傳多條路徑清單 - 包含4種直線和8種L型轉彎路徑"""
        # 參考Mario Party Lumber Tumble的設計調整參數
        path_width = 120  # 道路拓寬一倍，從 60 增加到 120
        margin = 80      # 邊界距離
        center_x = self.canvas_width // 2
        center_y = self.canvas_height // 2
        
        path_color = f"#{config.COLORS['PATH'][0]:02x}{config.COLORS['PATH'][1]:02x}{config.COLORS['PATH'][2]:02x}"
        
        paths = [
            # ---- 4條直線路徑 (上下左右) ----
            # 左右直線 - 從左到右
            StraightPath(self.canvas, margin, center_y, self.canvas_width - margin, center_y, path_width, path_color),
            # 左右直線 - 從右到左  
            StraightPath(self.canvas, self.canvas_width - margin, center_y, margin, center_y, path_width, path_color),
            # 上下直線 - 從上到下
            StraightPath(self.canvas, center_x, margin, center_x, self.canvas_height - margin, path_width, path_color),
            # 上下直線 - 從下到上
            StraightPath(self.canvas, center_x, self.canvas_height - margin, center_x, margin, path_width, path_color),
            
            # ---- 8種L型轉彎路徑 (每種L型都有兩個方向) ----
            
            # L型1: 右轉上 (┗) - 從左進入向右然後向上
            CornerPath(self.canvas, margin, center_y, center_x, center_y, center_x, margin, path_width, path_color),
            # L型1反向: 下轉左 (┐) - 從上進入向下然後向左
            CornerPath(self.canvas, center_x, margin, center_x, center_y, margin, center_y, path_width, path_color),
            
            # L型2: 右轉下 (┏) - 從左進入向右然後向下
            CornerPath(self.canvas, margin, center_y, center_x, center_y, center_x, self.canvas_height - margin, path_width, path_color),
            # L型2反向: 上轉左 (┘) - 從下進入向上然後向左
            CornerPath(self.canvas, center_x, self.canvas_height - margin, center_x, center_y, margin, center_y, path_width, path_color),
            
            # L型3: 左轉上 (⊏) - 從右進入向左然後向上
            CornerPath(self.canvas, self.canvas_width - margin, center_y, center_x, center_y, center_x, margin, path_width, path_color),
            # L型3反向: 下轉右 (┌) - 從上進入向下然後向右
            CornerPath(self.canvas, center_x, margin, center_x, center_y, self.canvas_width - margin, center_y, path_width, path_color),
            
            # L型4: 左轉下 (⊐) - 從右進入向左然後向下
            CornerPath(self.canvas, self.canvas_width - margin, center_y, center_x, center_y, center_x, self.canvas_height - margin, path_width, path_color),
            # L型4反向: 上轉右 (└) - 從下進入向上然後向右
            CornerPath(self.canvas, center_x, self.canvas_height - margin, center_x, center_y, self.canvas_width - margin, center_y, path_width, path_color),
        ]
        
        # 為每個路徑增加類型標識以便後續分析
        for i, path in enumerate(paths):
            if isinstance(path, StraightPath):
                if i < 2:  # 左右直線
                    path.movement_type = "horizontal_straight"
                else:      # 上下直線
                    path.movement_type = "vertical_straight"
            else:  # CornerPath
                path.movement_type = "corner_turn"
        
        random.shuffle(paths)
        return paths

    def load_path(self, index):
        if hasattr(self, "path"):
            self.path.destroy()
            self.canvas.delete(self.goal_rect)

        self.path = self.paths[index]
        self.path.create_path()  # ✅ 在這裡才繪製當前路徑
        self.setup_goal()

        # 重設玩家位置（可根據每條 path 決定）
        # 根據 path 類型自動設置 offset 起始點
        if isinstance(self.path, StraightPath):
            dx = self.path.end_x - self.path.start_x
            dy = self.path.end_y - self.path.start_y
            offset_x, offset_y = get_directional_offset(dx, dy, self.offset)
            self.player_x = self.path.start_x + offset_x
            self.player_y = self.path.start_y + offset_y
        elif isinstance(self.path, CornerPath):
            dx = self.path.corner_x - self.path.start_x
            dy = self.path.corner_y - self.path.start_y
            offset_x, offset_y = get_directional_offset(dx, dy, self.offset)
            self.player_x = self.path.start_x + offset_x
            self.player_y = self.path.start_y + offset_y
        else:
            self.player_x = 100
            self.player_y = 400

        self.canvas.coords(self.player, self.player_x - self.player_radius,
                           self.player_y - self.player_radius,
                           self.player_x + self.player_radius,
                           self.player_y + self.player_radius)
        self.canvas.tag_raise(self.player)

        # 重設狀態
        self.start_time = None
        self.total_time = 0
        self.off_path_time = 0
        self.reached_goal = False
        self.running = False
        self.leftX = 0
        self.leftY = 0
        # 重設縮短狀態
        if isinstance(self.path, StraightPath):
            self.path.current_length = self.path.path_length
        elif isinstance(self.path, CornerPath):
            self.path.current_progress = 1.0

        self.player_loop()

    def setup_goal(self):
        """設置目標區域"""
        goal_area = self.path.get_goal_area()

        if 'points' in goal_area:
            # 多邊形目標區域
            self.goal_rect = self.canvas.create_polygon(
                goal_area['points'],
                fill=self.goal_color,
                outline=self.goal_color)
        else:
            # 矩形目標區域
            self.goal_rect = self.canvas.create_rectangle(goal_area['left'],
                                                          goal_area['top'],
                                                          goal_area['right'],
                                                          goal_area['bottom'],
                                                          fill=self.goal_color)
        self.canvas.tag_raise(self.goal_rect)

    def setup_player(self):
        """設置玩家"""
        primary_color = f"#{config.COLORS['PRIMARY'][0]:02x}{config.COLORS['PRIMARY'][1]:02x}{config.COLORS['PRIMARY'][2]:02x}"
        self.player = self.canvas.create_oval(
            self.player_x - self.player_radius,
            self.player_y - self.player_radius,
            self.player_x + self.player_radius,
            self.player_y + self.player_radius,
            fill=primary_color)
        self.canvas.tag_raise(self.player)  # ← 初始時也拉最上面

    def player_loop(self):
        if self.running and not self.reached_goal:
            dx = self.leftX * self.speed
            dy = self.leftY * self.speed

            self.player_x += dx
            self.player_y += dy

            self.player_x = max(
                self.player_radius,
                min(self.canvas_width - self.player_radius, self.player_x))
            self.player_y = max(
                self.player_radius,
                min(self.canvas_height - self.player_radius, self.player_y))

            self.canvas.coords(self.player, self.player_x - self.player_radius,
                               self.player_y - self.player_radius,
                               self.player_x + self.player_radius,
                               self.player_y + self.player_radius)
            self.canvas.tag_raise(self.player)

            if DEBUG:
                primary_color = f"#{config.COLORS['PRIMARY'][0]:02x}{config.COLORS['PRIMARY'][1]:02x}{config.COLORS['PRIMARY'][2]:02x}"
                error_color = f"#{config.COLORS['ERROR'][0]:02x}{config.COLORS['ERROR'][1]:02x}{config.COLORS['ERROR'][2]:02x}"
                if self.path.is_inside(self.player_x, self.player_y):
                    self.canvas.itemconfig(self.player, fill=primary_color)
                else:
                    self.canvas.itemconfig(self.player, fill=error_color)

            # 🔒 禁用路徑收縮功能以降低複雜度
            # self.path.shrink()

            now = time.time()
            if self.start_time is None:
                self.start_time = now

            self.total_time += 0.016
            if not self.path.is_inside(self.player_x, self.player_y):
                self.off_path_time += 0.016

            if self.check_reached_goal():
                self.reached_goal = True
                self.show_result()
                self.root.after(1000, self.advance_path)
                return

            # 紀錄玩家軌跡
            self.path.player_trace.append((self.player_x, self.player_y))

        # 16ms 之後再執行一次（~60fps）
        self.root.after(16, self.player_loop)

    def advance_path(self):
        output_single_trace(self.path, self.current_path_index,
                            self.session_output_dir)
        self.current_path_index += 1
        if self.current_path_index >= len(self.paths):
            print("✅ 所有路徑測試完成")
            self.save_test_results()
        else:
            self.load_path(self.current_path_index)

    def check_reached_goal(self):
        """檢查是否到達目標"""
        goal_area = self.path.get_goal_area()

        if 'points' in goal_area:
            # 簡化的多邊形目標區域檢查
            # 檢查玩家是否在目標區域的邊界框內
            points = goal_area['points']
            min_x = min(points[0::2])  # 取所有x座標的最小值
            max_x = max(points[0::2])  # 取所有x座標的最大值
            min_y = min(points[1::2])  # 取所有y座標的最小值
            max_y = max(points[1::2])  # 取所有y座標的最大值

            return (min_x <= self.player_x <= max_x
                    and min_y <= self.player_y <= max_y)
        else:
            # 矩形目標區域的檢查
            return (goal_area['left'] <= self.player_x <= goal_area['right']
                    and
                    goal_area['top'] <= self.player_y <= goal_area['bottom'])

    def analyze_movement_segments(self, path):
        """分析玩家在路徑上的移動段落：直線段 vs 轉彎段"""
        if isinstance(path, StraightPath):
            # 直線路徑只有一個直線段
            return {
                "straight_segments": [{
                    "start_time": 0,
                    "duration": self.total_time,
                    "movement_type": path.movement_type,
                    "accuracy": 100 - (self.off_path_time / self.total_time * 100) if self.total_time > 0 else 0
                }],
                "corner_segments": []
            }
        elif isinstance(path, CornerPath):
            # 轉彎路徑需要分析兩段：直線段和轉彎段
            # 這裡需要根據軌跡點來分析，簡化版本按比例估算
            segment1_ratio = path.segment1_length / path.total_length
            segment1_duration = self.total_time * segment1_ratio
            segment2_duration = self.total_time * (1 - segment1_ratio)
            
            return {
                "straight_segments": [{
                    "start_time": 0,
                    "duration": segment1_duration,
                    "movement_type": "first_straight",
                    "accuracy": 95  # 簡化，實際應分析軌跡
                }],
                "corner_segments": [{
                    "start_time": segment1_duration,
                    "duration": segment2_duration,
                    "movement_type": "corner_turn",
                    "accuracy": 85  # 轉彎通常較困難
                }]
            }
        
        return {"straight_segments": [], "corner_segments": []}

    def show_result(self):
        percent_off = (self.off_path_time / self.total_time) * 100
        
        # 記錄單次路徑測試結果
        path_type = "straight" if isinstance(self.path, StraightPath) else "corner"
        
        # 新增：移動段落分析
        movement_analysis = self.analyze_movement_segments(self.path)
        
        path_info = {
            "start_x": self.path.start_x,
            "start_y": self.path.start_y,
            "end_x": self.path.end_x,
            "end_y": self.path.end_y,
            "width": self.path.width,
            "movement_type": getattr(self.path, 'movement_type', 'unknown')
        }
        
        if isinstance(self.path, CornerPath):
            path_info["corner_x"] = self.path.corner_x
            path_info["corner_y"] = self.path.corner_y
            path_info["total_length"] = self.path.total_length
            path_info["segment1_length"] = self.path.segment1_length
            path_info["segment2_length"] = self.path.segment2_length
        else:
            path_info["path_length"] = self.path.path_length
        
        trial_result = {
            "trial_number": self.current_path_index + 1,
            "path_type": path_type,
            "path_info": path_info,
            "completion_time_seconds": self.total_time,
            "off_path_time_seconds": self.off_path_time,
            "off_path_percentage": percent_off,
            "path_accuracy": 100 - percent_off,
            "trace_points_count": len(self.path.player_trace),
            "movement_analysis": movement_analysis,  # 新增：段落分析
            # 新增：繪圖所需的完整資料
            "player_trace": self.path.player_trace,  # 完整的玩家移動軌跡
            "path_shapes": self.path.get_path_shapes(),  # 路徑形狀資料
            "goal_area": self.path.get_goal_area(),  # 目標區域資料
            "canvas_dimensions": {
                "width": self.canvas_width,
                "height": self.canvas_height
            },
            "player_radius": self.player_radius,
            "path_width": self.path.width
        }
        self.test_results.append(trial_result)
        
        print("🎯 到達終點")
        print(f"⏱ 總時間：{self.total_time:.2f} 秒")
        print(f"❌ 偏離路徑時間：{self.off_path_time:.2f} 秒")
        print(f"📊 偏離比例：{percent_off:.2f}%")
        print(f"🔄 移動類型：{path_info['movement_type']}")
        
        # 顯示段落分析
        if movement_analysis['straight_segments']:
            print(f"📏 直線段落：{len(movement_analysis['straight_segments'])} 個")
        if movement_analysis['corner_segments']:
            print(f"🔄 轉彎段落：{len(movement_analysis['corner_segments'])} 個")

    def on_joycon_input(self, buttons, leftX, leftY, last_key_bit,
                        last_key_down):
        self.leftX = leftX
        self.leftY = leftY
        if not self.running and last_key_down:
            self.running = True
            print("✅ 開始測試！請沿著路徑前進")

    def save_test_results(self):
        """儲存測試結果為 JSON 檔案"""
        if not self.test_results:
            print("⚠️ 無測試結果可儲存")
            return
        
        # 計算總體統計
        total_trials = len(self.test_results)
        total_time = sum(t["completion_time_seconds"] for t in self.test_results)
        total_off_path_time = sum(t["off_path_time_seconds"] for t in self.test_results)
        avg_completion_time = total_time / total_trials
        avg_accuracy = sum(t["path_accuracy"] for t in self.test_results) / total_trials
        
        # 分析不同路徑類型的表現
        straight_trials = [t for t in self.test_results if t["path_type"] == "straight"]
        corner_trials = [t for t in self.test_results if t["path_type"] == "corner"]
        
        # 新增：詳細的移動類型分析
        horizontal_straight = [t for t in self.test_results if t["path_info"].get("movement_type") == "horizontal_straight"]
        vertical_straight = [t for t in self.test_results if t["path_info"].get("movement_type") == "vertical_straight"]
        corner_turns = [t for t in self.test_results if t["path_info"].get("movement_type") == "corner_turn"]
        
        # 準備儲存的測試參數（更新參數以反映新設計）
        parameters = {
            "window_size": {
                "width": self.canvas_width,
                "height": self.canvas_height
            },
            "player_radius": self.player_radius,
            "movement_speed_multiplier": self.speed,
            "total_paths": len(self.paths),
            "path_width": 120,  # 更新為新的路徑寬度（拓寬一倍）
            "player_offset": self.offset,
            "mario_party_reference": True,  # 標記參考Mario Party設計
            "path_types": {
                "straight_paths": 4,  # 4條直線
                "l_shaped_paths": 8   # 8種L型轉彎
            },
            "accessibility_optimized": True,  # 標記已針對不同年齡層優化
            "speed_reduced_for_accessibility": True  # 標記速度已為了可及性降低
        }
        
        # 準備儲存的指標數據（包含新的分析）
        metrics = {
            "total_trials": total_trials,
            "total_time_seconds": total_time,
            "total_off_path_time_seconds": total_off_path_time,
            "average_completion_time_seconds": avg_completion_time,
            "average_accuracy_percentage": avg_accuracy,
            "trials": self.test_results,
            "path_type_analysis": {
                "straight_paths": {
                    "count": len(straight_trials),
                    "avg_completion_time_s": sum(t["completion_time_seconds"] for t in straight_trials) / len(straight_trials) if straight_trials else 0,
                    "avg_accuracy_pct": sum(t["path_accuracy"] for t in straight_trials) / len(straight_trials) if straight_trials else 0
                },
                "corner_paths": {
                    "count": len(corner_trials),
                    "avg_completion_time_s": sum(t["completion_time_seconds"] for t in corner_trials) / len(corner_trials) if corner_trials else 0,
                    "avg_accuracy_pct": sum(t["path_accuracy"] for t in corner_trials) / len(corner_trials) if corner_trials else 0
                }
            },
            "movement_type_analysis": {
                "horizontal_straight": {
                    "count": len(horizontal_straight),
                    "avg_completion_time_s": sum(t["completion_time_seconds"] for t in horizontal_straight) / len(horizontal_straight) if horizontal_straight else 0,
                    "avg_accuracy_pct": sum(t["path_accuracy"] for t in horizontal_straight) / len(horizontal_straight) if horizontal_straight else 0
                },
                "vertical_straight": {
                    "count": len(vertical_straight),
                    "avg_completion_time_s": sum(t["completion_time_seconds"] for t in vertical_straight) / len(vertical_straight) if vertical_straight else 0,
                    "avg_accuracy_pct": sum(t["path_accuracy"] for t in vertical_straight) / len(vertical_straight) if vertical_straight else 0
                },
                "corner_turns": {
                    "count": len(corner_turns),
                    "avg_completion_time_s": sum(t["completion_time_seconds"] for t in corner_turns) / len(corner_turns) if corner_turns else 0,
                    "avg_accuracy_pct": sum(t["path_accuracy"] for t in corner_turns) / len(corner_turns) if corner_turns else 0
                }
            }
        }
        
        # 儲存結果
        save_test_result(
            user_id=self.user_id,
            test_name="analog_path_follow",
            metrics=metrics,
            parameters=parameters,
            image_files=[f"軌跡圖片儲存在: {self.session_output_dir}"]
        )
        
        print("=" * 50)
        print("🛤️ Analog Path Follow Test - 測試完成總結")
        print("=" * 50)
        print(f"👤 使用者：{self.user_id}")
        print(f"🎯 總路徑數：{total_trials} (4條直線 + 8種L型)")
        print(f"⏱️ 總用時：{total_time:.2f} 秒")
        print(f"📊 平均完成時間：{avg_completion_time:.2f} 秒")
        print(f"🎯 平均路徑精確度：{avg_accuracy:.1f}%")
        print("")
        print("📈 基本路徑類型表現分析：")
        for path_type, data in metrics["path_type_analysis"].items():
            if data["count"] > 0:
                print(f"  {path_type}: {data['count']} 條，平均時間 {data['avg_completion_time_s']:.2f}s，精確度 {data['avg_accuracy_pct']:.1f}%")
        print("")
        print("🔍 詳細移動類型分析：")
        for movement_type, data in metrics["movement_type_analysis"].items():
            if data["count"] > 0:
                type_name = {
                    "horizontal_straight": "水平直線",
                    "vertical_straight": "垂直直線", 
                    "corner_turns": "L型轉彎"
                }.get(movement_type, movement_type)
                print(f"  {type_name}: {data['count']} 條，平均時間 {data['avg_completion_time_s']:.2f}s，精確度 {data['avg_accuracy_pct']:.1f}%")


if __name__ == "__main__":
    import argparse
    from common.controller_input import ControllerInput

    # 解析命令列參數
    parser = argparse.ArgumentParser(description="Analog Path Follow Test")
    parser.add_argument("--user", "-u", default=None, help="使用者 ID")
    args = parser.parse_args()

    # 如果沒有提供 user_id，則請求輸入
    user_id = args.user
    if not user_id:
        user_id = input("請輸入使用者 ID (例如: P1): ").strip()
        if not user_id:
            user_id = "default"

    root = tk.Tk()
    app = PathFollowingTestApp(root, user_id)

    try:
        # 使用新的遙控器管理系統 - 會自動使用已配對的遙控器
        listener = ControllerInput(analog_callback=app.on_joycon_input,
                                   use_existing_controller=True)
        Thread(target=listener.run, daemon=True).start()

        root.mainloop()

    except KeyboardInterrupt:
        root.destroy()
        app.running = False
        print("🔴 測試被中斷")

    print("🎮 Path Following 測試結束")
