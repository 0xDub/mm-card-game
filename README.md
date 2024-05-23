# MM Casino Card Game

## The game:
- Each round, you will draw with replacement X cards within a range of 2-14, representing 2-10, J, Q, K, A")
- Some of the cards have a chance of being shown to you")
- You will be given a quote to bet on the sum of the cards drawn")
- You can bet LONG or SHORT at a certain size via 'L,10' or 'S,1' for example")
- If you don't like the odds, you can pass by pressing enter")
- Inventory is not held, it is realized at the end of each round and updates your balance")
- If you run out of money, the game is over")

Inspired by https://www.tradermath.org/market-games/market-taking-game/lobby

To the creators: if you'd like me to take this down please reach out, I'd be happy to comply no worries

<hr>

### `python3 game.py`
This is the main script to play the game. It starts with some default settings that can be changed at the top of the file

### `python3 auto.py`
Automatically plays the game based on expected values and saves it to a file for `analyze.py` to do sum statistics and stuff. Feel free to use it as inspiration for your own scripts!

### `python3 analyze.py`
Reads and does some basic analysis on the trades generated via `auto.py`
