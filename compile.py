"""
Compile module in python library pid.

Created on 16.11.2018

@author: Ruslan Dolovanyuk

example running:
    python compile.py build_ext --inplace

"""

from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

ext_modules = [
               Extension("audio", ["audio.py"]),
               Extension("board", ["board.py"]),
               Extension("card", ["card.py"]),
               Extension("checker", ["checker.py"]),
               Extension("constants", ["constants.py"]),
               Extension("game", ["game.py"]),
               Extension("loader", ["loader.py"]),
               Extension("player", ["player.py"]),
               Extension("processes", ["processes.py"]),
               Extension("speech", ["speech.py"]),
               Extension("Tolk", ["Tolk.py"]),
               Extension("zones", ["zones.py"])
              ]

setup(
      name='main',
      cmdclass={'build_ext': build_ext},
      ext_modules=ext_modules
)
