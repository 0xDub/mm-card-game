import statistics
import random
import time

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    UNDERLINE = '\033[4m'

CARDS = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
NUM_OF_CARDS = 3
SHOW_CARDS = 2
STARTING_BALANCE = 500

def generate_fair_price():
    mean_number = (sum(CARDS) / len(CARDS)) * NUM_OF_CARDS
    standard_deviation = statistics.stdev(CARDS * NUM_OF_CARDS) # concatenate the list NUM_OF_CARDS times
    fair_price = random.gauss(mean_number, standard_deviation)
    bid = round(fair_price - 1)
    ask = round(fair_price + 1)
    return bid, ask

def print_cards(drawn_cards):
    shown_cards = 0
    print_string = f"Pulls {bcolors.OKCYAN}|:|{bcolors.ENDC} "
    for card in drawn_cards:
        if random.choice([True, False]) and shown_cards < SHOW_CARDS:
            print_string += f"{card} | "
            shown_cards += 1
        else:
            print_string += "X | "
    print_string = print_string[:-3]
    print(print_string)

def calc_pnl(position, size, bid, ask, max_long_position, max_short_position, drawn_cards):
    real_price = sum(drawn_cards)

    print(bcolors.DIM + "-------------- Results --------------" + bcolors.ENDC)

    pnl = 0
    if position == "L":
        if size > max_long_position:
            print(bcolors.WARNING + f"Max long position is {max_long_position}. You tried to take {size}. Trade is not being recorded" + bcolors.ENDC)
        else:

            print_string = f"Drawn {bcolors.OKCYAN}|:|{bcolors.ENDC} "
            for i, card in enumerate(drawn_cards):
                print_string += f"{card} | "
            print_string = print_string[:-3]
            print(print_string)

            print(f"Open: {ask} | Realized: {real_price}")
            pnl = (real_price - ask) * size
    elif position == "S":
        if size > max_short_position:
            print(bcolors.WARNING + f"Max short position is {max_short_position}. You tried to take {size}. Trade is not being recorded" + bcolors.ENDC)
        else:

            print_string = f"Drawn {bcolors.OKCYAN}|:|{bcolors.ENDC} "
            for i, card in enumerate(drawn_cards):
                print_string += f"{card} | "
            print_string = print_string[:-3]
            print(print_string)

            print(f"Open: {bid} | Realized: {real_price}")
            pnl = (bid - real_price) * size
    return pnl

def get_position_and_size(user_input):
    position = user_input.split(",")[0].strip().upper()
    size = int(user_input.split(",")[1].strip())
    return position, size

def draw_card():
    return random.choice(CARDS)

def main():

    print()
    print(bcolors.HEADER + "=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=" + bcolors.ENDC)
    print(bcolors.HEADER + "=-=-=-=-= Welcome to the Card Casino! =-=-=-=-=" + bcolors.ENDC)
    print(bcolors.HEADER + "=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=" + bcolors.ENDC)
    print()

    print("The game:")
    print(" - Each round, you will draw with replacement X cards within a range of 2-14, representing 2-10, J, Q, K, A")
    print(" - Some of the cards have a chance of being shown to you")
    print(" - You will be given a quote to bet on the sum of the cards drawn")
    print(" - You can bet LONG or SHORT at a certain size via 'L,10' or 'S,1' for example")
    print(" - If you don't like the odds, you can pass by pressing enter")
    print(" - Inventory is not held, it is realized at the end of each round and updates your balance")
    print(" - If you run out of money, the game is over")
    print()

    print("Good luck!")
    print()

    balance = STARTING_BALANCE
    print(bcolors.DIM + f"NUM_OF_CARDS: {NUM_OF_CARDS} | SHOW_CARDS: {SHOW_CARDS}" + bcolors.ENDC)
    print(bcolors.OKGREEN + f"Starting balance: ${balance}" + bcolors.ENDC)

    while True:

        drawn_cards = []
        for i in range(NUM_OF_CARDS):
            drawn_cards.append(draw_card())

        print()
        print(bcolors.OKCYAN + "=--=--=--=--=--=--= Next Draw =--=--=--=--=--=--=" + bcolors.ENDC)
        print_cards(drawn_cards)

        bid, ask = generate_fair_price()
        
        print(f"Quote {bcolors.OKCYAN}|:|{bcolors.ENDC} {bid} | {ask}")
        print()

        max_short_position = round(balance / bid)
        max_long_position = round(balance / ask)

        if balance < bid or balance < ask:
            print(bcolors.FAIL + "You are out of money. Game over." + bcolors.ENDC)
            break

        print(bcolors.DIM + f"Max Short Position: {max_short_position}x | Max Long Position: {max_long_position}x" + bcolors.ENDC)
        user_input = input("Your Trade: ")
        if user_input == "":
            continue
        
        split_user_input = user_input.split(",")
        if len(split_user_input) != 2:
            print(bcolors.FAIL + "Invalid input. Please type position,size such as L,1 or S,5" + bcolors.ENDC)
            continue
        
        position = split_user_input[0].strip().upper()
        size = int(split_user_input[1].strip())
        print()

        pnl = calc_pnl(position, size, bid, ask, max_long_position, max_short_position, drawn_cards)
        balance += pnl

        if pnl > 0:
            print(bcolors.OKGREEN + f"PnL: ${pnl} | Balance: ${balance}" + bcolors.ENDC)
        elif pnl < 0:
            print(bcolors.FAIL + f"PnL: ${pnl} | Balance: ${balance}" + bcolors.ENDC)
        else:
            print(bcolors.DIM + f"PnL: ${pnl} | Balance: ${balance}" + bcolors.ENDC)

        time.sleep(1)

main()