from IPython.display import clear_output

from matplotlib import pyplot as plt
from matplotlib.patches import Rectangle
import random
from collections import defaultdict
import numpy as np
import time


absolute_directions = {0: "←", 1: "↑", 2: "→", 3: "↓"}
direction_steps = {0: np.array([-1, 0]), 1: np.array([0, -1]), 2: np.array([1, 0]), 3: np.array([0, 1])}
relative_directions = {-1: "←", 0: "↑", 1: "→"}

check_directions = np.array([[ 1,  1],
                             [ 0,  1],
                             [-1,  1],
                             [-1,  0],
                             [-1, -1],
                             [ 0, -1],
                             [ 1, -1],
                             [ 1,  0]])

def bools_to_int(bools):
    return sum(bit << idx for idx, bit in enumerate(bools))

class Snake:
    def __init__(self, pos, absolute_direction=0, relative_direction=0):
        self.init_state(pos, absolute_direction, relative_direction)
    
    def init_state(self, pos, absolute_direction=0, relative_direction=0):
        self.pos = pos
        self.absolute_direction = absolute_direction
        self.relative_direction = relative_direction
    
    def check_overlap(self, pos, range_start=0):
        for spos in self.pos[range_start:]:
            if (pos == spos).all():
                return True
        return False

    def __len__(self):
        return len(self.pos)
    

class SnakeGame:
    def __init__(self, grid_sz=(10, 10), cell_sz=5, snake_color='darkgreen', fruit_color='r', wall_color='k'):
        self.grid_sz = np.array(grid_sz)
        self.cell_sz = cell_sz
        self.snake_color = snake_color
        self.fruit_color = fruit_color
        self.wall_color = wall_color
        self.init_game()
    
    def random_position(self, border_space=1):
        return np.array([random.randint(border_space, self.grid_sz[0]-1-border_space), random.randint(border_space, self.grid_sz[1]-1-border_space)])

    def spawn_fruit(self, border_space=1):
        self.fruit_pos = self.random_position(border_space)
        while(self.snake.check_overlap(self.fruit_pos)):
            self.fruit_pos = self.random_position(border_space)

    def init_game(self, border_space = 1):
        self.snake = Snake([self.random_position(border_space)])
        self.spawn_fruit(border_space)
        # self.fruit_pos = self.snake.pos[0] - np.array([2, 0])
        
    def set_action(self, action):
        self.snake.relative_direction = action - 1

    def step(self, action=1):
        reward = False
        game_continues = True
        self.set_action(action)
        if self.snake.relative_direction != 0:
            self.snake.absolute_direction = (self.snake.absolute_direction + self.snake.relative_direction) % 4
            self.snake.relative_direction = 0
        last_pos = self.snake.pos[-1].copy()

        for i in range(len(self.snake)-2, -1, -1):
            self.snake.pos[i+1] = self.snake.pos[i].copy()

        self.snake.pos[0] += direction_steps[self.snake.absolute_direction]

        if (self.snake.pos[0] == self.fruit_pos).all():
            self.snake.pos.append(last_pos)
            reward = True
            self.spawn_fruit()
        if self.snake.check_overlap(self.snake.pos[0], 1):
            game_continues = False
        if (self.snake.pos[0] == 0).any() or (self.snake.pos[0][0] == self.grid_sz[0]-1) or (self.snake.pos[0][1] == self.grid_sz[1]-1):
            game_continues = False
        return game_continues, reward, self.get_state()

    def check_obstacle(self, pos):
        if (pos == 0).any() or (pos[0] == self.grid_sz[0]-1) or (pos[1] == self.grid_sz[1]-1):
            return True
        return self.snake.check_overlap(pos, 1)

    def get_state(self):
        test_dirs = [check_directions[(i + 2 * self.snake.absolute_direction) % len(check_directions)] for i in range(8)]
        obstacles_state = bools_to_int([self.check_obstacle(self.snake.pos[0] + dir) for dir in test_dirs[1:-1:2]])
        goal_dir = np.clip(self.fruit_pos - self.snake.pos[0], -1, 1)
        goal_state, = np.where((test_dirs == goal_dir).all(axis=1))
        return goal_state.item() * 8 + obstacles_state

    def plot_rectangle(self, ax, pos, sz, color):
        rect = Rectangle(pos, *sz, linewidth=0,edgecolor='none',facecolor=color)
        ax.add_patch(rect)

    def score(self):
        return len(self.snake)-1

    def render(self, episode=None, high_score=None, clear=True):
        if clear:
            clear_output(wait=True)
        fig = plt.figure()
        ax = fig.gca()
        ax.invert_yaxis()
        ax.tick_params(top=True, labeltop=True, bottom=False, labelbottom=False)
        
        self.plot_rectangle(ax, (0,0), np.array([self.grid_sz[0],1])*self.cell_sz, self.wall_color)
        self.plot_rectangle(ax, (0,(self.grid_sz[1]-1)*self.cell_sz), np.array([self.grid_sz[0],1])*self.cell_sz, self.wall_color)
        self.plot_rectangle(ax, (0,0), np.array([1, self.grid_sz[1]])*self.cell_sz, self.wall_color)
        self.plot_rectangle(ax, ((self.grid_sz[0]-1)*self.cell_sz, 0), np.array([1, self.grid_sz[1]])*self.cell_sz, self.wall_color)
        self.plot_rectangle(ax, self.fruit_pos * self.cell_sz, (self.cell_sz, self.cell_sz), self.fruit_color)

        for spos in self.snake.pos:
            self.plot_rectangle(ax, spos * self.cell_sz, (self.cell_sz, self.cell_sz), self.snake_color)

        ax.set_xticks(np.arange(0, (self.grid_sz[0]+1)*self.cell_sz, self.cell_sz))
        ax.set_yticks(np.arange(0, (self.grid_sz[1]+1)*self.cell_sz, self.cell_sz))
        
        if episode is None:
            label = ""
        else:
            label = f"Episode: {episode}\n"
        label += f"Score: {self.score()}"
        if high_score is not None:
            label += f"\nHigh score: {high_score}"
        plt.xlabel(label)
        plt.grid()
        plt.show()
