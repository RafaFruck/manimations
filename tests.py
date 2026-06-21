from manim import *

class CircularArrowExample(Scene):
    def construct(self):
        # Draws a circular arrow covering 180 degrees (PI) with a radius of 2
        circular_arrow = Arc(
            radius=2, 
            start_angle=0, 
            angle=PI, 
            color=YELLOW
        ).add_tip()
        
        self.play(Create(circular_arrow))
        self.wait()
