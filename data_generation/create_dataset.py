import os
import numpy as np
from tqdm import tqdm

import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from config import NUM_SAMPLES, WINDOW_SIZE, SNAKE_INITIAL_LENGTH
from data_generation.generate_BFS_maze import GridMap, bfs_distance, extract_window


def generate_dataset(grid_size, num_samples):
    X = []
    y = []
    gm = GridMap(grid_size)
    samples_collected = 0
    attempts = 0
    max_attempts = num_samples * 5

    pbar = tqdm(total=num_samples, desc=f"Grid {grid_size}x{grid_size}")
    while samples_collected < num_samples and attempts < max_attempts:
        attempts += 1
        snake, food = gm.place_snake_and_food(SNAKE_INITIAL_LENGTH)
        if food is None:
            continue
        head = snake[0]
        body_set = set(snake[1:])
        dist = bfs_distance(gm.grid, head, food, body_set, grid_size)
        if dist > 0:
            features = extract_window(gm.grid, head, food, WINDOW_SIZE, grid_size, body_set)
            X.append(features)
            y.append(dist)
            samples_collected += 1
            pbar.update(1)
    pbar.close()
    return np.array(X, dtype=np.float32), np.array(y, dtype=np.float32)


def save_dataset(X, y, grid_size):
    raw_dir = os.path.join("data", "raw", f"{grid_size}x{grid_size}")
    proc_dir = os.path.join("data", "processed", f"{grid_size}x{grid_size}")
    os.makedirs(raw_dir, exist_ok=True)
    os.makedirs(proc_dir, exist_ok=True)

    indices = np.random.permutation(len(X))
    split = int(len(X) * 0.8)
    train_idx = indices[:split]
    val_idx = indices[split:]

    np.save(os.path.join(raw_dir, "X_train.npy"), X[train_idx])
    np.save(os.path.join(raw_dir, "y_train.npy"), y[train_idx])
    np.save(os.path.join(raw_dir, "X_val.npy"), X[val_idx])
    np.save(os.path.join(raw_dir, "y_val.npy"), y[val_idx])
    np.save(os.path.join(proc_dir, "X_all.npy"), X)
    np.save(os.path.join(proc_dir, "y_all.npy"), y)

    print(f"  Saved: train={len(train_idx)}, val={len(val_idx)}, total={len(X)}")


def run(grid_size):
    num = NUM_SAMPLES.get(grid_size, 10000)
    X, y = generate_dataset(grid_size, num)
    save_dataset(X, y, grid_size)
    return X, y


if __name__ == "__main__":
    from config import AVAILABLE_GRID_SIZES
    for size in AVAILABLE_GRID_SIZES:
        run(size)
