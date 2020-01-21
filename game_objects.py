import numpy as np
from global_vals import *
import time
class GameObject():
    def __init__(self, art, scene, x, y, fore = 'WHITE', back = 'BLACK'): 
        self._fore = fore
        self._back = back
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
            self._scene.remove_from_scene(self, permanent = True)

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

class Projectile(GameObject):
    def __init__(self, art, scene, x, y, fore = 'WHITE', back = 'BLACK'):
        super().__init__(art, scene, x, y, fore, back)
        self._velx = PEW_VEL
        
    def check_collisions(self):
        for i in self._scene.get_beams():
            if not (self.get_x() + self.get_width() <= i.get_x() or i.get_x() + i.get_width() <= self.get_x() or self.get_y() < i.get_y() - i.get_height() or i.get_y() < self.get_y() - self.get_height()): 
                self._scene.remove_from_scene(i, permanent = True)
                self._scene.remove_from_scene(self, permanent = True)
                return True

        for i in self._scene.get_viserion():
            if not (self.get_x() + self.get_width() <= i.get_x() or i.get_x() + i.get_width() <= self.get_x() or self.get_y() < i.get_y() - i.get_height() or i.get_y() < self.get_y() - self.get_height()): 
                i.decrease_lives()
                self._scene.remove_from_scene(self, permanent = True)
                return True

        for i in self._scene.get_player():
            if not (self.get_x() + self.get_width() <= i.get_x() or i.get_x() + i.get_width() <= self.get_x() or self.get_y() < i.get_y() - i.get_height() or i.get_y() < self.get_y() - self.get_height()): 
                if not i.shield_active():
                    i.decrease_lives()
                self._scene.remove_from_scene(self, permanent = True)
                return True
        return False
        
class PewPew(Projectile):
    def __init__(self, scene, x, y, fore = 'WHITE', back = 'BLACK'):
        super().__init__(PEW, scene, x, y, fore, back)
        
    def move(self):
        if  self._x + self._velx + self._width < WIDTH:
            self._scene.remove_from_scene(self)
            self._x += self._velx
            if not self.check_collisions():
                self._scene.add_to_scene(self)
        else:
            self._scene.remove_from_scene(self ,permanent = True)

class IceBall(Projectile):
    def __init__(self, scene, x, y, fore = 'WHITE', back = "BLACK"):
        super().__init__(ICEBALL, scene, x, y, fore, back)
    
    def move(self):
        if self._x - self._velx > PLAYER_INIT[0]:
            self._scene.remove_from_scene(self)
            self._x -= self._velx
            if not self.check_collisions():
                self._scene.add_to_scene(self)
        else:
            self._scene.remove_from_scene(self, permanent = True)

class Player(GameObject):
    def __init__(self, scene, art = MANDO_SPRITE, fore = 'WHITE', back = 'BLACK'):
        super().__init__(art, scene, *PLAYER_INIT, fore, back)
        self._vely = 0
        self._velx = 0
        self._score = 0
        self._lives = PLAYER_LIVES
        self._shield_active = False
        self._shield_start = None

    def move_right(self, force = ACCX):
        if self._x + self._velx + self._width + force < WIDTH and self._x + self._velx  + force> PLAYER_INIT[0]:
            self._scene.remove_from_scene(self)
            self._velx += force
            if self._velx > MAX_VELX:
                self._velx = MAX_VELY
            self._x = self._x + self._velx
            # self._y = max(self._y + self._vely, SKY + self._height + 1) 
            self.check_collisions()
            self._scene.add_to_scene(self)
            # self._scene.message_board(str(self._vely))
        else:
            self._velx = 0
        
    def move_left(self, force = ACCX):
        if self._x + self._velx + self._width - force < WIDTH and self._x + self._velx - force> PLAYER_INIT[0]:
            self._scene.remove_from_scene(self)
            self._velx -= force
            if self._velx < MIN_VELX:
                self._velx = MIN_VELY
            self._x = self._x + self._velx
            # self._y = max(self._y + self._vely, SKY + self._height + 1) 
            self.check_collisions()
            self._scene.add_to_scene(self)
        else:
            self._velx = 0

    
    def move_vertically(self):
        if self.get_y() + self._vely < HEIGHT  and self.get_y() + self._vely - self.get_height()> SKY:
            self._scene.remove_from_scene(self)
            self._y += self._vely
            self.check_collisions()
            self._scene.add_to_scene(self)
            return True
        return False

    def check_collisions(self):
        for i in self._scene.get_coins():
            if not (self.get_x() + self.get_width() <= i.get_x() or i.get_x() + i.get_width() <= self.get_x() or self.get_y() < i.get_y() - i.get_height() or i.get_y() < self.get_y() - self.get_height()): 
                self._score += 10
                self._scene.remove_from_scene(i, permanent = True)

        for i in self._scene.get_beams():
            if not (self.get_x() + self.get_width() <= i.get_x() or i.get_x() + i.get_width() <= self.get_x() or self.get_y() < i.get_y() - i.get_height() or i.get_y() < self.get_y() - self.get_height()): 
                self._scene.remove_from_scene(i, permanent = True)
                if not self.shield_active():
                    self._lives -= 1
                    time.sleep(0.5)

        for i in self._scene.get_speedups():
            if not (self.get_x() + self.get_width() <= i.get_x() or i.get_x() + i.get_width() <= self.get_x() or self.get_y() < i.get_y() - i.get_height() or i.get_y() < self.get_y() - self.get_height()): 
                self._scene.remove_from_scene(i, permanent = True)
                self._scene.do_speedup()
        
    
    def pull(self, x, y, force):
        if abs(self._x - x) <= MAG_RANGE_X and abs(self._y - y) <= MAG_RANGE_Y:
            if self._x - x > 0:
                self.move_left(force)
            elif self._x + self._width - x < 0: 
                self.move_right(force)

            if self._y - self._height - y > 0:
                self._vely = min(MIN_VELY, self._vely - force)
            elif self._y - y < 0:
                self._vely = max(MAX_VELY, self._vely + force)
            self.move_vertically()
        
    def reset_velx(self):
        self._velx = 0

    def jet(self):
        if self.get_y() + self._vely - ACCY < HEIGHT  and self.get_y() + self._vely - ACCY - self.get_height()> SKY:
            self._scene.remove_from_scene(self)
            self._vely -= ACCY
            if self._vely < -3:
                self._vely = -3
            self._y = self._y + self._vely
            # self._y = max(self._y + self._vely, SKY + self._height + 1) 
            self.check_collisions()
            self._scene.add_to_scene(self)
            self._scene.message_board(str(self._vely))
        else:
            self._vely = 0
            

    def gravity(self): 
        if self.get_y() + self._vely + GRAVITY < HEIGHT and self.get_y() + self._vely + GRAVITY - self.get_height() > SKY:
            self._scene.remove_from_scene(self)
            self._vely += GRAVITY
            self._y = self._y + self._vely
            self.check_collisions()
            self._scene.message_board(str(self._vely))
            self._scene.add_to_scene(self)
        else:
            self._vely = 0

        if self.get_y() == PLAYER_INIT[1]:
            self._vely = 0

    def fire(self):
        pew = PewPew(self._scene, self.get_x() + self.get_width(), self.get_y() - self.get_height() + 1)
        self._scene.add_to_scene(pew, 'pewpews')
    
    def activate_shield(self):
        self._scene.remove_from_scene(self)
        super().__init__(MANDO_SHIELD, self._scene, self.get_x(), self.get_y(), self._fore, self._back)
        self._scene.add_to_scene(self)
        self._velx = 0
        self._shield_active = True
        self._shield_start = time.time()
    
    def deactivate_shield(self):
        self._scene.remove_from_scene(self)
        super().__init__(MANDO_SPRITE, self._scene, self.get_x(), self.get_y(), self._fore, self._back)
        self._scene.add_to_scene(self)
        self._velx = 0
        self._shield_active = False
        self._shield_start = None
    
    def decrease_lives(self, i = 1):
        self._lives -= i
    
    def shield_active(self):
        return self._shield_active

    def check_score(self):
        return self._score
    
    def check_lives(self):
        return self._lives
    
class Viserion(GameObject):
    def __init__(self, scene, art = VISERION, fore = 'WHITE', back = 'BLACK'):
        wd = 0
        ht = 0
        for i in art.split('\n'):
            wd = max(len(i), wd)
            ht += 1
        super().__init__(art, scene, WIDTH - 1 - wd, SKY + 1 + ht, fore, back)
        self._vely = 0
        self._lives = BOSS_LIVES
    
    def check_collisions(self):
        for i in self._scene.get_pewpews():
            if not (self.get_x() + self.get_width() <= i.get_x() or i.get_x() + i.get_width() <= self.get_x() or self.get_y() < i.get_y() - i.get_height() or i.get_y() < self.get_y() - self.get_height()): 
                self._scene.remove_from_scene(i, permanent = True)
                self.decrease_lives()
                return True
        return False

    def decrease_lives(self, i = 1):
        if self._lives == 0:
            self._scene.remove_from_scene(self)
            time.sleep(0.5)
        self._lives -= i
    
    def check_lives(self):
        return self._lives
    
    def move_vertically(self):
        if self.get_y() + self._vely < HEIGHT  and self.get_y() + self._vely - self.get_height() > SKY:
            self._scene.remove_from_scene(self)
            self._y += self._vely
            self.check_collisions()
            self._scene.add_to_scene(self)
            return True
        return False
    
    def pull(self, y, force = VISERION_ACC):
        if self._y - self._height - y > 0:
                self._vely = min(MIN_VELY, self._vely - force)
        elif self._y - y < 0:
            self._vely = max(MAX_VELY, self._vely + force)
        self.move_vertically()
    
    def fire(self):
        wd = 0
        ht = 0
        for i in ICEBALL.split('\n'):
            wd = max(len(i), wd)
            ht += 1
        pew = IceBall(self._scene, self.get_x() - 1 - wd, self.get_y() - self.get_height() + ht)    
        self._scene.add_to_scene(pew, 'iceballs')
    

class Coin(GameObject):
    def __init__(self, scene, x, y, fore = 'WHITE', back = 'BLACK'):
        super().__init__(COIN, scene, x, y, fore, back)

class Beam(GameObject):
    def __init__(self, btype, scene, x, y, fore = 'WHITE', back = 'BLACK'):
        super().__init__(btype, scene, x, y, fore, back)

class Magnet(GameObject):
    def __init__(self, scene, x, y, fore = 'WHITE', back = 'BLACK'):
        super().__init__(MAGNET, scene, x, y, fore, back)

class SpeedUp(GameObject):
    def __init__(self, scene, x, y, fore = 'WHITE', back = 'BLACK'):
        super().__init__(SPEEDUP, scene, x, y, fore, back)