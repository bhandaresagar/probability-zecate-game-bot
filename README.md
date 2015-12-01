# probability-zecate-game-bot
AI player for dice game zecate 

Zacate is a traditional dice game played in some parts of Latin America. It can be played alone or against
two or more players. Here are the rules. At the beginning of each turn, the player rolls a set of 5 dice. He or
she inspects the dice, and chooses any subset (including none or all) to roll again. He or she again inspects
the dice, and again rerolls any subset. The turn is then over, and the player must assign the outcome to
exactly one of the following categories, depending on which 5 dice are showing after the third roll:

• Unos: The player can add the number of dice that show 1 to his or her score.
• Doses: The player can count the number of dice that show 2, multiply by 2, and add to the score.
• Treses: The player can count the number of dice that show 3, multiply by 3, and add to the score.
• Cuatros: The player can count the number of dice that show 4, multiply by 4, and add to the score.
• Cincos: The player can count the number of dice that show 5, multiply by 5, and add to the score.
• Seises: The player can count the number of dice that show 6, multiply by 6, and add to the score.
• Pupusa de queso: If the five dice are either 1, 2, 3, 4, 5 or 2, 3, 4, 5, 6, the player can add 40 points to
their score. (Note that for this and all other categories, the order of the dice is not important.)
• Pupusa de frijol: If the four of the five dice are either 1, 2, 3, 4, or 2, 3, 4, 5, or 3, 4, 5, 6, the player
can add 30 points to their score.
• Elote: If three of the dice show the same number, and the other two dice are also the same, the player
can add 25 points to their score.
• Triple: If three of the dice are the same, the player can add up the values of all five dice and add this
to their score.
• Cuadruple: If four of the dice are the same, the player can add up the values of all five dice and add
the sum to their score.
• Quntupulo: If all five dice are the same, the player can add 50 points to their score.
• Tamal: The sum of all five dice, no matter what they are.

Players often have a choice of which category to fill with any particular roll, but each category may be
filled only once per game. A player can also choose to assign a roll to a category that does not match
the requirements, but then nothing is added to their score. After 13 turns, all categories are full, and the
game ends. If the player managed to get a score of at least 63 totaled across the first six categories (Unos
through Seises), they get a bonus of 35 points added to their score.
The program plays one-player Zacate as well as possible, i.e. getting the highest possible score.
The goal is to achieve as high an average score as possible in after running program multiple times so that player plays many games.

Commandline : python zacate.py