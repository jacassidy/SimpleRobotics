from manim import *
from manium import *

class Test(Scene):
    def construct(self):

        self.camera.background_color = ManimColor("#f2f2f2")
        # Create an object
        # circle = Circle(2, color = ManimColor("#1251b5"), stroke_width = 8)#Arc(radius= 1, start_angle= 0, angle=-2)
        # self.play(Create(circle))

        mainTex = MathTex(r"\pi \times 1 \times 1", color = BLACK, font_size = 20)
        newMainTex = SplitTex(mainTex, 19)
        # newTex = AddTex(mainTex, r"\times 1")

        self.add(mainTex)
        self.play(FadeIn(newMainTex), FadeOut(mainTex))
        self.wait(1)


       
  
