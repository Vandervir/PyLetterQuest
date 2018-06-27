from collections import OrderedDict

from database import Database
from image_recognition import ImageRecognition
from mouse import Mouse
from text_recognition import TextRecognition


class ChestMinigame:

    def __init__(self):
        self.ir = ImageRecognition()
        self.tr = TextRecognition()
        self.db = Database()
        self.mouse = Mouse()

        self.clear_minigame()
        self.button_map_init()


    def clear_minigame(self):
        self.length = 0
        self.guesses_left = 9
        self.guesses = 0
        self.guessed_letters = ''
        self.wrong_letters = ''
        self.base_letters = ''
        self.match_list = []
        self.word, self.length = self.db.get_random_word()
        self.base_letters = 'AEORS'
        self.guess_string_letters = ''
        for x in range(0, self.length):
            self.guess_string_letters += '_'

    def determine_word_length(self):
        x0 = 2153
        y0 = 188
        x1 = 2201
        y1 = 237
        resume = True
        previous_res = True
        self.length = 0
        for i in range(0, 11):
            # length = i + 1
            current_res = self.ir.is_the_same_image((x0, y0, x1, y1), 'img/chest/tile1.png', resume=resume,
                                            acceptable_ratio=0.6)
            # print('#{} is {}'.format(i + 1, current_res))
            resume = False
            if current_res == False and previous_res == True:
                self.length = i
            previous_res = current_res
            x0 += 2 + 48
            x1 += 2 + 48
        print('length {}'.format(self.length))
        pass

    def button_map_init(self):
        letters = dict()
        letters['Q'] = {'row': 0, 'col': 0}
        letters['W'] = {'row': 0, 'col': 1}
        letters['E'] = {'row': 0, 'col': 2}
        letters['R'] = {'row': 0, 'col': 3}
        letters['T'] = {'row': 0, 'col': 4}
        letters['Y'] = {'row': 0, 'col': 5}
        letters['U'] = {'row': 0, 'col': 6}
        letters['I'] = {'row': 0, 'col': 7}
        letters['O'] = {'row': 0, 'col': 8}
        letters['P'] = {'row': 0, 'col': 9}
        letters['A'] = {'row': 1, 'col': 0}
        letters['S'] = {'row': 1, 'col': 1}
        letters['D'] = {'row': 1, 'col': 2}
        letters['F'] = {'row': 1, 'col': 3}
        letters['G'] = {'row': 1, 'col': 4}
        letters['H'] = {'row': 1, 'col': 5}
        letters['J'] = {'row': 1, 'col': 6}
        letters['K'] = {'row': 1, 'col': 7}
        letters['L'] = {'row': 1, 'col': 8}
        letters['Z'] = {'row': 2, 'col': 0}
        letters['X'] = {'row': 2, 'col': 1}
        letters['C'] = {'row': 2, 'col': 2}
        letters['V'] = {'row': 2, 'col': 3}
        letters['B'] = {'row': 2, 'col': 4}
        letters['N'] = {'row': 2, 'col': 5}
        letters['M'] = {'row': 2, 'col': 6}
        self.button_map = letters

    def click_letter(self, letter):
        position = self.button_map[letter]
        x = 2096 + (position['col'] * 50)
        y = 397 + (position['row'] * 50)
        self.mouse.click_and_back(x, y)

    def try_input(self):
        if self.guesses_left < 1:
            print('GAME OVER')
            return
        letter = ''
        if self.guesses < 5:
            letter = self.base_letters[self.guesses]
        else:
            # db prediction time
            res = self.db.try_find_words(self.guess_string_letters, self.length, self.wrong_letters)
            #TODO remove debug
            if res == []:
                print(self.guess_string_letters, self.length, self.wrong_letters)
            letter = self.try_guess_next_letter(res)
        print(letter)

        self.guessed_letters = "".join((self.guessed_letters, letter))
        self.click_letter(letter)

        correct = self.recognize_letters(letter)
        # res, correct, count2, match_list = self.test_word(letter)
        # print(res, correct, count2, match_list)

        if not correct:
            self.wrong_letters = "".join((self.wrong_letters, letter))
            self.guesses_left -= 1
            print('#{} GUESSES LEFT'.format(self.guesses_left))
        # else:
            # self.match_list += match_list
        self.guesses += 1


    def recognize_letters(self, letter):
        x0 = 2159
        y0 = 192
        x1 = 2195
        y1 = 231
        match = 0
        for count in range (0, self.length):
            result = self.tr.detect_text((x0, y0, x1, y1), resume=False)
            if result.__len__() == 1 and result == letter:
                match+=1
                self.guess_string_letters = self.guess_string_letters[0:count] + letter + self.guess_string_letters[count + 1:]
                print(result)
            x0 += 14 + 36
            x1 += 14 + 36

        return match > 0

    def get_correct_letters(self):
        pass

    def test_set_length(self, length):
        self.length = length
        self.base_letters = self.probability_dict[length]
        pass

    def test_word(self, guess_letter):
        res = ''
        count = 0
        correct = False
        count2 = 0
        match_list = []
        for letter in self.word:
            if letter == guess_letter:
                res += guess_letter
                count2 += 1
                correct = True
                match_list.append({'letter': letter, 'place': count})
                self.guess_string_letters = self.guess_string_letters[0:count] + letter + self.guess_string_letters[count + 1:]
            else:
                res += '-'

            count += 1

        return res, correct, count2, match_list

    def try_guess_next_letter(self, array):
        sum = dict()
        for word, length in array:
            for letter in word:
                letter = str(letter)
                if letter in self.guessed_letters:
                    continue
                if not sum.has_key(letter):
                    sum[letter] = 1
                else:
                    sum[letter] += 1
        import operator
        sum = sorted(sum.items(), key=operator.itemgetter(1), reverse=False)
        return sum.pop()[0]
