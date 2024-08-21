from manim import *

# def CopyMathTex(mathTex, newText):
#     newMathTex = MathTex(newText, font_size =mathTex.font_size )
#     newMathTex.match_style(mathTex)
#     # newMathTex.set_font_size(mathTex.font_size)
#     #newMathTex.move_to(mathTex.get_center())
#     return newMathTex



def CopyText(text_obj, newText):
    # Create a new Text object with the new text
    newTextObj = Text(newText)
    
    # Copy the style from the original Text object
    newTextObj.match_style(text_obj)
    newTextObj.set_font_size(text_obj.font_size)
    newTextObj.move_to(text_obj.get_center())

    return newTextObj

