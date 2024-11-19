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

if __name__ == "__main__":
    main()