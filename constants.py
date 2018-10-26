"""
Module contain constants.

Created on 22.07.2018

@author: Ruslan Dolovanyuk

"""


class Colors:
    """Contain main colors."""
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GRAY = (128, 128, 128)
    SILVER = (192, 192, 192)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    YELLOW = (255, 255, 0)

    DARKGREEN = (0, 127, 0)


class Cards:
    """Contain play cards constants."""
    black_suits = ['club', 'spade']
    red_suits = ['diamond', 'heart']
    suits = black_suits + red_suits
