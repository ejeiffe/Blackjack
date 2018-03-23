import random
import os

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10,
         'Queen':10, 'King':10, 'Ace':11}

class Card:
    
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
    
    def __str__(self):
        return f'{self.rank} of {self.suit}'

class Deck:
    #single deck - to be reset after every hand
    def __init__(self):
        self.deck = []  
        for suit in suits:
            for rank in ranks:
                card = Card(suit, rank)
                self.deck.append(card)
    
    def __str__(self):
        str_out = ''
        for card in self.deck:
            str_out += f'{card}\n '
        return str_out

    def shuffle(self):
        random.shuffle(self.deck)
        
    def deal(self):
        dealt_card = self.deck.pop()
        return dealt_card

class Hand:
    def __init__(self):
        self.cards = []  
        self.value = 0   
        self.aces = 0    
    
    def add_card(self,card):
        self.cards.append(card)
        self.value += values[card.rank]
        if card.rank == 'Ace':
            self.aces += 1
    
    def adjust_for_ace(self):
        if self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1


class Chips:
    
    def __init__(self):
        self.total = 100  #Players start with $100
        self.bet = 0
        
    def win_bet(self):
        self.total += self.bet

    def win_blackjack(self):
        self.total += self.bet*2
    
    def lose_bet(self):
        self.total -= self.bet

class Player:

    def __init__(self): #initialize with empty hand, default chips
        self.name = input("What's your name? ")
        self.hand = Hand()
        self.split_hand = None
        self.chips = Chips()
        self.still_in = True
        self.still_playing = True

    def reset_hand(self):
        self.hand = Hand() #replaces old hand with empty one
        self.split_hand = None
        self.still_in = True

    def show_hand(self, hand):
        print(f"\n{self.name}'s Hand: ", *hand.cards, sep='\n ')
        print(f"Hand value = {hand.value}")

    def show_total(self):
        print(f"\n{self.name} has ${self.chips.total}")


class Dealer:

    def __init__(self):
        self.hand = Hand()

    def reset_hand(self):
        self.hand = Hand() #replaces old hand with empty one

    def show_some(self):
        print("\nDealer's Hand:")
        print("<card hidden>")
        print(" ", self.hand.cards[1])

    def show_all(self):
        print(f"\nDealer's Hand: ", *self.hand.cards, sep='\n ')
        print(f"Hand value = {self.hand.value}")

def clear():
    os.system( 'cls' )

def take_bet(player):
    while True:
        try:
            bet = int(input(f"{player.name}, place your bet: "))
        except:
            print("I need an integer - try again!")
            continue
        else:
            if bet > player.chips.total:
                print(f"You only have ${player.chips.total}!")
            else:
                player.chips.bet = bet
                break

def hit(deck, hand):
    hand.add_card(deck.deal())
    hand.adjust_for_ace()

def split_hand(player):
    player.split_hand = Hand()
    split_card = player.hand.cards.pop()
    player.hand.value = values[player.hand.cards[0].rank]
    player.split_hand.add_card(split_card)
    print("Splitting...")
    print("New hands: ", '\n', *player.hand.cards, '\n', *player.split_hand.cards)

def split_check(player):
    #checks if player has a pair and enough money to double their bet
    if values[player.hand.cards[0].rank] == values[player.hand.cards[1].rank] and player.chips.bet <= 0.5*player.chips.total:
        while True:
            spl = input(f"{player.name}, you have a pair! Would you like to split? y/n: ")
            if len(spl) < 1:
                continue
            elif spl[0].lower() == 'y':
                split_hand(player)
                break
            elif spl[0].lower() == 'n':
                break
            else:
                continue

def double(deck, player, hand):
    print(f"Doubling {player.name}'s bet to ${player.chips.bet*2}")
    player.chips.bet *= 2
    hit(deck, hand)

def player_busts(player):
    print(f"{player.name} busts!")
    player.chips.lose_bet()
    player.still_in = False

def player_wins(player):
    print(f"{player.name} wins ${player.chips.bet}!")
    player.chips.win_bet()

def player_blackjack(player):
    print(f"Blackjack! {player.name} wins ${player.chips.bet*2}!")
    player.chips.win_blackjack()
    player.still_in = False

def dealer_busts(player_list):
    print("Dealer busts!")
    for player in still_in_list:
        if player.split_hand and player.hand.value < 21 and player.split_hand.value < 21:
            player_wins(player)
            player_wins(player)
        else:
            player_wins(player)
    
def player_loses(player):
    print(f"{player.name} loses ${player.chips.bet}!")
    player.chips.lose_bet()
    
def push(player):
    print(f"Push! {player.name} and dealer are tied.")
    print(f"{player.name}'s bet returned.")

def compare(player, dealer, hand):
    if hand.value < 21:
        if hand.value > dealer.hand.value:
            player_wins(player)
        elif hand.value == dealer.hand.value:
            push(player)
        else:
            player_loses(player)

def play_hand(deck, player, hand):
    if player.still_in:
        hand_active = True
        if player.chips.bet <= 0.5*player.chips.total:
            player.show_hand(hand)
            while True:
                    choice = input(f"\n{player.name}, what would you like to do?\n 1. Hit\n 2. Stand\n 3. Double\nYour choice: ")
                    if choice == '1':
                        print(f"{player.name} hits!")
                        hit(deck, hand)
                        break
                    elif choice == '2':
                        print(f"{player.name} stands.")
                        hand_active = False
                        break
                    elif choice == '3':
                        double(deck, player, hand)
                        hand_active = False
                        break
        while hand_active and len(hand.cards) < 5 and hand.value < 21:
            player.show_hand(hand)
            while True:
                choice = input(f"\n{player.name}, what would you like to do?\n 1. Hit\n 2. Stand\nYour choice: ")
                if choice == '1':
                    print(f"{player.name} hits!")
                    hit(deck, hand)
                    break
                elif choice == '2':
                    print(f"{player.name} stands.")
                    hand_active = False
                    break
                else:
                    continue
        player.show_hand(hand)
        if hand.value > 21:
            player_busts(player)
        elif hand.value == 21:
            print("Twenty-one!")
            player_wins(player)
            player.still_in = False

if __name__ == "__main__":
    """Multiplayer Blackjack game"""
    print("Welcome to Blackjack!")
    #setting up player list
    all_player_list = []
    while True:
        try:
            i = int(input("How many players? "))
        except:
            continue
        else:
            break
    for n in range(0,i):
        print("\nPlayer "+str(n+1))
        all_player_list.append("player"+str(n+1))
        all_player_list[n] = Player()

    #initialise dealer
    dealer = Dealer()

    #set up player list for the first time
    player_list = []
    for player in all_player_list:
        player_list.append(player)

    playing = True

    while playing:
        clear()
        #reset deck and active player list
        #taking bets
        for player in player_list:
            player.show_total()
            take_bet(player)

        #dealing    
        deck = Deck()

        deck.shuffle()
        print("Dealing...")
        dealer.hand.add_card(deck.deal())
        dealer.hand.add_card(deck.deal())
        dealer.show_some()
        for player in player_list:
            player.hand.add_card(deck.deal())
            player.hand.add_card(deck.deal())
            player.show_hand(player.hand)
            if player.hand.value == 21:
                player_blackjack(player)

      
        #players play their hands
        for player in player_list:
            dealer.show_some()
            split_check(player)
            play_hand(deck, player, player.hand)
            if player.split_hand:
                player.still_in = True
                play_hand(deck, player, player.split_hand)

        #checking if anyone is still in:
        still_in_list = []
        for player in player_list:
            if player.still_in:
                still_in_list.append(player)

        #dealer's hand
        if len(still_in_list) > 0:
            dealer.show_all()
            while dealer.hand.value < 17:
                print("Dealer hits...")
                hit(deck, dealer.hand)
                dealer.show_all()

        #check to see who wins/loses
            if dealer.hand.value > 21:
                dealer_busts(still_in_list)
            else:
                for player in still_in_list:
                    if player.split_hand:
                        compare(player, dealer, player.hand)
                        compare(player, dealer, player.split_hand)
                    else:
                        compare(player, dealer, player.hand)

        #review player total chips, ask if they want to play again
        for player in player_list:
            player.show_total()
            if player.chips.total <= 0:
                print(f"You're out of money {player.name}! No more gambling for you!")
                player.still_playing = False
            else:
                while True:
                    again = input(f"Another hand, {player.name}? y/n: ")
                    if len(again) == 0:
                        continue
                    elif again[0].lower() == 'y':
                        break
                    elif again[0].lower() == 'n':
                        player.still_playing = False
                        break
                    else:
                        continue

        #reset player list for anyone still playing
        player_list = []
        for player in all_player_list:
            if player.still_playing:
                player_list.append(player)

        #check for active players
        if len(player_list) == 0:
            print("\nThanks for playing!")
            for player in all_player_list:
                player.show_total()            
            playing = False
        else: #set up for next hand
            for player in player_list:
                player.reset_hand()
            dealer.reset_hand()
            try:
                input("Press enter to play the next hand...")
            except SyntaxError:
                pass







