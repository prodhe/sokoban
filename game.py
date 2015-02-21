#!/usr/bin/python
# -*- coding: utf-8 -*-

# imports

from Tkinter import *
from tkFileDialog import askopenfilename
#from sokoban_engine import Game
from enginenew import Sokoban
from sys import argv

# restart
def restart():
    g.load()
    w.itemconfig(screen, text=g.show())

# restart
def undo():
    g.undo()
    w.itemconfig(screen, text=g.show())

# open new level
def openfile():
    filename = askopenfilename(parent=root)
    g.load(filename)
    w.itemconfig(screen, text=g.show())

# handle key presses
def key(event):

    # get key
    press = event.keysym

    # valid keys if still in game
    if not g.finished():
        if press in ('Up','k'):
            g.move((0, -1))
        elif press in ('Down', 'j'):
            g.move((0, 1))
        elif press in ('Left', 'h'):
            g.move((-1, 0))
        elif press in ('Right', 'l'):
            g.move((1, 0))
        elif press in ('U', 'u'):
            g.undo()

    # if exit
    if press in ('Escape', 'q'):
        root.quit()

    ## if victory
    if g.finished():
        if press == 'space':
            g.init()

    # update GUI
    w.itemconfig(screen, text=g.show())

defaultLevel = """
 #######
#       #
#       #
# @ o . #
#       #
#       #
 #######
"""

# initialize
g = Sokoban()

if len(argv) == 2:
    g.load(argv[2])
else:
    g.load()


# GUI and game loop

root = Tk()

menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Undo", command=undo)
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
screen = w.create_text(300,250, anchor=CENTER, font="Courier", fill="#dedede", text=g.show())

# listen for key presses
root.bind("<Key>", key)

# loop
root.mainloop()
#root.destroy()


