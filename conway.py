"""
conway.py
A simple Python/matplotlib implementation of Conway's Game of Life.
"""

import sys
import os
import argparse
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

ON = 255
OFF = 0
vals = [ON, OFF]

def randomGrid(N):
    """returns a grid of NxN random values"""
    return np.random.choice(vals, N*N, p=[0.3, 0.7]).reshape(N, N)

def addGlider(i, j, grid):
    """adds a glider with top left cell at (i, j)"""
    glider = np.array([[0,    0, 255],
                       [255,  0, 255],
                       [0,  255, 255]])
    grid[i:i+3, j:j+3] = glider

def update(frameNum, img, grid, N):
    # copy grid since we require 8 neighbors for calculation
    # and we go line by line
    newGrid = grid.copy()
    for x in range(1, N-1):
        for y in range(1, N-1):
            accum_cel = grid[x-1,y-1] + grid[x-1,y] + grid[x-1,y+1] + grid[x,y-1] + grid[x,y+1] + grid[x+1,y-1] + grid[x+1,y] + grid[x+1,y+1]
            accum_cel /= 255
            if grid[x,y] == 255:
                if accum_cel == 2 or accum_cel == 3:
                    pass
                else:
                    newGrid[x,y] = 0
            else:
                if accum_cel == 3:
                    newGrid[x,y] = 255

    # update data
    img.set_data(newGrid)
    grid[:] = newGrid[:]
    return img,

def fillGrid(grid, file):
    f = open("{0}\{1}".format(os.getcwd(),file),'r')
    raw_coords = f.readlines()
    coords = [i.strip() for i in raw_coords]
    for i in coords:
        coord = i.split(",")
        grid[int(coord[1]),int(coord[0])] = 255
    return grid

# main() function
def main():
    # Command line args are in sys.argv[1], sys.argv[2] ..
    # sys.argv[0] is the script name itself and can be ignored
    # parse arguments
    parser = argparse.ArgumentParser(description="Runs Conway's Game of Life conway.py")
    parser.add_argument("N", type=int, help="Size of universe")
    parser.add_argument("-i", "--interval", type=int, help="Update interval in miliseconds")
    parser.add_argument("-f", "--file", type=str,
                        help="File with initial configuration of cells. Config file should"
                             "be one cell per line with X & Y coordinate separated by a comma. "
                             "For example: 15,45")
    args = parser.parse_args()
    # set grid size
    N = args.N
    # set animation update interval
    updateInterval = args.interval

    # declare grid
    grid = np.array([])

    if args.file:
        print("Setting grid of {0} x {0}".format(N))
        print("Setting initial configuration with file {0}".format(args.file))
        print("Update interval = {0}".format(updateInterval))
        a = (N,N)
        grid = np.zeros(a, dtype=int)
        grid = fillGrid(grid, args.file)
        fig, ax = plt.subplots()
        img = ax.imshow(grid, interpolation='nearest')
        ani = animation.FuncAnimation(fig, update, fargs=(img, grid, N, ),
                                      frames = 5,
                                      interval=updateInterval,
                                      save_count=5)

        plt.show()
    else:
        print("Setting grid of {0} x {0}".format(N))
        print("Update interval = {0}".format(updateInterval))
        # populate grid with random on/off - more off than on
        grid = randomGrid(N)
        # Uncomment lines to see the "glider" demo
        #grid = np.zeros(N*N).reshape(N, N)
        #addGlider(1, 1, grid)

        # set up animation

        fig, ax = plt.subplots()
        img = ax.imshow(grid, interpolation='nearest')
        ani = animation.FuncAnimation(fig, update, fargs=(img, grid, N, ),
                                      frames = 5,
                                      interval=updateInterval,
                                      save_count=5)
        plt.show()

# call main
if __name__ == '__main__':
    main()