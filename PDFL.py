from manim import *
from manium import *
from scipy.integrate import quad  # Import quad from scipy


class PID(Scene):
    def construct(self):
        CustomBackground(self)
        
        #Write in PID tex
        P_text = MathTex("P", color = BLACK, font_size = 100)
        I_text = AddTex(P_text, "I")
        D_text = AddTex(I_text, "D")

        PID_text_group = VGroup(P_text, I_text, D_text)

        PID_text_group.move_to((0,0,0))

        self.play(Write(P_text), Write(I_text), Write(D_text))
        self.wait(1)

        #Break down PID acronym
        porportional_text = MathTex("Porportional", color = BLACK, font_size = 40).move_to((-4,1,0))
        integral_text = MathTex("Integral", color = BLACK, font_size = 40).move_to((0,1,0))
        differential_text = MathTex("Differential", color = BLACK, font_size = 40).move_to((4,1,0))

        porportional_text = SplitTex(porportional_text, 1, aligned_edge=UP)
        integral_text = SplitTex(integral_text, 1, aligned_edge=UP)
        differential_text = SplitTex(differential_text, 1, aligned_edge=UP)
        
        self.play(Transform(P_text, porportional_text[0]), FadeIn(porportional_text[1]))
        self.wait(1)

        self.play(Transform(I_text, integral_text[0]), FadeIn(integral_text[1]))
        self.wait(1)

        self.play(Transform(D_text, differential_text[0]), FadeIn(differential_text[1]))
        self.wait(1)

        #Draw axis for porportional
        p_axes = Axes(
            x_range=[0, 2, 1],  # x-axis from -3 to 3
            y_range=[0, 2, 1],  # y-axis from -1 to 9
            axis_config={
                "color": CBlue,
                "include_ticks": False,  # No tick marks
                "include_tip": False     # No arrow tips
            }).scale(.2).move_to((-4, -.8, 0))
        
        p_graph = p_axes.plot(lambda x: x, color = COrange)

        p_x_label = p_axes.get_x_axis_label(Text("Error", color = BLACK).scale(0.5))
        p_y_label = p_axes.get_y_axis_label(Text("Response", color = BLACK).scale(0.5))

        self.play(Create(p_axes), Create(p_graph))
        self.play(Write(p_x_label), Write(p_y_label))
        self.wait(1)
        #Trace Axis
        # Create a dot at the starting point of the graph
        p_dot = Dot(color=WHITE,                    # Fill color
            stroke_color=BLACK,             # Border color
            stroke_width=2,                 ).move_to(p_axes.i2gp(p_axes.x_range[0], p_graph))

        p_x_tracker = ValueTracker(p_axes.x_range[0])

        p_dot.add_updater(lambda d: d.move_to(p_axes.i2gp(p_x_tracker.get_value(), p_graph)))

        self.play(FadeIn(p_dot))
        self.play(p_x_tracker.animate.set_value(p_axes.x_range[1]), run_time = 2)
        self.play(FadeOut(p_dot))
        self.wait(1)

        #Draw axis for integral
        # Create axes
        i_axes = Axes(
            x_range=[0, 2 * PI, PI / 4],  # x-axis from -π to π
            y_range=[-1.5, 1.5, 0.5],   # y-axis from -1.5 to 1.5
            axis_config={
                "color": CBlue,
                "include_ticks": False,  # No tick marks
                "include_tip": False     # No arrow tips
            }).scale(.2).move_to((0, -.8, 0))
        
        i_x_label = i_axes.get_x_axis_label(Text("Time", color = BLACK).scale(0.5))
        i_y_label = i_axes.get_y_axis_label(Text("Error", color = BLACK).scale(0.5))

        # Create the sine function graph
        i_sine_graph = i_axes.plot(lambda x: np.sin(x), color=COrange)

        # Initialize a ValueTracker for the x-value up to which the area is filled
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

        # Display the current area value on the screen
        i_area_value = DecimalNumber(
            calculate_area(i_x_tracker.get_value()), 
            num_decimal_places=2, 
            color=BLACK
        ).next_to(i_axes, DOWN)

        i_area_value.add_updater(lambda o: o.set_value(calculate_area(i_x_tracker.get_value())))

        # Add everything to the scene
        self.play(Create(i_axes), Create(i_sine_graph))
        self.play(Write(i_x_label), Write(i_y_label))
        self.wait(1)

        # Animate the filling of the area from left to right
        self.play(FadeIn(i_dot), Write(i_area_value), FadeIn(i_area))
        self.play(i_x_tracker.animate.set_value(2*PI), run_time=6)
        i_area_value.clear_updaters()
        self.play(FadeOut(i_dot), FadeOut(i_area_value))
        # Wait before ending the scene
        self.wait(2)

        #Derivative Section
        # Create axes
        d_axes = Axes(
            x_range=[0, 6 * PI, PI],  # x-axis from 0 to 6π
            y_range=[-1.5, 1.5, 0.5],  # y-axis from -1.5 to 1.5
            axis_config={
                "color": BLUE,
                "include_ticks": False,  # No tick marks
                "include_tip": False     # No arrow tips
            }).scale(.2).move_to((4, -.8, 0))
        
        d_x_label = d_axes.get_x_axis_label(Text("Time", color=BLACK).scale(0.5))
        d_y_label = d_axes.get_y_axis_label(Text("Distance", color=BLACK).scale(0.5))

        # Original function: e^(-x) * sin(x)
        d_sine_graph = d_axes.plot(lambda x: np.exp(-0.2 * x) * np.sin(x), color=ORANGE)

        # Initialize a ValueTracker for the x-value
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
            direction= UP * calculate_derivative(d_x_tracker.get_value()), # RIGHT * 0.1 +,
            color=BLACK
        ).move_to(d_dot.get_center()))

        # Display the current derivative value on the screen
        d_derivative_value = DecimalNumber(
            calculate_derivative(d_x_tracker.get_value()), 
            num_decimal_places=2, 
            color=BLACK
        ).next_to(d_axes, DOWN)

        d_derivative_value.add_updater(lambda o: o.set_value(calculate_derivative(d_x_tracker.get_value())))

        # Add everything to the scene
        self.play(Create(d_axes), Create(d_sine_graph))
        self.play(Write(d_x_label), Write(d_y_label))
        self.wait(1)

        # Animate the vector representing the derivative
        self.play(FadeIn(d_dot), Write(d_derivative_value), FadeIn(d_vector))
        self.play(d_x_tracker.animate.set_value(6*PI), run_time=8, rate_func=linear)
        d_derivative_value.clear_updaters()
        self.play(FadeOut(d_dot), FadeOut(d_derivative_value), FadeOut(d_vector))
        # Wait before ending the scene
        self.wait(2)

        all_objects = VGroup(
            P_text, I_text, D_text,
            porportional_text, integral_text, differential_text,
            p_axes, p_graph, p_x_label, p_y_label, p_dot,
            i_axes, i_sine_graph, i_x_label, i_y_label, i_area, i_dot, i_area_value,
            d_axes, d_sine_graph, d_x_label, d_y_label, d_dot, d_vector, d_derivative_value
        )

        # oP_text = MathTex("P", color = BLACK, font_size = 100)
        # oI_text = AddTex(oP_text, "I")
        # oD_text = AddTex(oI_text, "D")

        # oPID_text_group = VGroup(oP_text, oI_text, oD_text)

        # oPID_text_group.move_to((0,0,0))

        self.play(FadeOut(all_objects),
                #   Transform(P_text, oP_text),
                #   Transform(I_text, oI_text),
                #   Transform(D_text, oD_text)
                  )
        self.wait(1)


        
class PIDDemo(Scene):
    def construct(self):
        CustomBackground(self)

        # PID constants
        P = 0.0001  # Proportional gain
        I = -0.00000001  # Integral gain
        D = 0.005  # Derivative gain 

        # Initialize value trackers for time and error components
        time_tracker = ValueTracker(0)
        error_tracker = ValueTracker(1.5)  # Start with an error near the top
        integral_tracker = ValueTracker(0)
        derivative_tracker = ValueTracker(0)

        # Create axes
        axes = Axes(
            x_range=[0, 10, 1],  # x-axis representing time from 0 to 10 seconds
            y_range=[-2, 2, 0.5],  # y-axis representing error from -2 to 2
            axis_config={
                "color": CBlue,  # Change axes color to CBlue
                "include_ticks": True,
                "include_tip": False
            }
        ).scale(0.8).move_to(DOWN)

        x_label = axes.get_x_axis_label(Text("Time", color=BLACK).scale(0.5))
        y_label = axes.get_y_axis_label(Text("Error", color=BLACK).scale(0.5))

        # Display the PID constants above the graph with colored P, I, D
        pid_constants = MathTex(
            f"P = {P:.3f} \\quad I = {I:.5f} \\quad D = {D:.5f}",
            substrings_to_isolate=["P", "I", "D"]
        ).to_edge(UP).shift(DOWN)

        pid_constants.set_color_by_tex("P", RED)
        pid_constants.set_color_by_tex("I", GREEN)
        pid_constants.set_color_by_tex("D", BLUE)
        pid_constants.set_color(BLACK)

        # Function to calculate the PID response (acceleration)
        def pid_response(t):
            error = error_tracker.get_value()
            integral = integral_tracker.get_value()
            derivative = derivative_tracker.get_value()

            response = P * error + I * integral + D * derivative
            return -response

        # Create a dot that tracks the error value on the graph
        dot = always_redraw(lambda: Dot(
            color=WHITE, 
            fill_color=WHITE, 
            stroke_color=BLACK, 
            stroke_width=2
        ).move_to(axes.c2p(time_tracker.get_value(), error_tracker.get_value())))

        # Draw a vertical line from the dot to the x-axis
        vertical_line = always_redraw(lambda: axes.get_vertical_line(
            dot.get_bottom(), line_func=Line, color=CBlue
        ))

        # Draw the graph based on the response (acceleration)
        graph = VGroup()
        last_point = axes.c2p(0, error_tracker.get_value())
        graph.add(Line(last_point, last_point))

        response_velocity = 0

        def update_graph(mob):
            nonlocal response_velocity
            new_time = time_tracker.get_value()
            dt = new_time - last_point[0]
            response = pid_response(new_time)
            new_error = error_tracker.get_value() + (response_velocity * dt + .5 * response * dt**2)
            response_velocity += response * dt

            # Update trackers
            integral_tracker.set_value(integral_tracker.get_value() + error_tracker.get_value() * dt)
            derivative_tracker.set_value(response_velocity)

            # Update error tracker
            error_tracker.set_value(new_error)

            # Print the current y-value (error)
            print(f"Time: {new_time:.2f}, Error: {new_error:.2f}, Integral: {integral_tracker.get_value():.2f}, Derivative {derivative_tracker.get_value():.6f}")

            # Create the next segment of the graph
            new_point = axes.c2p(new_time, new_error)
            mob.add(Line(last_point, new_point, color=COrange))
            last_point[:] = new_point

        graph.add_updater(update_graph)

        # Add elements to the scene
        self.play(Create(axes), Write(pid_constants), Write(x_label), Write(y_label))
        self.add(graph, dot, vertical_line)
        self.play(time_tracker.animate.set_value(10), run_time=10, rate_func=linear)
        self.wait(2)

        # Clear graph and switch values
        newP = 0.0001  # Proportional gain
        newI = -0.00000001 # Integral gain
        newD = 0.05  # Derivative gain #-0.00005

        # Fade out the graph and reset the dot to the original point
        graph.clear_updaters()
        self.play(FadeOut(graph), time_tracker.animate.set_value(0), error_tracker.animate.set_value(1.5),
                  Transform(pid_constants, MathTex(
                        f"P = {newP:.3f} \\quad I = {newI:.5f} \\quad D = {newD:.5f}",
                        substrings_to_isolate=["P", "I", "D"]
                    ).to_edge(UP).set_color(BLACK).shift(DOWN)),
                  run_time=3)
        
        integral_tracker.set_value(0)
        derivative_tracker.set_value(0)
        response_velocity = 0
        
        # Update PID constants
        
        pid_constants.set_color_by_tex("P", RED)
        pid_constants.set_color_by_tex("I", GREEN)
        pid_constants.set_color_by_tex("D", BLUE)

        # Update the PID constants
        P = newP
        I = newI
        D = newD

        # Draw the graph again with the new constants
        graph = VGroup()
        last_point = axes.c2p(0, error_tracker.get_value())
        graph.add(Line(last_point, last_point))
        graph.add_updater(update_graph)

        self.add(graph)
        self.play(time_tracker.animate.set_value(10), run_time=10, rate_func=linear)
        self.wait(1)

         # Clear graph and switch values
        newP = 0.001  # Proportional gain
        newI = 0.00000001 # Integral gain
        newD = 0.05  # Derivative gain #-0.00005

        # Fade out the graph and reset the dot to the original point
        graph.clear_updaters()
        self.play(FadeOut(graph), time_tracker.animate.set_value(0), error_tracker.animate.set_value(1.5),
                  Transform(pid_constants, MathTex(
                        f"P = {newP:.3f} \\quad I = {newI:.5f} \\quad D = {newD:.5f}",
                        substrings_to_isolate=["P", "I", "D"]
                    ).to_edge(UP).set_color(BLACK).shift(DOWN)),
                  run_time=3)
        
        integral_tracker.set_value(0)
        derivative_tracker.set_value(0)
        response_velocity = 0
        
        # Update PID constants
        
        pid_constants.set_color_by_tex("P", RED)
        pid_constants.set_color_by_tex("I", GREEN)
        pid_constants.set_color_by_tex("D", BLUE)

        # Update the PID constants
        P = newP
        I = newI
        D = newD

        # Draw the graph again with the new constants
        graph = VGroup()
        last_point = axes.c2p(0, error_tracker.get_value())
        graph.add(Line(last_point, last_point))
        graph.add_updater(update_graph)

        self.add(graph)
        self.play(time_tracker.animate.set_value(10), run_time=10, rate_func=linear)
        self.wait(1)

        
class DiffEq(Scene):
    def construct(self):
        CustomBackground(self)

        # Initial equation
        main_eq = MathTex(r"m a = -k x - \beta v", color=BLACK, font_size=100)
        main_eq.become(SplitTexMany(main_eq, [1, 5, 8, 12, 18]))

        # Transformed equation
        transformed_eq = MathTex(r"m a = -k x - \beta v", color=BLACK, font_size=70)
        transformed_eq.become(SplitTexMany(transformed_eq, [1, 5, 8, 12, 18]))


        # Display the main equation
        self.play(Write(main_eq), run_time=2)
        self.wait(1)

        # Transform the equation: move it up and shrink it
        self.play(Transform(main_eq, transformed_eq.to_edge(UP).shift(DOWN)))
        self.wait(1)

        # Create axes
        axes = Axes(
            x_range=[0, 10, 1],
            y_range=[-2, 2, 0.5],
            axis_config={
                "color": CBlue,
                "include_ticks": True,
                "include_tip": False
            }
        ).scale(0.8).to_edge(DOWN)

        # Damped system equation: critically damped
        def damped_system(t):
            return np.exp(-t)

        # Plot the damped system graph
        graph = axes.plot(damped_system, color=COrange)

        # Fade in the graph below the equation
        self.play(FadeIn(axes), Create(graph), run_time=3)
        self.wait(2)

        newTex = MathTex(r"m a = k x + \beta v", color=BLACK, font_size=100)
        newTex.become(SplitTexMany(newTex, [1, 3, 5, 7, 9, 12, 17]))


        #Fade out graph and recenter
        self.play(FadeOut(axes), FadeOut(graph), 
                  Transform(main_eq, newTex),
                  run_time=2)
        
        self.play(Emphasize(main_eq[1]))
        self.play(Emphasize(main_eq[4]))
        self.play(Emphasize(main_eq[7]))

        self.wait(1)

        #Divide by M
        p_text = ReplaceTex(main_eq[3], r"P", shift= (0,-.1,0))
        d_text = ReplaceTex(main_eq[6], r"D", shift= (0,-.1,0))

        # self.play(FadeOut(main_eq[0]), Transform(main_eq[3], ReplaceTex(main_eq[3], r"\frac{k}{m}")),
        #           Transform(main_eq[6], ReplaceTex(main_eq[6], r"\frac{\beta}{m}")))
        # self.wait(1)

        #Replace with P and D
        self.play(Transform(main_eq[3], p_text),
                  Transform(main_eq[6], d_text))
        self.wait(1)
