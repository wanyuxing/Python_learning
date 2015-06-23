'''This Python Program can only run on Codeskulptor,
Implementation of classic arcade game Pong - Henry Wan
'''

import simplegui
import random

# initialize globals - positions and velocity encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
pad_velocity = 5
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
acceleration = 1
count = 3
paddle1_pos = [[PAD_WIDTH - 1, HEIGHT / 2 - HALF_PAD_HEIGHT - 1], 
               [PAD_WIDTH - 1, HEIGHT / 2 + HALF_PAD_HEIGHT], 
               [0, HEIGHT / 2 + HALF_PAD_HEIGHT],
               [0, HEIGHT / 2 - HALF_PAD_HEIGHT - 1]] 
paddle2_pos = [[WIDTH - PAD_WIDTH - 1, HEIGHT / 2 - HALF_PAD_HEIGHT - 1],
               [WIDTH - PAD_WIDTH - 1, HEIGHT / 2 + HALF_PAD_HEIGHT], 
               [WIDTH - 1, HEIGHT / 2 + HALF_PAD_HEIGHT],
               [WIDTH - 1, HEIGHT / 2 - HALF_PAD_HEIGHT - 1]]
score1, score2 = 0, 0
paddle1_vel, paddle2_vel = 0, 0
ball_pos = [WIDTH / 2, HEIGHT / 2]
ball_vel = [random.randrange(2, 4), random.randrange(1, 3)]

# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_pos = [WIDTH / 2, HEIGHT / 2]
    if direction == 'RIGHT':
        ball_vel = [random.randrange(2, 4), random.randrange(1, 3)]
    elif direction == 'LEFT':
        ball_vel = [-random.randrange(2, 4), random.randrange(1, 3)]

# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2, count  # these are ints
    score1, score2 = 0, 0
    paddle1_vel, paddle2_vel = 0, 0
    spawn_ball('RIGHT')
    count = 3
    timer.start()
    
def countdown():
    global count
    count -= 1
    print count 
    if count <= 0:
        timer.stop()   
        
timer = simplegui.create_timer(1000, countdown)
timer.start()

def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
    global paddle1_vel, paddle2_vel, direction, acceleration    
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
    
    if timer.is_running():
        canvas.draw_circle([WIDTH / 2, HEIGHT / 2], BALL_RADIUS, 1, 'White')
        canvas.draw_text('Countdown ' + str(count), [WIDTH / 2 - 50, HEIGHT / 2 - 50], 20, 'Red')
    else: 
    # update ball
        ball_pos[0] += ball_vel[0]
        ball_pos[1] += ball_vel[1]
    
    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 1, 'White')
    
    # update paddle's vertical position, keep paddle on the screen
    if paddle1_pos[0][1] + paddle1_vel >=0 and paddle1_pos[1][1] + paddle1_vel < HEIGHT:
        paddle1_pos[0][1] += paddle1_vel
        paddle1_pos[1][1] += paddle1_vel
        paddle1_pos[2][1] += paddle1_vel
        paddle1_pos[3][1] += paddle1_vel
        
    if paddle2_pos[0][1] + paddle2_vel >=0 and paddle2_pos[1][1] + paddle2_vel < HEIGHT:
        paddle2_pos[0][1] += paddle2_vel
        paddle2_pos[1][1] += paddle2_vel
        paddle2_pos[2][1] += paddle2_vel
        paddle2_pos[3][1] += paddle2_vel
 
    # draw paddles
    canvas.draw_polygon(paddle1_pos, 1, 'Yellow')
    canvas.draw_polygon(paddle2_pos, 1, 'Yellow')
    
    # determine whether paddle and ball collide    
    if ball_pos[1] - BALL_RADIUS <= 0 or ball_pos[1] + BALL_RADIUS >= HEIGHT - 1:
        ball_vel[1] = - ball_vel[1]
    
    if ball_vel[0] > 0:
        if ball_pos[0] + BALL_RADIUS >= paddle2_pos[0][0] and ball_pos[1] >= paddle2_pos[0][1] and ball_pos[1] <= paddle2_pos[2][1]:
            ball_vel[0] = - ball_vel[0] - acceleration
        if ball_pos[0] + BALL_RADIUS >= WIDTH - 1:
            score1 += 1
            spawn_ball('LEFT')
    else:
        if ball_pos[0] - BALL_RADIUS <= paddle1_pos[0][0] and ball_pos[1] >= paddle1_pos[0][1] and ball_pos[1] <= paddle1_pos[2][1]:
            ball_vel[0] = - ball_vel[0] + acceleration
        if ball_pos[0] - BALL_RADIUS <=0:
            score2 += 1
            spawn_ball('RIGHT')
    
    # draw scores
    canvas.draw_text(str(score1) + ' / ' + str(score2), (530, 30), 20, 'Red')
        
def keydown(key):
    global paddle1_vel, paddle2_vel, pad_velocity
    if chr(key) == 'S':
        paddle1_vel += pad_velocity
    if chr(key) == '(':
        paddle2_vel += pad_velocity
    if chr(key) == 'W':
        paddle1_vel -= pad_velocity
    if chr(key) == '&':
        paddle2_vel -= pad_velocity
        
def keyup(key):
    global paddle1_vel, paddle2_vel, pad_velocity
    if chr(key) == 'S':
        paddle1_vel -= pad_velocity
    if chr(key) == '(':
        paddle2_vel -= pad_velocity
    if chr(key) == 'W':
        paddle1_vel += pad_velocity
    if chr(key) == '&':
        paddle2_vel += pad_velocity

# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)

# add restart button and setup countdown
button1 = frame.add_button('Start/Restart', new_game, 100)

# start frame
new_game()
frame.start()
