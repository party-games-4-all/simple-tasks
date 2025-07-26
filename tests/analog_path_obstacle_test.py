"""
路徑追蹤測試 (障礙物版本) - 簡化版本
- 已禁用灰色區域和紅線障礙物功能以降低複雜度
- 已禁用路徑收縮功能以降低複雜度
- 現在只是基本的路徑追蹤測試
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
from common.utils import get_directional_offset
from data.trace_plot import output_single_trace

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

        self.checkpoints = []  # 每個 checkpoint 含灰色區、紅線、範圍座標、狀態
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
        """創建直線路徑與灰區＋紅線檢查點（方向適應）"""
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

        # 🔒 禁用檢查點創建以降低複雜度
        # 準備灰色區域與紅線
        self.checkpoints = []
        # trigger_half_length = self.trigger_width / 2
        # trigger_half_width = self.width / 2

        # 單位向量
        # ux = self.dx / self.path_length
        # uy = self.dy / self.path_length
        # perp_x = -uy
        # perp_y = ux

        # for pos in self.checkpoint_positions:
        #     # 中心點
        #     cx = self.start_x + self.dx * pos
        #     cy = self.start_y + self.dy * pos

        #     # 四個角
        #     p1x = cx - ux * trigger_half_length + perp_x * trigger_half_width
        #     p1y = cy - uy * trigger_half_length + perp_y * trigger_half_width
        #     p2x = cx + ux * trigger_half_length + perp_x * trigger_half_width
        #     p2y = cy + uy * trigger_half_length + perp_y * trigger_half_width
        #     p3x = cx + ux * trigger_half_length - perp_x * trigger_half_width
        #     p3y = cy + uy * trigger_half_length - perp_y * trigger_half_width
        #     p4x = cx - ux * trigger_half_length - perp_x * trigger_half_width
        #     p4y = cy - uy * trigger_half_length - perp_y * trigger_half_width

        #     # 灰色區域
        #     rect_id = self.canvas.create_polygon(p1x,
        #                                          p1y,
        #                                          p2x,
        #                                          p2y,
        #                                          p3x,
        #                                          p3y,
        #                                          p4x,
        #                                          p4y,
        #                                          fill="",
        #                                          outline="gray",
        #                                          width=5)

        #     # 紅線：畫在區塊前端（從 cx + dx * 半長）
        #     # 找出紅線兩端：與區域前緣重合
        #     front_cx = cx + ux * trigger_half_length
        #     front_cy = cy + uy * trigger_half_length
        #     line_half = trigger_half_width

        #     lx1 = front_cx + perp_x * line_half
        #     ly1 = front_cy + perp_y * line_half
        #     lx2 = front_cx - perp_x * line_half
        #     ly2 = front_cy - perp_y * line_half

        #     red_line_id = self.canvas.create_line(lx1,
        #                                           ly1,
        #                                           lx2,
        #                                           ly2,
        #                                           fill="red",
        #                                           width=3)

        #     # 判斷封鎖方向：用主軸最大值來決定
        #     axis = "x" if abs(self.dx) >= abs(self.dy) else "y"
        #     line_pos = front_cx if axis == "x" else front_cy

        #     self.path_elements.extend([rect_id, red_line_id])
        #     self.checkpoints.append({
        #         "rect_id":
        #         rect_id,
        #         "line_id":
        #         red_line_id,
        #         "area": (min(p1x, p2x, p3x, p4x), min(p1y, p2y, p3y, p4y),
        #                  max(p1x, p2x, p3x, p4x), max(p1y, p2y, p3y, p4y)),
        #         "cleared":
        #         False,
        #         "line_pos":
        #         line_pos,
        #         "axis":
        #         axis
        #     })

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


class PathFollowingTestApp:

    def __init__(self, root, user_id=None):
        self.root = root
        self.user_id = user_id or "default"
        self.root.title("🎮 Path Following 測試 (簡化版本 - 無障礙物)")
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

            # 🟥 禁用紅線封鎖邏輯以降低複雜度
            # for cp in self.path.checkpoints:
            #     if not cp["cleared"]:
            #         axis = cp["axis"]
            #         pos = cp["line_pos"]
            #         if axis == "x":
            #             if ((self.path.dx > 0 and next_x > pos)
            #                     or (self.path.dx < 0 and next_x < pos)):
            #                 next_x = pos
            #         elif axis == "y":
            #             if ((self.path.dy > 0 and next_y > pos)
            #                     or (self.path.dy < 0 and next_y < pos)):
            #                 next_y = pos

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

            # 🔒 禁用路徑收縮功能以降低複雜度
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

    # 🔒 禁用按鈕解鎖功能以降低複雜度
    # def on_joycon_button(self, buttons, leftX, leftY, last_key_bit,
    #                      last_key_down):
    #     if not last_key_down:
    #         return

    #     for cp in self.path.checkpoints:
    #         if not cp["cleared"]:
    #             x1, y1, x2, y2 = cp["area"]
    #             if x1 <= self.player_x <= x2 and y1 <= self.player_y <= y2:
    #                 cp["cleared"] = True
    #                 self.canvas.delete(cp["line_id"])
    #                 self.canvas.delete(cp["rect_id"])
    #                 print("🟢 檢查點解除：灰色區域與紅線已移除")


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
        # 🔒 禁用按鈕回調以降低複雜度
        listener = ControllerInput(analog_callback=app.on_joycon_input)
        # listener = ControllerInput(analog_callback=app.on_joycon_input,
        #                           button_callback=app.on_joycon_button)
        Thread(target=listener.run, daemon=True).start()

        root.mainloop()

    except KeyboardInterrupt:
        root.destroy()
        app.running = False
        print("🔴 測試被中斷")

    print("🎮 Path Following 測試結束")
