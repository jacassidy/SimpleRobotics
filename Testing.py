from manim import *
from manium import *
from scipy.integrate import quad  # Import quad from scipy


class Test(Scene):
    def construct(self):
        CustomBackground(self)
        
        # Write in PID text
        P_text = MathTex("P", color=BLACK, font_size=100)
        I_text = AddTex(P_text, "I")
        D_text = AddTex(I_text, "D")

        PID_text_group = VGroup(P_text, I_text, D_text)
        PID_text_group.move_to((0, 0, 0))

        self.play(Write(P_text), Write(I_text), Write(D_text))
        self.wait(1)

        # Break down PID acronym
        proportional_text = MathTex("Proportional", color=BLACK, font_size=40).move_to((-4, 1, 0))
        integral_text = MathTex("Integral", color=BLACK, font_size=40).move_to((0, 1, 0))
        differential_text = MathTex("Differential", color=BLACK, font_size=40).move_to((4, 1, 0))

        proportional_text = SplitTex(proportional_text, 1, aligned_edge=UP)
        integral_text = SplitTex(integral_text, 1, aligned_edge=UP)
        differential_text = SplitTex(differential_text, 1, aligned_edge=UP)

        self.play(Transform(P_text, proportional_text[0]), FadeIn(proportional_text[1]))
        self.wait(1)

        self.play(Transform(I_text, integral_text[0]), FadeIn(integral_text[1]))
        self.wait(1)

        self.play(Transform(D_text, differential_text[0]), FadeIn(differential_text[1]))
        self.wait(1)

        # Proportional Section
        # Draw axis for Proportional
        p_axes = Axes(
            x_range=[0, 2, 1],  # x-axis from 0 to 2
            y_range=[0, 2, 1],  # y-axis from 0 to 2
            axis_config={
                "color": CBlue,
                "include_ticks": False,  # No tick marks
                "include_tip": False  # No arrow tips
            }).scale(.2).move_to((-4, -.8, 0))

        p_graph = p_axes.plot(lambda x: x, color=COrange)

        p_x_label = p_axes.get_x_axis_label(Text("Error", color=BLACK).scale(0.5))
        p_y_label = p_axes.get_y_axis_label(Text("Response", color=BLACK).scale(0.5))

        # Proportional equation
        p_equation = MathTex(r"P = x \cdot k_P", color=BLACK).next_to(p_axes, DOWN)

        # Trace Axis
        p_x_tracker = ValueTracker(p_axes.x_range[0])

        p_dot = Dot(color=WHITE, stroke_color=BLACK, stroke_width=2).move_to(p_axes.i2gp(p_x_tracker.get_value(), p_graph))

        p_dot.add_updater(lambda d: d.move_to(p_axes.i2gp(p_x_tracker.get_value(), p_graph)))

        # Display x value during animation
        p_value_display = always_redraw(lambda: MathTex(
            f"x = {p_x_tracker.get_value():.2f}",
            color=BLACK
        ).next_to(p_equation, DOWN))

        self.play(Create(p_axes), Create(p_graph), Write(p_equation))
        self.play(Write(p_x_label), Write(p_y_label))
        self.wait(1)

        self.play(FadeIn(p_dot))
        self.play(Write(p_value_display))
        self.play(p_x_tracker.animate.set_value(p_axes.x_range[1]), run_time=2)
        self.play(FadeOut(p_dot), FadeOut(p_value_display))
        self.wait(1)

        # Integral Section
        # Draw axis for Integral
        i_axes = Axes(
            x_range=[0, 2 * PI, PI / 4],  # x-axis from 0 to 2π
            y_range=[-1.5, 1.5, 0.5],  # y-axis from -1.5 to 1.5
            axis_config={
                "color": CBlue,
                "include_ticks": False,  # No tick marks
                "include_tip": False  # No arrow tips
            }).scale(.2).move_to((0, -.8, 0))

        i_x_label = i_axes.get_x_axis_label(Text("Time", color=BLACK).scale(0.5))
        i_y_label = i_axes.get_y_axis_label(Text("Error", color=BLACK).scale(0.5))

        # Integral equation
        i_equation = MathTex(r"I = A \cdot k_I", color=BLACK).next_to(i_axes, DOWN)

        # Create the sine function graph
        i_sine_graph = i_axes.plot(lambda x: np.sin(x), color=COrange)

        i_x_tracker = ValueTracker(0)

        # Create the area under the curve as an always_redraw object
        i_area = always_redraw(lambda: i_axes.get_area(
            i_sine_graph,
            x_range=[0, i_x_tracker.get_value()],
            color=BLUE,
            opacity=0.5
        ))

        # Create a dot that tracks the current value on the sine graph
        i_dot = always_redraw(lambda: Dot(
            color=WHITE,
            fill_color=WHITE,
            stroke_color=BLACK,
            stroke_width=2
        ).move_to(i_axes.i2gp(i_x_tracker.get_value(), i_sine_graph)))

        def calculate_area(x_val):
            area, _ = quad(lambda x: np.sin(x), 0, x_val)
            return area

        # Display the current area value during animation
        i_area_value_display = always_redraw(lambda: MathTex(
            f"A = {calculate_area(i_x_tracker.get_value()):.2f}",
            color=BLACK
        ).next_to(i_equation, DOWN))

        # Add everything to the scene
        self.play(Create(i_axes), Create(i_sine_graph), Write(i_equation))
        self.play(Write(i_x_label), Write(i_y_label))
        self.wait(1)

        # Animate the filling of the area from left to right
        self.play(FadeIn(i_dot), Write(i_area_value_display), FadeIn(i_area))
        self.play(i_x_tracker.animate.set_value(2 * PI), run_time=6)
        i_area_value_display.clear_updaters()
        self.play(FadeOut(i_dot), FadeOut(i_area_value_display))
        self.wait(2)

        # Derivative Section
        # Draw axis for Derivative
        d_axes = Axes(
            x_range=[0, 6 * PI, PI],  # x-axis from 0 to 6π
            y_range=[-1.5, 1.5, 0.5],  # y-axis from -1.5 to 1.5
            axis_config={
                "color": CBlue,
                "include_ticks": False,  # No tick marks
                "include_tip": False  # No arrow tips
            }).scale(.2).move_to((4, -.8, 0))

        d_x_label = d_axes.get_x_axis_label(Text("Time", color=BLACK).scale(0.5))
        d_y_label = d_axes.get_y_axis_label(Text("Distance", color=BLACK).scale(0.5))

        # Derivative equation
        d_equation = MathTex(r"D = v \cdot k_D", color=BLACK).next_to(d_axes, DOWN)

        # Original function: e^(-x) * sin(x)
        d_sine_graph = d_axes.plot(lambda x: np.exp(-0.2 * x) * np.sin(x), color=COrange)

        d_x_tracker = ValueTracker(0)

        # Function to calculate the derivative
        def calculate_derivative(x_val):
            return np.exp(-0.2 * x_val) * (np.cos(x_val) - 0.2 * np.sin(x_val))

        # Create a dot that tracks the current value on the sine graph
        d_dot = always_redraw(lambda: Dot(
            color=WHITE,
            fill_color=WHITE,
            stroke_color=BLACK,
            stroke_width=2
        ).move_to(d_axes.i2gp(d_x_tracker.get_value(), d_sine_graph)))

        # Create a vector to represent the derivative
        d_vector = always_redraw(lambda: Vector(
            direction=UP * calculate_derivative(d_x_tracker.get_value()),
            color=BLACK
        ).move_to(d_dot.get_center()))

        # Display the current derivative value during animation
        d_derivative_value_display = always_redraw(lambda: MathTex(
            f"v = {calculate_derivative(d_x_tracker.get_value()):.2f}",
            color=BLACK
        ).next_to(d_equation, DOWN))

        # Add everything to the scene
        self.play(Create(d_axes), Create(d_sine_graph), Write(d_equation))
        self.play(Write(d_x_label), Write(d_y_label))
        self.wait(1)

        # Animate the vector representing the derivative
        self.play(FadeIn(d_dot), Write(d_derivative_value_display), FadeIn(d_vector))
        self.play(d_x_tracker.animate.set_value(6 * PI), run_time=8, rate_func=linear)
        d_derivative_value_display.clear_updaters()
        self.play(FadeOut(d_dot), FadeOut(d_derivative_value_display), FadeOut(d_vector))
        self.wait(2)

        # Fade everything out at the end
        all_objects = VGroup(
            P_text, I_text, D_text,
            proportional_text, integral_text, differential_text,
            p_axes, p_graph, p_x_label, p_y_label, p_dot, p_value_display,
            i_axes, i_sine_graph, i_x_label, i_y_label, i_area, i_dot, i_area_value_display,
            d_axes, d_sine_graph, d_x_label, d_y_label, d_dot, d_vector, d_derivative_value_display
        )

        self.play(FadeOut(all_objects))
        self.wait(1)



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


       
  
