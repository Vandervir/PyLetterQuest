import os
from pytesseract import pytesseract
from configuration import Configuration
from game_control import GameControl
from screen import grab_screen


class TextRecognition:
    tiles_number_horizontal = 5
    tiles_number_veritical = 3

    def __init__(self):
        self.PYTESSERACT_CONFIG = '--psm 13 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        self.PYTESSERACT_CONFIG3 = '--psm 8 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        self.PYTESSERACT_CONFIG2 = '--psm 13 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz?'
        os.putenv("TESSDATA_PREFIX", os.path.dirname(os.path.abspath(__file__)))
        self.c = Configuration()
        self.gc = GameControl()

    def add_letter(self, x, y, letter):
        if self.map.has_key(letter):
            self.map[letter].append({'x': x, 'y': y, 'letter': letter})
        else:
            self.map[letter] = [{'x': x, 'y': y, 'letter': letter}]
            pass

    def recognize_tiles(self):
        self.gc.resume_game()
        self.letters = ''
        self.map = dict()
        for x in range(1, self.tiles_number_horizontal + 1):
            for y in range(1, self.tiles_number_veritical + 1):
                region = self.c.get_range_coords('tile_{}_{}'.format(x, y))
                screen = grab_screen(region)

                letter = pytesseract.image_to_string(image=screen, config=self.PYTESSERACT_CONFIG, )
                if letter.__len__() > 1:
                    continue
                self.letters = "".join((self.letters, letter))
                self.add_letter(x, y, letter)
                print('tile_{}_{}: {}'.format(x, y, letter))

    def detect_text(self, region, resume=True):
        if resume:
            self.gc.resume_game()
        screen = grab_screen(region)
        return pytesseract.image_to_string(image=screen, config=self.PYTESSERACT_CONFIG3)

    def get_letters(self):
        return self.letters

    def get_letters_map(self):
        return self.map
