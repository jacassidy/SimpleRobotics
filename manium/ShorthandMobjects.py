from manim import *
from manim.typing import *
from typing import *

def EqLine(
        start: Callable[[], Point3D],
        end: Callable[[], Point3D],
        buff: float = 0,
        path_arc: float | None = None,
        **kwargs,
    ):

    line = Line(start(), end(), buff, path_arc, **kwargs)
    line.add_updater(line.put_start_and_end_on(start(), end()))

    return line

def EqArc(
        radius: float,
        start_angle: Callable[[], float],
        angle: Callable[[], float],
        arc_center: Callable[[], Point3D],
        num_components: int = 9,
        **kwargs
    ):
    
    arc = Arc(radius, start_angle(), angle(), num_components, arc_center(), **kwargs)
    arc.add_updater(arc.become(Arc(radius, start_angle(), angle(), num_components, arc_center(), **kwargs)))

    return arc