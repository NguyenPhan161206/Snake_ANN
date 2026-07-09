import os
import sys
import numpy as np
from tensorflow.keras.models import load_model

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from config import WINDOW_SIZE


class AnnHeuristic:
    def __init__(self, grid_size):
        model_path = os.path.join("models", f"{grid_size}x{grid_size}", "model.keras")
        if not os.path.exists(model_path):
            raise FileNotFoundError(
                f"Model not found at {model_path}. Train first."
            )
        self.model = load_model(model_path)
        self.grid_size = grid_size
        self.window_size = WINDOW_SIZE
        self.cache = {}

    def precompute(self, head, food, body):
        body_set = set(body)
        grid = np.zeros((self.grid_size, self.grid_size), dtype=int)
        for r, c in body_set:
            if 0 <= r < self.grid_size and 0 <= c < self.grid_size:
                grid[r, c] = 1
        if food:
            grid[food[0], food[1]] = 2
        self.cache = {}
        cells = []
        positions = []
        for r in range(self.grid_size):
            for c in range(self.grid_size):
                if (r, c) not in body_set:
                    cells.append((r, c))
        if not cells:
            return
        batch_features = []
        for r, c in cells:
            features = self._extract_fast(grid, (r, c), food, body_set)
            batch_features.append(features)
            positions.append((r, c))
        batch = np.array(batch_features, dtype=np.float32)
        preds = self.model.predict(batch, verbose=0).flatten()
        for pos, val in zip(positions, preds):
            self.cache[pos] = float(val)

    def _extract_fast(self, grid, head, food, body_set):
        half = self.window_size // 2
        r_start = head[0] - half
        c_start = head[1] - half
        window = np.full((self.window_size, self.window_size), 1, dtype=np.float32)
        for wr in range(self.window_size):
            for wc in range(self.window_size):
                gr = r_start + wr
                gc = c_start + wc
                if 0 <= gr < self.grid_size and 0 <= gc < self.grid_size:
                    window[wr, wc] = float(grid[gr, gc])
        dx = float(food[0] - head[0]) if food else 0.0
        dy = float(food[1] - head[1]) if food else 0.0
        return np.concatenate([window.flatten(), [dx, dy]])

    def predict(self, head, food, body):
        val = self.cache.get(head)
        if val is not None:
            return val
        return abs(head[0] - food[0]) + abs(head[1] - food[1])
