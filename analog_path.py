import tkinter as tk
import time
import math
from threading import Thread
from abc import ABC, abstractmethod


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

        self.create_path()

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
        """檢查點是否在直線路徑內"""
        if self.path_length == 0:
            distance = math.sqrt((x - self.start_x)**2 + (y - self.start_y)**2)
            return distance <= self.width / 2

        # 計算當前起點位置（因為從終點收縮回來）
        ratio = self.current_length / self.path_length
        current_start_x = self.end_x - self.dx * ratio
        current_start_y = self.end_y - self.dy * ratio

        # 計算當前線段方向
        current_dx = self.end_x - current_start_x
        current_dy = self.end_y - current_start_y
        current_length_sq = current_dx**2 + current_dy**2

        if current_length_sq == 0:
            return False

        # 投影
        dx = x - current_start_x
        dy = y - current_start_y
        t = (dx * current_dx + dy * current_dy) / current_length_sq
        t = max(0, min(1, t))

        # 最近點
        nearest_x = current_start_x + t * current_dx
        nearest_y = current_start_y + t * current_dy

        # 距離
        distance = math.sqrt((x - nearest_x)**2 + (y - nearest_y)**2)
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

        self.create_path()

    def create_path(self):
        """創建轉彎路徑"""
        # 創建第一段（起點到轉彎點）
        self.segment1 = self._create_segment(self.start_x, self.start_y,
                                             self.corner_x + (self.width / 2),
                                             self.corner_y)

        # 創建第二段（轉彎點到終點）
        self.segment2 = self._create_segment(self.corner_x, self.corner_y,
                                             self.end_x, self.end_y)

        if self.segment1:
            self.path_elements.append(self.segment1)
        if self.segment2:
            self.path_elements.append(self.segment2)

    def _create_segment(self, x1, y1, x2, y2):
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

        return self.canvas.create_polygon(points,
                                          fill=self.color,
                                          outline=self.color)

    def is_inside(self, x, y):
        """檢查點是否在轉彎路徑內"""
        # 檢查是否在第一段路徑內
        if self._point_in_segment(x, y, self.start_x, self.start_y,
                                  self.corner_x, self.corner_y):
            return True

        # 檢查是否在第二段路徑內
        if self._point_in_segment(x, y, self.corner_x, self.corner_y,
                                  self.end_x, self.end_y):
            return True

        return False

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

    def shrink(self):
        """收縮轉彎路徑"""
        if self.current_progress > 0:
            self.current_progress = max(
                0,
                self.current_progress - self.shrink_speed / self.total_length)
            self._update_path()

    def _update_path(self):
        """根據當前進度更新路徑"""
        # 計算當前應該顯示的路徑長度
        current_length = self.total_length * self.current_progress

        if current_length <= 0:
            # 隱藏所有路徑元素
            for element in self.path_elements:
                self.canvas.coords(element, 0, 0, 0, 0)
            return

        if current_length >= self.segment1_length:
            # 顯示完整的第一段
            if self.segment1:
                segment1_points = self._create_segment_points(
                    self.start_x, self.start_y, self.corner_x, self.corner_y)
                self.canvas.coords(self.segment1, *segment1_points)

            # 顯示部分第二段
            remaining_length = current_length - self.segment1_length
            ratio = remaining_length / self.segment2_length

            end_x = self.corner_x + (self.end_x - self.corner_x) * ratio
            end_y = self.corner_y + (self.end_y - self.corner_y) * ratio

            if self.segment2:
                segment2_points = self._create_segment_points(
                    self.corner_x, self.corner_y, end_x, end_y)
                self.canvas.coords(self.segment2, *segment2_points)
        else:
            # 只顯示部分第一段
            ratio = current_length / self.segment1_length
            end_x = self.start_x + (self.corner_x - self.start_x) * ratio
            end_y = self.start_y + (self.corner_y - self.start_y) * ratio

            if self.segment1:
                segment1_points = self._create_segment_points(
                    self.start_x, self.start_y, end_x, end_y)
                self.canvas.coords(self.segment1, *segment1_points)

            # 隱藏第二段
            if self.segment2:
                self.canvas.coords(self.segment2, 0, 0, 0, 0)

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

    def __init__(self, root):
        self.root = root
        self.root.title("🎮 Path Following 測試")
        self.canvas_width = 1200
        self.canvas_height = 800
        self.canvas = tk.Canvas(root,
                                width=self.canvas_width,
                                height=self.canvas_height,
                                bg='white')
        self.canvas.pack()

        self.player_radius = 8
        self.goal_color = "red"

        self.player_x = 100
        self.player_y = 400
        self.leftX = 0
        self.leftY = 0
        self.speed = 13

        self.off_path_time = 0
        self.total_time = 0
        self.start_time = None
        self.running = False
        self.reached_goal = False

        # 創建路徑（可以選擇不同類型的路徑）
        self.setup_path()
        self.setup_goal()
        self.setup_player()

        Thread(target=self.player_loop, daemon=True).start()

    def setup_path(self):
        """設置路徑，可以選擇不同類型"""
        # 選擇路徑類型
        path_type = "straight"  # 可改為 "corner" 來測試轉彎路徑

        if path_type == "straight":
            # 直線路徑
            self.path = StraightPath(self.canvas,
                                     start_x=50,
                                     start_y=400,
                                     end_x=self.canvas_width - 50,
                                     end_y=400,
                                     width=80)
        elif path_type == "corner":
            # 轉彎路徑
            self.path = CornerPath(self.canvas,
                                   start_x=50,
                                   start_y=400,
                                   corner_x=600,
                                   corner_y=400,
                                   end_x=600,
                                   end_y=200,
                                   width=80)

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

    def setup_player(self):
        """設置玩家"""
        self.player = self.canvas.create_oval(
            self.player_x - self.player_radius,
            self.player_y - self.player_radius,
            self.player_x + self.player_radius,
            self.player_y + self.player_radius,
            fill="skyblue")

    def player_loop(self):
        while True:
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
                    min(self.canvas_height - self.player_radius,
                        self.player_y))

                self.canvas.coords(self.player,
                                   self.player_x - self.player_radius,
                                   self.player_y - self.player_radius,
                                   self.player_x + self.player_radius,
                                   self.player_y + self.player_radius)

                self.path.shrink()

                now = time.time()
                if self.start_time is None:
                    self.start_time = now

                self.total_time += 0.016
                if not self.path.is_inside(self.player_x, self.player_y):
                    self.off_path_time += 0.016

                # 檢查是否到達目標（簡化版，可以根據路徑類型調整）
                if self.check_reached_goal():
                    self.reached_goal = True
                    self.show_result()

            time.sleep(0.016)

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
        if not self.running:
            self.running = True
            print("✅ 開始測試！請沿著路徑前進")


if __name__ == "__main__":
    from controller_input import ControllerInput

    root = tk.Tk()
    app = PathFollowingTestApp(root)

    listener = ControllerInput(analog_callback=app.on_joycon_input)
    Thread(target=listener.run, daemon=True).start()

    root.mainloop()

    print("🎮 Path Following 測試結束")
