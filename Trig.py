from manim import *
import manim
from manium import *

class Sin(Scene):
    def construct(self):
        self.scale = 2

        initialAxisWidth = 2
        zoomedAxisWidth = 4
        
        circleStrokeWidth = 7

        self.radialLineAngle = ValueTracker(1)

        initialRadialLineWidth = 12

        finalRadialLineWidth = 8

        pixelsToScreen = 4/720

        # Set up the white background
        self.camera.background_color = ManimColor("#f2f2f2")

        background_rect = Rectangle(width=config.frame_width, height=config.frame_height)
        background_rect.set_fill(ManimColor("#dedede"), opacity=1)
        background_rect.set_stroke(width=0)
        self.add(background_rect)

        xAxis = Line(start=(0, -4, 0), end=(0,4,0), color = BLACK, stroke_width = initialAxisWidth)
        yAxis = Line(start=(-7, 0, 0), end=(7,0,0), color = BLACK, stroke_width = initialAxisWidth)

        unitCircle = Circle(self.scale, ManimColor("#1251b5"), stroke_width = circleStrokeWidth, cap_style = manim.constants.CapStyleType.ROUND)

        zeroZeroPoint = Circle(radius = initialRadialLineWidth * pixelsToScreen, fill_color = ManimColor("#ff9408"), stroke_width = 0, fill_opacity = 1)

        unitCircleRadiusLine = Line((0,0,0), (0,0,0), color = ManimColor("#ff9408"),
                    cap_style = manim.constants.CapStyleType.ROUND, stroke_width = initialRadialLineWidth)
        unitCircleRadiusLine.add_updater(lambda l: l.put_start_and_end_on((0,0,0), (self.getLineAngleCos(), 
                    self.getLineAngleSin(), 0)))

        radiusLineLengthValue = ValueTracker(0)

        radiusLineLengthVisual = DecimalNumber(radiusLineLengthValue.get_value(), 2, color = ManimColor("#ff9408"))
        radiusLineLengthVisual.move_to((self.scale * .35, self.scale * .5, 0))
        radiusLineLengthVisual.add_updater(lambda d: d.set_value(radiusLineLengthValue.get_value()))

        sinLine = Line((0,0,0), (0,0,0), stroke_width = finalRadialLineWidth, color = BLUE)
        sinLine.add_updater(lambda l: l.put_start_and_end_on((self.getLineAngleCos(), 
                    self.getLineAngleSin(), 0), (self.getLineAngleCos(), 0, 0)))
        
        sinAngleArc = Arc()
        sinAngleArc.add_updater(lambda a: a.become(
            Arc(.4 * self.scale, 0, self.radialLineAngle.get_value(), color = ManimColor("#ff9408"), stroke_width = 2)))
        
        sinLineBrace = Brace(Line(start = (self.scale, 0, 0), end = (self.scale, sinLine.get_length(), 0)), direction = RIGHT, color = BLUE)

        xAxis.set_z_index(0)
        yAxis.set_z_index(0)
        unitCircle.set_z_index(1)
        unitCircleRadiusLine.set_z_index(2)
        sinLine.set_z_index(3)
        sinAngleArc.set_z_index(3)
        sinLineBrace.set_z_index(3)
        zeroZeroPoint.set_z_index(4)
    

        # Fade to white background
        self.play(background_rect.animate.set_fill(WHITE, opacity=0), run_time=.55)

        self.play(Create(xAxis), Create(yAxis))

        self.play(xAxis.animate.set_stroke(width = zoomedAxisWidth), yAxis.animate.set_stroke(width = zoomedAxisWidth))

        self.play(Create(unitCircle))

        self.play(GrowFromCenter(zeroZeroPoint), FadeIn(radiusLineLengthVisual))

        self.play(Create(unitCircleRadiusLine), zeroZeroPoint.animate.move_to((self.getLineAngleCos(), 
                    self.getLineAngleSin(), 0)), radiusLineLengthValue.animate.set_value(1), run_time = 2)
        
        self.play(unitCircleRadiusLine.animate.set_stroke(width = finalRadialLineWidth),
                  zeroZeroPoint.animate.scale(1.5), Create(sinAngleArc), run_time = .4)

        #Moving angle around
        zeroZeroPoint.add_updater(lambda p: p.move_to((self.getLineAngleCos(), self.getLineAngleSin(), 0)))
        
        self.play(self.radialLineAngle.animate.set_value(2), run_time = .5)
        self.play(self.radialLineAngle.animate.set_value(30*DEGREES), run_time = .5)

        #Explaining Sin
        self.play(Create(sinLine))

        self.play(FadeIn(sinLineBrace), FadeOut(radiusLineLengthVisual))

        # Hold the final frame for a while
        self.wait(2)

    def getLineAngleCos(self):
        return self.scale * np.cos(self.radialLineAngle.get_value())
    
    def getLineAngleSin(self):
        return self.scale * np.sin(self.radialLineAngle.get_value())
    
class RadiansInitialExplanation(Scene):
    def construct(self):
        self.scale = 2

        initialAxisWidth = 2
        zoomedAxisWidth = 4
        
        circleStrokeWidth = 7

        self.radialLineAngle = ValueTracker(0)

        radialLineWidth = 8

        pixelsToScreen = 4/720

        # Set up the white background
        self.camera.background_color = ManimColor("#f2f2f2")

        background_rect = Rectangle(width=config.frame_width, height=config.frame_height)
        background_rect.set_fill(ManimColor("#dedede"), opacity=1)
        background_rect.set_stroke(width=0)
        self.add(background_rect)

        #Axis
        xAxis = Line(start=(0, -4, 0), end=(0,4,0), color = BLACK, stroke_width = initialAxisWidth)
        yAxis = Line(start=(-7, 0, 0), end=(7,0,0), color = BLACK, stroke_width = initialAxisWidth)

        #Circle arc
        circleArc = Arc()
        circleArc.add_updater(lambda a: a.become(
            Arc(self.scale, 0, self.radialLineAngle.get_value(), stroke_width = circleStrokeWidth, 
                color = ManimColor("#1251b5"))
        ))

        arcBottomLine = Line((0,0,0), (self.scale,0,0), color = ManimColor("#1251b5"),
                    cap_style = manim.constants.CapStyleType.ROUND, stroke_width = circleStrokeWidth)

        arcMovingLine = arcBottomLine.copy()

        arcMovingLine.add_updater(lambda l: l.put_start_and_end_on((0,0,0), (self.getLineAngleCos(), 
                    self.getLineAngleSin(), 0)))
        
        angleArc = Arc()
        angleArc.add_updater(lambda a: a.become(
            Arc(.4 * self.scale, 0, self.radialLineAngle.get_value(), stroke_color = ManimColor("#ff9408"), stroke_width = 2,
                fill_color = ManimColor("#f2f2f2"), fill_opacity = 1).set_z_index(2)))
        
        angleArcFill = Polygon((0,0,0), (0,0,0), (0,0,0), fill_color = ManimColor("#f2f2f2"), 
                        fill_opacity = 1, stroke_width = 0)
        
        def triganleLambda(p):
            p.set_points_as_corners([
                (0,0,0),
                (.4 * self.scale, 0, 0),
                (.4 * self.getLineAngleCos(), .4 * self.getLineAngleSin(), 0),
                (0,0,0)
            ])
            p.set_z_index(2)
        
        angleArcFill.add_updater(triganleLambda)
        
        arcAngleVisualFontSize = 25
        arcAngleVisualDistanceFromOrigin = .25

        arcAngleVisual = DecimalNumber(0, 2, color = ManimColor("#ff9408"), font_size=arcAngleVisualFontSize)
        
        def arcAngleVisualLambda(d):
            d.set_value(self.radialLineAngle.get_value())
            d.move_to((arcAngleVisualDistanceFromOrigin * self.getLineAngleCos(self.radialLineAngle.get_value()/2),
                       arcAngleVisualDistanceFromOrigin * self.getLineAngleSin(self.radialLineAngle.get_value()/2), 0))
            d.set_z_index(5)
        
        arcAngleVisual.add_updater(arcAngleVisualLambda)
        arcAngleVisualNiceNumbers = MathTex(rf"1", color = ManimColor("#ff9408"), 
                        font_size=arcAngleVisualFontSize).move_to(
                        (arcAngleVisualDistanceFromOrigin * self.getLineAngleCos(.5),
                        arcAngleVisualDistanceFromOrigin * self.getLineAngleSin(.5), 0))

        # displayAngle = arcAngleVisualNiceNumbers

        #Center Text first circle
        centerInitialFontSize = 64

        centerTextPI = MathTex(r"\pi", font_size = centerInitialFontSize, color = BLACK).move_to((0,0,0))
        centerText2PI = MathTex(r"2 \times \pi", font_size = centerInitialFontSize, color = BLACK).move_to((0,0,0))
        centerTextTAU = MathTex(r"2 \times \pi = \tau", font_size = centerInitialFontSize, color = BLACK).move_to((0,0,0))

        centerText = centerTextPI.copy()

        #Changing height order
        xAxis.set_z_index(0)
        yAxis.set_z_index(0)

        angleArc.set_z_index(1)
        angleArcFill.set_z_index(1)

        arcAngleVisual.set_z_index(5)
        arcAngleVisualNiceNumbers.set_z_index(2)

        circleArc.set_z_index(3)
        arcBottomLine.set_z_index(3)
        arcMovingLine.set_z_index(3)

        centerText.set_z_index(9)
        
        

        # Fade to white background
        self.play(background_rect.animate.set_fill(WHITE, opacity=0), Create(xAxis), Create(yAxis), run_time=.55)
        
        #Draw Axis
        #self.play(Create(xAxis), Create(yAxis))
        self.play(xAxis.animate.set_stroke(width = zoomedAxisWidth), yAxis.animate.set_stroke(width = zoomedAxisWidth),
                  Create(arcBottomLine))

        #Draw intiial angle of 1 rad
        self.add(arcMovingLine, angleArc, circleArc)
        self.play(self.radialLineAngle.animate.set_value(1).set_rate_func(smooth),
                  GrowFromCenter(arcAngleVisualNiceNumbers))

        self.wait(.2)

        #interpolate between angles for show
        self.remove(arcAngleVisualNiceNumbers)
        self.add(arcAngleVisual)
        self.add(angleArcFill)

        targetAngle = 2.6
        halfTime = 1.8

        self.play(self.radialLineAngle.animate(rate_func = linear).set_value(targetAngle), run_time = halfTime)
        self.play(self.radialLineAngle.animate(rate_func = linear).set_value(1), run_time = halfTime)

        self.add(arcAngleVisualNiceNumbers)
        self.remove(arcAngleVisual)
        angleArcFill.clear_updaters()
        self.remove(angleArcFill)

        arcAngleVisual.clear_updaters()

        self.wait(1)
        
        #Turn to full circle
        startAngle = 1
        finalAngle = TAU

        angleArc.add_updater(self.fadeBetweenAngles(startAngle, finalAngle, self.radialLineAngle.get_value))
        arcBottomLine.add_updater(self.fadeBetweenAngles(startAngle, finalAngle, self.radialLineAngle.get_value))
        arcMovingLine.add_updater(self.fadeBetweenAngles(startAngle, finalAngle, self.radialLineAngle.get_value))
        xAxis.add_updater(self.fadeBetweenAngles(startAngle, finalAngle, self.radialLineAngle.get_value))
        yAxis.add_updater(self.fadeBetweenAngles(startAngle, finalAngle, self.radialLineAngle.get_value))

        self.play(self.radialLineAngle.animate.set_value(TAU).set_rate_func(smooth), FadeOut(arcAngleVisualNiceNumbers))

        #Add PI text
        self.play(Write(centerText))

        self.wait(.5)

        self.play(Transform(centerText, centerText2PI))
        self.wait(.7)
        self.play(Transform(centerText, centerTextTAU))

        # Hold the final frame for a while
        self.wait(2)

    def fadeBetweenAngles(self, startAngle, finalAngle, angleFunction):

        def fadeOut(o):
            zeroedAngleFucntion = angleFunction() - startAngle
            zeroedFinalAngle = finalAngle - startAngle

            normalizedFunction = zeroedAngleFucntion / zeroedFinalAngle

            opacity = 1 - normalizedFunction

            o.set_stroke(opacity = opacity)
        
        return fadeOut

    def getLineAngleCos(self, angle = None):
        if angle is None:
            return self.scale * np.cos(self.radialLineAngle.get_value())
        return self.scale * np.cos(angle)
    
    def getLineAngleSin(self, angle = None):
        if angle is None:
            return self.scale * np.sin(self.radialLineAngle.get_value())
        return self.scale * np.sin(angle)
    
class CircleCircumference(Scene):
    def construct(self):
        self.scale = 2

        radialLineWidth = 8
        circleStrokeWidth = 7
        pixelsToScreen = 4/720

        self.camera.background_color = ManimColor("#f2f2f2")

        self.radialLineAngle = ValueTracker(30*DEGREES)

        unitCircle = Circle(self.scale, ManimColor("#1251b5"), stroke_width = circleStrokeWidth, cap_style = manim.constants.CapStyleType.ROUND)

        unitCircleRadiusLine = Line((0,0,0), (0,0,0), color = ManimColor("#ff9408"),
                    cap_style = manim.constants.CapStyleType.ROUND, stroke_width = radialLineWidth)
        unitCircleRadiusLine.add_updater(lambda l: l.put_start_and_end_on((0,0,0), (self.getLineAngleCos(), 
                    self.getLineAngleSin(), 0)))

        radiusLineLengthValue = ValueTracker(0)

        radiusLineLengthVisual = DecimalNumber(radiusLineLengthValue.get_value(), 2, color = ManimColor("#ff9408"))
        radiusLineLengthVisual.move_to((self.scale * .35, self.scale * .5, 0))
        radiusLineLengthVisual.add_updater(lambda d: d.set_value(radiusLineLengthValue.get_value()))

        unitCircle.set_z_index(1)
        unitCircleRadiusLine.set_z_index(2)
        
        self.add(radiusLineLengthVisual)
        #Display Unit circle with line
        self.play(Create(unitCircle), Create(unitCircleRadiusLine), radiusLineLengthValue.animate.set_value(1), run_time = 2)
        
        #Move circle to bottom right
        self.play(unitCircle.animate.move_to((PI, -1, 0)).scale(.5), FadeOut(radiusLineLengthVisual), FadeOut(unitCircleRadiusLine))
        
        #Unravel Circle into Line

        circumferenceLine = Line((0,0,0), (0,0,0))
        self.remove(unitCircle)
        unitCircle = Circle(self.scale /2, ManimColor("#1251b5"), stroke_width = circleStrokeWidth, cap_style = manim.constants.CapStyleType.ROUND).move_to((PI, -1, 0))
        self.add(unitCircle)
        

        self.wait(.2)
        self.play(UnravelCircle(unitCircle, circumferenceLine, PI/2), run_time = 2)

        #Label circumference with brace and bring in bottom circle

        displayCenter = np.array([0, -2, 0])
        displayCircle = Circle(radius=1, color=ManimColor("#1251b5"), stroke_width = 6).move_to(displayCenter)
        displayCircleRadiusLine = Line(displayCenter, displayCenter + np.array([np.cos(30*DEGREES), np.sin(30*DEGREES), 0]), color = ManimColor("#ff9408"), stroke_width = 5)

        circumferenceBrace = Brace(circumferenceLine, UP, color = BLACK)
        circumferenceText = Text("Circumference", color = BLACK, font_size=40)

        baseCircumferenceEquasion = MathTex(r"2 \times \pi \times r", color = BLACK, font_size=40)
        circumferenceEquasion = SplitTex(baseCircumferenceEquasion, 13)
        self.remove(baseCircumferenceEquasion)
        sceneText = MathTex(r"T", color = BLACK, font_size=40)

        circumferenceText.next_to(circumferenceBrace, UP)
        circumferenceEquasion.next_to(circumferenceBrace, UP)

        self.play(FadeIn(circumferenceBrace), FadeIn(circumferenceText),
                  FadeIn(displayCircleRadiusLine), FadeIn(displayCircle))
        self.wait(1)
        #Highlight both circumferences

        self.play(Highlight(displayCircle), Highlight(circumferenceLine), run_time = 2)

        self.wait(1)

        #Show circumference Equasion
        self.wait(.5)
        self.play(Transform(circumferenceText, circumferenceEquasion))

        self.remove(circumferenceText)
        circumferenceText = circumferenceEquasion.next_to(circumferenceBrace, UP)
        self.add(circumferenceText)

        #Display r = 1
        rEq1 = CopyMathTex(circumferenceText[0], r" r = 1")

        fullBox = VGroup(circumferenceText.copy(), rEq1).arrange(RIGHT)
        fullBox.next_to(circumferenceBrace, UP)

        rEqualsOne = fullBox[1].copy()

        self.wait(1)
        self.play(circumferenceText.animate.next_to(fullBox[0].get_left(), RIGHT, buff  = 0), FadeIn(rEqualsOne))

        #Highlight radius of circle
        self.play(Highlight(displayCircleRadiusLine), run_time = 2)

        self.wait(1)

        #Substitute r for 1

        self.play(Transform(circumferenceText[1], AddTex(circumferenceText[0], r"\times 1")))

        # fullBox = VGroup(circumferenceEquasionReq1, rEq1).arrange(RIGHT)
        # fullBox.next_to(circumferenceBrace, UP)

        self.wait(1)
        # self.play(Transform(circumferenceText, fullBox[0]), Transform(rEqualsOne, fullBox[1]))
        
        #Remove r = 1 and center

        self.play(circumferenceText.animate.next_to(circumferenceBrace, UP), FadeOut(rEqualsOne))

        #remove 1
        # circumferenceEquasionSimplified = CopyMathTex(circumferenceEquasion, r"2 \times \pi")

        # circumferenceEquasionSimplified.next_to(circumferenceBrace, UP)

        # circumferenceEquasionReq2 = CopyMathTex(circumferenceEquasion, r"2 \times \pi")
        # circumferenceEquasionReq2.next_to(circumferenceText.get_left(), RIGHT, buff = 0)
        # self.add(circumferenceEquasionReq2)

        self.wait(1)
        #self.play(Transform(circumferenceText, circumferenceEquasionSimplified))
        self.play(FadeOut(circumferenceText[1]), circumferenceText[0].animate.next_to(circumferenceBrace, UP))
        circumferenceText = circumferenceText[0]
        # self.remove(circumferenceEquasionSimplified)

        #Shift Right to show "origional Circle"
        newLine = Line((0,0,0), (PI*2,0,0), color = ManimColor("#1251b5"), stroke_width = 5)
        newBrace = Brace(newLine, UP, color = BLACK)

        circle = Circle(1, color = ManimColor("#1251b5"), stroke_width = 5, fill_opacity = 0)
        circleCenterText = CopyMathTex(sceneText, r"2 \times \pi")
        
        circleGroup = VGroup(circle, circleCenterText)
        circleGroup.move_to((-10,0,0))

        self.add(circleGroup)
        # self.add(circleCenterText)
        self.play(Transform(circumferenceLine, newLine), Transform(circumferenceBrace, newBrace),
                    circumferenceText.animate.next_to(newBrace, UP), 
                    circleGroup.animate.move_to((-1-PI/2, 0, 0)),
                    FadeOut(displayCircleRadiusLine).set_rate_func(split_time(smooth, 2, 0)),
                    FadeOut(displayCircle).set_rate_func(split_time(smooth, 2, 0)),
                    
                    run_time = 2)
        
        self.wait(1)

        #Fade out to close scene
        self.play(FadeOut(circumferenceLine),FadeOut(circumferenceBrace),FadeOut(
                    circumferenceText),FadeOut(
                    circleGroup), run_time = 2)

        self.wait(2)

    def getLineAngleCos(self, angle = None):
        if angle is None:
            return self.scale * np.cos(self.radialLineAngle.get_value())
        return self.scale * np.cos(angle)
    
    def getLineAngleSin(self, angle = None):
        if angle is None:
            return self.scale * np.sin(self.radialLineAngle.get_value())
        return self.scale * np.sin(angle)
    
    def fadeBetweenvalues(self, start, final, function):

        def fade(o):
            zeroedAngleFucntion = function() - start
            zeroedFinalAngle = final - start

            normalizedFunction = zeroedAngleFucntion / zeroedFinalAngle

            opacity = normalizedFunction

            o.set_opacity = (opacity)
        
        return fade

class ArcLengthToAngleRelation(Scene):
    def construct(self):

        self.scale = 1.5

        radialLineWidth = 8
        circleStrokeWidth = 7

        cutLineStroke = 4

        self.camera.background_color = ManimColor("#f2f2f2")

        unitCircle = Circle(self.scale, ManimColor("#1251b5"), stroke_width = circleStrokeWidth, cap_style = manim.constants.CapStyleType.ROUND)

        self.play(Create(unitCircle))

        
        # Cut circle into thirds vertically 
        xVal = 0.265

        rightLine = Line((xVal * self.scale ,self.scale + .4,0), (xVal * self.scale,-self.scale - .4,0), color = BLACK,
                    cap_style = manim.constants.CapStyleType.ROUND, stroke_width = cutLineStroke)
        
        leftLine = Line((-xVal * self.scale,self.scale + .4,0), (-xVal * self.scale,-self.scale - .4,0), color = BLACK,
                    cap_style = manim.constants.CapStyleType.ROUND, stroke_width = cutLineStroke)
        
        self.play(Create(leftLine), Create(rightLine))

        self.wait(1)

        #Uncut circle into thirds
        self.play(Uncreate(leftLine), Uncreate(rightLine))

        self.wait(1)

        #Cut circle into thirds by angle
        topLine = Line((0,self.scale,0), (0,0,0), color = BLACK,
                    cap_style = manim.constants.CapStyleType.ROUND, stroke_width = cutLineStroke)

        rightLine = Line((0,0,0), (np.cos(-30 * DEGREES) * self.scale,np.sin(-30 * DEGREES) * self.scale,0), color = BLACK,
                    cap_style = manim.constants.CapStyleType.ROUND, stroke_width = cutLineStroke)
        
        leftLine = Line((0,0,0), (np.cos(210 * DEGREES) * self.scale,np.sin(210 * DEGREES) * self.scale,0), color = BLACK,
                    cap_style = manim.constants.CapStyleType.ROUND, stroke_width = cutLineStroke)
        
        unitCircle.set_z_index(2)
        leftLine.set_z_index(1)
        rightLine.set_z_index(1)
        topLine.set_z_index(1)

        self.play(Create(topLine).set_rate_func(split_first_half(smooth_first_half)), 
                  Create(leftLine).set_rate_func(split_second_half(smooth_second_half)), 
                  Create(rightLine).set_rate_func(split_second_half(smooth_second_half)))

        self.wait(1)

        #Draw 3 angles
        firstArc = Arc(.2 * self.scale, PI/2, -PI*2/3, stroke_color = ManimColor("#ff9408"), stroke_width = 2,
                fill_color = ManimColor("#f2f2f2"), fill_opacity = 1).set_z_index(0)
        
        secondArc = Arc(.2 * self.scale, -PI/6, -PI*2/3, stroke_color = ManimColor("#ff9408"), stroke_width = 2,
                fill_color = ManimColor("#f2f2f2"), fill_opacity = 1).set_z_index(0)
        
        thirdArc = Arc(.2 * self.scale, 7*PI/6, -PI*2/3, stroke_color = ManimColor("#ff9408"), stroke_width = 2,
                fill_color = ManimColor("#f2f2f2"), fill_opacity = 1).set_z_index(0)
        
        self.play(Create(firstArc), Create(secondArc), Create(thirdArc))

        self.wait(1)
        #Swap circle for two arcs
        unitCircle.become(Arc(radius=self.scale, start_angle= PI/2, angle=TAU*2/3, color=ManimColor("#1251b5"), stroke_width = circleStrokeWidth))
        thirdCircle = Arc(radius=self.scale, start_angle= PI/2, angle=-TAU*1/3, color=ManimColor("#1251b5"), stroke_width = circleStrokeWidth)
        thirdCircle.set_z_index(2)
        self.add(thirdCircle)

        #Move everything to the left
        notFocusedOpacity = .2
        newCenter = np.array([-2.5,0,0])

        self.play(firstArc.animate.move_arc_center_to(newCenter),
                  secondArc.animate.move_arc_center_to(newCenter).set_opacity(opacity=notFocusedOpacity),
                  thirdArc.animate.move_arc_center_to(newCenter).set_opacity(opacity=notFocusedOpacity),
                  unitCircle.animate.move_arc_center_to(newCenter).set_stroke(opacity=notFocusedOpacity),
                  thirdCircle.animate.move_arc_center_to(newCenter),
                  topLine.animate.move_to(newCenter + np.array([0,self.scale/2,0])),
                  leftLine.animate.move_to(newCenter + np.array([np.cos(210*DEGREES) * self.scale/2,np.sin(210*DEGREES) * self.scale/2,0])).set_opacity(opacity=notFocusedOpacity),
                  rightLine.animate.move_to(newCenter+ np.array([np.cos(-30*DEGREES) * self.scale/2,np.sin(-30*DEGREES) * self.scale/2,0])),
                  )
        
        self.wait(1)

        #Definition for next animations
        textAngleVector = np.array([np.cos(PI/6), np.sin(PI/6), 0])

        #Highlight Angle and display Equasion
        angleEquasion = MathTex(r"\theta = 1/3 \times Angle", color = BLACK, font_size = 40).next_to((1, 1, 0), RIGHT)
        questionMark1 = MathTex("?", color = BLACK, font_size = 60).next_to((1, 1, 0), LEFT)
        angleLabel = MathTex(r"\theta", color = BLACK, font_size = 20).move_to(newCenter + textAngleVector * .15)

        self.play(firstArc.animate(rate_func = there_and_back_with_pause).move_to((np.cos(PI/6) * .5, np.sin(PI/6) * .5, 0)).scale(1.3), 
                  FadeIn(angleEquasion).set_rate_func(split_time(smooth, 3, 0)),
                  FadeIn(angleLabel).set_rate_func(split_time(smooth, 3, 2)),
                  FadeIn(questionMark1).set_rate_func(split_time(smooth, 3, 0)),

                  run_time = 2.4)

        self.wait(1)

        #Emphasize area amd display Equasion
        areaEquasion = MathTex(r"A = 1/3 \times Area", color = BLACK, font_size = 40).next_to((1, 0, 0), RIGHT)
        areaLabel = CopyMathTex(areaEquasion, r"A").move_to(newCenter + textAngleVector * .8)
        questionMark2 = MathTex("?", color = BLACK, font_size = 60).next_to((1, 0, 0), LEFT)


        scaleFactor = 1.5


        self.play(topLine.animate(rate_func = there_and_back_with_pause).move_to(newCenter + np.array([0, scaleFactor/2 * self.scale, 0])).scale(scaleFactor),
                  rightLine.animate(rate_func = there_and_back_with_pause).move_to(newCenter + np.array([np.cos(-30*DEGREES) * scaleFactor/2 * self.scale, np.sin(-30*DEGREES) * scaleFactor/2 * self.scale, 0])).scale(scaleFactor),
                  ScaleArc(thirdCircle, scaleFactor).set_rate_func(there_and_back_with_pause),
                  FadeIn(areaEquasion).set_rate_func(split_time(smooth, 3, 0)),
                  FadeIn(areaLabel).set_rate_func(split_time(smooth, 3, 2)),
                  FadeIn(questionMark2).set_rate_func(split_time(smooth, 3, 0)),

                  run_time = 2)
        

        self.wait(1)

        #HighlightArclength and fade in equasion
        arcLengthEquasion = MathTex(r"S = 1/3 \times Circumference", color = BLACK, font_size = 40).next_to((1, -1, 0), RIGHT)
        arcLengthLabel  =CopyMathTex(arcLengthEquasion, r"S").move_to(newCenter + textAngleVector * 2 + np.array([-.2, 0, 0]))
        questionMark3 = MathTex("?", color = BLACK, font_size = 60).next_to((1, -1, 0), LEFT)


        self.play(FadeIn(arcLengthEquasion).set_rate_func(split_time(smooth, 3, 0)),
                  FadeIn(arcLengthLabel).set_rate_func(split_time(smooth, 3, 2)),
                  ScaleArc(thirdCircle, 1.5).set_rate_func(there_and_back_with_pause),
                  FadeIn(questionMark3).set_rate_func(split_time(smooth, 3, 0)),
                  run_time = 2)

        self.wait(1)

        #Fade out question marks and move text in

        self.play(FadeOut(questionMark1),
                  FadeOut(questionMark2),
                  FadeOut(questionMark3)
                  )
        self.play(angleEquasion.animate.next_to((.3,1,0), RIGHT),
                  areaEquasion.animate.next_to((.3,0,0), RIGHT),
                  arcLengthEquasion.animate.next_to((.3,-1,0), RIGHT))
        
        self.wait(1)

        #Remove area and restructure

        self.play(arcLengthEquasion.animate.next_to((.3,0,0), RIGHT),
                  FadeOut(areaEquasion),
                  FadeOut(areaLabel),


            run_time = 2
        )
        
        self.wait(1)

        #Change Equasions to match Values one at a time, ending with S = theta
        thetaEq = MathTex(r"\theta = ", color = BLACK, font_size = 40).next_to((.3, 1.04, 0), RIGHT)
        angleThird = AddTex(thetaEq, r"1/3", shift=-SlashShift(40)+ np.array([0, +.015, 0]))
        angleTwoPi = AddTex(angleThird, r"\times Angle", shift = SlashShift(40))

        newAngleEquasion = VGroup(thetaEq, angleThird, angleTwoPi)
        self.add(newAngleEquasion)
        self.remove(angleEquasion)
        angleEquasion = newAngleEquasion
    
        #Change Angle equasion to be numeric 
        self.play(Transform(angleEquasion[2], AddTex(angleEquasion[1], r"\times 2 \times \pi", aligned_edge=DOWN, shift = SlashShift(40)))) 
        self.wait(1)

        #Change circumference equasion to be numeric
        newArcLengthEquasion = SplitTex(arcLengthEquasion, 7, aligned_edge = DOWN, shift = SlashShift(40))
        self.add(newArcLengthEquasion)
        self.remove(arcLengthEquasion)
        arcLengthEquasion = newArcLengthEquasion

        self.play(Transform(arcLengthEquasion[1], AddTex(arcLengthEquasion[0], r"\times 2 \times \pi \times r", aligned_edge=DOWN, shift= SlashShift(40))))
        self.wait(1)

        #Remove r from circumference equasion
        self.remove(arcLengthEquasion)
        Seq = MathTex(r"S =", color = BLACK, font_size = 40).next_to((.3,.04,0), RIGHT)
        third = AddTex(Seq, r"1/3", shift= -SlashShift(40) + np.array([0, +.015, 0]))
        twoPi = AddTex(third, r"\times 2 \times \pi", shift=SlashShift(40))
        are = AddTex(twoPi[1], r"\times r")
        arcLengthEquasion = VGroup(Seq, third, twoPi, are)
        self.add(arcLengthEquasion)


        self.play(FadeOut(are))
        self.wait(1)

        #Show theta equals S
        sEqTheta = CopyMathTex(arcLengthEquasion[0], r"\theta = S").next_to((.3, -1, 0), RIGHT)
        self.play(FadeIn(sEqTheta))
        self.wait(1)

        #Change 1/3 to be a variable
        aValue = ValueTracker(1/3)
        aDisplayValue = MathTex(rf"a = {aValue.get_value():.2f}", font_size = 60, color = BLACK).move_to((0, 2, 0))
        
        arcEquasionAVarialbe = AddTex(Seq, r"a")
        angleEquasionAVarialbe = AddTex(thetaEq, r"a")
        self.play(FadeIn(aDisplayValue),
                  Transform(third, arcEquasionAVarialbe),
                  twoPi.animate.next_to(arcEquasionAVarialbe, RIGHT, buff = SpaceBuff(40)).shift(SlashShift(40)/2),
                  Transform(angleThird, angleEquasionAVarialbe),
                  angleTwoPi.animate.next_to(angleEquasionAVarialbe, RIGHT, buff = SpaceBuff(40)).shift(SlashShift(40)/2),

                  FadeOut(leftLine),
                  FadeOut(secondArc),
                  FadeOut(thirdArc))
        
        aDisplayValue.add_updater(lambda a: a.become(MathTex(rf"a = {aValue.get_value():.2f}", font_size = 60, color = BLACK).move_to((0, 2, 0))))

        self.wait(1)

        #Track styles
        bigText = MathTex(r"\times", font_size = 40, color = BLACK)
        mediumText = MathTex(r"\times", font_size = 30, color = BLACK)
        smallText = CopyMathTex(angleLabel, r"\times")

        #Add value labels to Arc length and angle
        self.play(
                  Transform(arcLengthLabel, CopyMathTex(mediumText, rf"S = {aValue.get_value() * 2 * PI:.2f}").next_to(newCenter + np.array([np.cos(PI/2 - aValue.get_value()* PI), np.sin(PI/2 - aValue.get_value() * PI), 0]) * self.scale * 1, np.array([np.cos(PI/2 - aValue.get_value()* PI), np.sin(PI/2 - aValue.get_value() * PI), 0]))),
                  Transform(angleLabel, CopyMathTex(smallText, rf"\theta = {aValue.get_value() * 2 * PI:.2f}").next_to(newCenter + np.array([np.cos(PI/2 - aValue.get_value()* PI), np.sin(PI/2 - aValue.get_value() * PI), 0]) * self.scale * .08, np.array([np.cos(PI/2 - aValue.get_value()* PI), np.sin(PI/2 - aValue.get_value() * PI), 0])))
                  )

        self.wait(1)

        #Show Various angles

        unitCircle.become(Arc(radius=self.scale, start_angle= PI/2, angle=TAU, color=ManimColor("#1251b5"), stroke_width = circleStrokeWidth)).set_stroke(opacity=notFocusedOpacity).move_to(newCenter)
        thirdCircle.add_updater(lambda a:
                                a.become(Arc(radius=self.scale, start_angle= PI/2, angle=-aValue.get_value() * 2 * PI, color=ManimColor("#1251b5"), stroke_width = circleStrokeWidth)).move_arc_center_to(newCenter)) 

        firstArc.add_updater(lambda a:
                             a.become(Arc(.2 * self.scale, PI/2, -aValue.get_value() * 2 * PI, stroke_color = ManimColor("#ff9408"), stroke_width = 2,
                fill_color = ManimColor("#f2f2f2"), fill_opacity = 1).set_z_index(0).move_arc_center_to(newCenter)))

        rightLine.add_updater(lambda l:
                              l.put_start_and_end_on(newCenter, newCenter + self.scale * np.array([np.cos(PI/2 - aValue.get_value()* PI * 2), np.sin(PI/2 - aValue.get_value() * PI* 2), 0])))

        self.remove(Seq)
        self.remove(third)
        self.remove(twoPi)
        self.remove(are)
        arcLengthEquasion = CopyMathTex(bigText, rf"S = {aValue.get_value():.2f} \times 2 \times \pi").next_to((.3,0,0), RIGHT)
        self.add(arcLengthEquasion)

        arcLengthEquasion.add_updater(lambda a:
                                      a.become(CopyMathTex(bigText, rf"S = {aValue.get_value():.2f} \times 2 \times \pi").next_to((.3,0,0), RIGHT)))
        
        angleEquasion.add_updater(lambda e:
                                  e.become(CopyMathTex(bigText, rf"\theta = {aValue.get_value():.2f} \times 2 \times \pi").next_to((.3,1,0), RIGHT)))

        arcLengthLabel.add_updater(lambda e:
                                   e.become(CopyMathTex(mediumText, rf"S = {aValue.get_value() * 2 * PI:.2f}").next_to(newCenter + np.array([np.cos(PI/2 - aValue.get_value()* PI), np.sin(PI/2 - aValue.get_value() * PI), 0]) * self.scale * 1, np.array([np.cos(PI/2 - aValue.get_value()* PI), np.sin(PI/2 - aValue.get_value() * PI), 0]))))

        angleLabel.add_updater(lambda a:
                               a.become(CopyMathTex(smallText, rf"\theta = {aValue.get_value() * 2 * PI:.2f}").next_to(newCenter + np.array([np.cos(PI/2 - aValue.get_value()* PI), np.sin(PI/2 - aValue.get_value() * PI), 0]) * self.scale * .08, np.array([np.cos(PI/2 - aValue.get_value()* PI), np.sin(PI/2 - aValue.get_value() * PI), 0]))))


        self.play(aValue.animate(rate_func = linear).set_value(.7), run_time = 4)
        self.play(aValue.animate(rate_func = linear).set_value(1/3), run_time = 4)
        self.wait(1)

        #Fade out and ask So what?
        background_rect = Rectangle(width=config.frame_width, height=config.frame_height)
        background_rect.set_fill(ManimColor("#f2f2f2"), opacity=0)
        background_rect.set_stroke(width=0)
        background_rect.set_z_index(10)
        self.add(background_rect)

        self.play(background_rect.animate.set_fill(opacity=1))

        soWhat = Text("So What?", color = BLACK, font_size=90).set_z_index(11)
        
        self.play(Write(soWhat))
        self.wait(2)
        
        #Simplify Equasions behind the scene and fade back in
        self.remove(arcLengthEquasion)
        self.remove(angleEquasion)
        arcLengthEquasion = CopyMathTex(bigText, rf"S = a \times 2 \times \pi").next_to((.3,0,0), RIGHT)
        angleEquasion = CopyMathTex(bigText, rf"\theta = a \times 2 \times \pi").next_to((.3,1,0), RIGHT)
        self.add(arcLengthEquasion)
        self.add(angleEquasion)

        self.remove(arcLengthLabel)
        self.remove(angleLabel)
        arcLengthLabel = CopyMathTex(smallText, rf"S").next_to(newCenter + np.array([np.cos(PI/2 - aValue.get_value()* PI), np.sin(PI/2 - aValue.get_value() * PI), 0]) * self.scale * 1, np.array([np.cos(PI/2 - aValue.get_value()* PI), np.sin(PI/2 - aValue.get_value() * PI), 0]))
        angleLabel = CopyMathTex(smallText, rf"\theta").next_to(newCenter + np.array([np.cos(PI/2 - aValue.get_value()* PI), np.sin(PI/2 - aValue.get_value() * PI), 0]) * self.scale * .08, np.array([np.cos(PI/2 - aValue.get_value()* PI), np.sin(PI/2 - aValue.get_value() * PI), 0]))
        self.add(arcLengthLabel)
        self.add(angleLabel)
        
        self.remove(aDisplayValue)
        self.play(FadeOut(background_rect), FadeOut(soWhat))
        self.wait(1)

        #return to equasion with r and draw radius line
        radiusLine = Line(newCenter, newCenter +  np.array([self.scale * np.cos(-PI* 4/5),self.scale * np.sin(-PI * 4/5),0]), color = ManimColor("#ff9408"),
                    cap_style = manim.constants.CapStyleType.ROUND, stroke_width = 4).set_z_index(0)
        radiusLabel = Text("r", font_size=30, color = ManimColor("#ff9408")).set_opacity(0).move_to(newCenter + np.array([0, self.scale * .1, 0]))

        areAgain = AddTex(arcLengthEquasion, r"\times r")
        self.play(FadeOut(sEqTheta), 
                #   Transform(arcLengthEquasion, CopyMathTex(bigText, rf"S = a \times 2 \times \pi \times r").next_to((.3,0,0), RIGHT)),
                  FadeIn(areAgain),
                  radiusLabel.animate.set_opacity(1).move_to(newCenter + np.array([self.scale * -.05, self.scale * .1, 0]) + self.scale/2 * np.array([np.cos(-PI * 4/5), np.sin(-PI* 4/5), 0])),
                  Create(radiusLine), run_time =2)
        self.wait(1)

        #Highlight equivilancy

        invisibleLine1 = Line((.37,1,0), (.9,1,0)).set_opacity(0)
        highlightThetaBrace = Brace(invisibleLine1, direction=DOWN, color = BLACK)
        invisibleLine2 = Line((1.3,0,0), (3.05,0,0)).set_opacity(0)
        highlightEquivilencyBrace = Brace(invisibleLine2, direction=DOWN, color = BLACK)

        self.play(FadeIn(highlightEquivilencyBrace), FadeIn(highlightThetaBrace))

        self.wait(1)

        #Create Final Equasion

        firstHalfFinal = CopyMathTex(bigText, rf"S = \theta").next_to((.3,0,0), RIGHT)
        self.play(Transform(arcLengthEquasion, firstHalfFinal),
                  areAgain.animate.next_to(firstHalfFinal, RIGHT, buff = SpaceBuff(40)),
                  Transform(highlightEquivilencyBrace, Brace(Line((1.28,0,0), (1.3 + .3,0,0)), direction=DOWN, color = BLACK) ))
        self.wait(1)

        #highlight final equasion
        self.play(FadeOut(highlightThetaBrace),
                  Transform(highlightEquivilencyBrace, Brace(Line((.4,0,0), (2.3,0,0)), direction=DOWN, color = BLACK) ))
        self.wait(1)

        #Fill screen with final equasion

        arcLengthEquasion.become(CopyMathTex(bigText, rf"S = \theta \times r").next_to((.3,0,0), RIGHT))
        self.remove(areAgain)

        thirdCircle.clear_updaters()
        firstArc.clear_updaters()

        self.play(FadeOut(unitCircle),
                  FadeOut(thirdCircle),
                  FadeOut(firstArc),
                  FadeOut(radiusLabel),
                  FadeOut(radiusLine),
                  FadeOut(topLine),
                  FadeOut(rightLine),
                  FadeOut(angleLabel),
                  FadeOut(arcLengthLabel),
                  FadeOut(angleEquasion),
                  FadeOut(highlightEquivilencyBrace),
                  Transform(arcLengthEquasion, MathTex(rf"S = \theta \times r", font_size = 100, color = BLACK)),
                  run_time = 2)
        
        self.wait(1)

        #Move to top and then display a bunch of useful properties
        self.play(arcLengthEquasion.animate.move_to((0,2,0)))
        self.wait(1)

