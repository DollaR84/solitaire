"""
Main module for running solitaire game.

Created on 03.09.2018

@author: Ruslan Dolovanyuk

"""

import multiprocessing

from game import Game

if __name__ == '__main__':
    multiprocessing.freeze_support()
    game = Game()
    game.mainloop()
