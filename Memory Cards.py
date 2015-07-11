''' implementation of card game, which can only run CodeSkultor.org
(http://www.codeskulptor.org/) - Henry Wan
'''

import simplegui
import random

counts = 0

# helper function to initialize globals
def new_game():
    global cards, counts, newLabel
    cards = []
    counts = 0
    newLabel = 'Turns = 0'
    label.set_text(newLabel)
    for i in range(16):
        cards.append([i / 2, False, 'Green', False])
    random.shuffle(cards)

# define event handlers
def mouseclick(pos):
    # add game state logic here
    global cards, counts, newLabel, flip
    mouse_pos = list(pos)
    x = mouse_pos[0]
    y = mouse_pos[1]
    if x > 0  and x < 800 and y > 0  and y < 100 and cards[x / 50][1] == False:
        cards[x / 50][1] = True
        cards[x / 50][2] = 'Black'
        counts += 1
        newLabel = 'Turns = ' + str(counts)
        label.set_text(newLabel)
        for i in range(16):
            if cards[i][3] == False and i != (x / 50) and cards[i][1] == True:
                if cards[i][0] == cards[x / 50][0]:
                    cards[i][3] = True
                    cards[x / 50][3] = True
                else:  
                    cards[i][1] = False
                    cards[i][2] = 'Green'
                           
# cards are logically 50x100 pixels in size    
def draw(canvas):
    global cards
    for i in range(16):
        canvas.draw_polygon([(50 * i, 0), (50 * (i + 1), 0), (50 * (i + 1), 100), (50 * i, 100)], 1, 'Red', cards[i][2])
    for j in range(16):
        if cards[j][1] == True or cards[j][3] == True:
            canvas.draw_text(str(cards[j][0]), (50 * j + 15, 60), 40, 'White')

# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()