from manim import *
from manim_play_timeline import play_timeline
import numpy as np

class Torque(Scene):
    def create_arrow_at_angle(self, start, length, angle_in_rad, color=RED):
        length = float(length)
        end = start + np.array([
            length * np.cos(angle_in_rad),
            length * np.sin(angle_in_rad),
            0.0
        ])
        return Arrow(start=start, end=end, color=color, stroke_width=12)
    
    def construct(self):
        t = ValueTracker(0)
        self.add(t)
        obj = Dot(color=WHITE, radius=0.3, z_index=5)
        obj.add_updater(lambda mob: mob.set_x(2.5 * np.cos(t.get_value())))
        obj.add_updater(lambda mob: mob.set_y(2.5 * np.sin(t.get_value())))
        traj = Circle(2.5, color=TEAL, stroke_opacity=0.5)
        rad = Line(color=GOLD)
        rad.add_updater(lambda mob: mob.become(
            Line(ORIGIN, obj.get_center(), color=GOLD)
        ))
        force = Arrow(color=MAROON)
        force.add_updater(lambda mob: mob.become(
            self.create_arrow_at_angle(obj.get_center(), 2.5, t.get_value() + PI * 0.5, color=MAROON)
        ))
        txt = MathTex(r"\vec{\tau}", r"=", r"r", r"\cdot", r"\vec{F}")
        txt.move_to([0, 1.4, 0])
        slice0 = txt[0]
        slice1 = txt[1]
        slice2 = txt[2]
        slice2.set_color(GOLD)
        slice3 = txt[3]
        slice4 = txt[4:]
        slice4.set_color(MAROON)
        arr0 = Arrow([0.2, 1.0, 0], [1.25, 0, 0], color=GOLD)
        arr1 = Arrow([1.0, 1.4, 0], [2.5, 1, 0], color=MAROON)
        arr2 = Arrow([-0.8, 1.2, 0], [0, -1, 0])
        Nm = Text("Nm").scale(1.5).shift([0, -1.5, 0])
        m = Text("m", color=GOLD).shift([0.4, 0.4, 0]).scale(0.6)
        N = Text("N", color=MAROON).shift([1.5, 1, 0]).scale(0.6)
        timeline = {
        1.0: [
            Create(obj, run_time=0)
        ],
        2.0: [
            Create(rad, run_time=0)
        ],
        3.0: [
            Create(traj, run_time=0)
        ],
        5.0: [
            Write(force, run_time=1)
        ],
        7.0: [
            Write(slice0, run_time=0)
        ],
        8.0: [
            Write(slice1, run_time=0)
        ],
        9.0: [
            Write(slice2, run_time=0),
            Create(arr0, run_time=0)
        ],
        10.0: [
            Write(slice3, run_time=0)
        ],
        11.0: [
            Write(slice4, run_time=0),
            Create(arr1, run_time=0)
        ],
        12.0: [
            Write(m, run_time=0)
        ],
        13.0: [
            Write(N, run_time=0)
        ],
        14.0: [
            Create(arr2, run_time=0),
            Write(Nm, run_time=0)
        ],
        15.0: [
            ApplyMethod(t.animate.increment_value(2 * PI), run_time=2)
        ],
        }
        self.play(Create(NumberPlane()))
        play_timeline(self, timeline)
