import random
# this block of code is where im storing global variables
deck = []
dealer = []
player = []
draw = 1
play = 1
player_points = 0
dealer_points = 0
with open('money.txt', 'r') as file:
        cash = int(file.read())



def main():
    make_cards()
    print("Blackjack")
    print("blackjack payment is 3:2")
    # at first i had the game play through main but i made game its own function so i could repeat stuff
    while play == 1:
        game()

def game():
    global draw
    global cash
    global play

    # Reset deck and hands
    reset_deck()
    player.clear()
    dealer.clear()
    
    cash = int(cash)
    if cash < 5:
        purchase()
    else:
        pass
    bet()
    draw_dealer_card()
    draw_dealer_card()
    print("DEALER'S SHOW CARD:")
    print(show_dealer_card())
    draw_player_card()
    draw_player_card()
    print("YOUR HAND:")
    show_player_cards()
    player_total()
    dealer_total()

    # Player turn
    draw = 1
    while draw == 1:
        hit_or_stand()
        player_total()
        dealer_total()
        check_player_bust(player_points)
        if draw == 2 and player_points <= 21:
            print("Game Over. You chose to stand!")
            print("DEALERS CARDS:")
            show_dealer_cards()
            print()
            print("YOUR POINTS: ", player_points)
            print("DEALERS POINTS: ", dealer_points)
            check_win(player_points, dealer_points)
            break
        elif player_points > 21:
            print("You busted!")
            break
    
    print()
    choice = input("would you like to continue (y/n):")
    if choice == 'y':
        play = 1
    elif choice == 'n':
        play = 2
        return play


    
def purchase():
    global cash
    print("BUY SOME TOKENS!!")
    print("100 tokens - 10 dollars")
    print("200 tokens - 20 dollars")
    print("500 tokens - 40 dollars")
    choice = int(input("how many tokens would you like (100, 200, 500): "))
    with open('money.txt', 'r') as file:
        cash = cash + choice
        cash = str(cash)
    with open('money.txt', 'w') as file:
        file.write(cash)
        


    

# this function opens and writes the money.txt file
def bet():
    global bet_amount
    global cash
    with open('money.txt', 'r') as file:
        cash = int(file.read())
        print("money: ", cash)
        bet_amount = int(input("bet: "))
        new_total = cash - bet_amount
        new_total = str(new_total)
    with open('money.txt', 'w') as file:
        file.write(new_total)
    with open('money.txt', 'r') as file:
        cash = int(file.read())
        print(cash)
        return bet_amount

#makes the deck
def make_cards():
    suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    rank_value = {
        '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10,
        'J': 10, 'Q': 10, 'K': 10, 'A': [1, 11]
    }

    global deck
    for suit in suits:
        for rank in ranks:
            card = {'card': f"{rank} of {suit}", 'value': rank_value[rank]}
            deck.append(card)


#resets the deck before each game
def reset_deck():
    global deck
    deck = []
    make_cards()


# the next two functions handle drawing cards for the dealer and player respectively using the random module
def draw_dealer_card():
    card = random.choice(deck)
    dealer.append(card)
    deck.remove(card)
    return card['card']

def draw_player_card():
    card = random.choice(deck)
    player.append(card)
    deck.remove(card)
    handle_ace_choice(card, player_points)
    return card['card']

# the next two functions show the cards as "rank of suit" for the dealer and player respectively
def show_dealer_card():
    card = dealer[0]
    return card['card']

def show_player_cards():
    for card in player:
        print(card['card'])

def show_dealer_cards():
    for card in dealer:
        print(card['card'])

# checks player total
def player_total():
    global player_points
    player_points = 0
    for card in player:
        if isinstance(card['value'], list):  # Ace
            player_points += handle_ace_choice(card, player_points)
        else:
            player_points += card['value']
    return player_points


def dealer_total():
    global dealer_points
    dealer_points = 0
    for card in dealer:
        if isinstance(card['value'], list):
            ace_value = 11 if dealer_points + 11 <= 21 else 1
            dealer_points += ace_value
        else:
            dealer_points += card['value']
    return dealer_points



def check_player_bust(player_points):
    global draw
    if player_points > 21:
        draw = 2
        print("You busted!")


# asks if the player wants to hit or stand and changes the draw variable accordingly
def hit_or_stand():
    global draw
    hit_stand = input("Hit or Stand? (hit/stand): ")
    if hit_stand == "hit":
        draw_player_card()
        draw_dealer_card()
        show_player_cards()
        check_player_bust(player_points)
        
    elif hit_stand == "stand":
        draw = 2


# gives the player a choice of using 11 or 1 for the value of the ace unless an 11 would make the player bust in which case ace is worth 1 
def handle_ace_choice(card, current_points):
    if 'final_value' in card:
        return card['final_value']

    if card['card'].startswith('A'):
        print(f"You drew an Ace! Current total: {current_points}")
        if current_points + 11 <= 21:
            ace_value = int(input("Would you like the Ace to be 11 or 1? (Enter 11 or 1): "))
            while ace_value not in [1, 11]:
                ace_value = int(input("Invalid choice. Please enter 11 or 1: "))
        else:
            print("An 11 would cause a bust, so the Ace will be worth 1.")
            ace_value = 1


        card['final_value'] = ace_value
        return ace_value

    return card['value']


def win():
    global cash
    winings = int(bet_amount * 1.5)
    cash = cash + winings
    cash = str(cash)
    with open('money.txt', 'w') as file:
        file.write(cash)

#checks to see if a player won, tied, or lost after they stand
def check_win(player_points, dealer_points):
    global cash
    if player_points > dealer_points or dealer_points > 21:
        win()
        print(f"You win! New balance: {cash}")
    elif player_points == dealer_points:
        print("It's a tie! Your bet is returned.")
        with open('money.txt', 'r+') as file:
            file.seek(0)
            file.write(str(cash + bet_amount))
    else:
        print("Sorry, you lose.")


 

main()