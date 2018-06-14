# -*- coding: utf-8 -*-

from database import Database
from dictionary_tree import TreeCreator
from game_control import GameControl
from text_recognition import TextRecognition


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