# Automatic Zacate game player
# B551 Fall 2015
# Sagar Bhadare ID: sagabhan@indiana.edu
#
# Based on skeleton code by D. Crandall
#
#

'''

A brief report on the program:

Run Command: python zecate.py
Input parameters: none
Expected sample output:
Min/max/mean scores: 131 323 214.36

Algorithm: Expectation based algorithm


The algorithm calculates the current as well as expected score for all available categories.
The expected score is given as E(x) = x * P(x)
That is, probability of X being max * score at max

Then the comparison is performed between all the expected scores and maximum is chosen for re-roll or scoring.

Algo ExpectiZecate

Dice <- Current rolled dices
Score_Board <- Current score board
Numbers = { "unos" , "doses" , "treses"  , "cuatros"  , "cincos"  , "seises" }
ExpValues = []


For each category in Numbers:
    if category is available:
        count <- max occurrence

    Exp1 = get current + expected score and dices to re-roll for max(count)

if bonus available:
    increase Exp1 score
add Exp1 to ExpValues

for each of remaining categories:

    if category available:
         Exp <- current + expected score for category, dices to re-roll for max score
         add Exp to ExpValues

maxExp <- max(ExpValues)

if lastRole:
    return category of maxExp
else:
    return re-roll of maxExp


Average Score Achieved : for 500 runs

1  Min/max/mean scores: 118 293 206.25
2  Min/max/mean scores: 123 315 207.12
3  Min/max/mean scores: 126 314 209.64
4  Min/max/mean scores: 117 326 212.02
5  Min/max/mean scores: 113 309 210.01
'''

from copy import deepcopy
from ZacateState import Dice
from ZacateState import Scorecard
import random


class Expectation:
    def __init__(self, cat, score, re_roll):
        self.cat = cat
        self.score = score
        self.re_roll = re_roll


class ZacateAutoPlayer:
    def __init__(self):
        self.cats = {"seises": 6, "cincos": 5, "cuatros": 4, "treses": 3, "doses": 2, "unos": 1}
        self.mapping = {6: "seises", 5: "cincos", 4: "cuatros", 3: "treses", 2: "doses", 1: "unos"}
        self.is_last_roll = False  # True when last roll is complete

    def first_roll(self, dice, scorecard):
        self.is_last_roll = False
        return self.get_next_roll(dice, scorecard)

    def second_roll(self, dice, scorecard):
        self.is_last_roll = False
        return self.get_next_roll(dice, scorecard)

    def third_roll(self, dice, scorecard):
        self.is_last_roll = True
        return self.get_cat(dice, scorecard)

    def get_dice_count(self, dice, value):
        return str(dice).count(str(value))

    def get_not_matching_pos(self, dice, value):  # get the dices not matching to given values

        nomatch = []
        for i, val in enumerate(dice.dice):
            if val != value:
                nomatch.append(i)
        return nomatch

    def get_matching_pos(self, dice, value):  # get the dices matching to given values

        match = []
        for i, val in enumerate(dice.dice):
            if val == value:
                match.append(i)
        return match

    def get_expectation_values(self, dice, scorecard):  # calculates the expected value of dices for each category
        expectation_values = []
        total = scorecard.totalscore  # current total score

        counts = []
        maps = {}
        cat = ''
        firstSixCats = len(
            set(self.cats.keys()) - set(scorecard.scorecard.keys()))  # number of available categories from first six
        totalCats = len(set(scorecard.scorecard.keys()))  # total available categories

        for key in set(self.cats.keys()) - set(scorecard.scorecard.keys()):
            val = self.cats.get(key)
            count = self.get_dice_count(dice, val)
            counts.append(count)
            maps[count] = key
            max_occurance = max(counts)

        if firstSixCats > 0:
            cat = maps.get(max_occurance)  # get the category for dice having maximum count

            if cat not in scorecard.scorecard:
                exp = self.get_hexa_exp(cat, dice)

                if max_occurance >= 3 and not scorecard.bonusflag:  # if bonus is still available increse \\
                    # the expected score for first six categories
                    exp.score += 5

                expectation_values.append(exp)

        if "quintupulo" not in scorecard.scorecard:
            exp = self.get_quintupulo_exp(dice)
            expectation_values.append(exp)

        if "pupusa de queso" not in scorecard.scorecard:
            exp = self.get_pupusa_de_queso_exp(dice)
            expectation_values.append(exp)

        if "pupusa de frijol" not in scorecard.scorecard:
            exp = self.get_pupusa_de_frijol_exp(dice)
            expectation_values.append(exp)

        if "elote" not in scorecard.scorecard:
            exp = self.check_Elote(dice)
            expectation_values.append(exp)

        if "triple" not in scorecard.scorecard:
            exp = self.get_triple_exp(dice)
            expectation_values.append(exp)

        if "cuadruple" not in scorecard.scorecard:
            exp = self.get_cuadruple_exp(dice)
            expectation_values.append(exp)

        if "tamal" not in scorecard.scorecard and (sum(
                dice.dice) > 20 or totalCats > 11):  # approach tamal only if score is hihg or no less categories remaining
            exp = self.get_tamal_exp(dice)
            expectation_values.append(exp)

        return expectation_values

    def get_next_roll(self, dice, scorecard):  # gives next dices to roll for round 2 and round 3

        expectation_values = self.get_expectation_values(dice, scorecard)

        maxScore = -1  # current max expected score
        nextRoll = []  # dices to re-roll

        for exp in expectation_values:
            if exp.score > maxScore:
                maxScore = exp.score
                nextRoll = deepcopy(exp.re_roll)

        return nextRoll

    def get_cat(self, dice, scorecard):  # get category for which the score should be assigned

        expectation_values = self.get_expectation_values(dice, scorecard)

        maxScore = -1
        next_cat = ''

        for exp in expectation_values:
            if exp.score > maxScore:
                maxScore = exp.score
                next_cat = exp.cat

        if next_cat == '':  # if no category matched, assign to random from available
            next_cat = random.choice(list(set(Scorecard.Categories) - set(scorecard.scorecard.keys())))

        return next_cat

    def get_pupusa_de_queso_exp(self, dice):
        cat = "pupusa de queso"
        dice_values = str(dice)
        dice_values = dice_values.replace(" ", "")
        all_values = [0, 1, 2, 3, 4]

        in_place_15 = []

        for i in range(1, 6):  # check for 12345 combination
            pos = dice_values.find(str(i))
            if pos != -1:
                in_place_15.append(dice_values.index(str(i)))

        in_place_26 = []
        if len(in_place_15) != 5:
            for i in range(2, 7):  # check for 23456 combination
                pos = dice_values.find(str(i))
                if pos != -1:
                    in_place_26.append(dice_values.index(str(i)))

        re_roll = []
        current_score = 0
        if len(in_place_15) > len(in_place_26):
            re_roll = list(set(all_values) - set(in_place_15))
        else:
            re_roll = list(set(all_values) - set(in_place_26))

        if len(re_roll) == 0:
            current_score = 40
        elif not self.is_last_roll:  # add expected score to the current score
            current_score += pow(0.1667, len(re_roll))

        return Expectation(cat, current_score, re_roll)

    def check_Elote(self, dice):
        counts = [dice.dice.count(i) for i in range(1, 7)]
        cat = "elote"
        current_score = 0
        re_roll = []
        if 3 in counts and 2 in counts:
            current_score = 25
        else:
            max_occurance = counts.index(max(counts))
            max_occurance += 1
            current_score = max(counts)

            for i, val in enumerate(dice.dice):
                if val != max_occurance:
                    re_roll.append(i)

        return Expectation(cat, current_score, re_roll)

    def get_triple_exp(self, dice):
        counts = [dice.dice.count(i) for i in range(1, 7)]
        cat = "triple"
        current_score = 0
        re_roll = []
        if max(counts) >= 3:
            current_score = sum(dice.dice)
        else:
            current_score = max(counts)

        max_occurance = counts.index(max(counts))
        max_occurance += 1

        for i, val in enumerate(dice.dice):
            if val != max_occurance:
                re_roll.append(i)

        return Expectation(cat, current_score, re_roll)

    def get_cuadruple_exp(self, dice):
        counts = [dice.dice.count(i) for i in range(1, 7)]
        cat = "cuadruple"
        current_score = 0
        re_roll = []
        if max(counts) >= 4:
            current_score = sum(dice.dice)
        else:
            current_score = max(counts)

        max_occurance = counts.index(max(counts))
        max_occurance += 1

        for i, val in enumerate(dice.dice):
            if val != max_occurance:
                if max(counts) >= 4 and val > 3:  # re-roll the last dice only if it is less than 3
                    continue
                re_roll.append(i)

        return Expectation(cat, current_score, re_roll)

    def get_tamal_exp(self, dice):
        counts = [dice.dice.count(i) for i in range(1, 7)]
        cat = "tamal"
        current_score = 0
        re_roll = []
        if counts[0] > 0:
            re_roll = self.get_matching_pos(dice, 1)

        if counts[1] > 0:
            re_roll = re_roll + self.get_matching_pos(dice, 2)

        current_score = sum(dice.dice)
        return Expectation(cat, current_score, re_roll)

    def get_quintupulo_exp(self, dice):
        counts = [dice.dice.count(i) for i in range(1, 7)]
        cat = "quintupulo"
        current_score = 0
        re_roll = []
        if 5 in counts:
            current_score = 50
        else:
            max_occurance = counts.index(max(counts))
            max_occurance += 1
            for i, val in enumerate(dice.dice):
                if val != max_occurance:
                    re_roll.append(i)
            current_score += pow(0.1667, len(re_roll)) * 50  # add expected score based on probability of all in place

        return Expectation(cat, current_score, re_roll)

    def get_pupusa_de_frijol_exp(self, dice):
        cat = "pupusa de frijol"
        dice_values = str(dice)
        dice_values = dice_values.replace(" ", "")
        all_values = [0, 1, 2, 3, 4]
        current_score = 0

        in_place_14 = []

        for i in range(1, 5):
            pos = dice_values.find(str(i))
            if pos != -1:
                in_place_14.append(dice_values.index(str(i)))

        in_place_25 = []
        if len(in_place_14) != 4:
            for i in range(2, 6):
                pos = dice_values.find(str(i))
                if pos != -1:
                    in_place_25.append(dice_values.index(str(i)))

        in_place_36 = []
        if len(in_place_14) != 4 and len(in_place_25) != 4:
            for i in range(3, 7):
                pos = dice_values.find(str(i))
                if pos != -1:
                    in_place_36.append(dice_values.index(str(i)))

        maxLen = max(len(in_place_14), len(in_place_25), len(in_place_36))

        re_roll = []

        if maxLen == len(in_place_14):
            re_roll = list(set(all_values) - set(in_place_14))
        elif maxLen == len(in_place_25):
            re_roll = list(set(all_values) - set(in_place_25))
        else:
            re_roll = list(set(all_values) - set(in_place_36))

        if len(re_roll) == 1:
            current_score = 30

        exp = current_score

        if not self.is_last_roll:
            exp += (len(re_roll) * (1 / 6) + maxLen / 4) * 30  # add expected score based on x*P(x)

        return Expectation(cat, exp, re_roll)

    def get_hexa_exp(self, cat, dice):

        dice_val = self.cats.get(cat)

        # calcualte expectation for given category
        in_place = self.get_dice_count(dice, dice_val)
        currentscore = in_place * dice_val
        re_roll = self.get_not_matching_pos(dice, dice_val)
        prob_reroll = len(re_roll) * 1.0 / 6
        exp = currentscore
        if not self.is_last_roll:  # add expected score based on x*P(x)
            exp += prob_reroll * dice_val

        return Expectation(cat, exp, re_roll)
