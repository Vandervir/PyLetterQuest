import re


class WordClassification:

    def __init__(self):
        self.new_search()

    def new_search(self):
        self.best_word = ''
        self.best_points = 0

    def get_word(self):
        return self.best_word

    def run(self, word):
        self.word = word
        self.points = 0
        self._get_length_points()
        self._get_one_point_letters()
        self._get_two_point_letters()
        self._get_three_point_letters()
        self._get_letter_combo_points()
        if self.points > self.best_points:
            print('new best word: {}'.format(word))
            self.best_points = self.points
            self.best_word = self.word
            return True
        return False

    def _get_length_points(self):
        self.points += self.word.__len__() * 2

    def _get_one_point_letters(self):
        letters = 'AOGUERNLTSDI'
        for letter in letters:
            self.points += self.word.count(letter) * 2

    def _get_two_point_letters(self):
        letters = 'CFHMYPVWB'
        for letter in letters:
            self.points += self.word.count(letter) * 4

    def _get_three_point_letters(self):
        letters = 'QJXKZ'
        for letter in letters:
            self.points += self.word.count(letter) * 6

    def _get_letter_combo_points(self):
        matches = re.finditer(r"(\w)\1+", self.word)
        for matchNum, match in enumerate(matches):
            self.points +=  5