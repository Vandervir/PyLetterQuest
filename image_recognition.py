import os

import cv2
import scipy
import imutils
from skimage.measure import compare_ssim

from game_control import GameControl
from screen import grab_screen


class ImageRecognition:

    def __init__(self):
        self.gc = GameControl()
        pass

    def is_the_same_image(self, region, image_path, acceptable_ratio=0.6, overwrite=False, resume=True):
        score = self.get_image_similarity_score(region, image_path, overwrite, resume)
        return score > acceptable_ratio

    def get_image_similarity_score(self, region, image_path, overwrite=False, resume=True):
        if resume:
            self.gc.resume_game()
        screen = grab_screen(region)
        if overwrite:
            cv2.imwrite(image_path, screen)
        if not os.path.exists(image_path):
            raise Exception('Image do not exist')
        pattern_image = cv2.imread(image_path)
        grayA = cv2.cvtColor(pattern_image, cv2.COLOR_BGR2GRAY)
        grayB = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
        score, diff = compare_ssim(grayA, grayB, full=True)
        # print(score)
        return score
