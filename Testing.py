from manim import *
from manium import *
from scipy.integrate import quad  # Import quad from scipy


class Test(Scene):
    def construct(self):
        pass



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

        # Load your SVG file
        svg_object = SVGMobject("5203_2402_0014__91946__97788_edge.svg")
        
        # You can scale, rotate, and position the SVG as needed
        svg_object.scale(2)  # Scaling the SVG
        svg_object.set_color(WHITE)  # Set the color of the SVG

        # Animate the SVG appearance
        self.play(Create(svg_object), run_time =3)
        self.wait(2)


       
  
