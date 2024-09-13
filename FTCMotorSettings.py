from manim import *
from manium import *


class TagLine(Scene):
    def construct(self):
          # Colors
        blue = CBlue
        orange = COrange
        
        # Text elements
        title = Text("Simple Robotics", font_size=72, color=BLACK)
        tagline = Text("We're here to make this simple.", font_size=36, color=BLACK)
        svg_object = SVGMobject("Tet.svg")
        svg_object.set_color(BLACK)
        
        # Positioning the elements
        title.shift(UP * 0.5)
        tagline.shift(DOWN * 0.5)
        
        # Background rectangle to emphasize the text
        CustomBackground(self)
        # Create a writing effect for the title
        self.play(Write(title), run_time=1.5)
        
        # Swoop in effect for tagline
        self.play(FadeIn(tagline))
        
        # Fill effect for title and tagline
        self.play(
            title.animate.set_color(blue),
            tagline.animate.set_color(orange),
            run_time=1
        )

        self.wait(1)

        self.play(Write(svg_object))
        
        # Fade out everything
        self.play(FadeOut(title), FadeOut(tagline), FadeOut(svg_object), run_time=1)

class Thumbnail(Scene):
    def construct(self):
        #Draw in motors
        motor1 = SVGMobject("GobuildaAtt2.svg").scale(1.5).move_to((-4,-.1,0)).set_color(CBlue)
        motor2 = SVGMobject("GobuildaAtt2.svg").scale(1.5).move_to((0,-.1,0)).set_color(WHITE)
        motor3 = SVGMobject("GobuildaAtt2.svg").scale(1.5).move_to((4,-.1,0)).set_color(COrange)

        self.play(Write(motor1), Write(motor2), Write(motor3), run_time = 4)
        self.wait(1.5)

        #Write in text above motors
        rWe = Text("Run Without Encoder", color = WHITE, font_size= 25).next_to(motor1, UP, buff = .25)
        rWOe = Text("Run With Encoder", color = WHITE, font_size= 25).next_to(motor2, UP, buff = .25)
        rPos = Text("Run To Position", color = WHITE, font_size= 25).next_to(motor3, UP, buff = .25)

        self.play(Write(rWe))
        self.wait(1)
        self.play(Write(rWOe))
        self.wait(1)
        self.play(Write(rPos))
        self.wait(4)

        #Fade out everything
        self.play(FadeOut(rWe), FadeOut(rWOe), FadeOut(rPos), FadeOut(motor1), FadeOut(motor2), FadeOut(motor3))
        self.wait(1)

class Settings(Scene):
    def construct(self):
        CustomBackground(self)

        #Draw in motors
        motor1 = SVGMobject("GobuildaAtt2.svg").scale(1.5).move_to((-4,-.1,0)).set_color(BLACK)
        motor2 = SVGMobject("GobuildaAtt2.svg").scale(1.5).move_to((0,-.1,0)).set_color(BLACK)
        motor3 = SVGMobject("GobuildaAtt2.svg").scale(1.5).move_to((4,-.1,0)).set_color(BLACK)

        self.play(Write(motor1), Write(motor2), Write(motor3), run_time = 4)
        self.wait(1.5)

        #Write in text above motors
        rWe = Text("Run Without Encoder", color = BLACK, font_size= 50).next_to(motor1, UP, buff = 1)
        rWOe = Text("Run With Encoder", color = BLACK, font_size= 50).next_to(motor2, UP, buff = 1)
        rPos = Text("Run To Position", color = BLACK, font_size= 50).next_to(motor3, UP, buff = 1)

        self.play(Write(rWe))
        self.wait(1)
        self.play(Write(rWOe))
        self.wait(1)
        self.play(Write(rPos))
        self.wait(4)

        #Fade out everything
        self.play(FadeOut(rWe), FadeOut(rWOe), FadeOut(rPos), FadeOut(motor1), FadeOut(motor2), FadeOut(motor3))
        self.wait(1)

class MotorCurrent(Scene):
    def construct(self):
        CustomBackground(self)
        # Create stator (outer part of the motor)
        stator = Circle(radius=2, color=DARK_GRAY, stroke_width=6)

        # Create rotor (slightly smaller inner rotating part of the motor)
        rotor = Circle(radius=0.8, color=DARK_GRAY, stroke_width=4)

        self.play(Create(rotor), Create(stator))

        # Create 8 lines going from the rotor to the stator
        for i in range(8):
            angle = i * PI / 4  # Divide circle into 8 parts (360 degrees / 8)
            start = [0.8 * np.cos(angle), 0.8 * np.sin(angle), 0]  # Start point on rotor
            end = [2 * np.cos(angle), 2 * np.sin(angle), 0]  # End point on stator
            line = Line(start=start, end=end, color=DARK_GRAY, stroke_width=3)
            self.play(Create(line), run_time = .2)

        #Create Wires
        length = 1

        redStart = 2 *unitVector(PI/2 + PI/3)
        redEnd = redStart + np.array([-length, 0, 0])
        red_wire = Line(redStart, redEnd, stroke_width = 12, color = RED, cap_style = constants.CapStyleType.ROUND)
        blackStart = 2 * unitVector(-PI/2 + -PI/3)
        blackEnd = blackStart + np.array([-length, 0, 0])
        black_wire = Line(blackStart, blackEnd, stroke_width = 12, color = BLACK, cap_style = constants.CapStyleType.ROUND)

        red_wire.set_z_index(0)
        black_wire.set_z_index(0)

        self.play(Create(red_wire), Create(black_wire))

        # Hold the diagram on screen
        self.wait(2)


        # Create arrows indicating the magnetic field direction due to current
        arrowLength = 1

        redEnd -= np.array([.2, 0, 0])
        blackEnd -= np.array([.2, 0, 0])

        current_arrow_1 = Arrow(start=redEnd+ np.array([-arrowLength,0,0]), end=redEnd, buff=-0.0, color=CBlue, stroke_width=6)
        current_arrow_2 = Arrow(start=blackEnd , end=blackEnd + np.array([-arrowLength,0,0]), buff=-0.0, color=CBlue, stroke_width=6)
        
        self.play(FadeIn(current_arrow_1), FadeIn(current_arrow_2))

        self.wait(2)

        #Add in position tracker
        currentAngle = ValueTracker(2 * PI/3)

        rotation_arrow = CurvedArrow(start_point=[-1, 1, 0], end_point=[1, 1, 0], color=COrange, angle = -PI/2, stroke_width=8)
        rotor_position_line = always_redraw(lambda: Line((0,0,0), .8 * unitVector(currentAngle.get_value()), 
                                                         color = COrange, stroke_width = 6,cap_style = constants.CapStyleType.ROUND))

        self.play(FadeIn(rotor_position_line), FadeIn(rotation_arrow))
        self.wait(2)
        
        #Animate clockwise
        self.play(currentAngle.animate.set_value(-8 * PI+ 2 * PI/3), run_time = 4.5)

        self.wait(2)

        #Reverse current arrows
        self.play(current_arrow_1.animate.put_start_and_end_on(redEnd, redEnd+ np.array([-arrowLength,0,0])),
                  current_arrow_2.animate.put_start_and_end_on(blackEnd + np.array([-arrowLength,0,0]), blackEnd))
        
        self.wait(1)
        #Reverse direction arrow
        self.play(Transform(rotation_arrow, CurvedArrow(start_point=[1, 1, 0], end_point=[-1, 1, 0], color=COrange, angle = PI/2, stroke_width=8)))

        self.wait(1)

        #Animate coutner clockwise
        self.play(currentAngle.animate.set_value(2 * PI/3), run_time = 4.5)

        self.wait(2)

        #Increase Current
        self.play(current_arrow_1.animate.set_stroke(width = 10),
                  current_arrow_2.animate.set_stroke(width = 10))
        
        self.wait(1)

        self.play(rotation_arrow.animate.set_stroke(width = 16))
        
        self.wait(1)

        #Moves P fast
        self.play(currentAngle.animate.set_value(40 * PI + 2 * PI/3), run_time = 4.5)

        self.wait(2)

        #Add in text bellow

        mainText = Text("motor.setPower(P)", color = BLACK, font_size= 40)

        #Add in asterisk for later trust
        asterisk = Text("*", color = BLACK, font_size= 40).next_to(mainText, RIGHT, buff = 0).shift((0.05, .3, 0))

        vgroup = VGroup(mainText, asterisk)
        vgroup.move_to((0,-2.8, 0))
        vgroup.move_to((0, mainText.get_center()[1], 0))

        #mainText.move_to((0,-2.8, 0))

        self.play(Write(mainText), 
                  current_arrow_1.animate.set_stroke(width = 6),
                  current_arrow_2.animate.set_stroke(width = 6),
                  rotation_arrow.animate.set_stroke(width = 8))

        #Add p = above
        velocityTracker = ValueTracker(0)
        p_value_tracker = ValueTracker(0)

        def update_P():
            p_value_tracker.set_value(velocityTracker.get_value() * 0.5)
            return MathTex(rf"P = {p_value_tracker.get_value():.2f}", color = BLACK, font_size = 40).move_to((0, 2.5,0))

        p_value_visual = always_redraw(update_P)

        self.play(Write(p_value_visual))

        #Make things in image respond power
        currentAngle.add_updater(lambda t: t.set_value(t.get_value() + velocityTracker.get_value()))
        current_arrow_1.add_updater(lambda a: a.set_stroke(width = 6 * (1 + abs(p_value_tracker.get_value()))))
        current_arrow_2.add_updater(lambda a: a.set_stroke(width = 6 * (1 + abs(p_value_tracker.get_value()))))
        rotation_arrow.add_updater(lambda a: a.set_stroke(width = 8 * (1 + abs(p_value_tracker.get_value()))))
        
        self.play(velocityTracker.animate(rate_func = smooth).set_value(2), run_time = 4)
        self.play(velocityTracker.animate(rate_func = linear).set_value(0), run_time = 4)

        velocityTracker.set_value(0)

        #Swap Endpoints

        #Reverse current arrows
        current_arrow_1.put_start_and_end_on(redEnd+ np.array([-arrowLength,0,0]), redEnd)
        current_arrow_2.put_start_and_end_on(blackEnd, blackEnd + np.array([-arrowLength,0,0]))
        
        #Reverse direction arrow
        rotation_arrow.become(CurvedArrow(start_point=[-1, 1, 0], end_point=[1, 1, 0], color=COrange, angle = -PI/2, stroke_width=8))

        self.play(velocityTracker.animate(rate_func = linear).set_value(-2), run_time = 8)
        self.play(velocityTracker.animate(rate_func = smooth).set_value(0), run_time = 4)

        self.play(FadeOut(rotation_arrow))
        current_arrow_1.clear_updaters()
        current_arrow_2.clear_updaters()

        self.wait(1)

        self.play(Emphasize(mainText, scale_factor= .5), run_time = 2)
        self.wait(1)
        self.play(current_arrow_1.animate(rate_func = there_and_back_with_pause).set_stroke(width = 16),
                  current_arrow_2.animate(rate_func = there_and_back_with_pause).set_stroke(width = 12),
                   run_time = 2)


        self.wait(1)

        finalMainTextPos = vgroup[0].get_center()

        #Shift and add asterisk
        self.play(mainText.animate.move_to(finalMainTextPos), FadeIn(asterisk))
        self.wait(1)

        #Fade everything out
        self.play(FadeOut(vgroup))
        self.wait(1)

        self.play(FadeOut(*self.mobjects))

        self.wait(1)

class RWOENC(Scene):
    def construct(self):
        CustomBackground(self)

        #Draw in motors
        motor1 = SVGMobject("GobuildaAtt2.svg").scale(1.5).move_to((-3,-.1,0)).set_color(BLACK)

        #Write in text above motors
        rWe = Text("Run Without Encoder", color = BLACK, font_size= 25).next_to(motor1, UP, buff = .25)

        self.play(Write(rWe))
        #Add in motor SVG
        self.play(Write(motor1), run_time = 4)
        self.wait(1)

        image = ImageMobject("EncCable")
        image.scale(2).move_to((3,-.1,0))  # Optional scaling
        self.play(FadeIn(image))
        self.wait(2)

         # Draw arrow between the two objects
        arrow = Arrow(start=motor1.get_right(), end=image.get_left(), buff=0.1, color=COrange, stroke_width=8)
        self.play(Create(arrow), run_time=2)
        
        # Create a big 'X' over the arrow
        cross_line1 = Line(arrow.get_start()/2 + UP, arrow.get_end()/2 + DOWN, stroke_width=10, color=RED)
        cross_line2 = Line(arrow.get_end()/2 + UP, arrow.get_start()/2 + DOWN, stroke_width=10, color=RED)
        cross = VGroup(cross_line1, cross_line2)

        self.play(Create(cross), run_time=1)
        self.wait(2.5)

        # Make the 'X' fade away
        self.play(FadeOut(cross), run_time=2)
        self.wait(.5)

        # Create the checkmark using a single path (VMobject)
        checkmark = VMobject()
        checkmark.set_points_as_corners([ORIGIN, RIGHT * 0.5 + DOWN * 0.5, RIGHT * 1.5 + UP * 0.5])
        checkmark.set_stroke(color=GREEN, width=10)

        # Position the checkmark below the arrow
        checkmark.move_to(arrow.get_center() + DOWN * 1.5)

        # Fade in the green checkmark
        self.play(Create(checkmark), run_time=2)
        self.wait(9)
        self.play(FadeOut(*self.mobjects))

class RWENC(Scene):
    def construct(self):
        CustomBackground(self)

        #Draw in motors
        motor1 = SVGMobject("GobuildaAtt2.svg").scale(1.5).move_to((-3,-.1,0)).set_color(BLACK)

        #Write in text above motors
        rWe = Text("Run With Encoder", color = BLACK, font_size= 25).next_to(motor1, UP, buff = .25)

        self.play(Write(rWe))
        #Add in motor SVG
        self.play(Write(motor1), run_time = 4)
        self.wait(1)

        image = ImageMobject("EncCable")
        image.scale(1).move_to((-1.8,-1.3,0))  # Optional scaling
        self.play(FadeIn(image))
        self.wait(2)

        runWithEncoder = Text("motor.setPower()", color= BLACK, font_size = 30).move_to((2, 1.8, 0))
        motorSetPow = Text("power", color= BLACK, font_size = 50).move_to((2, -1.8, 0))

        self.play(Write(runWithEncoder), Write(motorSetPow))
        self.wait(2)

         # Draw arrow between the two objects

        arrow = Arrow(start=runWithEncoder.get_bottom(), end=motorSetPow.get_top(), buff=0.1, color=CBlue, stroke_width=5)
        self.play(Create(arrow), run_time=2)
        
        # Create a big 'X' over the arrow
        cross_line1 = Line(arrow.get_start() + RIGHT, arrow.get_end() + LEFT, stroke_width=8, color=RED)
        cross_line2 = Line(arrow.get_start() + LEFT, arrow.get_end() + RIGHT, stroke_width=8, color=RED)
        cross = VGroup(cross_line1, cross_line2)

        self.play(Write(cross_line1), Write(cross_line2))

        self.wait(12)

        self.play(FadeOut(*self.mobjects))


class BurnOut(Scene):
    def construct(self):
        CustomBackground(self)

        # Scale factor (0.8 of the original size)
        scale_factor = 0.8

        # Set up independent ValueTrackers for each motor
        motor_1_tracker = ValueTracker(0)
        motor_2_tracker = ValueTracker(0)

        # First motor setup
        motor_1_group, stator_1 = self.create_motor_group(motor_1_tracker, scale_factor)

        motor_1_group.shift(LEFT * 3)

        # Second motor setup (initially invisible, placed on the right)
        motor_2_group, stator_2 = self.create_motor_group(motor_2_tracker, scale_factor)
        motor_2_group.shift(RIGHT * 3)

        # Fade in the second motor
        self.play(FadeIn(motor_2_group), FadeIn(motor_1_group), run_time = 2)

        #Add captions
        rWOENC = Text("Run Without Encoder", font_size = 35, color = BLACK).move_to(stator_1.get_center() + np.array([0,-2.2, 0]))
        rWENC = Text("Run With Encoder", font_size = 35, color = BLACK).move_to(stator_2.get_center() + np.array([0,-2.2, 0]))

        self.wait(5)
        #Add power of .1 at bottom
        power = Text("Power = .1", color = BLACK, font_size=45).move_to((0, -3, 0))
        self.play(Write(power))
        self.wait(1)

        self.play(Write(rWENC), Write(rWOENC))
        

        # Animate both motors independently
        self.animate_motor(stator_1.get_center(), motor_1_tracker, .1, scale_factor)
        self.wait(1)
        self.animate_motor(stator_2.get_center(), motor_2_tracker, .1, scale_factor, run_timer = 2)
        self.wait(6)
        self.play(motor_2_tracker.animate.set_value(1), run_time = 4)
        self.wait(.5)

        # Set the center of the battery at [0,0,0] for now (replace with desired position)
        battery_center = np.array([0, 2.5, 0])

        # Create battery cap (small rectangle on the right side after rotation)
        battery_cap = Rectangle(height=0.4, width=0.2, fill_color=BLACK, fill_opacity=1)

        # Create battery outer frame (rotated 90 degrees clockwise, so width becomes height)
        battery_outer = Rectangle(height=1, width=2, stroke_color=BLACK, stroke_width=6).set_z_index(10)
        battery_cap.next_to(battery_outer, RIGHT, buff=0)

        # Create the battery fill (initially full and green, rotated to fit)
        battery_fill = Rectangle(height=0.9, width=1.8, fill_color=GREEN, fill_opacity=1)
        battery_fill.move_to(battery_outer.get_center())
        battery_fill_left = battery_fill.get_left()

        # Position the battery and components at the specified center point
        battery_group = VGroup(battery_outer, battery_cap, battery_fill)
        battery_group.move_to(battery_center)

        # Add the battery components to the scene
        self.play(FadeIn(battery_outer), FadeIn(battery_cap), FadeIn(battery_fill))
        self.wait(1)

        # Create a ValueTracker to control the battery level (1 is full, 0 is empty)
        battery_level = ValueTracker(1)

        # Always redraw battery fill to match the battery level
        def update_battery_fill(fill):
            new_width = battery_level.get_value() * 1.8  # Battery width is 1.8 when full (rotated)
            new_color = interpolate_color(RED, GREEN, battery_level.get_value())
            fill.become(Rectangle(height=0.9, width=new_width, fill_color=new_color, fill_opacity=1))
            fill.move_to(battery_fill_left + np.array([new_width / 2-.1, 0, 0]) + battery_center)  # Align to left
            return fill

        battery_fill.add_updater(update_battery_fill)

        # Animate the battery level from full to empty and change color accordingly
        self.play(battery_level.animate.set_value(0.1), run_time=5, rate_func=linear)

        # Wait at the end
        self.wait(1)

        # Remove the updater
        battery_fill.clear_updaters()
        self.wait(9)
        # Final cleanup, fade out both motors
        self.play(FadeOut(*self.mobjects))
        self.wait(1)



    def create_motor_group(self, value_tracker, scale_factor=1.0):
        """Creates a motor group with stator, rotor, wires, and arrows, scaled down by a factor."""
        # Create stator (outer part of the motor)
        stator = Circle(radius=2 * scale_factor, color=DARK_GRAY, stroke_width=6 * scale_factor)

        # Create rotor (inner rotating part of the motor)
        rotor = Circle(radius=0.8 * scale_factor, color=DARK_GRAY, stroke_width=4 * scale_factor)

        # Create 8 lines going from the rotor to the stator
        lines = VGroup()
        for i in range(8):
            angle = i * PI / 4
            start = [0.8 * np.cos(angle) * scale_factor, 0.8 * np.sin(angle) * scale_factor, 0]
            end = [2 * np.cos(angle) * scale_factor, 2 * np.sin(angle) * scale_factor, 0]
            line = Line(start=start, end=end, color=DARK_GRAY, stroke_width=3 * scale_factor)
            lines.add(line)

        # Create wires
        red_wire, black_wire = self.create_wires(scale_factor)

        # Create arrows (current indicators)
        current_arrow_1, current_arrow_2 = self.create_arrows(red_wire, black_wire, value_tracker, scale_factor)

        # Return the motor group
        motor_group = VGroup(stator, rotor, lines, red_wire, black_wire, current_arrow_1, current_arrow_2)
        return motor_group, stator

    def create_wires(self, scale_factor=1.0):
        """Creates red and black wires for the motor, scaled down by a factor."""
        length = 1 * scale_factor
        redStart = 2 * unitVector(PI / 2 + PI / 3) * scale_factor
        redEnd = redStart + np.array([-length, 0, 0])
        red_wire = Line(redStart, redEnd, stroke_width=12 * scale_factor, color=RED, cap_style=constants.CapStyleType.ROUND)

        blackStart = 2 * unitVector(-PI / 2 + -PI / 3) * scale_factor
        blackEnd = blackStart + np.array([-length, 0, 0])
        black_wire = Line(blackStart, blackEnd, stroke_width=12 * scale_factor, color=BLACK, cap_style=constants.CapStyleType.ROUND)

        return red_wire, black_wire

    def create_arrows(self, red_wire, black_wire, value_tracker, scale_factor=1.0):
        """Creates current arrows for the motor, scaled down by a factor."""
        arrowLength = 1 * scale_factor
        redEnd = red_wire.get_end() - np.array([0.2, 0, 0]) * scale_factor
        blackEnd = black_wire.get_end() - np.array([0.2, 0, 0]) * scale_factor

        current_arrow_1 = Arrow(start=redEnd + np.array([-arrowLength, 0, 0]), end=redEnd, buff=-0.0, color=CBlue, stroke_width=6 * scale_factor )
        current_arrow_2 = Arrow(start=blackEnd, end=blackEnd + np.array([-arrowLength, 0, 0]), buff=-0.0, color=CBlue, stroke_width=6 * scale_factor)

        current_arrow_1.add_updater(lambda a: a.set_stroke(width = 6 * scale_factor * (1 + value_tracker.get_value())))
        current_arrow_2.add_updater(lambda a: a.set_stroke(width = 6 * scale_factor * (1 + value_tracker.get_value())))

        return current_arrow_1, current_arrow_2

    def animate_motor(self, center, value_tracker, target_p_value, scale_factor=1.0, run_timer = 4.5):
        """Sets up motor rotation based on value tracker, scaled down by a factor."""
        # Extract components
        rotor_position_line = always_redraw(lambda: Line(
            np.array([0, 0, 0]) + center, 
            0.8 * scale_factor * unitVector(value_tracker.get_value() *.001) + center, 
            color=COrange, 
            stroke_width=6 * scale_factor, 
            cap_style=constants.CapStyleType.ROUND
        ))

        p_text = always_redraw(lambda: MathTex(rf"P = {value_tracker.get_value():.2f}", color = BLACK, 
                                               font_size = 40 * scale_factor).move_to(np.array([0, 2.5 * scale_factor,0]) + center))

        rotation_arrow = CurvedArrow(
            start_point=np.array([-1 * scale_factor, 1 * scale_factor, 0]) + center, 
            end_point=np.array([1 * scale_factor, 1 * scale_factor, 0]) + center, 
            color=COrange, 
            angle=-PI / 2, 
            stroke_width=8 * scale_factor
        )

        rotation_arrow.add_updater(lambda a: a.set_stroke(width =scale_factor * 8 * (1 + abs(value_tracker.get_value()*2))))

        # Animate motor rotation (specifics can be adjusted later)
        self.play(FadeIn(rotor_position_line), FadeIn(rotation_arrow), Write(p_text))
        self.play(value_tracker.animate.set_value(target_p_value), run_time=run_timer)
        self.wait(2)


class setPower(Scene):
    def construct(self):
        CustomBackground(self)

        mainText = Text("motor.setPower()", color = BLACK, font_size= 60)
        asterisk = Text("*", color = BLACK, font_size= 60).next_to(mainText, RIGHT, buff = 0).shift((0.05, .3, 0))

        vgroup = VGroup(mainText, asterisk)
        vgroup.move_to(ORIGIN)
        vgroup.shift((0, -vgroup[0].get_center()[1], 0))

        finalMainTextPos = vgroup[0].get_center()
        mainText.move_to(ORIGIN)

        #Write in command
        self.play(Write(vgroup[0]))
        self.wait(1)

        #Shift and add asterisk
        self.play(mainText.animate.move_to(finalMainTextPos), FadeIn(asterisk))
        self.wait(1)

        #Fade everything out
        self.play(FadeOut(vgroup))
        self.wait(1)

