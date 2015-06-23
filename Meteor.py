''' This Python program can only run on Codeskulptor,
this is to check wheter a shooting star crosses a
rectangular obstacle - Henry Wan'''

import simplegui

# starting point and velocity vector setup
star = [10, 20]
vector = [3, 0.7]

# four verticles of rectangular
rect_ul = [50, 50]
rect_ur = [180, 50]
rect_lr = [180, 140]
rect_ll = [50, 140]

# draw rectangular and meteor
def draw_handler(canvas):
    canvas.draw_line(rect_ul, rect_ur, 2, 'red')
    canvas.draw_line(rect_ul, rect_ll, 2, 'red')
    canvas.draw_line(rect_ur, rect_lr, 2, 'red')
    canvas.draw_line(rect_ll, rect_lr, 2, 'red')
    canvas.draw_line([10, 20], star, 2, 'white')
    
# Tiker setup to determine meteor's position
def timer_handler():
    star[0] += vector[0]
    star[1] += vector[1]

# setup frame and timer

frame = simplegui.create_frame('Test', 800, 600)
frame.set_draw_handler(draw_handler)
timer = simplegui.create_timer(100, timer_handler)

# start frame and timer

frame.start()
timer.start()

