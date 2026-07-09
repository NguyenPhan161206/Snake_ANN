import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from config import WINDOW_SIZE


def plot_sample(grid_size, sample_idx=0):
    proc_dir = os.path.join("data", "processed", f"{grid_size}x{grid_size}")
    X = np.load(os.path.join(proc_dir, "X_all.npy"))
    y = np.load(os.path.join(proc_dir, "y_all.npy"))

    features = X[sample_idx]
    label = y[sample_idx]
    window = features[:WINDOW_SIZE * WINDOW_SIZE].reshape(WINDOW_SIZE, WINDOW_SIZE)
    dx, dy = features[-2], features[-1]

    fig, axes = plt.subplots(1, 2, figsize=(10, 5))

    ax = axes[0]
    cmap = plt.cm.colors.ListedColormap(['white', 'black', 'red'])
    bounds = [-0.5, 0.5, 1.5, 2.5]
    norm = plt.cm.colors.BoundaryNorm(bounds, cmap.N)
    ax.imshow(window, cmap=cmap, norm=norm, interpolation='nearest')
    ax.set_title(f"Window {WINDOW_SIZE}x{WINDOW_SIZE} around head")
    ax.grid(True, color='gray', linewidth=0.5)

    ax = axes[1]
    ax.axis('off')
    info = (
        f"Grid size: {grid_size}x{grid_size}\n"
        f"Window size: {WINDOW_SIZE}x{WINDOW_SIZE}\n"
        f"Input features: {X.shape[1]}\n"
        f"Label (BFS distance): {label}\n"
        f"Relative food pos: (dx={dx}, dy={dy})\n\n"
        f"Legend:\n"
        f"  White = empty\n"
        f"  Black = obstacle\n"
        f"  Red   = food"
    )
    ax.text(0.1, 0.5, info, fontsize=12, verticalalignment='center',
            fontfamily='monospace', transform=ax.transAxes)

    out_dir = os.path.join("results", "plots")
    os.makedirs(out_dir, exist_ok=True)
    plt.tight_layout()
    plt.savefig(os.path.join(out_dir, f"sample_{grid_size}x{grid_size}.png"), dpi=150)
    plt.close()
    print(f"Saved sample plot to results/plots/sample_{grid_size}x{grid_size}.png")


def run(grid_size):
    plot_sample(grid_size)


if __name__ == "__main__":
    from config import AVAILABLE_GRID_SIZES
    for size in AVAILABLE_GRID_SIZES:
        run(size)
