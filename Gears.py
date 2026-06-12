from manim import *
from manim_gearbox import *
import numpy as np

class Gears(Scene):
    def BeltFunction(self, t):
        x = 0.0
        y = 0.0
        t = t % 131
        if t >= 0.0 and t < 25.0:
            x = t * 9.0 / 50.0 - 2.0
            y = 1.5 - t / 50.0
        if t >= 25.0 and t < 56.0:
            x = np.sin((t - 25.0)/10.0) + 2.5
            y = np.cos((t - 25.0)/10.0)
        if t >= 56.0 and t < 81.0:
            x = 2.5 - 9 * (t - 56.0) / 50.0
            y = -1.0 - (t - 56.0) / 50.0
        if t >= 81.0 and t <= 130.0:
            x = -1.5 * np.sin((t - 81.0)/15.0) - 2
            y = -1.5 * np.cos((t - 81.0)/15.0)
        return (x, y, 0)
    
    def BeltFunctionX(self, t):
        value, _, _ = self.BeltFunction(t)
        return value
    
    def BeltFunctionY(self, t):
        _, value, _ = self.BeltFunction(t)
        return value
    
    def BeltDerivativeParametric(self, t):
        if 0.0 <= t < 25.0:
            dxdt = 9.0 / 50.0
            dydt = -1.0 / 50.0
        if 25.0 <= t < 56.0:
            u = (t - 25.0) / 10.0
            dxdt = 0.1 * np.cos(u)
            dydt = -0.1 * np.sin(u)
        if 56.0 <= t < 81.0:
            dxdt = -9.0 / 50.0
            dydt = -1.0 / 50.0
        if 81.0 <= t <= 130.0:
            v = (t - 81.0) / 15.0
            dxdt = -0.1 * np.cos(v)
            dydt = 0.1 * np.sin(v)
        return (dxdt, dydt, 0.0)

    def BeltDerivativeAngle(self, t):
        dxdt, dydt, _ = self.BeltDerivativeParametric(t)
        angle = np.arctan2(dydt, dxdt)
        return angle

    def construct(self):
        gear1 = Gear(15)
        gear2 = Gear(10)

        self.play(Create(gear1))
        self.play(Rotate(gear1, angle=PI, run_time=2))
        self.wait(8)

        self.play(gear1.animate.shift(-gear1.rp * 1 * RIGHT))
        gear2.mesh_to(gear1)
        self.play(Create(gear2))
        self.wait(8)

        self.play(Rotate(gear1, gear1.pitch_angle * 5), Rotate(gear2, - gear2.pitch_angle * 5), run_time=2)
        self.play(Rotate(gear1, - gear1.pitch_angle * 5), Rotate(gear2, gear2.pitch_angle * 5), run_time=2)
        self.wait(8)

        self.play(gear2.animate.shift(RIGHT * 1.5), gear1.animate.shift(LEFT * 0.5))
        beltFunction = ParametricFunction(self.BeltFunction, t_range= (0, 129), fill_opacity=0, stroke_width=50).set_color(TEAL_C)
        self.play(Create(beltFunction, run_time=2))
        self.play(beltFunction.animate.set_stroke(opacity=0.5))
        self.wait(8)

        self.play(Rotate(gear1, gear1.pitch_angle * 5, rate_func=rate_functions.ease_in_out_quint), Rotate(gear2, gear2.pitch_angle * 5, rate_func=rate_functions.ease_in_out_quint), run_time=2)
        self.play(Rotate(gear1, gear1.pitch_angle * 150, rate_func=linear), Rotate(gear2, gear2.pitch_angle * 150, rate_func=linear), run_time=60)