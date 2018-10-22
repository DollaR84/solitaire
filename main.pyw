"""
Main module for running solitaire game.

Created on 03.09.2018

@author: Ruslan Dolovanyuk

"""

import multiprocessing
import pickle
import random
import time

import pygame

from configparser import ConfigParser

from audio import Sound
from audio import Music

from board import Board

from constants import Colors

from player import Actions
from player import Player

from speech import Speech


class Game:
    """Main running class for game."""

    def __init__(self):
        """Initialize running class."""
        self.config = ConfigParser()
        self.config.read('settings.ini')
        self.size_x = self.config.getint('screen', 'size_x')
        self.size_y = self.config.getint('screen', 'size_y')

        with open('languages.dat', 'rb') as lang_file:
            self.phrases = pickle.load(lang_file)[self.config.get('total', 'language')]

        self.speech = Speech(self.config)
        self.speech.speak(self.phrases['start'])

        pygame.init()
        pygame.font.init()
        pygame.mixer.init()

        self.screen = pygame.display.set_mode((self.size_x, self.size_y))
        pygame.display.set_caption(self.phrases['solitaire'])

        self.sounds = Sound(self.config.getfloat('audio', 'sound_volume'))
        self.music = Music(self.config.getfloat('audio', 'music_volume'))

        self.board = Board(self.config, self.screen, self.sounds)
        self.player = Player(self.board, self.speech, self.phrases)
        self.game_over = True
        self.win = False
        self.STOPPED_PLAYING = pygame.USEREVENT + 1

        pygame.mixer.music.set_endevent(self.STOPPED_PLAYING)
        self.fontObj = pygame.font.SysFont('arial', 50)
        self.clock = pygame.time.Clock()

        random.seed()
        self.music_play()
        self.new_game()

    def mainloop(self):
        """Run main loop game."""
        self.running = True
        while self.running:
            self.handle_events()
            self.draw()

            self.clock.tick(15)
            pygame.display.flip()

        self.speech.speak(self.phrases['finish'])
        pygame.quit()

    def handle_events(self):
        """Check all game events."""
        for event in pygame.event.get():
            if pygame.QUIT == event.type:
                self.running = False
            if self.STOPPED_PLAYING == event.type:
                self.music_play()
            elif pygame.KEYDOWN == event.type:
                if pygame.K_ESCAPE == event.key:
                    self.running = False
                elif pygame.K_F1 == event.key:
                    self.help()
                elif pygame.K_F2 == event.key:
                    self.change_music()
                elif pygame.K_F3 == event.key:
                    self.change_card_by()
                elif pygame.K_F4 == event.key:
                    self.change_deck()
                elif pygame.K_F5 == event.key:
                    self.new_game()
                elif pygame.K_TAB == event.key and pygame.key.get_mods() & pygame.KMOD_SHIFT:
                    if not self.game_over:
                        self.player.actions(Actions.ChangeZoneDown)
                elif pygame.K_TAB == event.key:
                    if not self.game_over:
                        self.player.actions(Actions.ChangeZoneUp)
                elif pygame.K_LEFT == event.key:
                    if not self.game_over:
                        self.player.actions(Actions.ChangeRowDown)
                elif pygame.K_RIGHT == event.key:
                    if not self.game_over:
                        self.player.actions(Actions.ChangeRowUp)
                elif pygame.K_UP == event.key:
                    if not self.game_over:
                        self.player.actions(Actions.ChangeCardUp)
                elif pygame.K_DOWN == event.key:
                    if not self.game_over:
                        self.player.actions(Actions.ChangeCardDown)
                elif pygame.K_SPACE == event.key and pygame.key.get_mods() & pygame.KMOD_SHIFT:
                    if not self.game_over:
                        self.player.actions(Actions.Drop)
                elif pygame.K_SPACE == event.key:
                    if not self.game_over:
                        self.player.actions(Actions.Take)

    def draw(self):
        """Main draw function."""
        self.screen.fill(Colors.GRAY)
        self.board.draw()
        if self.game_over:
            if self.win:
                textSurfaceObj = self.fontObj.render(self.phrases['win'], True, Colors.GREEN)
            else:
                textSurfaceObj = self.fontObj.render(self.phrases['game_over'], True, Colors.RED)
            textRectObj = textSurfaceObj.get_rect()
            textRectObj.center = (self.size_x//2, self.size_y//2)
            self.screen.blit(textSurfaceObj, textRectObj)
        else:
            self.player.draw()

    def music_play(self):
        """Change music play."""
        if self.config.getboolean('audio', 'music'):
            name = random.choice(self.music.get_music_names())
            self.music.play(name)

    def new_game(self):
        """Start new game."""
        self.speech.speak(self.phrases['new_game'])
        self.game_over = False
        self.win = False
        self.board.create_deck()
        self.board.clear_zones()
        self.board.distribution()
        self.player.reset()
        self.player.speak()

    def help(self):
        """Speak help for keys control game."""
        file_name = 'help_' + self.config.get('total', 'language') + '.txt'
        with open(file_name, 'r', encoding='utf8') as help_file:
            data = help_file.readlines()
            for line in [line for line in data if '\n' != line]:
                self.speech.speak(line)
                time.sleep(0.1)

    def change_music(self):
        """On or off music in game."""
        if self.config.getboolean('audio', 'music'):
            self.config.set('audio', 'music', 'false')
            pygame.mixer.music.stop()
            self.speech.speak(self.phrases['music_off'])
        else:
            self.config.set('audio', 'music', 'true')
            self.music_play()
            self.speech.speak(self.phrases['music_on'])
        with open('settings.ini', 'w') as config_file:
            self.config.write(config_file)

    def change_card_by(self):
        """Change incoming card: by 1 or by 3."""
        if '3' == self.config.get('board', 'delivery'):
            self.config.set('board', 'delivery', '1')
            self.speech.speak(self.phrases['by1'])
        else:
            self.config.set('board', 'delivery', '3')
            self.speech.speak(self.phrases['by3'])
        with open('settings.ini', 'w') as config_file:
            self.config.write(config_file)

    def change_deck(self):
        """Change deck on game: 52 or 36."""
        if 'half' == self.config.get('board', 'deck'):
            self.config.set('board', 'deck', 'full')
            self.speech.speak(self.phrases['52_cards'])
        else:
            self.config.set('board', 'deck', 'half')
            self.speech.speak(self.phrases['36_cards'])
        with open('settings.ini', 'w') as config_file:
            self.config.write(config_file)

if __name__ == '__main__':
    multiprocessing.freeze_support()
    game = Game()
    game.mainloop()
