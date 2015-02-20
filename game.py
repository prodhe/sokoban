#!/usr/bin/python
# -*- coding: utf-8 -*-

# imports

from Tkinter import *
from tkFileDialog import askopenfilename
from sokoban_engine import Game
from sys import argv

# restart
def restart():
    g.init()
    w.itemconfig(screen, text=g.output())

# open new level
def openfile():
    filename = askopenfilename(parent=root)
    with open(filename) as f:
        g.changeLevel(f.read())
    w.itemconfig(screen, text=g.output())

# handle key presses
def key(event):

    # get key
    press = event.keysym

    # valid keys if still in game
    if not g.victory():
        if press in ('Up','k'):
            g.move((0, -1))
        elif press in ('Down', 'j'):
            g.move((0, 1))
        elif press in ('Left', 'h'):
            g.move((-1, 0))
        elif press in ('Right', 'l'):
            g.move((1, 0))

    # if exit
    if press in ('Escape', 'q'):
        root.quit()

    ## if victory
    if g.victory():
        if press == 'space':
            g.init()

    # update GUI
    w.itemconfig(screen, text=g.output())

defaultLevel = """
 #######
#       #
#       #
# @ o . #
#       #
#       #
 #######
"""

# check args on commandline
if len(argv) == 2:
    try:
        with open(argv[1]) as f:
            level = f.read()
    except:
        level = defaultLevel
else:
    level = defaultLevel

# initialize
g = Game(level)
g.init()

# GUI and game loop

root = Tk()

menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Restart", command=restart)
filemenu.add_separator()
filemenu.add_command(label="Open", command=openfile)
filemenu.add_separator()
filemenu.add_command(label="Quit Sokoban", command=root.quit)
menubar.add_cascade(label="File", menu=filemenu)
helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="About")
menubar.add_cascade(label="Help", menu=helpmenu)

root.title("Sokoban")
root.config(menu=menubar)

w = Canvas(root, background="#222", width=600, height=500)
w.pack()
screen = w.create_text(300,250, anchor=CENTER, font="Courier", fill="#dedede", text=g.output())

# listen for key presses
root.bind("<Key>", key)

# loop
root.mainloop()
#root.destroy()


