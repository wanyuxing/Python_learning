''' This program is only workable on CodeSkulptor
"Stopwatch: The Game" - Henry Wan
'''

import simplegui

# define global variables, msec is one 10th of a sec

count = 0
msec = 0
sec = 0
minute = 0
win = 0
attempt = 0

'''define helper function format that converts time
in tenths of seconds into formatted string A:BC.D
'''

def format(count):
    minute = count / 600
    sec = (count - 600 * minute) / 10
    msec = (count - 600 * minute ) % 10
    if sec >= 10:
        return str(minute) + ':' + str(sec) + '.' + str(msec)
    else:
        return str(minute) + ':0' + str(sec) + '.' + str(msec)
    
# define event handlers for buttons; "Start", "Stop", "Reset"

def start():
    timer.start()

def stop():
    global attempt, win
    if timer.is_running():
        attempt = attempt + 1
        if count % 10 == 0:
            win = win + 1
    timer.stop()
    

def reset():
    global count, msec, sec, minute, win, attempt
    timer.stop()
    count, msec, sec, minute, win, attempt = 0, 0, 0, 0, 0, 0

# define event handler for timer with 0.1 sec interval

def timer_handler():
    global count, msec, sec, minute
    count = count + 1
    format(count)
    
# define draw handler

def draw_handler(canvas):
    global count, msec, sec, minute, win, attempt
    canvas.draw_text(format(count), (100, 150), 50, 'White')
    canvas.draw_text(str(win) + '/' + str(attempt), (250, 20), 20, 'Red')
    
# create frame

frame = simplegui.create_frame("Stopwatch: The Game", 300, 300)
timer = simplegui.create_timer(100, timer_handler)
frame.set_draw_handler(draw_handler)

# register event handlers

button1 = frame.add_button('Start', start, 50)
button2 = frame.add_button('Stop', stop, 50)
button3 = frame.add_button('Reset', reset, 50)

# start frame

frame.start()
