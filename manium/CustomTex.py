from manim import *

def CopyMathTex(mathTex, newText):
    """
    Initializes a new MathTex object with the same styles as the original one.
    
    Parameters:
    mathTex: The original MathTex object to copy styles from.
    newText: The new text for the new MathTex object.
    
    Returns:
    MathTex: A new MathTex object with the same styles as the original.
    """
    # Extract styles from the original MathTex object
    font_size = mathTex.font_size
    color = mathTex.get_color()
    # stroke_width = mathTex.get_stroke_width()
    # fill_opacity = mathTex.get_fill_opacity()
    # stroke_color = mathTex.get_stroke_color()
    # fill_color = mathTex.get_fill_color()
    
    # Initialize the new MathTex object with the extracted styles
    newMathTex = MathTex(
        newText,
        font_size=font_size,
        color=color,
        # # fill_opacity=fill_opacity,
        # stroke_color = stroke_color,
        # stroke_width = stroke_width,
        # # fill_color = fill_color,
    )
    # newMathTex.set_stroke(stroke_color, width=stroke_width)
    # newMathTex.set_fill(fill_color, opacity=fill_opacity)
    
    return newMathTex

def SpaceBuff(fontSize):
    return .173 * fontSize/40

def SlashShift(fontSize):
    return np.array([0,.108,0]) * fontSize/40

def AddTex(mathTex, newText, aligned_edge = DOWN, shift = (0,0,0)):
    
    newTex = CopyMathTex(mathTex, newText)
    # print("Add Tex: " +"|" + newText[:6]+ "|")
    if newText[:6] == r"\times":
        newTex = SplitTex(newTex, 6)

    newTex.next_to(mathTex, RIGHT, buff = SpaceBuff(mathTex.font_size), aligned_edge=aligned_edge).shift(shift)

    return newTex

def SplitTex(mathTex, fence_index, aligned_edge = DOWN, shift = (0,0,0)):
    firstTex = CopyMathTex(mathTex, mathTex.tex_string[:fence_index])
    # if firstTex.tex_string[-6:] == r"\times":
    #     firstTex = SplitTex(firstTex, len(firstTex.tex_string)- 6)
    firstTex.next_to(mathTex.get_left(), RIGHT, buff = 0)

    secondTex = AddTex(firstTex, mathTex.tex_string[fence_index:], aligned_edge=aligned_edge, shift=shift)

    group = VGroup(firstTex, secondTex)

    return group