# Marrakech board game

> This repository is made for the Introduction to Programming course project - Dec 2015.

Marrakech board game implemented in `python 2.7` using [Pygame](https://www.pygame.org/news).

---

**Dependencies:**
- [Pygame](https://www.pygame.org/wiki/GettingStarted)

---

Board game rules ([BoardGameGeek](https://boardgamegeek.com/boardgame/29223/marrakech)'s description):

In Marrakech each player takes the role of a rug salesperson who tries to outwit the competition. Each player starts with **10 coins** and an **equal number of carpets**.

On your turn, you may: 
1. Rotate Assam 90 degrees. 
2. Roll the dice and move him forward as many spaces as showing (d6: 1, 2, 2, 3, 3, 4).
3. If Assam reaches the edge of the board, follow the curve and continue moving in the next row.
4. If Assam lands on another player's carpet, you must pay that player 1 coin per square showing that is contiguous with the landed-on square.
5. Place one of your carpets orthogonally adjacent to Assam (but may not directly overlay another carpet).

The game ends when all players have played all carpets. Each gets 1 coin per visible square. The player with most coins wins!

---

To play, run `main.py`.

On each player's turn:
1. To rotate Assam 90 degrees or to go straight, click on either `Left`, `Straight`, or `Right`.
2. To roll the dice and move Assam, click on `Dice!`.
3. To place your carpet, click on two tiles orthogonally adjacent to Assam (The red circle!)

- Note 1: Each player's turn is indicated with the colored circle on the top right corner of the window.
- Note 2: The three small circles on Assam indicates the direction he is facing
- Note 3: The number inside each carpet indicates the number of the round that the carpet is placed on that tile.

![Marrakech board in Pygame](/pygame-board.png)
