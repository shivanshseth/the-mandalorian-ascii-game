import numpy as np
from global_vals import *
import time
class GameObject():
    def __init__(self, art, scene, x, y, fore = 'WHITE', back = 'BLACK'): 
        self._width = 0
        self._height = 0
        self._velx = VELX
        self._scene = scene
        self._display = scene.display
        art = art.split('\n')
        for i in art:
            self._height += 1
            if len(i) > self._width:
                self._width = len(i)

        assert x + self._width < WIDTH and SKY <= y < HEIGHT

        self._art_box = np.full((self._height, self._width), (' '))
        for i in range(len(art)):
            self._art_box[i, :] = list(art[i]) + [' '] * (self._width - len(art[i]))
        self._x = x 
        self._y = y
    
        
    def move_left(self):
        if self._x - self._velx > PLAYER_INIT[0]:
            self._scene.remove_from_scene(self)
            self._x -= self._velx
            self._scene.add_to_scene(self)

        else:
            self._scene.remove_from_scene(self ,permanent = True)

    
    def get_x(self):
        return self._x
    
    def get_y(self):
        return self._y
    
    def get_height(self):
        return self._height

    def get_width(self):
        return self._width

    def get_art_box(self):
        return self._art_box       

class PewPew(GameObject):

    def __init__(self, scene, x, y, fore = 'WHITE', back = 'BLACK'):
        super().__init__(PEW, scene, x, y, fore, back)
        self._velx = PEW_VEL
        
    def check_collisions(self):
        for i in self._scene.get_beams():
            if not (self.get_x() + self.get_width() <= i.get_x() or i.get_x() + i.get_width() <= self.get_x() or self.get_y() < i.get_y() - i.get_height() or i.get_y() < self.get_y() - self.get_height()): 
                self._scene.remove_from_scene(i, permanent = True)
                self._scene.remove_from_scene(self, permanent = True)
                return True
        return False
    
    def move_right(self):
        if  self._x + self._velx + self._width < WIDTH:
            self._scene.remove_from_scene(self)
            self._x += self._velx
            if not self.check_collisions():
                self._scene.add_to_scene(self)


class Player(GameObject):
    def __init__(self, scene):
        super().__init__(MANDO_SPRITE, scene, *PLAYER_INIT)
        self._vely = VELY
        self._score = 0
        self._lives = LIVES

    def move_right(self):
        if  self._x + self._velx + self._width < WIDTH:
            self._scene.remove_from_scene(self)
            self._x += self._velx
            self.check_collisions()
            self._scene.add_to_scene(self)
        
    def move_left(self):
        if self._x - self._velx > PLAYER_INIT[0]:
            self._scene.remove_from_scene(self)
            self._x -= self._velx
            self.check_collisions()
            self._scene.add_to_scene(self)
    
    def jet(self):
        self._scene.remove_from_scene(self)
        self._y = max(self._y + self._vely, SKY + self._height + 1) 
        self.check_collisions()
        self._scene.add_to_scene(self)

    def gravity(self): 
        self._scene.remove_from_scene(self)
        self._y = min(self._y + GRAVITY, PLAYER_INIT[1])
        self.check_collisions()
        self._scene.add_to_scene(self)

    def fire(self):
        pew = PewPew(self._scene, self.get_x() + self.get_width(), self.get_y() - self.get_height() + 1)
        self._scene.add_to_scene(pew, 'pewpews')

    def check_collisions(self):
        for i in self._scene.get_coins():
            if not (self.get_x() + self.get_width() <= i.get_x() or i.get_x() + i.get_width() <= self.get_x() or self.get_y() < i.get_y() - i.get_height() or i.get_y() < self.get_y() - self.get_height()): 
                self._score += 10
                self._scene.remove_from_scene(i, permanent = True)

        for i in self._scene.get_beams():
            if not (self.get_x() + self.get_width() <= i.get_x() or i.get_x() + i.get_width() <= self.get_x() or self.get_y() < i.get_y() - i.get_height() or i.get_y() < self.get_y() - self.get_height()): 
                self._lives -= 1
                self._scene.remove_from_scene(i, permanent = True)
                time.sleep(0.5)
    
    def check_score(self):
        return self._score
    
    def check_lives(self):
        return self._lives
    


class Coin(GameObject):
    def __init__(self, scene, x, y):
        super().__init__(COIN, scene, x, y)

class Beam(GameObject):
    def __init__(self, btype, scene, x, y):
        super().__init__(btype, scene, x, y)

class Magnet(GameObject):
    def __init__(self, scene, x, y):
        super().__init__()