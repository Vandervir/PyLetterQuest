from time import sleep

from configuration import Configuration
from mouse import Mouse


class GameControl:

    def __init__(self):
        self.configuration = Configuration()
        self.mouse = Mouse()
        pass

    def resume_game(self):
        coords = self.configuration.get_button_coords(Configuration.BUTTON_RESUME_GAME)
        coords = tuple(coords)
        self.mouse.click_and_back(*coords)
        pass

    def click_letter(self, letter_dict):
        coords = self.configuration.get_button_coords('tile_{}_{}'.format(letter_dict['x'], letter_dict['y']))
        coords = tuple(coords)
        self.mouse.click_and_back(*coords)


    def shuffle_tiles(self):
        coords = self.configuration.get_button_coords(Configuration.BUTTON_SHUFFLE_TILES)
        coords = tuple(coords)
        self.mouse.click_and_back(*coords)

    def accept_word(self):
        coords = self.configuration.get_button_coords(Configuration.BUTTON_ACCEPT_TILES)
        coords = tuple(coords)
        self.mouse.click_and_back(*coords)

    def animation_break(self):
        sleep(2)