import numpy as np
from collections import deque


class GridMap:
    def __init__(self, grid_size):
        self.grid_size = grid_size
        self.grid = np.zeros((grid_size, grid_size), dtype=int)
        self.snake = []
        self.food = None

    def place_snake_and_food(self, snake_length=3):
        self.grid[:, :] = 0
        head_r = np.random.randint(0, self.grid_size)
        head_c = np.random.randint(0, self.grid_size)
        self.snake = [(head_r, head_c)]
        self.grid[head_r, head_c] = 1
        for _ in range(snake_length - 1):
            last = self.snake[-1]
            neighbors = []
            for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nr, nc = last[0] + dr, last[1] + dc
                if 0 <= nr < self.grid_size and 0 <= nc < self.grid_size and self.grid[nr, nc] == 0:
                    neighbors.append((nr, nc))
            if not neighbors:
                break
            chosen = neighbors[np.random.randint(len(neighbors))]
            self.snake.append(chosen)
            self.grid[chosen[0], chosen[1]] = 1
        empty_cells = [(r, c) for r in range(self.grid_size) for c in range(self.grid_size)
                       if self.grid[r, c] == 0]
        if empty_cells:
            self.food = empty_cells[np.random.randint(len(empty_cells))]
            self.grid[self.food[0], self.food[1]] = 2
        return self.snake, self.food


def bfs_distance(grid, start, goal, body_set, grid_size):
    if start == goal:
        return 0
    queue = deque()
    queue.append((start[0], start[1], 0))
    visited = set()
    visited.add(start)
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    while queue:
        r, c, dist = queue.popleft()
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < grid_size and 0 <= nc < grid_size:
                if (nr, nc) == goal:
                    return dist + 1
                if (nr, nc) not in visited and (nr, nc) not in body_set and grid[nr, nc] != 1:
                    visited.add((nr, nc))
                    queue.append((nr, nc, dist + 1))
    return -1


def extract_window(grid, head, food, window_size=7, grid_size=None, body_set=None):
    if grid_size is None:
        grid_size = grid.shape[0]
    half = window_size // 2
    r_start = head[0] - half
    c_start = head[1] - half
    window = np.full((window_size, window_size), 1, dtype=int)
    for wr in range(window_size):
        for wc in range(window_size):
            gr = r_start + wr
            gc = c_start + wc
            if 0 <= gr < grid_size and 0 <= gc < grid_size:
                if (gr, gc) == food:
                    window[wr, wc] = 2
                elif (gr, gc) in body_set:
                    window[wr, wc] = 1
                else:
                    window[wr, wc] = 0
            else:
                window[wr, wc] = 1
    dx = food[0] - head[0]
    dy = food[1] - head[1]
    features = np.concatenate([window.flatten(), [dx, dy]])
    return features
