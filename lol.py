from scene import Scene
from game_objects import GameObject, Player
from global_vals import *
import tty, sys, termios, time, os, colorama
import random
from utils.async_input import KBHit

os.system('setterm -cursor off')
os.system('clear')
sc = Scene()
sc.create_border()
pl = Player(sc)
sc.add_to_scene(pl)
kb = KBHit()
frame = 0
while True:
    game_over = 0

    if pl.check_lives() == -1:
        game_over = 1
        break

    frame =(frame + 1)%60
    rd1 = random.randint(0,60)
    rd2 = random.randint(0,60)

    if rd1 > 56:
        sc.gen_coins()
    if frame%4:
        sc.scroll()
    if rd2 > 58:
        sc.gen_beam()
    if frame%3:
        pl.gravity()
    
    sc.score_lives(pl)
    sc.print_scene()

    START = time.time()

    if kb.kbhit():
        c = kb.getch()
    else:
        c = ' '
        
    if c == 'q':
        break
    elif c == 'd':
        pl.move_right()
    elif c == 'a':
        pl.move_left()
    elif c == 'w':
        pl.jet()
    elif c == 'f':
        pl.fire()

    NOW = time.time()
    diff = NOW - START
    if diff < 0.05:
        time.sleep(0.05 - diff) 

if game_over:
    sc.message_board('GAME OVER, press q to exit')
    while True:
        sc.print_scene()
        if kb.kbhit():
            c = kb.getch()
        else:
            c = ' '
        pass
        if c == 'q':
            break
        
kb.set_normal_term()
os.system('setterm -cursor on')
