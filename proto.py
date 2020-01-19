import tty, sys, termios, time, os, colorama
from utils.async_input import KBHit

MAXY, MAXX = [int(i) for i in os.popen('stty size', 'r').read().split()]
def place_cursor(x, y):
    sys.stdout.write("\x1b[%d;%df%s" % (y, x, ''))
    sys.stdout.flush()

class Object():
    def __init__(self, design):
        self.width = 0
        self.height = 0
        for i in design.split('\n'):
            self.height += 1
            if len(i) > self.width:
                self.width = len(i)
        self.__MAXY, self.__MAXX = [int(i) for i in os.popen('stty size', 'r').read().split()]
        self.__x = 0
        self.__y = 0
        self.__velX = 2
        self.__velY=2
        self.__design = design
    
    def place(self, x, y):
        self.__x = x
        self.__y = y
        place_cursor(x, y)
        # print(self._design + 'as', end = '') 
        sys.stdout.write("%s" % (self.__design))
        sys.stdout.flush()

class Player:
    def __init__(self, design):
        self.__MAXY, self.__MAXX = [int(i) for i in os.popen('stty size', 'r').read().split()]
        self.__x = 0
        self.__y = 0
        self.__velX = 2
        self.__velY=2
        self.gravity = 10
        self.__in_air = False
        self.__design = design
        self.velY=2
        

    # def move_right(self):
    #     if(self.__x + self.__velX < MAXX):
    #         place_cursor(self.__x, self.__y)
    #         self.__x += self.__velX
    #         print(' '*self.__velX + self.__design, end)

    def move_left(self):
        if(self.__x - self.__velX > 0):
            place_cursor(self.__x - self.__velX, self.__y)
            self.__x -= self.__velX
            print(self._design + ' '*self.__velX, end = '')  
            sys.stdout.flush()

    def jet(self):
        place_cursor(self.__x, self.__y)
        print(' '*3, end = '')
        self.__y -= self.__velY
        place_cursor(self.__x, self.__y)
        print(self.__design + ' ', end = '')
        sys.stdout.flush()
        

        
#main

os.system('setterm -cursor off')
os.system('clear')
colorama.init()
pl = Player('Boi')
pl.place(0, MAXY-0)
kb = KBHit()

while True:
    # print('lul')
    if kb.kbhit():
        c = kb.getch()
    else:
        c = ' '
    if c == 'q':
        break
    elif c == 'd':
        pl.move_right()
        # print('d')
    elif c == 'a':
        pl.move_left()
        # print('a')
    elif c == 'w':
        pl.jet()
        # print('a')
    # os.system('sleep 0.05')
    print(pl.__x)

kb.set_normal_term()
os.system('setterm -cursor on')
