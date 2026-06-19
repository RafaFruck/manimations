from manim import *
from manim_gearbox import *
from manim_play_timeline import play_timeline
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
    
    def BeltFunctionArray(self, t):
        x, y, z = self.BeltFunction(t)
        return [x, y, z]
    
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
    
    def create_arrow_at_angle(self, start_point, length, angle_in_rad, color=RED):
        start = np.array(start_point, dtype=float)
        # Ensure length is a numeric scalar
        if not isinstance(length, (int, float, np.number)):
            raise TypeError(f"length must be a number, got {type(length).__name__}")
        length = float(length)
        end = start + np.array([
            length * np.cos(angle_in_rad),
            length * np.sin(angle_in_rad),
            0.0
        ])
        return Arrow(start=start, end=end, color=color, stroke_width=12)


    def construct(self):
        gear1 = Gear(15)
        gear2 = Gear(10)

        self.play(Create(gear1))
        self.play(Rotate(gear1, angle=PI, run_time=2))
        self.wait()

        self.play(gear1.animate.shift(-gear1.rp * 1 * RIGHT))
        gear2.mesh_to(gear1)
        self.play(Create(gear2))
        self.wait()

        self.play(Rotate(gear1, gear1.pitch_angle * 5), Rotate(gear2, - gear2.pitch_angle * 5), run_time=2)
        self.play(Rotate(gear1, - gear1.pitch_angle * 5), Rotate(gear2, gear2.pitch_angle * 5), run_time=2)
        self.wait()

        self.play(gear2.animate.shift(RIGHT * 1.5), gear1.animate.shift(LEFT * 0.5))
        beltFunction = ParametricFunction(self.BeltFunction, t_range= (0, 129), fill_opacity=0, stroke_width=50).set_color(TEAL_C)
        self.play(Create(beltFunction, run_time=2))
        self.play(beltFunction.animate.set_stroke(opacity=0.5))
        self.wait()
        self.add(NumberPlane())
        
        arrow0 = self.create_arrow_at_angle(self.BeltFunctionArray(105.5), 1.5, self.BeltDerivativeAngle(105.5))
        arrow1 = self.create_arrow_at_angle(self.BeltFunctionArray(11.1), 1.5, self.BeltDerivativeAngle(11.1))
        arrow2 = self.create_arrow_at_angle(self.BeltFunctionArray(67.1), 1.5, self.BeltDerivativeAngle(67.1))
        arrow3 = self.create_arrow_at_angle(self.BeltFunctionArray(46), 1.5, self.BeltDerivativeAngle(46))
        '''v0 = MathTex(r"\vec{v}", color=RED)
        v1 = MathTex(r"\vec{v}", color=RED)
        v2 = MathTex(r"\vec{v}", color=RED)
        v3 = MathTex(r"\vec{v}", color=RED)'''
        v0 = Text("v⃗", color=RED)
        v1 = Text("v⃗", color=RED)
        v2 = Text("v⃗", color=RED)
        v3 = Text("v⃗", color=RED)
        v0.move_to([-4, 0.8, 0])
        v1.move_to([0.7, 1.5, 0])
        v2.move_to([-0.5, -2, 0])
        v3.move_to([3.4, -1.4, 0])
        #circArrow0 = CurvedArrow()
        w0 = Text("w⃗", color=GREEN)
        self.play(Rotate(gear1, gear1.pitch_angle * 5, rate_func=rate_functions.ease_in_out_quint), Rotate(gear2, gear2.pitch_angle * 5, rate_func=rate_functions.ease_in_out_quint), run_time=2)
        timeline = {
        0.0: [
            Rotate(gear1, gear1.pitch_angle * -150, rate_func=linear, run_time=60),
            Rotate(gear2, gear2.pitch_angle * -150, rate_func=linear, run_time=60),
            Create(arrow0, run_time=1),
            Create(v0, run_time=1),
        ],
        0.3: [
            Create(arrow1, run_time=1),
            Create(v1, run_time=1),
        ],
        0.6: [
            Create(arrow2, run_time=1),
            Create(v2, run_time=1),
        ],
        0.9: [
            Create(arrow3, run_time=1),
            Create(v3, run_time=1),
        ],

        }
        play_timeline(self, timeline)