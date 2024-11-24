import random
# this block of code is where im storing global variables
deck = []
dealer = []
dealer_card_only = []
player = []
draw = 1

def main():
    make_cards()
    print("Blackjack")
    print("blackjack payment is 3:2")
    # at first i had the game play through main but i made game its own function so i could repeat stuff
    play = 1
    while play == 1:
        game()

def game():
    bet()
    draw_dealer_card()
    draw_dealer_card()
    print("DEALER'S SHOW CARD:")
    print(show_dealer_card())
    draw_player_card()
    draw_player_card()
    print("YOUR HAND:")
    show_player_cards()

    # while draw is equal to 1 the player can hit or stand
    while draw == 1:
        hit_or_stand()
        player_points = player_total()
        check_player_bust(player_points)
        if draw == 2:
            print("Game Over. You chose to stand!")
            break  # Exit the loop if player stands
        elif player_points > 21:
            print("You busted!")
            break  # Exit the loop if the player busts


    

# this function opens and writes the money.txt file
def bet():
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

def make_cards():
    suits = ['Hearts', 'Diamonds', 'CLubs', 'Spades']
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    rank_value = {
        '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10,'J': 10, 'Q': 10, 'K': 10, 'A': [1, 11]
    }

    for suit in suits:
        for rank in ranks:
            card = {'card': f"{rank} of {suit}", 'value': rank_value[rank]}
            deck.append(card)

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
    handle_ace_choice(card)
    return card['card']

# the next two functions show the cards as "rank of suit" for the dealer and player respectively
def show_dealer_card():
    card = dealer[0]
    return card['card']

def show_player_cards():
    for card in player:
        print(card['card'])

# checks player total
def player_total():
    player_points = 0
    for card in player:
        if isinstance(card['value'], list):
            player_points += handle_ace_choice(card)
        else:
            player_points += card['value']
    return player_points


def check_player_bust(player_points):
    global draw
    if player_points > 21:
        draw = 2
        print("You busted!")


# asks if the player wants to hit or stand and changes the draw variable accordingly
def hit_or_stand():
    global draw
    hit_stand = input("Hit or Stand? (hit/stand):")
    if hit_stand.lower() == "hit":
        draw = 1
    elif hit_stand.lower() == "stand":
        draw = 2
    return draw


# gives the player a choice of using 11 or 1 for the value of the ace unless an 11 would make the player bust in which case ace is worth 1 
def handle_ace_choice(card):
    if card['card'].startswith('A'):
        if player_total() + 11 <= 21:  
            print(f"You drew an Ace! You can choose 11 or 1. Current total: {player_total()}")
            ace_value = 11  
        else:
            ace_value = 1  
        return ace_value
    return 0  



main()