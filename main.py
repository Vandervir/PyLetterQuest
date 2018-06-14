# -*- coding: utf-8 -*-
import logging
import os

from configuration import Configuration
from database import Database
from dictionary_tree import TreeCreator
from game_control import GameControl
from mouse import Mouse
from text_recognition import TextRecognition


def init():
    logging.basicConfig(filename='error.log', level=logging.DEBUG)

def test_buttons():
    c = Configuration()
    m = Mouse()
    import time

    for ix in [Configuration.BUTTON_RESUME_GAME, Configuration.BUTTON_ACCEPT_TILES, Configuration.BUTTON_SHUFFLE_TILES]:
        x,y = c.get_button_coords(ix)
        print("{}. - {} {}".format(ix, x, y))
        m.mouse.move(x, y)
        time.sleep(1)
    print()

def test_game_control():
    gc = GameControl()
    gc.resume_game()

def test_database_search():
    d = Database()
    res = d.find_longest_word('ASDFGHJKL')
    print(res)

def test_recognize():
    a = TextRecognition()
    a.recognize_tiles()


def test_game():
    tr = TextRecognition()
    d = Database()
    gc = GameControl()

    tc = TreeCreator()

    while True:
        tr.recognize_tiles()
        word_map = tr.get_letters_map()
        print('Found letters: {}'.format(tr.get_letters()))
        # word, word_length = d.find_longest_word(tr.get_letters())
        word = tc.search(tr.get_letters())

        if word is None or word == '':
            print('Word not found - shuffling')
            gc.shuffle_tiles()
            continue
        print('Found word: {}'.format(word))
        for letter in word:
            letter_dict = word_map[letter].pop()
            gc.click_letter(letter_dict)
            print('writting letter: {}'.format(letter))
        gc.accept_word()
        print('accepting word')
        gc.animation_break()



if __name__ == '__main__':
    print('Letter Quest')
    test_game()
    pass