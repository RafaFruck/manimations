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
        if t >= 81.0 and t < 131.0:
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
        if 81.0 <= t < 131.0:
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

        self.wait()
        self.play(Create(gear1))
        self.play(Rotate(gear1, angle=PI, run_time=2))
        self.wait(3)

        self.play(gear1.animate.shift(-gear1.rp * 1 * RIGHT))
        gear2.mesh_to(gear1)
        self.play(Create(gear2))
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
        arrow4 = self.create_arrow_at_angle(self.BeltFunctionArray(105.5), 1.5, self.BeltDerivativeAngle(105.5) + PI, color=PINK)
        arrow5 = self.create_arrow_at_angle(self.BeltFunctionArray(16), 1.5, self.BeltDerivativeAngle(16) + PI, color=PINK)
        arrow6 = self.create_arrow_at_angle(self.BeltFunctionArray(72), 1.5, self.BeltDerivativeAngle(72) + PI, color=PINK)
        arrow7 = self.create_arrow_at_angle(self.BeltFunctionArray(46), 1.5, self.BeltDerivativeAngle(46) + PI, color=PINK)
        v0 = MathTex(r"\vec{v}", color=RED)
        v1 = MathTex(r"\vec{v}", color=RED)
        v2 = MathTex(r"\vec{v}", color=RED)
        v3 = MathTex(r"\vec{v}", color=RED)
        v0.move_to([-4, 0.8, 0])
        v1.move_to([0.7, 1.8, 0])
        v2.move_to([-0.2, -1.8, 0])
        v3.move_to([3.4, -1.4, 0])
        v4 = MathTex(r"\vec{v}", color=PINK)
        v5 = MathTex(r"\vec{v}", color=PINK)
        v6 = MathTex(r"\vec{v}", color=PINK)
        v7 = MathTex(r"\vec{v}", color=PINK)
        v4.move_to([-4, -0.6, 0])
        v5.move_to([0.1, 1.9, 0])
        v6.move_to([0.4, -2, 0])
        v7.move_to([4.2, -0.1, 0])
        circArrow0 = Arc(
            radius=0.8, 
            start_angle=1.5 * PI, 
            angle=-1.5 * PI,
            arc_center=[-1.82, -0.18, 0],
            color=GREEN
        ).add_tip()
        circArrow1 = Arc(
            radius=0.4, 
            start_angle=1.5 * PI, 
            angle=-1.5 * PI,
            arc_center=[2.705, -0.17, 0],
            color=GREEN
        ).add_tip()
        w0 = MathTex(r"\vec{\omega}_a", color=GREEN)
        w0.move_to([-2, 0, 0])
        w1 = MathTex(r"\vec{\omega}_b", color=GREEN)
        w1.move_to([2.5, 0, 0])
        w1.scale(0.8)
        self.add(NumberPlane())
        self.play(Rotate(gear1, gear1.pitch_angle * 5, rate_func=rate_functions.ease_in_out_quint), Rotate(gear2, gear2.pitch_angle * 5, rate_func=rate_functions.ease_in_out_quint), Create(arrow4), Create(v4), Create(arrow5), Create(v5), Create(arrow6), Create(v6), Create(arrow7), Create(v7), run_time=2)
        self.play(Uncreate(arrow4), Uncreate(v4), Uncreate(arrow5), Uncreate(v5), Uncreate(arrow6), Uncreate(v6), Uncreate(arrow7), Uncreate(v7))
        self.wait(5)
        diameter0 = Line([-2, 1.5, 0], [-2, -1.5, 0], color=GOLD)
        diameter1 = Line([2.5, 1, 0], [2.5, -1, 0], color=GOLD)
        diaText0 = MathTex("d = 30", color=GOLD)
        diaText1 = MathTex("d = 20", color=GOLD)
        diaText0.next_to(diameter0, UP)
        diaText1.next_to(diameter1, UP)
        diaText0.scale(1.5)
        diaText1.scale(1.5)
        formula0 = MathTex(r" \lvert \vec{\omega}_a  \rvert = \frac{ \lvert \vec{v}  \rvert}{r}", color=GOLD)
        formula1 = MathTex(r" \lvert \vec{\omega}_b  \rvert = \frac{ \lvert \vec{v}  \rvert}{r}", color=GOLD)
        formula = MathTex(r" \lvert \vec{\omega}  \rvert = \frac{ \lvert \vec{v}  \rvert}{r}", color=GOLD)
        formula.move_to([0, 3, 0])
        formula.scale(1.5)
        fornula = formula.copy()
        formula0.scale(1.5)
        formula1.scale(1.5)
        formula0.move_to([-4, 3, 0])
        formula1.move_to([4, 3, 0])
        formula2 = MathTex(r" \lvert \vec{\omega}_a  \rvert = \frac{{ \lvert \vec{v}  \rvert}}{15}", color=GOLD)
        formula3 = MathTex(r" \lvert \vec{\omega}_b  \rvert = \frac{{ \lvert \vec{v}  \rvert}}{10}", color=GOLD)
        formula4 = MathTex(r" \lvert \vec{\omega}_a  \rvert = \frac{{ \lvert \vec{v}  \rvert}}{d / 2}", color=GOLD)
        formula5 = MathTex(r" \lvert \vec{\omega}_b  \rvert = \frac{{ \lvert \vec{v}  \rvert}}{d / 2}", color=GOLD)
        formula2.move_to([-4, 3, 0])
        formula3.move_to([4, 3, 0])
        formula4.move_to([-4, 3, 0])
        formula5.move_to([4, 3, 0])
        formula2.scale(1.5)
        formula3.scale(1.5)
        formula4.scale(1.5)
        formula5.scale(1.5)
        circs = VGroup()
        torqueText = MathTex("Torque", color=BLACK)
        torqueText.scale(7)
        torqueColorful = AnimatedBoundary(torqueText, colors=[PURE_RED, PURE_YELLOW, PURE_GREEN, PURE_CYAN, PURE_BLUE, PURE_MAGENTA], cycle_rate=6)
        for i in range(26):
            if i < 10:
                circ = Circle(0.5, color=PURPLE_A).move_to(self.BeltFunctionArray(22.5 + 4 * i))
            elif i == 10:
                circ = Circle(0.5, color=PURPLE_A).move_to(self.BeltFunctionArray(77))
            elif 10 < i < 24:
                circ = Circle(0.5, color=PURPLE_A).move_to(self.BeltFunctionArray(76 + 4 * (i - 10)))
            elif i == 24:
                circ = Circle(0.5, color=PURPLE_A).move_to(self.BeltFunctionArray(134))
            else:
                 circ = Circle(0.5, color=PURPLE_A).move_to(self.BeltFunctionArray(135.5))
            circs.add(circ)
        powerEq0 = MathTex(r"P = \omega \cdot \tau", color=GOLD).shift([0, 3, 0]).scale(2)
        powerEq1 = MathTex(r"\omega_a \cdot \tau_a = \omega_b \cdot \tau_b", color=GOLD).shift([0, 3, 0]).scale(2)
        powerEq2 = MathTex(r"\frac{v}{15} \cdot \tau_a = \frac{v}{10} \cdot \tau_b", color=GOLD).shift([0, 3, 0]).scale(2)
        powerEq3 = MathTex(r"\frac{\tau_a}{15} = \frac{\tau_b}{10}", color=GOLD).shift([0, 3, 0]).scale(2)

        timeline = {
        0.0: [
            Rotate(gear1, gear1.pitch_angle * -225, run_time=75),
            Rotate(gear2, gear2.pitch_angle * -225, run_time=75),
            Create(arrow0, run_time=1),
            Write(v0, run_time=1),
            Create(arrow1, run_time=1),
            Write(v1, run_time=1),
            Create(arrow2, run_time=1),
            Write(v2, run_time=1),
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
            Create(diameter0, run_time=2),
            Create(diameter1, run_time=2),
            Write(diaText0, run_time=2),
            Write(diaText1, run_time=2),
        ],
        10.0: [
            Write(formula, run_time=2)
        ],
        12.0: [
            Transform(fornula, formula0, run_time=1),
            Transform(formula, formula1, run_time=1),
        ],
        14.0: [
            Transform(fornula, formula4, run_time=1),
            Transform(formula, formula5, run_time=1),
        ],
        16.0: [
            Transform(fornula, formula2, run_time=1),
            Transform(formula, formula3, run_time=1),
            FadeOut(diameter0, run_time=1),
            FadeOut(diameter1, run_time=1),
            Unwrite(diaText0, run_time=1),
            Unwrite(diaText1, run_time=1),
        ],
        23.0: [
            Unwrite(fornula, run_time=1),
            Unwrite(formula, run_time=1),
        ],
        27.0: [
            SpinInFromNothing(torqueText, angle=8 * PI, run_time=2),
            SpinInFromNothing(torqueColorful, angle=8 * PI, run_time=2),
        ],
        32.0: [
            Unwrite(torqueText, run_time=1),
            Unwrite(torqueColorful, run_time=1),
        ],
        34.0: [
            Write(powerEq0, run_time=2)
        ],
        39.0: [
            Transform(powerEq0, powerEq1, run_time=1),
        ],
        41.0: [
            Transform(powerEq0, powerEq2, run_time=1)
        ],
        43.0: [
            Transform(powerEq0, powerEq3, run_time=1)
        ],
        47.0: [
            Unwrite(powerEq0, run_time=1)
        ],
        56.0: [
            Create(circs[4], run_time=0.3),
        ],
        58.0: [
            Create(circs[14], run_time=0.3),
        ],
        59.0: [
            Create(circs[6], run_time=0.3),
        ],
        60.0: [
            Create(circs[17], run_time=0.3),
        ],
        60.5: [
            Create(circs[7], run_time=0.3),
        ],
        60.9: [
            Create(circs[23], run_time=0.3),
            Create(circs[20], run_time=0.3),
        ],
        61.2: [
            Create(circs[24], run_time=0.3),
            Create(circs[21], run_time=0.3),
            Create(circs[3], run_time=0.3),
        ],
        61.4: [
            Create(circs[15], run_time=0.3),
            Create(circs[0], run_time=0.3),
            Create(circs[1], run_time=0.3),
            Create(circs[5], run_time=0.3),
        ],
        61.5: [
            Create(circs[19], run_time=0.3),
            Create(circs[12], run_time=0.3),
            Create(circs[2], run_time=0.3),
            Create(circs[8], run_time=0.3),
            Create(circs[18], run_time=0.3),
        ],
        61.6: [
            Create(circs[9], run_time=0.3),
            Create(circs[10], run_time=0.3),
            Create(circs[11], run_time=0.3),
            Create(circs[13], run_time=0.3),
            Create(circs[16], run_time=0.3),
            Create(circs[22], run_time=0.3),
        ],
        64.4: [
            *[ApplyMethod(circ.set_opacity, 0.5, run_time=0.3) for circ in circs]
        ],
        64.7: [
            *[Uncreate(circ, run_time=0.3) for circ in circs]
        ],
        }
        play_timeline(self, timeline)
        self.wait()