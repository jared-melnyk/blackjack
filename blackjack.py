'''
Play a game of blackjack against the computer dealer
'''

import random
import os

width = os.get_terminal_size().columns

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('2', '3', '4', '5', '6', '7', 
	'8','9', '10', 'Jack', 'Queen', 'King', 'Ace')
values = {'2':2, '3':3, '4':4, '5':5, '6':6, 
	'7':7, '8':8, '9':9, '10':10, 'Jack':10, 'Queen':10, 
	'King':10, 'Ace':11}

class Card():
	'''
	A standard playing card
	'''

	def __init__(self, suit, rank):
		self.suit = suit
		self.rank = rank

	def __str__(self):
		return(f"{self.rank} of {self.suit}")

class Deck():
	'''
	A deck of 52 Cards
	'''

	def __init__(self):
		self.deck = []
		for suit in suits:
			for rank in ranks:
				self.deck.append(Card(suit, rank))

	def count(self):
		num_cards = 0
		for card in self.deck:
			num_cards += 1
		return num_cards

	def __str__(self):
		deck_disp = []
		for card in self.deck:
			deck_disp.append(str(card))
		return "\n".join(deck_disp)

	def shuffle(self):
		random.shuffle(self.deck)

	def deal(self):
		return(self.deck.pop())

class Hand():
	'''
	A hand of some number of Cards
	'''

	def __init__(self):
		self.cards = []
		self.value = 0
		self.aces = 0

	def __str__(self):
		hand_disp = ascii_version_of_card(*self.cards)
		return str(hand_disp)

	def add_card(self,card):
		self.cards.append(card)
		if card.rank == 'Ace':
			self.aces += 1
		self.value += values[card.rank]
		if self.value > 21 and self.aces > 0:
			self.value -= 10
			self.aces -= 1


class Chips:
	
	def __init__(self):
		self.total = 1000
		self.bet = 0

	def win_bet(self):
		self.total += self.bet

	def lose_bet(self):
		self.total -= self.bet


def take_bet():
	while True:

		try:
			bet = int(input(f'\nYou have {bankroll.total} chips.' 
				'\n\nHow many would you like to bet? '))
		except ValueError:
			print('\nYou must bet a whole number of chips.')
		else:
			if 0 < bet <= bankroll.total:
				return bet
			else:
				print(f'\nYour bet must be between 0 and {bankroll.total} chips.')


def take_hit(deck, hand):
	hand.add_card(deck.deal())

def player_move(deck, dealer_hand, player_hand):

	print('''\n\
1. Hit
2. Stay
''')
	
	while True:
		print(f'You have {player_hand.value}. There are {deck.count()} cards left in the deck.')
		try:
			move = int(input('\nEnter a number to make your move: '))
		except ValueError:
			print('You must enter 1 or 2!')
			continue
		if move == 1:
			take_hit(deck,player_hand)
			if player_hand.value > 21:
				player_busts(player_hand)
		elif move == 2:
			dealer_move(deck,dealer_hand, player_hand)
		else:
			print('You must enter 1 or 2!')

		break

	

def dealer_move(deck, dealer_hand, player_hand):
	global playing
	while dealer_hand.value <	 17:
		take_hit(deck, dealer_hand)
	playing = False
	display_hands(player_hand,dealer_hand,playing)
	if dealer_hand.value > 21:
		dealer_busts(dealer_hand)
	elif dealer_hand.value > player_hand.value:
		dealer_wins(dealer_hand)
	elif dealer_hand.value == player_hand.value:
		push()
	else:
		player_wins(player_hand)


def display_hands(player_hand,dealer_hand,playing):
	
	print('\nDEALER\'S HAND')
	if playing:
		print(ascii_version_of_hidden_card(*dealer_hand.cards))
	else:
		print(ascii_version_of_card(*dealer_hand.cards))

	print('\nYOUR HAND')
	print(ascii_version_of_card(*player_hand.cards))

def player_busts(hand):
    global playing
    playing = False
    display_hands(player_hand, dealer_hand, playing)
    print(f'\nYOU BUSTED WITH {player_hand.value}, GOOMBA!')
    bankroll.lose_bet()


def player_wins(hand):
    print(f'YOU WIN WITH {hand.value}')
    bankroll.win_bet()

def dealer_busts(hand):
    print(f'DEALER BUSTED WITH {hand.value}')
    bankroll.win_bet()
    
def dealer_wins(hand):
    print(f'DEALER WINS WITH {hand.value}')
    bankroll.lose_bet()
    
def push():
    print('OH GEEZ IT\'S A PUSH')

def got_cash():
	if bankroll.total > 0:
		return True
	else:
		print('\nYOU''RE BROKE, PLAYA!')
		print('\n1. Hit the ATM')
		print('2. Quit')
		while True:
			try:
				choice = int(input('\nWhat do you want to do? '))
			except ValueError:
				print('You must enter 1 or 2!')
			if choice == 1:
				bankroll.total = 1000
				return True
			elif choice == 2:
				print('\nGOODNIGHT, AND DON''T FORGET TO TIP THE DEALER!')
				print('\n' * 2)
				return False
			else:
				print('You must enter 1 or 2!')
			break


disp_card = """\
┌─────────┐
│{}       │
│         │
│         │
│    {}   │
│         │
│         │
│       {}│
└─────────┘
""".format('{rank: <2}', '{suit: <2}', '{rank: >2}')

disp_card_hidden = """\
┌─────────┐
│░░░░░░░░░│
│░░░░░░░░░│
│░░░░░░░░░│
│░░░░░░░░░│
│░░░░░░░░░│
│░░░░░░░░░│
│░░░░░░░░░│
└─────────┘
"""

def join_lines(strings):
    """
    Stack strings horizontally.
    This doesn't keep lines aligned unless the preceding lines have the same length.
    :param strings: Strings to stack
    :return: String consisting of the horizontally stacked input
    """
    liness = [string.splitlines() for string in strings]
    return '\n'.join(''.join(lines) for lines in zip(*liness))

def ascii_version_of_card(*cards):
    """
    Instead of a boring text version of the card we render an ASCII image of the card.
    :param cards: One or more card objects
    :return: A string, the nice ascii version of cards
    """

    # we will use this to prints the appropriate icons for each card
    name_to_symbol = {
        'Spades':   '♠',
        'Diamonds': '♦',
        'Hearts':   '♥',
        'Clubs':    '♣',
    }

    def card_to_string(card):
        # 10 is the only card with a 2-char rank abbreviation
        rank = card.rank if card.rank == '10' else card.rank[0]

        # add the individual card on a line by line basis
        return disp_card.format(rank=rank, suit=name_to_symbol[card.suit])


    return join_lines(map(card_to_string, cards))


def ascii_version_of_hidden_card(*cards):
    """
    Essentially the dealers method of print ascii cards. This method hides the first card, shows it flipped over
    :param cards: A list of card objects, the first will be hidden
    :return: A string, the nice ascii version of cards
    """

    return join_lines((disp_card_hidden, ascii_version_of_card(*cards[1:])))

while True:
	'''
	Play a game of blackjack
	'''
	bankroll = Chips()

	print('\n' * 40)
	print('             __'.center(width))
	print('             /(`o'.center(width))
	print('       ,-,   //  \\\\'.center(width))
	print('      (,,,)  ||   V'.center(width))
	print(' (,,,,)\//'.center(width))
	print(' (,,,/w)-\''.center(width))
	print('\,,/w)'.center(width))
	print('`V/uu'.center(width))
	print(' / |'.center(width))
	print(' | |'.center(width))
	print(' o o'.center(width))
	print(' \ |'.center(width))
	print('   \,/  ,\|,.  \,/'.center(width))

	print('\n')
	print('~~ WELCOME TO THE FLAMINGO ~~'.center(width))
	print('\n' * 4)

	
	while got_cash() == True:

		playing = True
		deck = Deck()
		dealer_hand = Hand()
		player_hand = Hand()

		bankroll.bet = take_bet()	

		deck.shuffle()
		for i in range(0,2):
			dealer_hand.add_card(deck.deal())
			player_hand.add_card(deck.deal())

		while playing:

			display_hands(player_hand,dealer_hand,playing)
			
			player_move(deck, dealer_hand, player_hand)

		

	break

'''
TODO
1. blackjack pays 3 to 2
2. run out of money / zero chips
3. auto stay on 21?
'''





























