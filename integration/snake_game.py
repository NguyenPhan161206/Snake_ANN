import os
import sys
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from config import SNAKE_INITIAL_LENGTH


class SnakeGame:
    def __init__(self, grid_size, snake_length=SNAKE_INITIAL_LENGTH):
        self.grid_size = grid_size
        self.snake_length = snake_length
        self.reset()

    def reset(self):
        self.snake = []
        self.food = None
        self.done = False
        self.steps = 0
        self.won = False
        self._place_random()
        return self

    def _place_random(self):
        grid = np.zeros((self.grid_size, self.grid_size), dtype=int)
        head_r = np.random.randint(0, self.grid_size)
        head_c = np.random.randint(0, self.grid_size)
        self.snake = [(head_r, head_c)]
        grid[head_r, head_c] = 1
        for _ in range(self.snake_length - 1):
            last = self.snake[-1]
            neighbors = []
            for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nr, nc = last[0] + dr, last[1] + dc
                if 0 <= nr < self.grid_size and 0 <= nc < self.grid_size and grid[nr, nc] == 0:
                    neighbors.append((nr, nc))
            if not neighbors:
                break
            chosen = neighbors[np.random.randint(len(neighbors))]
            self.snake.append(chosen)
            grid[chosen[0], chosen[1]] = 1
        empty = [(r, c) for r in range(self.grid_size) for c in range(self.grid_size)
                 if grid[r, c] == 0]
        if empty:
            self.food = empty[np.random.randint(len(empty))]
        return self.snake, self.food

    def step(self, direction):
        if self.done:
            return
        dr, dc = direction
        head = self.snake[0]
        new_head = (head[0] + dr, head[1] + dc)

        if not (0 <= new_head[0] < self.grid_size and 0 <= new_head[1] < self.grid_size):
            self.done = True
            self.won = False
            return

        if new_head in self.snake[:-1]:
            self.done = True
            self.won = False
            return

        self.snake.insert(0, new_head)
        if new_head == self.food:
            self.won = True
            self.done = True
        else:
            self.snake.pop()
        self.steps += 1

    def play_with_solver(self, solver):
        if self.done:
            return
        head = self.snake[0]
        path = solver.find_path(head, self.food, self.snake)
        if path is not None and len(path) > 1:
            next_pos = path[1]
            direction = (next_pos[0] - head[0], next_pos[1] - head[1])
            self.step(direction)
        else:
            self.done = True
            self.won = False
