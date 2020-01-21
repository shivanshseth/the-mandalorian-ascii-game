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
        self._iceballs = []
        self._speedups = []
        self._viserion = []
        self._is_boss_frame = False

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
            elif game_obj in self._viserion:
                self._viserion.remove(game_obj)
            elif game_obj in self._iceballs:
                self._iceballs.remove(game_obj)

        #Remove from grid
        x = game_obj.get_x()
        y = game_obj.get_y()
        wd = game_obj.get_width()
        ht = game_obj.get_height()
        self.grid[y - ht:y, x: x + wd] = np.full((ht, wd), ' ')
    
    def gen_coins(self):
        if len(self._coins) < 6:
            wd = 0
            ht = 0
            for i in COIN.split('\n'):
                wd = max(len(i), wd)
                ht += 1
            y = random.randint(SKY + 1 + ht , HEIGHT - 1)
            coin = Coin(self, WIDTH - 1 - wd, y)
            self.add_to_scene(coin)
            self._coins.append(coin)
            self._background.append(coin)

    def gen_beam(self):
        if len(self._beams) < 4:
            i = random.randint(1, 3)
            s = 'BEAM' + str(i)
            art = globals()[s]
            wd = 0
            ht = 0
            for i in art.split('\n'):
                wd = max(len(i), wd)
                ht += 1
            y = random.randint(SKY + 1 + ht , HEIGHT - 1)
            beam = Beam(art, self, WIDTH - 1 - wd, y)
            self.add_to_scene(beam)
            self._background.append(beam)
            self._beams.append(beam)
    
    def gen_magnet(self):
        if len(self._magnet) < 1:
            wd = 0
            ht = 0
            for i in MAGNET.split('\n'):
                wd = max(len(i), wd)
                ht += 1
            y = random.randint(SKY + 1 + ht , HEIGHT - 1)
            magnet = Magnet(self, WIDTH - 1 - wd, y)
            self._background.append(magnet)
            self._magnet.append(magnet)
    
    def gen_speedup(self):
        if len(self._speedups) < 1:
            wd = 0
            ht = 0
            for i in SPEEDUP.split('\n'):
                wd = max(len(i), wd)
                ht += 1
            y = random.randint(SKY + 1 + ht , HEIGHT - 1)
            su = SpeedUp(self, WIDTH - 1 - wd, y)
            self._background.append(su)
            self._speedups.append(su)
    
    def gen_iceballs(self):
        if self.is_boss_frame() and len(self._iceballs) <= ICEBALLS_PER_ATTACK:
            self._viserion[0].fire()

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

    def move_viserion(self):
        assert len(self._player) > 0
        assert len(self._viserion) > 0
        self._viserion[0].pull(self._player[0].get_y())


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

    def get_viserion(self):
        return self._viserion
    
    def get_player(self):
        return self._player
    
    def get_iceballs(self):
        return self._iceballs

    def start_boss(self):
        self._is_boss_frame = True

    def is_boss_frame(self):
        return self._is_boss_frame

    def next_frame(self, stop_background = False):
        for i in self._pewpews:
            i.move()

        for i in self._iceballs:
            i.move()

        if not stop_background:
            for i in self._background:
                i.move_left()
        for i in self._player:
            i.check_collisions()
        
        if self.is_boss_frame():
            self.move_viserion()
            self.gen_iceballs()
            
    def score_lives(self):
        player = self._player[0]
        s = 'LIVES: ' + str(player.check_lives())
        self.grid[SKY - 1, 2: 2 + len(s)] = list(s)
        s = 'TIME REMAINING: ' + str(player.check_lives())
        self.grid[SKY - 2, 2: 2 + len(s)] = list(s)
        s = 'SCORE: ' + str(player.check_score())
        self.grid[SKY - 1, -(len(s)+2): -2] = list(s)
        if self.is_boss_frame():
            s = 'VISERION LIVES: ' + str(self._viserion[0].check_lives())
            self.grid[SKY - 2, -(len(s)+2): -2] = list(s)

    def message_board(self, s):
        self.grid[SKY - 1, WIDTH//2 - 10: WIDTH//2 - 10 + len(s)] = list(s)
