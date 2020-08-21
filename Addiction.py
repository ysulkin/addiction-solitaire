#!/usr/bin/env python
# coding: utf-8

# In[319]:


import random
import string
from IPython.display import clear_output
import math
import colorama

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 
            'Nine':9, 'Ten':10, 'Jack':11, 'Queen':12, 'King':13, 'Ace':1}
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 
            'Nine':9, 'Ten':10, 'Jack':11, 'Queen':12, 'King':13, 'Ace':1}
playing = True


# In[ ]:





# In[320]:


class Card:
    
    
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.value = values[rank]
        
    def __str__(self):
        dsuit = {'Hearts': '♥', 'Diamonds': '♦', 'Spades': '♠', 'Clubs' : '♣'}
        drank = {2:'2', 3:'3', 4:'4', 5:'5', 6:'6', 7:'7', 8:'8', 
            9:'9', 10:'10', 11:'J', 12:'Q', 13:'K', 1:'A'}
        black = '\u001b[30m'
        if self.suit == 'Hearts' or self.suit == 'Diamonds':
            color = '\x1b[31m'
        else:
            color = black
        return '{}{}{}'.format(color, drank[self.value], dsuit[self.suit], black) 


# In[ ]:





# In[321]:


print(Card('Hearts', 'Two'))
print(Card('Spades', 'Two'))


# In[322]:


class Deck:
    
    def __init__(self):
        self.deck = []
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit,rank))
                
    def __str__(self):
        s = ''
        for card in self.deck:
            s += card.__str__() + '\n'
        return s
    
    def __len__(self):
        return len(self.deck)
            
    def shuffle(self):
        random.shuffle(self.deck)
        
    def deal(self):
        return self.deck.pop()


# In[ ]:





# In[291]:


class Game:
    
    def __init__(self):
        self.shuffles = 4
        self.board = [ [ None for i in range(13) ] for j in range(4) ]
        self.deck = Deck()
    
    def __str__(self):
        s = 'Shuffles: {}\n\t|'.format(self.shuffles)
        
        s += '\t'.join([str(i) for i in range(13)]) + '\n'+ '_'*113 + '\n'
        for i, row in enumerate(self.board):
            s += str(i) + '\t|'
            for col in row:
                if col == None:
                    s += '\t'
                else:
                    s += col.__str__() + '\t'
            s += '\n\t|\n'
        return s
    
    
    def refill_deck(self):
        self.deck.deck = [Card('Spades','Ace'), Card('Hearts','Ace'), Card('Diamonds','Ace'),Card('Clubs','Ace')]
        # iterate through each row
        for i in range(len(self.board)):
            # set valid test parameters
            j = 0
            if self.board[i][j] != None:
                suit = self.board[i][j].suit
                while self.board[i][j] != None and self.board[i][j].suit == suit and self.board[i][j].value == (j+2):
                    j += 1
                while j < 13:
                    card = self.board[i][j]
                    if card != None:
                        self.deck.deck.append(card)
                        self.board[i][j] = None
                    j += 1
                    
    def shuffle(self):
        # Check if shuffles are left
        self.deck.shuffle()
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j] == None:
                    cell = self.deck.deal()
                    if cell.rank != 'Ace':
                        self.board[i][j] = cell
        self.shuffles -= 1


# In[283]:


test_game = Game()


# In[315]:


test_game.refill_deck()


# In[ ]:





# In[323]:


test_game.shuffle()
print(test_game)


# In[317]:


print(test_game)


# In[213]:


def empty_cell(game, pos):
    row, col = pos
    if (0 <= row <= 3 and 0 <= col <= 12):
        return game.board[row][col] == None
    return False


# In[214]:


def get_rank(val): 
    for rank, value in values.items(): 
        if val == value: 
            return rank 


# In[196]:


def ask_for_suit(game):    
    while True:
        suit = input('Pick a suit: ')
        if suit in suits:
            return suit
            


# In[197]:


def erase_old_card(game, card):
    
    for i in range(len(game.board)):
        for j in range(len(game.board[i])):
            if game.board[i][j] != None and game.board[i][j].suit == card.suit and game.board[i][j].value == card.value:
                game.board[i][j] = None
                return game
    return game


# In[ ]:





# In[198]:


def pick_spot(game):

    while True:
        try:
            print(game)
            pos = input('Choose an empty space (row,col): ')
            row,col = int(pos[0]), int(pos[2:])
        except:
            # Case: not a cooradnet
            clear_output()
            print('Sorry, invalid format')
        else:
            # Case: not an empty cell
            if not empty_cell(game, (row, col)): 
                clear_output()
                print('Sorry, that is not an empty cell')
            elif col != 0 and (game.board[row][col - 1] == None or game.board[row][col - 1].value == 13):
                clear_output()
                print('Nothing to move there')
            elif col == 0:
                card = Card(ask_for_suit(game), 'Two')
                game = erase_old_card(game, card)
                game.board[row][col] = card
                clear_output()
                return game
            else:
                card = Card(game.board[row][col - 1].suit, get_rank(game.board[row][col - 1].value + 1))
                game = erase_old_card(game, card)
                game.board[row][col] = card
                clear_output()
                return game


# In[199]:


# pick_spot(test_game)


# In[200]:


print(test_game)


# In[201]:


def moves_available(game):
    spots = 0
    for i in range(len(game.board)):
        if game.board[i][0] == None:
            return True
        for j in range(1, len(game.board[i])):
            card = game.board[i][j]
            if card == None:
                if game.board[i][j - 1] != None and game.board[i][j - 1].value < 13:
                    return True
                else:
                    spots += 1
            if spots == 4:
                return False
    return False


# In[325]:


def won(game):
    for row in game.board:
        if row[0] == None or row[0].value != 2:
            return False
        suit = row[0].suit
        for (val, card) in zip(range(3, 14), row[1:14]):
            if card == None or card.suit != suit or card.value != val:
                return False
    return True


# In[203]:


print(test_game)
won(test_game)


# In[205]:


print(test_game)
test_game = test_game.refill_deck()
print(test_game)


# In[120]:


def end_game(outcome):
    if outcome == 'won':
        print('Yay you won!')
    else:
        print('Sorry, you lost :(')
    while True:
        playing = input("Play again? Y/N: ")
        if playing == 'Y':
            return True
        elif playing == 'N':
            return False
    return False


# In[ ]:


def play_game():
    playing = True
    print('Welcome to Addiction Solitaire!')

    while playing:
        # reset the game
        game = Game()
        game.shuffle()

        while True:
            if moves_available(game):
                game = pick_spot(game)
            else:
                if won(game):
                    playing = end_game('won')
                    break
                elif game.shuffles == 0:
                    playing = end_game('lost')
                    break
                else:
                    game.refill_deck()
                    print('Shuffling...no moves left')
                    game.shuffle()


# In[ ]:


play_game()


# In[ ]:





# In[ ]:




