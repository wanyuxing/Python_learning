''' This program is only workable on CodeSkulptor
Mini-project - Week 2 "Guess the Number" Game - Henry Wan
'''

# Import modules

import simplegui
import random
import math

''' Initialize a new game with global variables 
  - secret_number 
  - n (the total number of remaining guesses)
'''

def new_game1():
    '''Start a new game with range of [0, 100) and 
    initialize secret_number and number of guesses
    '''
    global secret_number, n, last_guess, lower, upper
    secret_number = random.randrange(0, 100)
    n = int(math.ceil(math.log(100, 2)))
    lower = 0
    upper = 99
    print 'New game. Range is from 0 to 100'
    print 'Number of remaining guesses is ', n
    print ''

def new_game2():
    ''' Start a new game with range of [0, 1000) and 
    initialize secret_number and number of guesses
    '''
    global secret_number, n, last_guess, lower, upper
    secret_number = random.randrange(0, 1000)
    n = int(math.ceil(math.log(1000, 2)))
    lower = 0
    upper = 999
    print 'New game. Range is from 0 to 1000'
    print 'Number of remaining guesses is ', n
    print ''

# Guess starts after the initialization

def input_guess(inp):
    # Compare guess and secret_number and then print outputs
    global secret_number, n, last_guess, lower, upper
    # Guess is only valid when n is not negative
    if n > 0:
        if int(inp) <= upper and int(inp) >= lower:
            n -= 1
            print 'Guess was ', inp
            print 'Number of remaining guesses is ', n
            # Compare guess and secret_number
            if int(inp) > secret_number:
                print 'Lower!'
                upper = int(inp) - 1
            elif int(inp) < secret_number:
                print 'Higher!'
                lower = int(inp) + 1
            else:
                print 'Correct!'
            print ''
        else:
            print 'The input is out of range, pls input again'
            print ''
    else:
        return
        
# Create 'Guess the Game' frame

frame = simplegui.create_frame('Guess the Number', 200, 200, 300)

# Add input box in the frame and assign inputs to event-handler

inp = frame.add_input('My Guess', input_guess, 100)

# Add two buttons to restart game and set guess range

button1 = frame.add_button('Range:0 - 100', new_game1, 100)
button2 = frame.add_button('Range:0 - 1000', new_game2,100)
