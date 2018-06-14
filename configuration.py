#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging
import math

from yaml import load
from yaml import Loader, Dumper


class Configuration:
    config = None
    CONFIG_DISPLAY = 'display'
    CONFIG_BUTTONS = 'buttons'
    CONFIG_RANGES = 'ranges'

    BUTTON_RESUME_GAME = 'resume_game'
    BUTTON_ACCEPT_TILES = 'accept_tiles'
    BUTTON_SHUFFLE_TILES = 'shuffle_tiles'
    BUTTON_TILE_1_1 = 'tile_1_1'
    BUTTON_TILE_2_1 = 'tile_2_1'
    BUTTON_TILE_3_1 = 'tile_3_1'
    BUTTON_TILE_4_1 = 'tile_4_1'
    BUTTON_TILE_5_1 = 'tile_5_1'
    BUTTON_TILE_1_2 = 'tile_1_2'
    BUTTON_TILE_2_2 = 'tile_2_2'
    BUTTON_TILE_3_2 = 'tile_3_2'
    BUTTON_TILE_4_2 = 'tile_4_2'
    BUTTON_TILE_5_2 = 'tile_5_2'
    BUTTON_TILE_1_3 = 'tile_1_3'
    BUTTON_TILE_2_3 = 'tile_2_3'
    BUTTON_TILE_3_3 = 'tile_3_3'
    BUTTON_TILE_4_3 = 'tile_4_3'
    BUTTON_TILE_5_3 = 'tile_5_3'

    DISPLAY_LEFT_TOP_CORNER_X = 'left_top_corner_x'
    DISPLAY_LEFT_TOP_CORNER_Y = 'left_top_corner_y'
    DISPLAY_GAME_RESOLUTION_WIDTH = 'game_resolution_width'
    DISPLAY_GAME_RESOLUTION_HEIGHT = 'game_resolution_height'
    DISPLAY_FIX_TOP = 'fix_top'
    DISPLAY_FIX_RIGHT = 'fix_right'

    def __init__(self):
        self.config = self.load_config()

    def load_config(self):
        stream = open('configuration.yaml', 'r')
        return load(stream, Loader=Loader)

    def get(self, category_name, name, default=None, var_type=None):
        try:
            return self.config['config'][category_name][name]
        except KeyError:
            if default is None:
                logging.warning('Missing yaml configuration - config.{}.{}'.format(category_name, name))
            return default


    def get_squares_coordinates(self, coord_x, coord_y):
        if coord_x > 5 or coord_x < 1 or coord_y > 3 or coord_y < 1:
            raise Exception('Tile of out range')

        return self.get_button_coords('tile_{}_{}'.format(coord_x, coord_y))

    def get_button_coords(self, name):
        try:
            variable = self.get(self.CONFIG_BUTTONS, name)
            fix_top = self.get(self.CONFIG_DISPLAY, self.DISPLAY_FIX_TOP)
            fix_right = self.get(self.CONFIG_DISPLAY, self.DISPLAY_FIX_RIGHT)
            left_top_corner_x = self.get(self.CONFIG_DISPLAY, self.DISPLAY_LEFT_TOP_CORNER_X)
            left_top_corner_y = self.get(self.CONFIG_DISPLAY, self.DISPLAY_LEFT_TOP_CORNER_Y)
            game_resolution_width = self.get(self.CONFIG_DISPLAY, self.DISPLAY_GAME_RESOLUTION_WIDTH)
            game_resolution_height = self.get(self.CONFIG_DISPLAY, self.DISPLAY_GAME_RESOLUTION_HEIGHT)
            x = math.floor(game_resolution_width * variable['x'] / 100) + left_top_corner_x + fix_right
            y = math.floor(game_resolution_height * variable['y'] / 100) + left_top_corner_y + fix_top
            return int(x), int(y)
        except TypeError:
            raise Exception('Button configuration {} do not exists'.format(name))

    def get_range_coords(self, name):
        try:
            variable = self.get(self.CONFIG_RANGES, name)
            fix_top = self.get(self.CONFIG_DISPLAY, self.DISPLAY_FIX_TOP)
            fix_right = self.get(self.CONFIG_DISPLAY, self.DISPLAY_FIX_RIGHT)
            left_top_corner_x = self.get(self.CONFIG_DISPLAY, self.DISPLAY_LEFT_TOP_CORNER_X)
            left_top_corner_y = self.get(self.CONFIG_DISPLAY, self.DISPLAY_LEFT_TOP_CORNER_Y)
            game_resolution_width = self.get(self.CONFIG_DISPLAY, self.DISPLAY_GAME_RESOLUTION_WIDTH)
            game_resolution_height = self.get(self.CONFIG_DISPLAY, self.DISPLAY_GAME_RESOLUTION_HEIGHT)
            x1 = math.floor(game_resolution_width * variable['x1'] / 100) + left_top_corner_x + fix_right
            y1 = math.floor(game_resolution_height * variable['y1'] / 100) + left_top_corner_y + fix_top
            x2 = math.floor(game_resolution_width * variable['x2'] / 100) + left_top_corner_x + fix_right
            y2 = math.floor(game_resolution_height * variable['y2'] / 100) + left_top_corner_y + fix_top
            return int(x1), int(y1),int(x2), int(y2)
        except TypeError:
            raise Exception('Button configuration {} do not exists'.format(name))
