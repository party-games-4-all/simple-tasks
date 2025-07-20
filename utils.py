def get_directional_offset(dx, dy, offset):
    """根據主方向決定 offset 應該加在哪一軸"""
    if abs(dx) > abs(dy):
        # 水平為主：偏移 x
        return (offset if dx >= 0 else -offset), 0
    else:
        # 垂直為主：偏移 y
        return 0, (offset if dy >= 0 else -offset)
