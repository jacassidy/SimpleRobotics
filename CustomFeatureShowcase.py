from manim import *
from manium import *

class Display(Scene):
    def construct(self):
        # Create an object
        circle = Circle(1)#Arc(radius= 1, start_angle= 0, angle=-2)

        posX = Line((0,0,0), (1,0,0))
        posY = Line((0,0,0), (0,1,0))
        negX = Line((0,0,0), (-1,0,0))
        negY = Line((0,0,0), (0,-1,0))

        self.play(Create(circle).set_rate_func(smooth), 
                  Create(posX).set_rate_func(split_portion(smooth, 4, 3)),
                  Create(posY).set_rate_func(split_portion(smooth, 4, 0)),
                  Create(negX).set_rate_func(split_portion(smooth, 4, 1)),
                  Create(negY).set_rate_func(split_portion(smooth, 4, 2)),
                  run_time = 3
                  )

        self.play(UnravelCircle(circle, start_angle= PI/2))

        # self.play(Highlight(circle))

        first_line = Line((0,0,0), (-1,0,0))
        self.add(first_line)
        second_line = Line((0,0,0), (1,0,0))

        self.play(Uncreate(first_line).set_rate_func(smooth_first_half), 
                  Create(second_line).set_rate_func(smooth_second_half), run_time = 2)

        self.wait(1)
        first_line = Line((0,0,0), (-1,0,0))
        self.play(Uncreate(second_line).set_rate_func(split_second_half(smooth_second_half)),
                  Create(first_line).set_rate_func(split_second_half(smooth_second_half)),
                  Uncreate(circle), run_time = 2)
        
        # self.play(Emphasize(circle), run_time = 2)

        # self.wait(1)

        # line = Line((0,0,0), (0,0,0))
        
        # self.play(UnravelCircle(circle, line, start_angle=PI, unravel_from_end=False))

        # text = Text("Helo")

        # self.play(Transform(line, text))

        # self.play(Emphasize(line))
  
