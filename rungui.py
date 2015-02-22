#
#   game.py
#


#
# imports
#

import os
import Tkinter as tk
import sokoban
from sys import argv
from tkFileDialog import askopenfilename


#
# functions
#

def restart():
    g.load()
    updategui()

def undo():
    g.undo()
    updategui()

def redo():
    g.redo()
    updategui()

def openfilegui():
    filename = askopenfilename(parent=root)
    g.load(filename)
    updategui()

def updategui():
    w.itemconfig(screen_game, text=g.output())
    w.itemconfig(screen_level, text=g.output_level_loaded())
    w.itemconfig(screen_moves, text="Moves:  %d" % g.history.count())

def get_levels(leveldir):
    levels = []
    if os.path.exists(leveldir) and os.path.isdir(leveldir):
        for filename in os.listdir(leveldir):
            levels.append(leveldir + os.path.sep + filename)
    return levels


#
# entry point
#

# initialize the game engine
g = sokoban.init()

# load a level
levels = get_levels("levels")
current_level = 0
if levels:
    g.load(levels[current_level])
else:
    g.load()


#
# GUI and game loop
#

root = tk.Tk()
root.title("Sokoban")

# menu
menubar = tk.Menu(root)
filemenu = tk.Menu(menubar, tearoff=0)
filemenu.add_command(label="Open level", command=openfilegui)
filemenu.add_separator()
filemenu.add_command(label="Undo move", command=undo)
filemenu.add_command(label="Redo move", command=redo)
filemenu.add_separator()
filemenu.add_command(label="Restart level", command=restart)
filemenu.add_separator()
filemenu.add_command(label="Quit", command=root.quit)
menubar.add_cascade(label="Sokoban", menu=filemenu)
root.config(menu=menubar)

# main screen
w = tk.Canvas(root, background="#222", width=600, height=500)
w.pack()
screen_game = w.create_text(300,250, anchor=tk.CENTER, font="Courier",
                            fill="#dedede", text=g.output())
screen_level = w.create_text(10,10, anchor=tk.NW, font="Courier",
                            fill="#efefef", text=g.output_level_loaded())
screen_moves = w.create_text(580,10, anchor=tk.NE, font="Courier",
                             fill="#efefef", text="Moves:  %d" % g.history.count())

# handle key presses
def key(event):

    # globals for level handling
    global current_level
    global levels

    # get key
    press = event.keysym

    if press in ('D', 'd'):
        print sokoban.log
    if press in ('Escape', 'q'):
        root.quit()
    if press in ('N', 'n') and levels:
        if (current_level < len(levels)-1):
            current_level += 1
            g.load(levels[current_level])
    if press in ('P', 'p') and levels:
        if (current_level > 0):
            current_level -= 1
            g.load(levels[current_level])

    if not g.finished():
        if press in ('Up','k'):
            g.move(0, -1)
        elif press in ('Down', 'j'):
            g.move(0, 1)
        elif press in ('Left', 'h'):
            g.move(-1, 0)
        elif press in ('Right', 'l'):
            g.move(1, 0)
        elif press in ('U', 'u'):
            g.undo()
        elif press in ('R', 'r'):
            g.redo()
    else:
        if press == 'space':
            g.load()

    updategui()

# listen for key presses
root.bind("<Key>", key)

# loop
root.mainloop()

#
# EOF
#
