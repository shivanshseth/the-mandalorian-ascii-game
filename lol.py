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
sc.add_to_scene(pl, 'player')
kb = KBHit()
frame = 0
sc.gen_coins()
sc.gen_beam()
GAME_START = time.time()

while True:
    FRAME_START = time.time()
    game_over = 0

    if pl.check_lives() <= -1:
        game_over = 1
        break
    
    if pl.shield_active():
        if time.time() - pl._shield_start > SHIELD_TIME:
            pl.deactivate_shield() 

    frame += 1
    rd1 = random.randint(0,100)
    rd2 = random.randint(0,100)

    if frame % 2 == 0:
        sc.magnet_pull()
    if frame % 10 == 0:
        sc.gen_coins()
    if frame %20 == 0 :
        sc.gen_beam()
    if frame %100 == 0 :
        sc.gen_speedup()
    if frame % 200 == 0:
        sc.gen_magnet() 
    
    sc.score_lives(pl)
    sc.print_scene()

    if kb.kbhit():
        c = kb.getch()
    else:
        c = '0'
        
    if c == 'q':
        break
    elif c == 'd':
        pl.move_right()
    elif c == 'a':
        pl.move_left()
    elif c == 'w':
        pl.jet()
    else:
        pl.gravity()
    if c == 'f':
        pl.fire()
    if c.isspace():
        pl.activate_shield()

    NOW = time.time()
    diff = NOW - FRAME_START
    if diff < sc.get_tpf():
        time.sleep(sc.get_tpf() - diff)

    sc.next_frame() 

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
