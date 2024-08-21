def FadeBetweenValues(start, final, function):

        def fade(o):
            zeroedAngleFucntion = function() - start
            zeroedFinalAngle = final - start

            normalizedFunction = zeroedAngleFucntion / zeroedFinalAngle

            opacity = normalizedFunction

            o.set_opacity = (opacity)
        
        return fade