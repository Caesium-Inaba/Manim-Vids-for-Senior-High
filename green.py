# 格林公式转又转
from manimlib import *

class VectorFieldExample(Scene):
    def construct(self):
        # 定义向量场函数
        def func(p):
            x, y = p[:, 0], p[:, 1]  # p 是 (n, 2) 或 (n, 3)
            r2 = x*x + y*y
            # 避免原点处除以零
            mask = r2 < 0.1
            vx = np.where(mask, 0.0, y / r2)
            vy = np.where(mask, 0.0, -x / r2)
            vz = np.zeros_like(vx)
            return np.column_stack([vx, vy, vz])
        
        # 创建坐标平面
        plane = NumberPlane(
            x_range=[-3, 3, 0.3],
            y_range=[-3, 3, 0.3],
        )
        
        # 创建向量场
        field = VectorField(
            func,
            plane,
            max_vect_len=0.5,  # 限制箭头长度
            color_map_name='viridis',  # 着色
        )
        
        self.add(plane, field)
        self.wait(2)

