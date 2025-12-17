class Yahtzee:

    @staticmethod
    def chance(d1, d2, d3, d4, d5):
        dice = [d1, d2, d3, d4, d5]
        return Yahtzee.chance_new(dice)

    @staticmethod
    def chance_new(dice):
        return sum(dice)

    @staticmethod
    def yahtzee(d1, d2, d3, d4, d5):
        dice = [d1, d2, d3, d4, d5]
        return Yahtzee.yahtzee_new(dice)

    def __init__(self, d1, d2, d3, d4, d5):
        self.dice = [d1, d2, d3, d4, d5]

    @staticmethod
    def yahtzee_new(dice):
        counts = Yahtzee.make_counts(dice)
        if 5 in counts:
            return 50
        return 0

    @staticmethod
    def sum_of_dice_with_value(dice, value):
        return sum(die for die in dice if die == value)

    @staticmethod
    def make_counts(dice):
        counts = [0] * 6
        for die in dice:
            counts[die - 1] += 1
        return counts

    @staticmethod
    def find_value_with_count(counts, target_count):
        for index, count in enumerate(counts):
            if count == target_count:
                return index + 1
        return 0

    @staticmethod
    def number_category(dice, value):
        return Yahtzee.sum_of_dice_with_value(dice, value)

    @staticmethod
    def ones(d1, d2, d3, d4, d5):
        return Yahtzee.number_category([d1, d2, d3, d4, d5], 1)

    @staticmethod
    def twos(d1, d2, d3, d4, d5):
        return Yahtzee.number_category([d1, d2, d3, d4, d5], 2)

    @staticmethod
    def threes(d1, d2, d3, d4, d5):
        return Yahtzee.number_category([d1, d2, d3, d4, d5], 3)

    def sum_for_number(self, value):
        return sum(die for die in self.dice if die == value)

    def fours(self):
        return self.sum_for_number(4)

    def fives(self):
        return self.sum_for_number(5)

    def sixes(self):
        return self.sum_for_number(6)

    @staticmethod
    def score_pair(d1, d2, d3, d4, d5):
        dice = [d1, d2, d3, d4, d5]
        counts = Yahtzee.make_counts(dice)
        for index in range(5, -1, -1):
            if counts[index] == 2:
                return (index + 1) * 2
        return 0

    @staticmethod
    def two_pair(d1, d2, d3, d4, d5):
        dice = [d1, d2, d3, d4, d5]
        counts = Yahtzee.make_counts(dice)

        first_pair_val = Yahtzee.find_value_with_count(counts, 2)
        if not first_pair_val:
            return 0

        counts[first_pair_val - 1] = 0
        second_pair_val = Yahtzee.find_value_with_count(counts, 2)

        if second_pair_val:
            return (first_pair_val + second_pair_val) * 2
        return 0

    @staticmethod
    def three_of_a_kind(d1, d2, d3, d4, d5):
        dice = [d1, d2, d3, d4, d5]
        counts = Yahtzee.make_counts(dice)
        for index in range(6):
            if counts[index] == 3:
                return (index + 1) * 3
        return 0

    @staticmethod
    def four_of_a_kind(d1, d2, d3, d4, d5):
        dice = [d1, d2, d3, d4, d5]
        counts = Yahtzee.make_counts(dice)
        for index in range(6):
            if counts[index] == 4:
                return (index + 1) * 4
        return 0

    @staticmethod
    def smallStraight(d1, d2, d3, d4, d5):
        dice = [d1, d2, d3, d4, d5]
        counts = Yahtzee.make_counts(dice)
        if all(counts[i] >= 1 for i in range(0, 5)):
            return 15
        return 0

    @staticmethod
    def largeStraight(d1, d2, d3, d4, d5):
        dice = [d1, d2, d3, d4, d5]
        counts = Yahtzee.make_counts(dice)
        if all(counts[i] >= 1 for i in range(1, 6)):
            return 20
        return 0

    @staticmethod
    def fullHouse(d1, d2, d3, d4, d5):
        dice = [d1, d2, d3, d4, d5]
        counts = Yahtzee.make_counts(dice)

        pair_value = Yahtzee.find_value_with_count(counts, 2)
        triple_value = Yahtzee.find_value_with_count(counts, 3)

        if pair_value and triple_value:
            return pair_value * 2 + triple_value * 3
        return 0
