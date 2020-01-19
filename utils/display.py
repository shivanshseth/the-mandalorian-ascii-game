import sys
from colorama import Fore, Back, Style, init
import os
from global_vals import *
init()

class Display:
    def __init__(self):
        os.system('clear')
        os.system('setterm -cursor off')

    def place_cursor(self, x, y):
        sys.stdout.write("\x1b[%d;%df%s" % (y,x, ''))
        sys.stdout.flush()

    def print_at(self, x, y, art):
        self.place_cursor(x,y)
        sys.stdout.write(art)
        sys.stdout.write(Style.RESET_ALL)
        sys.stdout.flush()
    
    def remove_at(self, x, y):
        self.print_at(x, y, ' ')