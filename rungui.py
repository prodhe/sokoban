#
#   game.py
#


#
# imports
#

from sys import argv
from tkFileDialog import askopenfilename
import Tkinter as tk
import sokoban


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

def openfile():
    filename = askopenfilename(parent=root)
    g.load(filename)
    updategui()

def updategui():
    w.itemconfig(screen, text=g.output())

# handle key presses
def key(event):

    # get key
    press = event.keysym

    if press in ('Escape', 'q'):
        root.quit()
    if press in ('D', 'd'):
        print sokoban.log

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


#
# entry point
#

# initialize the game engine
g = sokoban.init()

if len(argv) == 2:
    g.load(argv[2])
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
filemenu.add_command(label="Open level", command=openfile)
filemenu.add_separator()
filemenu.add_command(label="Undo", command=undo)
filemenu.add_command(label="Redo", command=redo)
filemenu.add_separator()
filemenu.add_command(label="Restart", command=restart)
filemenu.add_separator()
filemenu.add_command(label="Quit", command=root.quit)
menubar.add_cascade(label="Sokoban", menu=filemenu)
#helpmenu = tk.Menu(menubar, tearoff=0)
#helpmenu.add_command(label="About")
#menubar.add_cascade(label="Help", menu=helpmenu)
root.config(menu=menubar)

# main screen
w = tk.Canvas(root, background="#222", width=600, height=500)
w.pack()
screen = w.create_text(300,250, anchor=tk.CENTER, font="Courier", fill="#dedede", text=g.output())

# listen for key presses
root.bind("<Key>", key)

# loop
root.mainloop()

#
# EOF
#
