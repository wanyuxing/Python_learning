''' Mini-project #6 - Blackjack, which can only run on 
CodeSkulptor.org (http://www.codeskulptor.org/) - Henry Wan
'''
import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
info = ''
score = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}

# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        self.handObj = []
        self.fold = False

    def __str__(self):
        cardString = ''
        for i in range(len(self.handObj)):
            cardString += str(self.handObj[i]) + ' '
        return "Hand contains " + cardString

    def add_card(self, card):
        self.handObj.append(card)

    def get_value(self):
        totalValue = 0
        existA = False
        for i in range(len(self.handObj)):
            totalValue += VALUES[self.handObj[i].get_rank()]
            if (self.handObj[i].get_rank() == 'A'):
                existA = True
        if existA and totalValue + 10 <= 21:
            totalValue += 10
        return totalValue
   
    def draw(self, canvas, pos):
        for i in range(len(self.handObj)):
            if i == 0 and self.fold == True:
                canvas.draw_image(card_back, (CARD_CENTER[0], CARD_CENTER[1]), CARD_SIZE, [pos[0] + CARD_SIZE[0], pos[1] + CARD_SIZE[1]], CARD_SIZE)
            else:
                self.handObj[i].draw(canvas, [pos[0] + CARD_CENTER[0] + 80 * i, pos[1] + CARD_CENTER[1]])
           
# define deck class 
class Deck:
    def __init__(self):
        self.deckObj = []
        for i in range(len(SUITS)):
            for j in range(len(RANKS)):
                self.deckObj.append(Card(SUITS[i], RANKS[j]))

    def shuffle(self):
        random.shuffle(self.deckObj)

    def deal_card(self):
        return self.deckObj.pop(0)
    
    def __str__(self):
        deckString = ''
        for i in range(len(self.deckObj)):
            deckString += str(self.deckObj[i]) + ' '
        return "Hand contains " + deckString  

#define event handlers for buttons
def deal():
    global outcome, in_play, deck, dealer, player, info
    if not in_play:
        deck = Deck()
        dealer = Hand()
        player = Hand()
        deck.shuffle()
        dealer.fold = True
        dealer.add_card(deck.deal_card())
        player.add_card(deck.deal_card())
        dealer.add_card(deck.deal_card())
        player.add_card(deck.deal_card())
        in_play = True
        info = 'Hit or Stand?'
    else:
        dealer.add_card(deck.deal_card())
        player.add_card(deck.deal_card())

def hit():
    global outcome, in_play, deck, player, info, score
    if in_play:
        player.add_card(deck.deal_card())
        if player.get_value() > 21:
            outcome = 'You have busted'
            info = 'New deal?'
            in_play = False
            dealer.fold = False
            score -= 1
       
def stand():
    global outcome, in_play, deck, dealer, player, score, info
    if in_play:
        while (dealer.get_value() < 17):
            dealer.add_card(deck.deal_card())
        if dealer.get_value() > 21:
            outcome = 'Dealer has busted'
            info = 'New deal?'
            score += 1
            in_play = False
            dealer.fold = False
        elif dealer.get_value() >= player.get_value():
            outcome = 'Dealer wins'
            info = 'New deal?'
            score -= 1
            in_play = False
            dealer.fold = False
        else:
            outcome = 'Player wins'
            info = 'New deal?'
            score += 1
            in_play = False
            dealer.fold = False

# draw handler    
def draw(canvas):
    global outcome, score
    player.draw(canvas, [30, 400])
    dealer.draw(canvas, [30, 120])
    canvas.draw_text('BlackJack', (65, 50), 40, 'Yellow')
    canvas.draw_text('Dealer', (65, 120), 30, 'Black')
    canvas.draw_text('Player', (65, 400), 30, 'Black')
    scoreString = 'Score ' + str(score)
    canvas.draw_text(scoreString, (300, 50), 30, 'Red')
    canvas.draw_text(outcome, (300, 120), 30, 'Red')
    canvas.draw_text(info, (300, 400), 30, 'Black')
    
# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)

# get things rolling
deal()
frame.start()