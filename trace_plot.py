# trace_plot.py

import os
import time
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Rectangle
from matplotlib.lines import Line2D


def output_single_trace(path_obj, index, output_dir="trace_output"):
    """輸出單一路徑圖：含黑路徑、灰框、紅線、玩家軌跡"""

    trace_list = path_obj.player_trace
    if not trace_list:
        print(f"⚠️ 路徑 {index} 無軌跡資料")
        return

    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"{index}.png")

    fig, ax = plt.subplots(figsize=(8, 4))

    # ✅ 黑色背景路徑（完整長度，不收縮）
    if hasattr(path_obj, "_calculate_path_points"):
        original_len = path_obj.current_length
        path_obj.current_length = path_obj.path_length  # 暫時還原完整長度
        path_points = path_obj._calculate_path_points()
        path_obj.current_length = original_len  # 還原回來

        polygon = Polygon([[path_points[i], path_points[i + 1]]
                           for i in range(0, 8, 2)],
                          closed=True,
                          facecolor="black")
        ax.add_patch(polygon)

    # ✅ 灰色區塊（未被清除的）
    for cp in path_obj.checkpoints:
        x1, y1, x2, y2 = cp["area"]
        rect = Rectangle((x1, y1),
                         x2 - x1,
                         y2 - y1,
                         linewidth=2,
                         edgecolor='gray',
                         facecolor='none')
        ax.add_patch(rect)

        # ✅ 紅色封鎖線
        axis = cp["axis"]
        pos = cp["line_pos"]
        if axis == "x":
            ax.add_line(Line2D([pos, pos], [y1, y2], color='red', linewidth=2))
        else:
            ax.add_line(Line2D([x1, x2], [pos, pos], color='red', linewidth=2))

    # ✅ 藍色玩家軌跡點
    xs, ys = zip(*trace_list)
    ax.plot(xs, ys, 'deepskyblue', marker='.', linestyle='None', markersize=3)

    # ✅ 紅色目標區塊
    goal_area = path_obj.get_goal_area()
    if 'points' in goal_area:
        goal_pts = goal_area['points']
        polygon = Polygon([[goal_pts[i], goal_pts[i + 1]]
                           for i in range(0, 8, 2)],
                          closed=True,
                          facecolor='red')
        ax.add_patch(polygon)
    else:
        rect = Rectangle((goal_area['left'], goal_area['top']),
                         goal_area['right'] - goal_area['left'],
                         goal_area['bottom'] - goal_area['top'],
                         facecolor='red')
        ax.add_patch(rect)

    # ✅ 起點圓形
    start_x, start_y = trace_list[0]
    ax.plot(start_x,
            start_y,
            'o',
            color='deepskyblue',
            markersize=10,
            alpha=0.7)

    # 顯示設定
    ax.set_aspect('equal')
    ax.invert_yaxis()
    ax.axis('off')
    ax.set_title(f"Path {index}")
    plt.tight_layout()
    plt.savefig(output_path, dpi=200)
    plt.close()
    print(f"📷 已儲存路徑 {index} 軌跡圖：{output_path}")
