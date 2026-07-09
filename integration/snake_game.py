import os
import sys
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from config import SNAKE_INITIAL_LENGTH, SNAKE_START, OBSTACLE_DENSITY


class SnakeGame:
    def __init__(self, grid_size, snake_length=SNAKE_INITIAL_LENGTH):
        self.grid_size = grid_size
        self.snake_length = snake_length
        self.snake_start = SNAKE_START
        self.obstacle_density = OBSTACLE_DENSITY
        self.reset()

    def reset(self):
        self.snake = []
        self.food = None
        self.obstacles = set()
        self.done = False
        self.steps = 0
        self.won = False
        self._generate_obstacles()
        self._place_snake()
        self._place_food()
        return self

    def _generate_obstacles(self):
        self.obstacles = set()
        margin = 2
        for r in range(self.grid_size):
            for c in range(self.grid_size):
                if r <= margin and c <= margin:
                    continue
                if np.random.random() < self.obstacle_density:
                    self.obstacles.add((r, c))

    def _place_snake(self):
        head_r, head_c = self.snake_start
        self.snake = [(head_r, head_c)]
        body = [(head_r, head_c)]
        for _ in range(self.snake_length - 1):
            last = body[-1]
            neighbors = []
            for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nr, nc = last[0] + dr, last[1] + dc
                if (0 <= nr < self.grid_size and 0 <= nc < self.grid_size
                        and (nr, nc) not in body and (nr, nc) not in self.obstacles):
                    neighbors.append((nr, nc))
            if not neighbors:
                break
            chosen = neighbors[np.random.randint(len(neighbors))]
            body.append(chosen)
        self.snake = body

    def _place_food(self):
        occupied = set(self.snake) | self.obstacles
        empty = [(r, c) for r in range(self.grid_size) for c in range(self.grid_size)
                 if (r, c) not in occupied]
        if empty:
            self.food = empty[np.random.randint(len(empty))]
        else:
            self.food = None

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

        if new_head in self.obstacles:
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
        path = solver.find_path(head, self.food, self.snake, self.obstacles)
        if path is not None and len(path) > 1:
            next_pos = path[1]
            direction = (next_pos[0] - head[0], next_pos[1] - head[1])
            self.step(direction)
        else:
            self.done = True
            self.won = False
