"""
路徑追蹤測試 (障礙物版本)
- 包含藍色區域和紅線障礙物功能
- 路徑收縮功能已禁用
- 玩家需要按按鈕解除障礙物才能繼續前進
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
from common.utils import get_directional_offset
from common.trace_plot import output_single_trace

DEBUG = False


class Path(ABC):
    """抽象路徑基類"""

    def __init__(self, canvas, width, color="black"):
        self.canvas = canvas
        self.width = width
        self.color = color
        self.path_elements = []  # 儲存路徑的圖形元素
        self.shrink_speed = 3
        self.is_active = True

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

        self.checkpoints = []  # 每個 checkpoint 含藍色區、紅線、範圍座標、狀態
        self.checkpoint_positions = [0.3, 0.6]
        self.trigger_width = 50

        # 玩家軌跡
        self.player_trace = []

    def get_path_shapes(self):
        """回傳完整未收縮的直線路徑多邊形點位"""
        original_length = self.current_length
        self.current_length = self.path_length  # 暫時還原成完整長度
        points = self._calculate_path_points()
        self.current_length = original_length  # 還原
        return [[(points[i], points[i + 1]) for i in range(0, 8, 2)]]

    def create_path(self):
        """創建直線路徑與藍區＋紅線檢查點（方向適應）"""
        if self.path_length > 0:
            points = self._calculate_path_points()
            self.path_rect = self.canvas.create_polygon(points,
                                                        fill=self.color,
                                                        outline=self.color)
        else:
            half_width = self.width // 2
            self.path_rect = self.canvas.create_oval(self.start_x - half_width,
                                                     self.start_y - half_width,
                                                     self.start_x + half_width,
                                                     self.start_y + half_width,
                                                     fill=self.color,
                                                     outline=self.color)

        self.path_elements.append(self.path_rect)

        # 準備藍色區域與紅線
        self.checkpoints = []
        trigger_half_length = self.trigger_width / 2
        trigger_half_width = self.width / 2

        # 單位向量
        ux = self.dx / self.path_length
        uy = self.dy / self.path_length
        perp_x = -uy
        perp_y = ux

        for pos in self.checkpoint_positions:
            # 中心點
            cx = self.start_x + self.dx * pos
            cy = self.start_y + self.dy * pos

            # 四個角
            p1x = cx - ux * trigger_half_length + perp_x * trigger_half_width
            p1y = cy - uy * trigger_half_length + perp_y * trigger_half_width
            p2x = cx + ux * trigger_half_length + perp_x * trigger_half_width
            p2y = cy + uy * trigger_half_length + perp_y * trigger_half_width
            p3x = cx + ux * trigger_half_length - perp_x * trigger_half_width
            p3y = cy + uy * trigger_half_length - perp_y * trigger_half_width
            p4x = cx - ux * trigger_half_length - perp_x * trigger_half_width
            p4y = cy - uy * trigger_half_length - perp_y * trigger_half_width

            # 藍色按鈕觸發區域
            rect_id = self.canvas.create_polygon(p1x,
                                                 p1y,
                                                 p2x,
                                                 p2y,
                                                 p3x,
                                                 p3y,
                                                 p4x,
                                                 p4y,
                                                 fill="lightblue",
                                                 outline="blue",
                                                 width=3)

            # 紅線：畫在區塊前端（從 cx + dx * 半長）
            # 找出紅線兩端：與區域前緣重合
            front_cx = cx + ux * trigger_half_length
            front_cy = cy + uy * trigger_half_length
            line_half = trigger_half_width

            lx1 = front_cx + perp_x * line_half
            ly1 = front_cy + perp_y * line_half
            lx2 = front_cx - perp_x * line_half
            ly2 = front_cy - perp_y * line_half

            red_line_id = self.canvas.create_line(lx1,
                                                  ly1,
                                                  lx2,
                                                  ly2,
                                                  fill="red",
                                                  width=3)

            # 判斷封鎖方向：用主軸最大值來決定
            axis = "x" if abs(self.dx) >= abs(self.dy) else "y"
            line_pos = front_cx if axis == "x" else front_cy

            self.path_elements.extend([rect_id, red_line_id])
            self.checkpoints.append({
                "rect_id":
                rect_id,
                "line_id":
                red_line_id,
                "area": (min(p1x, p2x, p3x, p4x), min(p1y, p2y, p3y, p4y),
                         max(p1x, p2x, p3x, p4x), max(p1y, p2y, p3y, p4y)),
                "cleared":
                False,
                "line_pos":
                line_pos,
                "axis":
                axis
            })

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
        """檢查點是否在完整路徑內 (不考慮收縮)"""
        if self.path_length == 0:
            distance = math.hypot(x - self.start_x, y - self.start_y)
            return distance <= self.width / 2

        # 使用完整路徑 start → end 進行檢查
        dx = x - self.start_x
        dy = y - self.start_y

        segment_dx = self.end_x - self.start_x
        segment_dy = self.end_y - self.start_y
        segment_len_sq = segment_dx**2 + segment_dy**2

        if segment_len_sq == 0:
            return False

        # 投影參數 t：投影在 segment 上的相對位置（0~1）
        t = (dx * segment_dx + dy * segment_dy) / segment_len_sq

        # 超出路徑範圍
        if t < 0 or t > 1:
            return False

        # 找到投影點
        nearest_x = self.start_x + t * segment_dx
        nearest_y = self.start_y + t * segment_dy

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


class PathFollowingTestApp:

    def __init__(self, root, user_id=None):
        self.root = root
        self.user_id = user_id or "default"
        self.root.title("🎮 Path Following 測試 (障礙物版本)")
        self.canvas_width = config.WINDOW_WIDTH
        self.canvas_height = config.WINDOW_HEIGHT
        background_color = f"#{config.COLORS['BACKGROUND'][0]:02x}{config.COLORS['BACKGROUND'][1]:02x}{config.COLORS['BACKGROUND'][2]:02x}"
        self.canvas = tk.Canvas(root,
                                width=self.canvas_width,
                                height=self.canvas_height,
                                bg=background_color)
        self.canvas.pack()

        self.player_radius = 8
        self.goal_color = f"#{config.COLORS['TARGET'][0]:02x}{config.COLORS['TARGET'][1]:02x}{config.COLORS['TARGET'][2]:02x}"

        self.player_trace = []

        self.player_x = 100
        self.player_y = 400
        self.offset = 20
        self.leftX = 0
        self.leftY = 0
        self.speed = 13

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
        self.session_output_dir = os.path.join("data", "images", "analog_path_obstacle_trace", self.user_id, timestamp)
        os.makedirs(self.session_output_dir, exist_ok=True)

    def create_paths(self):
        """回傳多條路徑清單"""
        path_color = f"#{config.COLORS['PATH'][0]:02x}{config.COLORS['PATH'][1]:02x}{config.COLORS['PATH'][2]:02x}"
        paths = [
            # ---- 四條直線 ----
            # 從左往右 →
            StraightPath(self.canvas, 50, 400, 1150, 400, 80, path_color),
            # 從右往左 ←
            StraightPath(self.canvas, 1150, 400, 50, 400, 80, path_color),
            # 從上往下 ↓
            StraightPath(self.canvas, 600, 100, 600, 700, 80, path_color),
            # 從下往上 ↑
            StraightPath(self.canvas, 600, 700, 600, 100, 80, path_color),
        ]
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
        dx = self.path.end_x - self.path.start_x
        dy = self.path.end_y - self.path.start_y
        offset_x, offset_y = get_directional_offset(dx, dy, self.offset)
        self.player_x = self.path.start_x + offset_x
        self.player_y = self.path.start_y + offset_y

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

            # 嘗試移動玩家
            next_x = self.player_x + dx
            next_y = self.player_y + dy

            # 紅線封鎖邏輯
            for cp in self.path.checkpoints:
                if not cp["cleared"]:
                    axis = cp["axis"]
                    pos = cp["line_pos"]
                    if axis == "x":
                        if ((self.path.dx > 0 and next_x > pos)
                                or (self.path.dx < 0 and next_x < pos)):
                            next_x = pos
                    elif axis == "y":
                        if ((self.path.dy > 0 and next_y > pos)
                                or (self.path.dy < 0 and next_y < pos)):
                            next_y = pos

            # 邊界限制
            next_x = max(self.player_radius,
                         min(self.canvas_width - self.player_radius, next_x))
            next_y = max(self.player_radius,
                         min(self.canvas_height - self.player_radius, next_y))

            # 更新位置
            self.player_x = next_x
            self.player_y = next_y

            self.canvas.coords(self.player, self.player_x - self.player_radius,
                               self.player_y - self.player_radius,
                               self.player_x + self.player_radius,
                               self.player_y + self.player_radius)
            self.canvas.tag_raise(self.player)

            # 顏色：判斷是否在路徑內
            if DEBUG:
                primary_color = f"#{config.COLORS['PRIMARY'][0]:02x}{config.COLORS['PRIMARY'][1]:02x}{config.COLORS['PRIMARY'][2]:02x}"
                error_color = f"#{config.COLORS['ERROR'][0]:02x}{config.COLORS['ERROR'][1]:02x}{config.COLORS['ERROR'][2]:02x}"
                if self.path.is_inside(self.player_x, self.player_y):
                    self.canvas.itemconfig(self.player, fill=primary_color)
                else:
                    self.canvas.itemconfig(self.player, fill=error_color)

            # 路徑收縮功能 (已禁用)
            # self.path.shrink()

            # 時間紀錄
            now = time.time()
            if self.start_time is None:
                self.start_time = now
            self.total_time += 0.016
            if not self.path.is_inside(self.player_x, self.player_y):
                self.off_path_time += 0.016

            # 紀錄玩家軌跡
            self.path.player_trace.append((self.player_x, self.player_y))

            # 判斷是否到達終點
            if self.check_reached_goal():
                self.reached_goal = True
                self.show_result()
                self.root.after(1000, self.advance_path)
                return

        # 持續呼叫
        self.root.after(16, self.player_loop)

    def advance_path(self):
        # 儲存目前這段路徑的軌跡
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

    def show_result(self):
        percent_off = (self.off_path_time / self.total_time) * 100
        
        # 記錄單次路徑測試結果
        path_type = "straight" if isinstance(self.path, StraightPath) else "corner"
        path_info = {
            "start_x": self.path.start_x,
            "start_y": self.path.start_y,
            "end_x": self.path.end_x,
            "end_y": self.path.end_y
        }
        
        if hasattr(self.path, 'corner_x'):  # CornerPath
            path_info["corner_x"] = self.path.corner_x
            path_info["corner_y"] = self.path.corner_y
            if hasattr(self.path, 'total_length'):
                path_info["total_length"] = self.path.total_length
        else:  # StraightPath
            if hasattr(self.path, 'path_length'):
                path_info["path_length"] = self.path.path_length
        
        trial_result = {
            "trial_number": self.current_path_index + 1,
            "path_type": path_type,
            "path_info": path_info,
            "completion_time_seconds": self.total_time,
            "off_path_time_seconds": self.off_path_time,
            "off_path_percentage": percent_off,
            "path_accuracy": 100 - percent_off,
            "trace_points_count": len(self.path.player_trace) if hasattr(self.path, 'player_trace') else 0
        }
        self.test_results.append(trial_result)
        
        print("🎯 到達終點")
        print(f"⏱ 總時間：{self.total_time:.2f} 秒")
        print(f"❌ 偏離路徑時間：{self.off_path_time:.2f} 秒")
        print(f"📊 偏離比例：{percent_off:.2f}%")

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
        
        # 準備儲存的測試參數
        parameters = {
            "window_size": {
                "width": self.canvas_width,
                "height": self.canvas_height
            },
            "player_radius": self.player_radius,
            "movement_speed_multiplier": self.speed,
            "total_paths": len(self.paths),
            "path_width": 80,  # 固定路徑寬度
            "player_offset": self.offset,
            "test_variant": "obstacle_full"  # 完整障礙物版本
        }
        
        # 準備儲存的指標數據
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
            }
        }
        
        # 儲存結果
        save_test_result(
            user_id=self.user_id,
            test_name="analog_path_obstacle",
            metrics=metrics,
            parameters=parameters,
            image_files=[f"軌跡圖片儲存在: {self.session_output_dir}"]
        )
        
        print("=" * 50)
        print("🚧 Analog Path Obstacle Test - 測試完成總結")
        print("=" * 50)
        print(f"👤 使用者：{self.user_id}")
        print(f"🎯 總路徑數：{total_trials}")
        print(f"⏱️ 總用時：{total_time:.2f} 秒")
        print(f"📊 平均完成時間：{avg_completion_time:.2f} 秒")
        print(f"🎯 平均路徑精確度：{avg_accuracy:.1f}%")
        print("")
        print("📈 各路徑類型表現分析：")
        for path_type, data in metrics["path_type_analysis"].items():
            if data["count"] > 0:
                print(f"  {path_type}: {data['count']} 條，平均時間 {data['avg_completion_time_s']:.2f}s，精確度 {data['avg_accuracy_pct']:.1f}%")
        print("=" * 50)

    def on_joycon_button(self, buttons, leftX, leftY, last_key_bit,
                         last_key_down):
        if not last_key_down:
            return

        for cp in self.path.checkpoints:
            if not cp["cleared"]:
                x1, y1, x2, y2 = cp["area"]
                if x1 <= self.player_x <= x2 and y1 <= self.player_y <= y2:
                    cp["cleared"] = True
                    self.canvas.delete(cp["line_id"])
                    self.canvas.delete(cp["rect_id"])
                    print("🟢 檢查點解除：藍色區域與紅線已移除")


if __name__ == "__main__":
    import argparse
    from common.controller_input import ControllerInput

    # 解析命令列參數
    parser = argparse.ArgumentParser(description="Analog Path Obstacle Test")
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
        # 恢復按鈕回調以支持障礙物解除功能
        listener = ControllerInput(analog_callback=app.on_joycon_input,
                                  button_callback=app.on_joycon_button)
        Thread(target=listener.run, daemon=True).start()

        root.mainloop()

    except KeyboardInterrupt:
        root.destroy()
        app.running = False
        print("🔴 測試被中斷")

    print("🎮 Path Following 測試結束")
