import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import statistics

plt.style.use('dark_background')

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

def main():

    # =-= Reading =-= #

    with open(f"automatic_trades.txt", "r") as f:
        lines = f.readlines()
        lines = [x.rstrip() for x in lines]
        lines = [x.split(",") for x in lines if x != ""]
    data = pd.DataFrame(lines, columns=["difference", "pnl"])
    data = data.astype(float)

    # =-= Analyzing =-= #
    # (Take this with a grain of salt as I'm not a QR, this is mostly just messing around to try and learn something / gain some intuition)
    # The objective is to see how the standard deviation of the underlying distribution affects the PnL given the EV Difference of the trade
    # the standard deviation will be a little different than expected tho (I think) due to the possibility of known cards
    # 3 SD, expected percent: 0.15%
    # 2 SD, expected percent: 2.5%
    # 1 SD, expected percent: 16%

    print()
    print(bcolors.HEADER + "=-=-=-= PnL Analysis of Autoplay =-=-=-=" + bcolors.ENDC)
    print()

    pnl_mean = statistics.mean(data["pnl"])
    pnl_standard_deviation = statistics.stdev(data["pnl"])
    print(f"Total |:| Mean PnL: {round(pnl_mean, 2)}")
    print(f"Total |:| StDev PnL: {round(pnl_standard_deviation, 2)}")
    print()
    print(bcolors.DIM + "=--------------------------------------------=" + bcolors.ENDC)
    print()

    one_standard_deviation = statistics.stdev(CARDS * NUM_OF_CARDS)

    # let's cut the data frame by the standard deviation and see the probability of < -PnL
    _3_sd_data = data[data["difference"] > one_standard_deviation*3]
    _3_sd_percent = (len(_3_sd_data[_3_sd_data["pnl"] < 0]) / len(_3_sd_data)) * 100
    _3_sd_mean = statistics.mean(_3_sd_data["pnl"])
    _3_sd_standard_deviation = statistics.stdev(_3_sd_data["pnl"])
    print(f"3 SD |:| Mean PnL: {round(_3_sd_mean, 2)}")
    print(f"3 SD |:| StDev PnL: {round(_3_sd_standard_deviation, 2)}")
    print(f"3 SD |:| Negative PnL Trades: {round(_3_sd_percent, 2)}%")
    print()

    _2_sd_data = data[data["difference"] > one_standard_deviation*2]
    _2_sd_percent = (len(_2_sd_data[_2_sd_data["pnl"] < 0]) / len(_2_sd_data)) * 100
    _2_sd_mean = statistics.mean(_2_sd_data["pnl"])
    _2_sd_standard_deviation = statistics.stdev(_2_sd_data["pnl"])
    print(f"2 SD |:| Mean PnL: {round(_2_sd_mean, 2)}")
    print(f"2 SD |:| StDev PnL: {round(_2_sd_standard_deviation, 2)}")
    print(f"2 SD |:| Negative PnL Trades: {round(_2_sd_percent, 2)}%")
    print()

    _1_sd_data = data[data["difference"] > one_standard_deviation]
    _1_sd_percent = (len(_1_sd_data[_1_sd_data["pnl"] < 0]) / len(_1_sd_data)) * 100
    _1_sd_mean = statistics.mean(_1_sd_data["pnl"])
    _1_sd_standard_deviation = statistics.stdev(_1_sd_data["pnl"])
    print(f"1 SD |:| Mean PnL: {round(_1_sd_mean, 2)}")
    print(f"1 SD |:| StDev PnL: {round(_1_sd_standard_deviation, 2)}")
    print(f"1 SD |:| Negative PnL Trades: {round(_1_sd_percent, 2)}%")
    

    # =-= Plotting =-= #

    fig, ax = plt.subplots(1)
    ax.set_title("PnL Distribution")
    ax.set_xlabel("PnL")
    ax.set_ylabel("Frequency")

    ax.hist(data["pnl"], bins=100, color="#21fced", alpha=0.75)
    ax.axvline(x=0, color="white")
    ax.axvline(x=pnl_mean, color="#ed21fc", label="Mean")

    ax.legend()


    fig, ax = plt.subplots(1)
    ax.set_title("PnL vs EV Difference")
    ax.set_xlabel("PnL")
    ax.set_ylabel("EV Difference")

    sns.kdeplot(data=data, x="pnl", y="difference", ax=ax)

    ax.axhline(y=one_standard_deviation, color="green", label="1 SD")
    ax.axhline(y=one_standard_deviation*2, color="blue", label="2 SD")
    ax.axhline(y=one_standard_deviation*3, color="red", label="3 SD")

    ax.axvline(x=0, color="white")

    ax.legend()
    plt.show()


main()