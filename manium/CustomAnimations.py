from typing import Callable
from manim import *
from manim.animation.animation import DEFAULT_ANIMATION_LAG_RATIO, DEFAULT_ANIMATION_RUN_TIME
from manim.mobject.mobject import Mobject
from manim.utils.rate_functions import smooth
from typing import Tuple

class UnravelArc(Animation):
    def __init__(self, arc: Arc, exported_line: Line | None = None, unravel_from_end: bool = False, **kwargs) -> None:
        super().__init__(arc, remover=True, introducer=True, **kwargs)

        #Bring parameters into class
        self.arc            = arc
        self.exported_line  = exported_line

        #Necessary Animation Variables
        self.arc_radius             = self.mobject.height/2 #more accurate radius that adjusts to scaling
        self.arc_angle              = self.arc.angle
        self.arc_length             = self.arc_radius * self.arc_angle
        self.arc_start_center       = self.arc.get_center()

        self.stroke_width           = self.arc.stroke_width
        self.stroke_color           = self.arc.get_stroke_color()

        self.start_angle            = self.arc.start_angle  
        
        self.define_unravel(unravel_from_end)

        self.instantiate_mobjects()

    def define_unravel(self, unravel_from_end):
        if unravel_from_end:
            self.start_angle += self.arc_angle
            self.arc_angle = - self.arc_angle

        self.unravel_direction      = np.sign(self.arc.angle) * np.array(
                                            [np.cos(self.start_angle + PI/2 * np.sign(self.arc_angle)), 
                                            np.sin(self.start_angle + PI/2 * np.sign(self.arc_angle)), 
                                            0]
                                        )
        
        self.unravel_point = self.arc_start_center + np.array(
                [self.arc_radius * np.cos(self.start_angle),
                self.arc_radius * np.sin(self.start_angle),
                0]
            )  

    def _setup_scene(self, scene: Scene) -> None:
        # scene.add(self.arc)
        scene.add(self.line)

        return super()._setup_scene(scene)
    
    def begin(self) -> None:
        # self.mobject.set_opacity(opacity = 0)
        return super().begin()
    
    def instantiate_mobjects(self):
        #Create new Mobjects that will belong to the scene
        # self.arc = Arc(self.circle_radius, start_angle = self.start_angle, angle= TAU,
        #                 arc_center=self.circle_start_center, stroke_width = self.stroke_width,
        #                     stroke_color = self.stroke_color)
        
        line = Line(self.unravel_point, self.unravel_point, stroke_width = self.stroke_width,
                        stroke_color = self.stroke_color)
        
        if not self.exported_line is None:
            self.exported_line.become(line)
            self.line = self.exported_line
        else:
            self.line = line

    def clean_up_from_scene(self, scene: Scene) -> None:
        # scene.remove(self.arc)
        scene.remove(self.mobject)
        return super().clean_up_from_scene(scene)


    def interpolate_mobject(self, alpha: float) -> None:
        real_alpha = self.rate_func(alpha)

        self.update_line(real_alpha)
        self.update_arc(real_alpha)

        return super().interpolate_mobject(alpha)

    def update_line(self, alpha):
        alpha += .00001
        self.line.put_start_and_end_on(self.unravel_point + self.unravel_direction * alpha * self.arc_length, 
                                       self.unravel_point)

    def update_arc(self, alpha):
        self.arc.become(Arc(self.arc_radius, start_angle = self.start_angle, angle = (1 - alpha) * self.arc_angle, 
            arc_center = self.arc_start_center + self.unravel_direction * alpha * self.arc_length, 
            stroke_width = self.stroke_width, stroke_color = self.stroke_color))

class UnravelCircle(UnravelArc):
    def __init__(self, arc: Arc, exported_line: Line | None = None, start_angle: float = 0, unravel_from_end: bool = False, **kwargs) -> None:
        super().__init__(arc, exported_line, unravel_from_end, **kwargs)
        
        self.start_angle = start_angle

        self.define_unravel(unravel_from_end)


class Emphasize(Animation):
    def __init__(self, mobject: Mobject | None, scale_factor: float = 1.5, pause_porportion: float = .2, **kwargs):
        super().__init__(mobject, **kwargs)

        #parameters
        self.pause_porportion = pause_porportion
        self.scale_factor = scale_factor

        #calculations
        self.scale_alpha_porportion = (1 - self.pause_porportion) / 2
        self.scale_up_portion = self.scale_alpha_porportion
        self.scale_down_portion = self.scale_up_portion + self.pause_porportion
    
    def interpolate_mobject(self, alpha: float) -> None:
        
        if alpha <= self.scale_up_portion:
            #scale up
            real_alpha = self.rate_func(alpha / self.scale_alpha_porportion)
            self.set_scale_porportion(real_alpha)

        if alpha >= self.scale_down_portion:
            #scale down
            real_alpha = 1 - self.rate_func((alpha - self.scale_down_portion) / self.scale_alpha_porportion)
            self.set_scale_porportion(real_alpha)

        return super().interpolate_mobject(alpha)
    
    def set_scale_porportion(self, scale_porportion):
        self.mobject.set_height(self.starting_mobject.height * (1 + scale_porportion * self.scale_factor))

class Highlight(ShowPartial):
    def __init__(self, mobject: Mobject | None, color: ManimColor = WHITE, time_width: float = 0.1, **kwargs):
    
        self.time_width = time_width

        duplicate = mobject.copy()
        duplicate.set_stroke(width=mobject.get_stroke_width() / 3, color = color)

        super().__init__(duplicate, remover=True, introducer=True, **kwargs)        

    def _get_bounds(self, alpha: float) -> Tuple[float]:
        tw = self.time_width
        upper = interpolate(0, 1 + tw, alpha)
        lower = upper - tw
        upper = min(upper, 1)
        lower = max(lower, 0)
        return (lower, upper)

    def clean_up_from_scene(self, scene: Scene) -> None:
        super().clean_up_from_scene(scene)
        for submob, start in self.get_all_families_zipped():
            submob.pointwise_become_partial(start, 0, 1)

class ScaleArc(Animation):
    def __init__(self, mobject: Arc | None, max_scale: float = 0.5, **kwargs):
        super().__init__(mobject, **kwargs)

        #Bring parameters into class
        self.max_scale      = max_scale-1

        #Necessary Animation Variables
        self.arc_radius             = self.mobject.radius #more accurate radius that adjusts to scaling
        self.arc_angle              = self.mobject.angle
        self.arc_center             = self.mobject.get_arc_center()

        self.stroke_width           = self.mobject.stroke_width
        self.color                  = self.mobject.get_stroke_color()

        self.start_angle            = self.mobject.start_angle  
    
    def interpolate_mobject(self, alpha: float) -> None:
        scale_porportion = self.rate_func(alpha)
        self.mobject.become(Arc(radius=self.starting_mobject.radius * (1 + scale_porportion * self.max_scale), 
                            angle=self.arc_angle, arc_center=self.arc_center,
                            stroke_width = self.stroke_width, color = self.color, start_angle=self.start_angle))
        return super().interpolate_mobject(alpha)