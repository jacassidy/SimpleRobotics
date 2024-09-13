from manim import *
from manium import *
from scipy.integrate import quad  # Import quad from scipy


class Test(Scene):
    def construct(self):
        # Title
        title = Text("Understanding Radians").to_edge(UP)
        self.play(Write(title))
        self.wait(1)

        # Draw Circle with center O
        circle = Circle(radius=2)
        center_dot = Dot(ORIGIN)
        center_label = MathTex("O").next_to(center_dot, DOWN)
        self.play(Create(circle), FadeIn(center_dot, center_label))
        self.wait(1)

        # Draw radius
        radius_line = Line(ORIGIN, circle.point_at_angle(0))
        radius_label = MathTex("r").next_to(radius_line, UP)
        self.play(Create(radius_line), Write(radius_label))
        self.wait(1)

        # Mark off arc length equal to radius 'r'
        theta = 1  # 1 radian
        arc = Arc(radius=2, start_angle=0, angle=theta, color=YELLOW)
        arc_length_label = MathTex("\\text{Arc length} = r").set_color(YELLOW)
        arc_length_label.next_to(arc.point_from_proportion(0.5), UP+RIGHT)
        self.play(Create(arc), Write(arc_length_label))
        self.wait(1)

        # Draw second radius line
        radius_line_2 = Line(ORIGIN, circle.point_at_angle(theta))
        self.play(Create(radius_line_2))
        self.wait(1)

        # Show angle theta at center
        angle = Angle(radius_line_2, radius_line, radius=0.5, other_angle=False)
        theta_label = MathTex("1\\ \\text{radian}").next_to(angle, LEFT)
        self.play(Create(angle), Write(theta_label))
        self.wait(1)

        # Show circumference is 2*pi*r
        circumference_formula = MathTex("\\text{Circumference} = 2\\pi r").to_edge(DOWN)
        self.play(Write(circumference_formula))
        self.wait(1)

        # Indicate that full circle corresponds to 2*pi radians
        full_angle_label = MathTex("\\text{Full circle} = 2\\pi\\ \\text{radians}")
        full_angle_label.next_to(circumference_formula, UP)
        self.play(Write(full_angle_label))
        self.wait(1)

        # Show conversion between degrees and radians
        conversions = VGroup(
            MathTex("360^\\circ = 2\\pi\\ \\text{radians}"),
            MathTex("180^\\circ = \\pi\\ \\text{radians}"),
            MathTex("90^\\circ = \\dfrac{\\pi}{2}\\ \\text{radians}")
        ).arrange(DOWN, aligned_edge=LEFT).shift(LEFT*3 + UP)
        for conversion in conversions:
            self.play(Write(conversion))
            self.wait(1)

        # Conclude
        conclusion = Text("Radians relate angles directly to arc lengths.")
        conclusion.next_to(full_angle_label, DOWN)
        self.play(Write(conclusion))
        self.wait(2)

        # Fade out everything
        self.play(FadeOut(*self.mobjects))




class Plot(Scene):
    def construct(self):
        # Create axes
        axes = Axes(
            x_range=[0, 10, 1],  # x-axis from 0 to 10
            y_range=[0, 10, 1],  # y-axis from 0 to 10
            axis_config={
                "color": BLUE,
                "include_ticks": True,
                "include_tip": False
            }
        ).add_coordinates().scale(0.8).to_edge(DOWN)

        # Create some data points for the linear regression
        data_points = [
            [1, 2],
            [2, 2.5],
            [3, 3.1],
            [4, 4.5],
            [5, 4.8],
            [6, 6],
            [7, 6.5],
            [8, 7.5],
            [9, 8.4],
        ]

        # Convert data points to dots on the graph
        dots = VGroup(*[Dot(axes.c2p(x, y), color=YELLOW) for x, y in data_points])

        # Linear regression line (approximated for simplicity)
        regression_line = axes.plot(lambda x: 0.9 * x + 1, color=ORANGE)

        # Labels
        x_label = axes.get_x_axis_label(Text("X", color=BLACK).scale(0.5))
        y_label = axes.get_y_axis_label(Text("Y", color=BLACK).scale(0.5))

        # Add elements to the scene
        self.play(Create(axes), Write(x_label), Write(y_label))
        self.play(FadeIn(dots))
        self.play(Create(regression_line))
        self.wait(2)

class Test2(Scene):
    def construct(self):

        # Create axes
        axes = Axes(
            x_range=[-3, 3, 1],  # X-axis range
            y_range=[-1, 9, 1],  # Y-axis range
            axis_config={"color": BLUE},
        )

        # Define the function
        function = lambda x: x**2

        # Create the graph
        graph = axes.plot(function, color=YELLOW)

        # Add labels
        graph_label = axes.get_graph_label(graph, label="x^2")

        # Display axes and graph
        self.play(Create(axes), Create(graph), Write(graph_label))

        # Wait to display
        self.wait(2)

# Define the graph
        vertices = ["A", "B", "C", "D"]
        edges = [("A", "B"), ("B", "C"), ("C", "D"), ("D", "A")]

        # Create the graph
        graph = Graph(vertices, edges, layout="circular")

        # Add the graph to the scene
        self.play(Create(graph))

        # Wait for a moment to display
        self.wait(2)


       
  
