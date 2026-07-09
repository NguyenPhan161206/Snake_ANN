import os
import sys
import pickle
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from config import PLOTS_DIR


def plot_training(grid_size):
    hist_path = os.path.join(PLOTS_DIR, f"history_{grid_size}x{grid_size}.pkl")
    if not os.path.exists(hist_path):
        print(f"  No history found at {hist_path}. Train first.")
        return
    with open(hist_path, "rb") as f:
        history = pickle.load(f)

    fig, axes = plt.subplots(1, 2, figsize=(12, 4))

    axes[0].plot(history['loss'], label='Train Loss', color='blue')
    axes[0].plot(history['val_loss'], label='Val Loss', color='red')
    axes[0].set_xlabel('Epoch')
    axes[0].set_ylabel('MSE Loss')
    axes[0].set_title(f'Loss vs Epoch ({grid_size}x{grid_size})')
    axes[0].legend()
    axes[0].grid(True)

    if 'mae' in history:
        axes[1].plot(history['mae'], label='Train MAE', color='blue')
        axes[1].plot(history['val_mae'], label='Val MAE', color='red')
        axes[1].set_xlabel('Epoch')
        axes[1].set_ylabel('MAE')
        axes[1].set_title(f'MAE vs Epoch ({grid_size}x{grid_size})')
        axes[1].legend()
        axes[1].grid(True)

    min_val_loss = min(history['val_loss'])
    best_epoch = history['val_loss'].index(min_val_loss) + 1
    fig.suptitle(f'Best val_loss = {min_val_loss:.4f} at epoch {best_epoch}',
                 fontsize=12)
    plt.tight_layout()
    out_path = os.path.join(PLOTS_DIR, f"loss_{grid_size}x{grid_size}.png")
    plt.savefig(out_path, dpi=150)
    plt.close()
    print(f"  Saved loss plot: {out_path}")
    print(f"  Min val_loss: {min_val_loss:.4f} at epoch {best_epoch}")


def run(grid_size):
    plot_training(grid_size)


if __name__ == "__main__":
    from config import AVAILABLE_GRID_SIZES
    for size in AVAILABLE_GRID_SIZES:
        run(size)
