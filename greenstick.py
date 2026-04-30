# greenstick.py
import numpy as np
from scipy.integrate import solve_ivp
from manimlib import *

# 向量场 (除去原点)
def vortex_field(x, y):
    r2 = x*x + y*y
    if r2 < 1e-6:
        return np.array([0.0, 0.0])
    inv_r2 = 1.0 / r2
    return np.array([-y * inv_r2, x * inv_r2])

# 刚体木棍模拟类
class RigidRod:
    def __init__(self, center, angle, length, mass=1.0):
        self.center = np.array(center, dtype=float)
        self.angle = angle
        self.length = length
        self.mass = mass
        self.inertia = (1.0/12.0) * mass * length * length
        self.velocity = np.zeros(2)
        self.omega = 0.0

    def endpoints(self):
        half = 0.5 * self.length
        dir_vec = np.array([np.cos(self.angle), np.sin(self.angle)])
        return self.center + half*dir_vec, self.center - half*dir_vec

    def compute_force_torque(self, field_func, n_samples=21):
        t_vals = np.linspace(-0.5, 0.5, n_samples)
        dir_vec = np.array([np.cos(self.angle), np.sin(self.angle)])
        total_force = np.zeros(2)
        total_torque = 0.0
        for t in t_vals:
            pos = self.center + t * self.length * dir_vec
            f = field_func(pos[0], pos[1])
            dm = self.mass / n_samples
            total_force += f * dm
            lever = t * self.length
            torque = lever * (dir_vec[0]*f[1] - dir_vec[1]*f[0])
            total_torque += torque * dm
        return total_force, total_torque

def rod_ode(t, state, rod, field_func):
    x, y, vx, vy, angle, omega = state
    rod.center = np.array([x, y])
    rod.angle = angle
    rod.velocity = np.array([vx, vy])
    rod.omega = omega
    F, tau = rod.compute_force_torque(field_func, n_samples=31)
    ax = F[0] / rod.mass
    ay = F[1] / rod.mass
    alpha = tau / rod.inertia
    return [vx, vy, ax, ay, omega, alpha]

# ------------------------------------------------------------
class RodInVortexField(Scene):
    def construct(self):
        # 坐标系
        axes = NumberPlane(
            x_range=[-3, 3],
            y_range=[-3, 3],
            axis_config={"stroke_width": 2, "include_numbers": True}
        )
        self.add(axes)

        # 向量场 (需要传入 coordinate_system)
        def field_func_for_plot(pos):
            # pos 是 (n, 3) 数组
            x, y = pos[:, 0], pos[:, 1]
            r2 = x*x + y*y
            mask = r2 < 0.2
            inv_r2 = np.where(mask, 0.0, 1.0 / np.where(r2 == 0, 1, r2))  # 避免除零
            vx = np.where(mask, 0.0, -y * inv_r2)
            vy = np.where(mask, 0.0, x * inv_r2)
            vz = np.zeros_like(vx)
            return np.column_stack([vx, vy, vz])

        vector_field = VectorField(
            field_func_for_plot,
            coordinate_system=axes,          # 关键修复
            max_vect_len=0.2,
            color=BLUE_D,
            opacity=0.6
        )
        self.add(vector_field)

        # 奇点
        origin_dot = Dot(axes.c2p(0,0), color=RED, radius=0.1)
        origin_label = Text("奇点", font_size=20).next_to(origin_dot, UR)
        self.add(origin_dot, origin_label)

        # 初始化木棍
        rod = RigidRod(center=[2.0, 0.0], angle=0.0, length=0.8, mass=1.0)

        # 模拟
        T_max = 20.0
        dt_eval = 0.05
        t_eval = np.arange(0, T_max, dt_eval)
        state0 = [rod.center[0], rod.center[1],
                  rod.velocity[0], rod.velocity[1],
                  rod.angle, rod.omega]

        sol = solve_ivp(
            rod_ode,
            t_span=(0, T_max),
            y0=state0,
            t_eval=t_eval,
            args=(rod, vortex_field),
            method='RK45',
            rtol=1e-6,
            atol=1e-8
        )

        xs, ys, angles = sol.y[0], sol.y[1], sol.y[4]

        # 创建木棍视觉对象
        def make_rod_mobject(x, y, angle):
            dir_vec = np.array([np.cos(angle), np.sin(angle)])
            half = 0.5 * rod.length
            p1 = axes.c2p(x + half*dir_vec[0], y + half*dir_vec[1])
            p2 = axes.c2p(x - half*dir_vec[0], y - half*dir_vec[1])
            return Line(p1, p2, stroke_width=8, color=GREEN_E)

        rod_mobject = make_rod_mobject(xs[0], ys[0], angles[0])
        self.add(rod_mobject)

        # 轨迹点 (手动实现)
        trace = VMobject(stroke_color=YELLOW, stroke_width=2)
        trace.set_points_as_corners([axes.c2p(xs[0], ys[0])])
        self.add(trace)

        # 更新器
        time_tracker = ValueTracker(0)
        time_tracker.add_updater(lambda m, dt: m.increment_value(dt))
        
        def update_rod_and_trace():
            t = time_tracker.get_value()
            i = int(t / dt_eval)
            i = min(i, len(xs)-1)
            x, y, ang = xs[i], ys[i], angles[i]

            # 更新木棍
            new_rod = make_rod_mobject(x, y, ang)
            rod_mobject.become(new_rod)

            # 更新轨迹
            current_points = trace.get_points()
            new_point = axes.c2p(x, y)
            # 如果距离上一个点足够远才添加，避免过于密集
            if len(current_points) == 0 or np.linalg.norm(new_point - current_points[-1]) > 0.02:
                current_points = np.append(current_points, [new_point], axis=0)
                trace.set_points_as_corners(current_points)

        # ManimGL 可能没有 add_updater，使用 always_redraw 或手动动画
        rod_mobject.add_updater(lambda mob, dt: update_rod_and_trace())
        trace.add_updater(lambda mob, dt: update_rod_and_trace())

        self.wait(T_max + 0.5)