from pymouse import PyMouse
from time import sleep


class Mouse:
    mouse = None

    def __init__(self):
        self.mouse = PyMouse()

    def click(self, x, y, time=0.15):
        self.mouse.press(x, y)
        sleep(time)
        self.mouse.release(x, y)
        sleep(time)

    def click_and_back(self, x, y):
        coord_x, coord_y = self.mouse.position()
        self.click(x, y)
        self.mouse.move(coord_x, coord_y)
