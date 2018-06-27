# -*- coding: utf-8 -*-
import copy
import time

from chest_minigame import ChestMinigame
from database import Database
from dictionary_tree import TreeCreator
from game_control import GameControl
from game_state_detector import GameStateDetector
from text_recognition import TextRecognition


class MainMan:
    def __init__(self):
        self.state = None
        self.gsd = GameStateDetector()
        self.tr = TextRecognition()
        self.d = Database()
        self.gc = GameControl()
        self.tc = TreeCreator()
        self.ch = ChestMinigame()

    def main_loop(self):
        while True:
            print('Detecting states')
            self.state = self.gsd.get_game_state()
            print(self.state)
            self.monster_battle()
            self.shopping_time()
            self.chest_hangman_minigame()
            self.chest_hangman_prize()
            time.sleep(3)

    def is_current_state(self, state_name):
        return self.state is state_name

    def chest_hangman_minigame(self):
        if not self.is_current_state(self.gsd.STATE_CHEST_MINIGAME):
            return

        self.ch.determine_word_length()
        while True:
            if self.gsd.get_game_state() == self.gsd.STATE_CHEST_MINIGAME_PRIZE:
                self.chest_hangman_prize()
            self.ch.try_input()

    def chest_hangman_prize(self):
        self.ch.clear_minigame()
        if not self.is_current_state(self.gsd.STATE_CHEST_MINIGAME_PRIZE):
            return
        # TODO add science
        self.gc.chest_reward_prize(3)

    def shopping_time(self):
        if not self.is_current_state(self.gsd.STATE_SHOP):
            return
        # todo
        self.gc.exit_shop()

    def monster_battle(self):
        if not self.is_current_state(self.gsd.STATE_MONSTER_BATTLE):
            return

        self.tr.recognize_tiles()
        clean_word_map = self.tr.get_letters_map()
        word_map = copy.deepcopy(clean_word_map)
        # print('Found letters: {}'.format(self.tr.get_letters()))

        first_word = self.tc.search(self.tr.get_letters())
        print('search finish: {}'.format(first_word))
        while True:
            try:
                word = self.tc.get_next_word()
            except KeyError:
                print('End of dictionary - no word is correct')
                print('Problem with recognising')
                print('Activate madman enter mode')
                raise Exception('Madman mode required')

            # TODO use potion method

            # TODO use purify method

            if word is None:
                print('No word - shuffling')
                self.gc.shuffle_tiles()
                return
            # print(word_map)
            for letter in word:
                letter_dict = word_map[letter].pop()
                self.gc.click_letter(letter_dict)
                print('writting letter: {}'.format(letter))
            if self.gsd.ms_has_correct_word():
                print('correct word')
                self.gc.accept_word()
                self.gc.animation_break()
                return
            else:
                print('cancelling word')
                word_map = copy.deepcopy(clean_word_map)
                self.gc.cancel_word()


if __name__ == '__main__':
    print('Letter Quest')
    mm = MainMan()
    mm.main_loop()
