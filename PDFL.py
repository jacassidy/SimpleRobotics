from manim import *
from manium import *
from scipy.integrate import quad  # Import quad from scipy

class ForceAssumption(Scene):
    def construct(self):
        CustomBackground(self)
        equasion = MathTex(r"F = \alpha \cdot Power", color = BLACK, font_size = 90)
        equasion.move_to(ORIGIN)
        self.wait(1)
        self.play(Write(equasion), run_time = 3.5)
        self.wait(5)
        self.play(FadeOut(equasion))
        self.wait(1)

class PID(Scene):
    def construct(self):
        CustomBackground(self)
        
        # Write in PID text
        P_text = MathTex("P", color=BLACK, font_size=100)
        I_text = AddTex(P_text, "I")
        D_text = AddTex(I_text, "D")

        PID_text_group = VGroup(P_text, I_text, D_text)
        PID_text_group.move_to((0, 0, 0))
        self.wait(.5)
        self.play(Write(P_text), Write(I_text), Write(D_text), run_time = 2)
        self.wait(4.5)

        # Break down PID acronym
        proportional_text = MathTex("Porportional", color=BLACK, font_size=40).move_to((-4, 1, 0))
        integral_text = MathTex("Integral", color=BLACK, font_size=40).move_to((0, 1, 0))
        differential_text = MathTex("Differential", color=BLACK, font_size=40).move_to((4, 1, 0))

        proportional_text = SplitTex(proportional_text, 1, aligned_edge=UP, space_buff = False)
        integral_text = SplitTex(integral_text, 1, aligned_edge=UP, space_buff = False)
        differential_text = SplitTex(differential_text, 1, aligned_edge=UP, space_buff = False)

        self.play(Transform(P_text, proportional_text[0]), FadeIn(proportional_text[1]))
        self.wait(.5)
        self.play(Transform(I_text, integral_text[0]), FadeIn(integral_text[1]))
        self.wait(.5)
        self.play(Transform(D_text, differential_text[0]), FadeIn(differential_text[1]))

        self.wait(3)

        #Show tunable weights
        kp = MathTex(r"k_P", color = BLACK, font_size = 100).next_to(proportional_text, DOWN, buff = .3)
        ki = MathTex(r"k_I", color = BLACK, font_size = 100).next_to(integral_text, DOWN, buff = .3)
        kd = MathTex(r"k_D", color = BLACK, font_size = 100).next_to(differential_text, DOWN, buff = .3)

        self.play(FadeIn(kp), FadeIn(ki), FadeIn(kd))
        self.wait(1.5)
        self.play(FadeOut(kp), FadeOut(ki), FadeOut(kd))
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
        self.play(p_x_tracker.animate.set_value(p_axes.x_range[1]), run_time=6)
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
        self.wait(6)

        # Animate the filling of the area from left to right
        self.play(FadeIn(i_dot), Write(i_area_value_display), FadeIn(i_area))
        self.play(i_x_tracker.animate.set_value(2 * PI), run_time=10)
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
        self.wait(1)
        self.play(d_x_tracker.animate.set_value(6 * PI), run_time=8, rate_func=linear)
        d_derivative_value_display.clear_updaters()
        self.play(FadeOut(d_dot), FadeOut(d_derivative_value_display), FadeOut(d_vector))
        self.wait(2)

        # Fade everything out at the end
        all_objects = VGroup(
            P_text, I_text, D_text,
            proportional_text, integral_text, differential_text,
            p_axes, p_graph, p_x_label, p_y_label,
            i_axes, i_sine_graph, i_x_label, i_y_label, i_area,
            d_axes, d_sine_graph, d_x_label, d_y_label,
        )

        self.play(FadeOut(all_objects))
        self.wait(1)
        
        #Create full equasion
        res = MathTex(r"Response =", color = BLACK, font_size = 80)
        p_comp = AddTex(res, "x \cdot k_P", aligned_edge=UP)
        first_plus = AddTex(p_comp, "+", aligned_edge=UP)
        i_comp = AddTex(first_plus, "A \cdot k_I", aligned_edge=UP)
        second_plus = AddTex(i_comp, "+", aligned_edge=UP)
        d_comp = AddTex(second_plus, "v \cdot k_D", aligned_edge=UP)

        full_equasion = VGroup(res, p_comp, first_plus, i_comp, second_plus, d_comp).move_to((0,0,0))

        p_equation.become(SplitTex(p_equation, 3))
        i_equation.become(SplitTex(i_equation, 3))
        d_equation.become(SplitTex(d_equation, 3))

        self.play(FadeOut(p_equation[0]), FadeOut(i_equation[0]), FadeOut(d_equation[0]),
                  Transform(p_equation[1], p_comp), 
                  Transform(i_equation[1], i_comp),
                  Transform(d_equation[1], d_comp),
                  FadeIn(first_plus), FadeIn(second_plus), FadeIn(res), run_time = 2.3
                  )
        self.wait(6)

        #Make values negative
        resCop = res.copy()

        self.play(Transform(p_equation[1], ReplaceTex(p_equation[1], "-x \cdot k_P").scale(.8).shift(LEFT * .2)),
                  Transform(i_equation[1], ReplaceTex(i_equation[1], "-A \cdot k_I").scale(.8).shift(LEFT * .2)),
                )
        self.wait(.5)
        self.play(                  Transform(d_equation[1], ReplaceTex(d_equation[1], "-v \cdot k_D").scale(.8).shift(LEFT * .2)),
)
        self.wait(2)
        self.play(                Transform(res, ReplaceTex(res, "-Response =").scale(.8).shift(LEFT * .2)))

        self.wait(4)
        #Transform back
        self.play(Transform(p_equation[1], p_comp), 
                  Transform(i_equation[1], i_comp),
                  Transform(d_equation[1], d_comp),
                  Transform(res, resCop))

        self.play(FadeOut(res), FadeOut(first_plus), FadeOut(second_plus), FadeOut(p_equation[1]), FadeOut(i_equation[1]), FadeOut(d_equation[1]))
        self.wait(6)
        
class PIDDemo(Scene):
    def construct(self):
        CustomBackground(self)

        # PID constants
        P = 0.0001  # Proportional gain
        I = 0  # Integral gain
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
                        f"k_P = {0.01} \\quad k_I = {0.00} \\quad k_D = {0.00}",
                        substrings_to_isolate=["k_P", "k_I", "k_D"]
                    ).to_edge(UP).set_color(BLACK).shift(DOWN)
        
        pid_constants.set_color_by_tex("k_P", RED)
        pid_constants.set_color_by_tex("k_I", GREEN)
        pid_constants.set_color_by_tex("k_D", BLUE)

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
        ).move_to(axes.c2p(time_tracker.get_value(), error_tracker.get_value()))).set_z_index(10)

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
        self.play(Create(axes), Write(pid_constants), Write(x_label), Write(y_label), run_time = 3)
        self.wait(.2)
        self.add(graph, dot, vertical_line)
        self.wait(6)
        self.play(time_tracker.animate.set_value(10), run_time=14.5, rate_func=linear)
        self.wait(.5)

        # Clear graph and switch values
        newP = 0.0001  # Proportional gain
        newI = -0.00000001 # Integral gain
        newD = 0.05  # Derivative gain #-0.00005

        # Fade out the graph and reset the dot to the original point
        graph.clear_updaters()
        self.play(FadeOut(graph), time_tracker.animate.set_value(0), error_tracker.animate.set_value(1.5),
                  run_time=3)
        
        self.wait(1)
        newHighTex = MathTex(
                        f"k_P = {0.01} \\quad k_I = {0.00} \\quad k_D = {5.00}",
                        substrings_to_isolate=["k_P", "k_I", "k_D"]
                    ).to_edge(UP).set_color(BLACK).shift(DOWN)
        
        newHighTex.set_color_by_tex("k_P", RED)
        newHighTex.set_color_by_tex("k_I", GREEN)
        newHighTex.set_color_by_tex("k_D", BLUE)

        self.play(Transform(pid_constants, newHighTex))
        
        self.wait(1)
        
        # integral_tracker.set_value(0)
        # derivative_tracker.set_value(0)
        response_velocity = 0
        
        # Update PID constants
        
        

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
        self.play(time_tracker.animate.set_value(10), run_time=13, rate_func=linear)
        self.wait(1)

         # Clear graph and switch values
        newP = 0.001  # Proportional gain
        newI = 0.00000001 # Integral gain
        newD = 0.05  # Derivative gain #-0.00005

        # Fade out the graph and reset the dot to the original point
        graph.clear_updaters()
        self.play(FadeOut(graph), time_tracker.animate.set_value(0), error_tracker.animate.set_value(1.5),
                  
                  run_time=3)
        
        self.wait(1)
        newHighTex = MathTex(
                        f"k_P = {0.1} \\quad k_I = {0.00} \\quad k_D = {5.00}",
                        substrings_to_isolate=["k_P", "k_I", "k_D"]
                    ).to_edge(UP).set_color(BLACK).shift(DOWN)
        
        newHighTex.set_color_by_tex("k_P", RED)
        newHighTex.set_color_by_tex("k_I", GREEN)
        newHighTex.set_color_by_tex("k_D", BLUE)

        self.play(Transform(pid_constants, newHighTex))
        
        self.wait(1)
        
        # integral_tracker.set_value(0)
        # derivative_tracker.set_value(0)
        response_velocity = 0
        
        # Update PID constants
        
        pid_constants.set_color_by_tex("k_P", RED)
        pid_constants.set_color_by_tex("k_I", GREEN)
        pid_constants.set_color_by_tex("k_D", BLUE)

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
        self.play(time_tracker.animate.set_value(10), run_time=4, rate_func=linear)
        self.wait(1)

        
class DiffEq(Scene):
    def construct(self):
        CustomBackground(self)

        # Initial equation
        main_eq = MathTex(r"m a = k x + \beta v", color=BLACK, font_size=100)
        main_eq.become(SplitTexMany(main_eq, [3, 5, 7, 9, 12, 17]))

        # Transformed equation
        transformed_eq = MathTex(r"m a = k x + \beta v", color=BLACK, font_size=70)
        transformed_eq.become(SplitTexMany(transformed_eq, [3, 5, 7, 9, 12, 17]))


        # Display the main equation
        self.wait(1)
        self.play(Write(main_eq), run_time=3)
        self.wait(2)

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
            # if t < 1:
            #     return 2
            return np.exp(-((t)*10)) * 2

        # Plot the damped system graph
        graph = axes.plot(damped_system, color=COrange)

        # Fade in the graph below the equation
        self.play(FadeIn(axes), Create(graph), run_time=3)
        self.wait(10)

        newTex = MathTex(r"m a = k x + \beta v", color=BLACK, font_size=100)
        newTex.become(SplitTexMany(newTex, [3, 5, 7, 9, 12, 17]))


        #Fade out graph and recenter
        self.play(FadeOut(axes), FadeOut(graph), 
                  Transform(main_eq, newTex),
                  run_time=2)
        
        self.wait(3)
        
        self.play(Emphasize(main_eq[0], scale_factor= .5), run_time = 2.5)
        # replace ma with F
        force = MathTex("F", color = BLACK, font_size = 100).next_to(main_eq[0].get_left(), RIGHT, buff = .2)
        new_text_group = VGroup(main_eq[0], main_eq[1],main_eq[2],main_eq[3],main_eq[4], main_eq[5], main_eq[6])
        self.play(Transform(main_eq[0], force))
        self.play(new_text_group.animate.move_to((0,0,0)))

        self.wait(.5)

        p_group = VGroup(main_eq[3], main_eq[2])
        d_group = VGroup(main_eq[5], main_eq[6])
        self.play(Emphasize(p_group, scale_factor= .5), run_time = 2)
        self.play(Emphasize(main_eq[4],scale_factor= .5), run_time = 2)
        self.play(Emphasize(d_group, scale_factor= .5), run_time = 2)
        self.wait(1)

        #Replace with P and D
        p_text = ReplaceTex(main_eq[2], r"k_P", shift= (-.15,-.1,0))
        d_text = AddTex(main_eq[4], r"k_D", shift= (0,-.1,0)).set_color(BLACK)

        pd_equasion = MathTex(r"Response = x \cdot k_P + v \cdot k_D", color = BLACK, font_size = 60).move_to((0,1,0))
        
        self.play(Transform(main_eq[2], p_text),
                  Transform(main_eq[5], d_text))
        self.play(main_eq.animate.move_to((0,-.5, 0)),
                  FadeIn(pd_equasion),
                    run_time = 2)
        self.wait(1)

class FL(Scene):
    def construct(self):
        CustomBackground(self)

        #Add Gravity and friction
        gravity = MathTex("Gravity", color = BLACK, font_size = 80).move_to((-3.5,1.5, 0))

        friction = MathTex("Friction", color = BLACK, font_size = 80).move_to((3.5,1.5, 0))
        self.wait(1)
        self.play(FadeIn(gravity), FadeIn(friction))
        self.wait(6)

        #Add assumption
        equasion = MathTex(r"F = \alpha \cdot Power", color = BLACK, font_size = 90)
        equasion.move_to(ORIGIN)
        self.wait(1)
        self.play(Write(equasion), run_time = 3.5)
        self.wait(3)

        #move assumption down
        moved_equasion = MathTex(r"F = \alpha \cdot Power", color = BLACK, font_size = 90).scale(.4).move_to((0,-2,0))

        self.play(Transform(equasion, moved_equasion))
        self.wait(2)

        #Add equasions for gravity and friction
        gravity_equasion = MathTex(r"\frac{G}{\alpha} = P_G", font_size = 40, color = BLACK).next_to(gravity, DOWN, buff = .3)
        friction_equasion = MathTex(r"\frac{F}{\alpha} = P_f", font_size = 40, color = BLACK).next_to(friction, DOWN, buff = .3)

        self.play(FadeIn(gravity_equasion), FadeIn(friction_equasion))
        self.wait(7.5)

        # Add arrow pointing up below gravity equation
        gravity_arrow = Arrow(start=UP, end=DOWN, color=CBlue).next_to(gravity_equasion , DOWN, buff=0.2)
        self.play(FadeIn(gravity_arrow))
        self.wait(1)

        # Add two arrows pointing into each other below friction equation
        friction_arrow_down = Arrow(start=UP, end=DOWN, color=CBlue).scale(.5).next_to(friction_equasion, DOWN, buff=0.2)
        friction_arrow_up = Arrow(start=DOWN, end=UP, color=CBlue).scale(.5).next_to(friction_arrow_down, DOWN, buff=0.2)
        self.play(FadeIn(friction_arrow_down), FadeIn(friction_arrow_up))
        self.wait(4.3)

        #FF and LL tex

        FF = Text("Feed Forward", color= BLACK, font_size=60).next_to(gravity_arrow, DOWN, buff =1)
        LL = Text("Lower Limit", color= BLACK, font_size=60).next_to(friction_arrow_up, DOWN, buff =1)

        self.play(FadeIn(FF), FadeIn(LL))
        self.wait(2)

        # Fade everything out
        all_objects = VGroup(gravity, friction, equasion, gravity_equasion, friction_equasion,
                             gravity_arrow, friction_arrow_down, friction_arrow_up, FF, LL)
        self.play(FadeOut(all_objects))
        self.wait(2)

    
from manim import *

class TransitionPIDDemo(Scene):
    def construct(self):
        CustomBackground(self)

        # PID constants for the last graph
        P = 0.001  # Proportional gain
        I = 0.00000001  # Integral gain
        D = 0.05  # Derivative gain

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
                "color": CBlue,  # Change axes color to BLUE
                "include_ticks": True,
                "include_tip": False
            }
        ).scale(0.8).move_to(DOWN)

        x_label = axes.get_x_axis_label(Text("Time", color=BLACK).scale(0.5))
        y_label = axes.get_y_axis_label(Text("Error", color=BLACK).scale(0.5))

        # Display the PID constants above the graph with colored P, I, D
        pid_constants = MathTex(
                        f"k_P = {0.1} \\quad k_I = {0.00} \\quad k_D = {5.00}",
                        substrings_to_isolate=["k_P", "k_I", "k_D"]
                    ).to_edge(UP).set_color(BLACK).shift(DOWN)
        
        pid_constants.set_color_by_tex("k_P", RED)
        pid_constants.set_color_by_tex("k_I", GREEN)
        pid_constants.set_color_by_tex("k_D", BLUE)

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
        ).move_to(axes.c2p(time_tracker.get_value(), error_tracker.get_value()))).set_z_index(10)

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
            mob.add(Line(last_point, new_point, color=ORANGE))
            last_point[:] = new_point

        graph.add_updater(update_graph)

        # Add elements to the scene
        self.play(Create(axes), Write(pid_constants), Write(x_label), Write(y_label), run_time=3)
        self.wait(0.2)
        self.add(graph, dot)
        self.play(time_tracker.animate.set_value(10), run_time=4, rate_func=linear)
        self.wait(1)

        # Fade out everything
        self.play(FadeOut(VGroup(axes, pid_constants, x_label, y_label, graph, dot)), run_time=3)
        self.wait(1)

        #Write in why PID
        WhyI = Text("Why is there an I in PID?", color = BLACK, font_size= 60)
        self.play(Write(WhyI, run_time = 2))
        self.wait(2)
        self.play(FadeOut(WhyI))
        self.wait(1)

class TransitionFFLL(Scene):
    def construct(self):
        CustomBackground(self)
        #Write in why PID
        WhyI = Text("Feed Forward and Lower Limit", color = BLACK, font_size= 60)
        self.play(Write(WhyI, run_time = 2))
        self.wait(2)
        self.play(FadeOut(WhyI))
        self.wait(1)

class TransitionWhatIsPID(Scene):
    def construct(self):
        CustomBackground(self)
        #Write in why PID
        WhyI = Text("What is a PID?", color = BLACK, font_size= 60)
        self.play(Write(WhyI, run_time = 2))
        self.wait(2)
        self.play(FadeOut(WhyI))
        self.wait(1)

class Regression(Scene):
    def construct(self):
        # Create axes
        axes = Axes(
            x_range=[0, 10, 1],  # x-axis from 0 to 10
            y_range=[0, 10, 1],  # y-axis from 0 to 10
            axis_config={
                "color": BLUE,
                "include_ticks": False,
                "include_tip": False
            }
        )
        #.add_coordinates().scale(0.8).to_edge(DOWN)

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
        x_label = axes.get_x_axis_label(Text("X", color=WHITE).scale(0.5))
        y_label = axes.get_y_axis_label(Text("Y", color=WHITE).scale(0.5))

        # Add elements to the scene
        self.play(Create(axes), Write(x_label), Write(y_label))
        self.play(FadeIn(dots))
        self.play(Create(regression_line))
        self.wait(2)

class WrapUp(Scene):
    def construct(self):
        CustomBackground(self)

        # Write in PID text
        P_text = MathTex("P", color=BLACK, font_size=100)
        D_text = AddTex(P_text, "D")
        F_text = AddTex(D_text, "F")
        L_text = AddTex(F_text, "L")


        PID_text_group = VGroup(P_text, D_text, F_text, L_text)
        PID_text_group.move_to((0, 0, 0))

        # Break down PID acronym
        proportional_text = MathTex("Porportional", color=BLACK, font_size=40).move_to((-5, 1.5, 0))
        differential_text = MathTex("Differential", color=BLACK, font_size=40).move_to((-1.5, 1.5, 0))
        ff_text = MathTex("Feed Forward", color=BLACK, font_size=40).move_to((1.5, 1.5, 0))
        ll_text = MathTex("Lower Limit", color=BLACK, font_size=40).move_to((5, 1.5, 0))


        proportional_text = SplitTex(proportional_text, 1, aligned_edge=UP, space_buff = False)
        differential_text = SplitTex(differential_text, 1, aligned_edge=UP, space_buff = False)
        ff_text = SplitTex(ff_text, 1, aligned_edge=UP, space_buff = False)
        ll_text = SplitTex(ll_text, 1, aligned_edge=UP, space_buff = False)

        self.wait(1)
        self.play(FadeIn(proportional_text), FadeIn(differential_text), FadeIn(ff_text), FadeIn(ll_text))
        self.wait(1)
        self.play(Transform(proportional_text[0], P_text), FadeOut(proportional_text[1]))
        self.play(Transform(differential_text[0], D_text), FadeOut(differential_text[1]))
        self.play(Transform(ff_text[0], F_text), FadeOut(ff_text[1]))
        self.play(Transform(ll_text[0], L_text), FadeOut(ll_text[1]))

        self.wait(2)
        self.play(FadeOut(proportional_text[0]),
                  FadeOut(differential_text[0]),
                  FadeOut(ff_text[0]),
                  FadeOut(ll_text[0]))
        self.wait(1)

class Thumbnail(Scene):
    def construct(self):
        
        PDFL = MathTex("PDFL", font_size = 100)

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
            # if t < 1:
            #     return 2
            return np.exp(-((t)*10)) * 2

        # Plot the damped system graph
        graph = axes.plot(damped_system, color=COrange)
        PDFL.next_to(graph, UP, buff = .5)
        system = VGroup(axes, graph, PDFL).move_to((0,0,0))
        # Fade in the graph below the equation
        self.play(FadeIn(axes), Create(graph), Write(PDFL), run_time=3)
        self.wait(10)