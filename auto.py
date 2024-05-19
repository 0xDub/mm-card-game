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

def generate_fair_price():
    mean_number = (sum(CARDS) / len(CARDS)) * NUM_OF_CARDS
    standard_deviation = statistics.stdev(CARDS * NUM_OF_CARDS) # concatenate the list NUM_OF_CARDS times
    fair_price = random.gauss(mean_number, standard_deviation)
    bid = round(fair_price - 1)
    ask = round(fair_price + 1)
    return bid, ask

def generate_expected_value(known_cards):
    expected_value = 0
    for card in known_cards:
        expected_value += card
    random_cards = NUM_OF_CARDS - len(known_cards)
    expected_value += (sum(CARDS) / len(CARDS)) * random_cards
    return expected_value

def calc_pnl(real_price, position, size, bid, ask):
    if position == "L":
        pnl = (real_price - ask) * size
    elif position == "S":
        pnl = (bid - real_price) * size
    return pnl

def draw_card():
    return random.choice(CARDS)

def main():
    trades_file = open("automatic_trades.txt", "w")

    print("[+] Starting automatic trades...")

    draws = 5000
    draw_count = 0
    while draw_count < draws:
        drawn_cards = []
        for i in range(NUM_OF_CARDS):
            drawn_cards.append(draw_card())

        shown_cards = 0
        known_cards = []
        for card in drawn_cards:
            if random.choice([True, False]) and shown_cards < SHOW_CARDS:
                known_cards.append(card)
                shown_cards += 1

        real_price = sum(drawn_cards)
        expected_value = generate_expected_value(known_cards)
        bid, ask = generate_fair_price()

        trade = False
        if expected_value > ask: # long
            pnl = calc_pnl(real_price, "L", 1, bid, ask)
            difference = expected_value - ask
            trade = True
        if expected_value < bid: # short
            pnl = calc_pnl(real_price, "S", 1, bid, ask)
            difference = bid - expected_value
            trade = True
        
        if trade:
            trades_file.write(f"{difference},{pnl}\n")
            time.sleep(0.0001)
            draw_count += 1

    print(bcolors.OKGREEN + "[+] Automatic trades finished" + bcolors.ENDC)

main()