#!/usr/bin/python
# -*- coding: utf-8 -*-

# imports

from Tkinter import *
from GameEngine import Game
from sys import argv

# initialize

g = Game()
defaultLevel = """
 #######
#       #
#       #
# @ o . #
#       #
#       #
 #######
"""

if len(argv) == 2:
    try:
        with open(argv[1]) as f:
            level = f.read()
    except:
        level = defaultLevel
else:
    level = defaultLevel

g.init(level)

# game loop and GUI

root = Tk()
root.title("Sokoban")

w = Canvas(root, background="#222", width=600, height=500)
w.pack()
screen = w.create_text(300,250, anchor=CENTER, font="Courier", fill="#dedede", text=g.output())

# handle key presses
def key(event):

    # get key
    press = event.keysym

    # valid keys if still in game
    if not g.victory():
        if press == 'Up':
            g.move((0, -1))
        elif press == 'Down':
            g.move((0, 1))
        elif press == 'Left':
            g.move((-1, 0))
        elif press == 'Right':
            g.move((1, 0))

    # if exit
    if press == 'Escape':
        root.quit()

    # update GUI
    w.itemconfig(screen, text=g.output())

    # if victory
    if g.victory():
        w.itemconfig(screen, text="Grattis!\n\n[ESC]\tavslutar\n[SPACE]\tbörjar om")
        if press == 'space':
            g.init(level)
            w.itemconfig(screen, text=g.output())



# listen for key presses
root.bind("<Key>", key)

# loop
root.mainloop()
#root.destroy()


