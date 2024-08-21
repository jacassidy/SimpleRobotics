from manim import *

half_way_threshold = smooth(.5)

def smooth_first_half(t: float, inflection: float = 10.0) -> float:
    return smooth(t=t/2, inflection=inflection) * 2

def smooth_second_half(t: float, inflection: float = 10.0) -> float:
    return smooth(t=t/2+.5, inflection=inflection) * 2 - 1

"""
Split rate function gets a fraction of a rate function, so for example 
smooth, 0, 2 will split the smooth function in 2 and return the first half of that function
in a range of 0 - 1 rather than 0 - .5

you probably want split_portion that returns a function that will occur over this smaller time interval
"""
# def split_rate_function(function, split, index):
#     def portion(t):
#         return function((t + index) / split) * split - index
#     return portion

def split_rate_function_interval(function, start, end):
    change = end - start
    funOfStart = function(start)
    invFunStartToEnd = 1 / (function(end) - funOfStart)

    def portion(t):
        return (function(t * change + start) - funOfStart) * invFunStartToEnd
    
    return portion

def split_first_half(function):
    return lambda t: function(t * 2) if t <= .5 else 1

def split_second_half(function):
    return lambda t: function(t * 2 -1) if t >= .5 else 0

"""
Splits a rate function by time, so entire rate function is completed within
time window defined by split and index
"""
def split_time(function, split, index):

    split_fraction = 1/split

    def split_func(t):
        if t < index * split_fraction:
            return 0
        if t > (index + 1) * split_fraction:
            return 1
        return function(t * split - index)

    return split_func

"""
This is probably what you actually want to use, it takes a given rate function and returns one
that will display the a fraction of a function, within the time it takes to complete that 
fraction of the rate function
"""
#Realized would need inverse of function to get where it would be at a certain time interval
# def split_portion(function, split, index):

#     start_time = function((index) / split)
#     end_time = function((1 + index) / split)

#     split_function = split_rate_function_interval(function, start_time, end_time)

#     def split_func(t):
#         if t < start_time:
#             return 0
#         if t > end_time:
#             return 1
#         return split_function(t)

#     return split_func