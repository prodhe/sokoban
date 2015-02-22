# Sokoban game engine

...in Python.

## How to run

You must have Python installed, obviously.

Clone this repository:

    git clone https://github.com/prodhe/sokoban.git

Or download it as a zip file:

    https://github.com/prodhe/sokoban/archive/master.zip

Run

    $ cd sokoban
    $ python rungui.py

## How to use

### Basic movement:

    UP      (k)
    DOWN    (j)
    LEFT    (h)
    RIGHT   (l)

### Game control:

    (U)ndo movement
    (R)edo movement
    (Esc)ape to quit

### Game play:

    @ +  Worker
    o *  Crate
    .    Storage
    #    Wall

Move your worker and push the crates, until they are all in storage.


## How to code

    # import
    import sokoban
    
    # init
    g = sokoban.init()
    
    # optionally load a level
    g.load("level.txt")
    
    # or load default and also restart
    g.load()
    
    # show ascii output
    g.output()

    # direction (eg. (-1,0) for left)
    g.move(x, y)

    # movement history traversal
    g.undo()
    g.redo()

    # when finished
    game.finished() == true

---
*by Prodhe*
