# Mazes

import lib601.util as util
from lib601.search import search

class Maze:
    def __init__(self, maze_text):
        #pass # Your code here
        self.maze_text = maze_text
        self.width = len(maze_text[0])
        self.height = len(maze_text)
        for i in range(self.height):
            for j in range(self.width):
                if maze_text[i][j] == "S":
                    self.start = (i, j)
                if maze_text[i][j] == "G":
                    self.goal = (i,j)

    def is_passable(self, loc):
        if loc[0] < 0 or loc[0] >= self.height:
            return False
        if loc[1] < 0 or loc[1] >= self.width:
            return False
        if self.maze_text[loc[0]][loc[1]] == ".":
            return True
        if self.maze_text[loc[0]][loc[1]] == "G":
            return True
        if self.maze_text[loc[0]][loc[1]] == "S":
            return True
        return False

def make_maze_successors(maze):
    ans = []
    for i in range(maze.height):
        jar = [[]]
        for j in range(maze.width):
            jar.append([])
        ans.append(jar)
    for i in range(maze.height):
        for j in range(maze.width):
            if maze.is_passable((i, j)):
                if i > 0:
                    if maze.is_passable((i-1, j)):
                        ans[i][j].append((i-1, j))
                if j > 0:
                    if maze.is_passable((i, j-1)):
                        ans[i][j].append((i, j-1))
                if i < maze.height-1:
                    if maze.is_passable((i+1, j)):
                        ans[i][j].append((i+1, j))
                if j < maze.width-1:
                    if maze.is_passable((i, j+1)):
                        ans[i][j].append((i, j+1))
    return lambda loc: ans[loc[0]][loc[1]]
 

# TEST CASES
#
# set up lists of strings to represent the four test mazes
small_maze_text = [line.strip() for line in open('small_maze.txt').readlines()]
medium_maze_text = [line.strip() for line in open('medium_maze.txt').readlines()]
large_maze_text = [line.strip() for line in open('large_maze.txt').readlines()]
huge_maze_text = [line.strip() for line in open('huge_maze.txt').readlines()]

# Your code here to run a search on a test maze

small_maze = Maze(small_maze_text)
medium_maze = Maze(medium_maze_text)
large_maze = Maze(large_maze_text)
huge_maze = Maze(huge_maze_text)

small = search(make_maze_successors(small_maze), small_maze.start, lambda x: x == small_maze.goal, False)
print(len(small))

medium = search(make_maze_successors(medium_maze), medium_maze.start, lambda x: x == medium_maze.goal, False)
print(len(medium))

large = search(make_maze_successors(large_maze), large_maze.start, lambda x: x == large_maze.goal, False)
print(len(large))

huge = search(make_maze_successors(huge_maze), huge_maze.start, lambda x: x == huge_maze.goal, False)
print(len(huge))
