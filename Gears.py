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
        
        arrow0 = self.create_arrow_at_angle(self.BeltFunctionArray(105.5), 1.5, self.BeltDerivativeAngle(105.5))
        arrow1 = self.create_arrow_at_angle(self.BeltFunctionArray(11.1), 1.5, self.BeltDerivativeAngle(11.1))
        arrow2 = self.create_arrow_at_angle(self.BeltFunctionArray(67.1), 1.5, self.BeltDerivativeAngle(67.1))
        arrow3 = self.create_arrow_at_angle(self.BeltFunctionArray(46), 1.5, self.BeltDerivativeAngle(46))
        arrow4 = self.create_arrow_at_angle(self.BeltFunctionArray(105.5), 1.5, self.BeltDerivativeAngle(105.5) + PI, color=PURPLE)
        arrow5 = self.create_arrow_at_angle(self.BeltFunctionArray(11.1), 1.5, self.BeltDerivativeAngle(11.1) + PI, color=PURPLE)
        arrow6 = self.create_arrow_at_angle(self.BeltFunctionArray(67.1), 1.5, self.BeltDerivativeAngle(67.1) + PI, color=PURPLE)
        arrow7 = self.create_arrow_at_angle(self.BeltFunctionArray(46), 1.5, self.BeltDerivativeAngle(46) + PI, color=PURPLE)
        v0 = Text("v⃗", color=RED)
        v1 = Text("v⃗", color=RED)
        v2 = Text("v⃗", color=RED)
        v3 = Text("v⃗", color=RED)
        v0.move_to([-4, 0.8, 0])
        v1.move_to([0.7, 1.8, 0])
        v2.move_to([-0.5, -2, 0])
        v3.move_to([3.4, -1.4, 0])
        v4 = Text("v⃗", color=PURPLE)
        v5 = Text("v⃗", color=PURPLE)
        v6 = Text("v⃗", color=PURPLE)
        v7 = Text("v⃗", color=PURPLE)
        v4.move_to([-4, 0.8, 0])
        v5.move_to([-0.5, 1.5, 0])
        v6.move_to([0.7, -2, 0])
        v7.move_to([3.4, -1.4, 0])
        circArrow0 = CurvedArrow([-2, -1, 0], [-1, 0 , 0], angle=PI * 1.5, radius=1, arc_center=[-2, 0, 0], color=GREEN)
        w0 = Text("ω⃗₀", color=GREEN)
        w0.move_to([-2, 0, 0])
        circArrow1 = CurvedArrow([2.5, -0.5, 0], [3, 0, 0], angle=PI * 1.5, radius=1, arc_center=[-2.5, 0, 0], color=GREEN, tip_length=0.2)
        w1 = Text("ω⃗₁", color=GREEN)
        w1.move_to([2.4, 0.33, 0])
        self.play(Rotate(gear1, gear1.pitch_angle * 5, rate_func=rate_functions.ease_in_out_quint), Rotate(gear2, gear2.pitch_angle * 5, rate_func=rate_functions.ease_in_out_quint), Create(arrow4), Create(v4), Create(arrow5), Create(v5), Create(arrow6), Create(v6), Create(arrow7), Create(v7), run_time=2)
        self.play(Uncreate(arrow4), Uncreate(v4), Uncreate(arrow5), Uncreate(v5), Uncreate(arrow6), Uncreate(v6), Uncreate(arrow7), Uncreate(v7))
        
        radius0 = Line([-2, 1.5, 0], [-2, -1.5, 0], color=GOLD)
        radius1 = Line([2.5, 1, 0], [2.5, -1, 0], color=GOLD)
        radText0 = Text("d = 30", color=GOLD)
        radText1 = Text("d = 20", color=GOLD)
        radText0.next_to(radius0, UP)
        radText1.next_to(radius1, UP)
        formula0 = Text("ω₀ = v / r", color=GOLD)
        formula1 = Text("ω₁ = v / r", color=GOLD)
        formula = Text("ω = v / r", color=GOLD)
        formula.move_to([0, 3, 0])
        formula0.move_to([-4, 3, 0])
        formula1.move_to([4, 3, 0])
        formula2 = Text("ω₀ = v / 15", color=GOLD)
        formula3 = Text("ω₁ = v / 10", color=GOLD)
        formula4 = Text("ω₀ = v / (d / 2)", color=GOLD)
        formula5 = Text("ω₁ = v / (d / 2)", color=GOLD)
        formula2.move_to([-4, 3, 0])
        formula3.move_to([4, 3, 0])
        formula4.move_to([-4, 3, 0])
        formula5.move_to([4, 3, 0])
        timeline = {
        0.0: [
            Rotate(gear1, gear1.pitch_angle * -150, rate_func=linear, run_time=60),
            Rotate(gear2, gear2.pitch_angle * -150, rate_func=linear, run_time=60),
            Create(arrow0, run_time=1),
            Write(v0, run_time=1),
        ],
        0.3: [
            Create(arrow1, run_time=1),
            Write(v1, run_time=1),
        ],
        0.6: [
            Create(arrow2, run_time=1),
            Write(v2, run_time=1),
        ],
        0.9: [
            Create(arrow3, run_time=1),
            Write(v3, run_time=1),
        ],
        5.5: [
            Write(w0, run_time=2),
            Create(circArrow0, run_time=2),
        ],
        6.0: [
            Write(w1, run_time=2),
            Create(circArrow1, run_time=2),
        ],
            9.0: [
            Create(radius0, run_time=2),
            Create(radius1, run_time=2),
            Write(radText0, run_time=2),
            Write(radText1, run_time=2),
        ],
        10.0: [
            Write(formula, run_time=2)
        ],
        12.0: [
            FadeOut(formula, run_time=1),
            Write(formula0, run_time=1),
            Write(formula1, run_time=1),
        ],
        14.0: [
            FadeOut(formula0, run_time=1),
            FadeOut(formula1, run_time=1),
            Write(formula4, run_time=1),
            Write(formula5, run_time=1),
        ],
        16.0: [
            FadeOut(formula4, run_time=1),
            FadeOut(formula5, run_time=1),
            Write(formula2, run_time=1),
            Write(formula3, run_time=1),
            FadeOut(radius0, run_time=1),
            FadeOut(radius1, run_time=1),
            FadeOut(radText0, run_time=1),
            FadeOut(radText1, run_time=1),
        ],
        }
        play_timeline(self, timeline)