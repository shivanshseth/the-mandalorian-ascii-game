from global_vals import *
from colorama import Fore, Back, Style, init
from utils.display import Display
import numpy as np
import random
from game_objects import Coin, Beam, PewPew, Magnet, SpeedUp

class Scene():

    def __init__(self):
        self.height = LIMIT_BOTTOM - LIMIT_TOP
        self.width = LIMIT_R - LIMIT_L
        self.grid = np.full((self.height, self.width), ' ')
        self.display = Display()
        self._tpf = TFP
        self._player = []
        self._background = []
        self._beams = []
        self._coins = []
        self._magnet = []
        self._pewpews = []
        self._speedups = []

    def create_border(self):
        self.grid[-1, :] = ['X']*self.width
        self.grid[0, :] = ['X']*self.width
        self.grid[SKY, :] = ['X'] *self.width
        self.grid[:, -1] = ['X']*self.height
        self.grid[:, 0] = ['X']*self.height
    
    def print_scene(self):
        for i in range(len(self.grid)):
            s = ''
            for j in range(len(self.grid[i])):
                s += self.grid[i][j]
            self.display.print_at(LIMIT_L, LIMIT_TOP+i, s)

    def add_to_scene(self, game_obj, obj_type = None):
        if obj_type:
             self.__dict__['_' + obj_type].append(game_obj)
        x = game_obj.get_x()
        y = game_obj.get_y()
        wd = game_obj.get_width()
        ht = game_obj.get_height()
        obj_box = game_obj.get_art_box()
        assert y - ht > SKY and y < HEIGHT
        self.grid[y - ht : y, x: x + wd] = obj_box

    def remove_from_scene(self, game_obj, permanent = False):
        #housekeeping
        if permanent:
            if game_obj in self._background: 
                self._background.remove(game_obj)
            if game_obj in self._coins: 
                self._coins.remove(game_obj)
            elif game_obj in self._beams: 
                self._beams.remove(game_obj)
            elif game_obj in self._pewpews: 
                self._pewpews.remove(game_obj)
            elif game_obj in self._magnet:
                self._magnet.remove(game_obj)  
            elif game_obj in self._speedups:
                self._speedups.remove(game_obj)  

        #Remove from grid
        x = game_obj.get_x()
        y = game_obj.get_y()
        wd = game_obj.get_width()
        ht = game_obj.get_height()
        self.grid[y - ht:y, x: x + wd] = np.full((ht, wd), ' ')
    
    def gen_coins(self):
        if len(self._coins) < 6:
            y = random.randint(SKY + 2 , HEIGHT - 2)
            coin = Coin(self, WIDTH - 3, y)
            self.add_to_scene(coin)
            self._coins.append(coin)
            self._background.append(coin)

    def gen_beam(self):
        if len(self._beams) < 4:
            i = random.randint(1, 3)
            s = 'BEAM' + str(i)
            y = random.randint(SKY + 5 , HEIGHT - 2)
            beam = Beam(globals()[s], self, WIDTH - 8, y)
            self.add_to_scene(beam)
            self._background.append(beam)
            self._beams.append(beam)
    
    def gen_magnet(self):
        if len(self._magnet) < 1:
            y = random.randint(SKY + 2 , HEIGHT - 2)
            magnet = Magnet(self, WIDTH - 5, y)
            self._background.append(magnet)
            self._magnet.append(magnet)
    
    def gen_speedup(self):
        if len(self._speedups) < 1:
            y = random.randint(SKY + 2 , HEIGHT - 2)
            su = SpeedUp(self, WIDTH - 5, y)
            self._background.append(su)
            self._speedups.append(su)
    
    def magnet_pull(self):
        assert len(self._player) > 0
        player = self._player[0]
        if len(self._magnet) > 0:
            magnet = self._magnet[0]
            player.pull(magnet.get_x(), magnet.get_y(), MAG_FORCE)
        else:
            player.reset_velx()

    def do_speedup(self, x = 1.5):
        self._tpf /= x
    
    def reset_speed(self):
        self._tpf = TFP

    def get_pewpews(self):
        return self._pewpews

    def get_background(self):
        return self._background

    def get_coins(self):
        return self._coins
    
    def get_beams(self):
        return self._beams

    def get_speedups(self):
        return self._speedups

    def get_tpf(self):
        return self._tpf

    def next_frame(self):
        for i in self._pewpews:
            i.move_right()

        for i in self._background:
            i.move_left()

        for i in self._player:
            i.check_collisions()
        
    def score_lives(self, player):
        s = 'SCORE: ' + str(player.check_score())
        self.grid[SKY - 1, 2: 2 + len(s)] = list(s)
        s = 'LIVES ' + str(player.check_lives())
        self.grid[SKY - 1, -(len(s)+2): -2] = list(s)
    
    def message_board(self, s):
        self.grid[SKY - 1, WIDTH//2 - 10: WIDTH//2 - 10 + len(s)] = list(s)
