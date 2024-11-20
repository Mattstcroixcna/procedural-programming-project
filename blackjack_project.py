def main():
    print("Blackjack")
    print("blackjack payment is 3:2")
    bet()

def bet():
    with open('money.txt', 'r') as file:
        cash = int(file.read())
        print("money: ", cash)
        bet = int(input("bet: "))
        new_total = cash - bet
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
        '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, 
    '7': 7, '8': 8, '9': 9, '10': 10, 
    'J': 10, 'Q': 10, 'K': 10, 'A': [1, 11]
    }
    deck = []

    for suit in suits:
        for rank in ranks:
            card = {'card': f"{rank} of {suit}", 'value': rank_value[rank]}
            deck.append(card)
