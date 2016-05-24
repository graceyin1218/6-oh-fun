# Graphics for Gridded Mazes
# For 6.01 Final Lab
# hartz, lpk S2014

import tkinter
import math

################################
# Color Handling
################################

red_hue = 0.0
green_hue = 120.0
blue_hue = 240.0
yellow_hue = 60.0
cyan_hue = 180.0
magenta_hue = 250.0

# given a probability, return a Tk Color
def prob_to_map_color(p, hue = cyan_hue, prior = 0.5):
    x = p - prior
    if p > prior:
        s = 1
        v = (1 - p) / (1 - prior)
    else:
        v = 1
        s = p / prior
    return rgb_to_py_color(hsv_to_rgb(hue, s, v))

#given an r,g,b tuple, return a matching Tk Color String
def rgb_to_py_color(color_vals):
    (r, g, b) = [math.floor(c*255.99) for c in color_vals]
    return '#%02x%02x%02x' % (r, g, b)

#given an h,s,v tuple, return a matching r,g,b tuple
def hsv_to_rgb(h, s, v):
    if s == 0:
        return (v, v, v)
    else:
        h = h/60  # sector 0 to 5
        i = math.floor( h )
        f = h - i        # factorial part of h
        p = v * ( 1 - s )
        q = v * ( 1 - s * f )
        t = v * ( 1 - s * ( 1 - f ) )
        if i == 0:
            return (v, t, p)
        elif i == 1:
            return (q, v, p)
        elif i == 2:
            return (p, v, t)
        elif i == 3:
            return (p, q, v)
        elif i == 4:
            return (t, p, v)
        else:
            return (v, p, q)



################################
# Abstract Base Class
################################

#Base class; gridded Tk Canvas associated with Maze instance
class MazeGraphicsWindow:
    title = 'MazeGraphicsWindow'
    cell_size = 5

    def __init__(self, maze):
        self.maze = maze
        self.window = tkinter.Toplevel()
        self.window.title(self.title)
        self.canvas = tkinter.Canvas(self.window,
                                     width=(self.cell_size+1)*self.maze.width,
                                     height=(self.cell_size+1)*self.maze.height)
        self.canvas.pack()
        self.drawn_cells = {}
        self.to_color = {}
        self.by_color = {"white":set()}
        self.dirty = set()
        for r in range(self.maze.height):
            for c in range(self.maze.width):
                x0 = c*(self.cell_size+1)-1
                x1 = x0+self.cell_size
                y0 = r*(self.cell_size+1)-1
                y1 = y0+self.cell_size
                cell = self.canvas.create_rectangle(x0,y0,x1,y1,
                                                    fill="white",
                                                    outline="white")
                self.drawn_cells[(r,c)] = cell
                self.to_color[(r,c)] = "white"
                self.by_color["white"].add((r,c))
                self.dirty.add((r,c))

    def render(self):
        d = set(self.dirty)
        for loc in d:
            self.blit_cell(loc,self.to_color[loc])

    def mark_cell(self, cell, color):
        if self.to_color[cell] != color:
            self.by_color[self.to_color[cell]].discard(cell)
            self.to_color[cell] = color
            self.dirty.add(cell)
            if color not in self.by_color:
                self.by_color[color] = set()
            self.by_color[color].add(cell)

    def mark_cells(self, cells, color):
        for cell in cells:
            self.mark_cell(cell, color)

    def blit_cell(self, loc, color):
        self.canvas.itemconfigure(self.drawn_cells[loc], fill=color, outline=color)
        self.dirty.discard(loc)

    def get_base_color(self, loc):
        return "white" if self.maze.is_clear(loc) else "black"

    def set_to_base_color(self, loc):
        self.mark_cell(loc, self.get_base_color(loc))

    def clearColor(self, color):
        for loc in self.by_color.get(color,set()):
            self.set_to_base_color()

    def redraw_world(self):
        for r in range(self.maze.height):
            for c in range(self.maze.width):
                self.set_to_base_color((r,c))

    def sonar_hit(self, loc):
        self.maze.sonar_hit(loc)
        self.draw_hit(loc)

    def sonar_pass(self, loc):
        self.maze.sonar_pass(loc)
        self.draw_pass(loc)

    draw_hit = draw_pass = set_to_base_color
 

##################################
# Specific Types of MazeGraphics 
##################################

#HeatMapWindow: for Bayesian Map, shows Probability of being occupied
class HeatMapWindow(MazeGraphicsWindow):
    title="HeatMap"
    def __init__(self, maze):
        MazeGraphicsWindow.__init__(self, maze)
        self.priorOcc = self.maze.prob_occupied((0,0))

    def get_base_color(self, loc):
        return prob_to_map_color(self.maze.prob_occupied(loc), prior=self.priorOcc)

#PathWindow: for all maps, shows passable and clear cells
class PathWindow(MazeGraphicsWindow):
    title="Path"
    def __init__(self, maze, show_passable):
        MazeGraphicsWindow.__init__(self, maze)
        self.show_passable = show_passable

    def get_base_color(self, loc):
        return "black" if not self.maze.is_clear(loc) else "red" if (self.show_passable and not self.maze.is_passable(loc)) else "white"
