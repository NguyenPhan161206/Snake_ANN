import os
import sys
import numpy as np
import matplotlib.pyplot as plt


def r2_score_manual(y_true, y_pred):
    ss_res = np.sum((y_true - y_pred) ** 2)
    ss_tot = np.sum((y_true - np.mean(y_true)) ** 2)
    return 1 - (ss_res / (ss_tot + 1e-10))

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from config import PLOTS_DIR


def evaluate_model(grid_size):
    from tensorflow.keras.models import load_model

    model_path = os.path.join("models", f"{grid_size}x{grid_size}", "model.keras")
    raw_dir = os.path.join("data", "raw", f"{grid_size}x{grid_size}")

    if not os.path.exists(model_path):
        print(f"  Model not found: {model_path}")
        return

    model = load_model(model_path)
    X_val = np.load(os.path.join(raw_dir, "X_val.npy"))
    y_val = np.load(os.path.join(raw_dir, "y_val.npy"))

    loss, mae = model.evaluate(X_val, y_val, verbose=0)
    y_pred = model.predict(X_val, verbose=0).flatten()
    r2 = r2_score_manual(y_val, y_pred)

    print(f"  Grid {grid_size}x{grid_size}:")
    print(f"    Test MSE: {loss:.4f}")
    print(f"    Test MAE: {mae:.4f}")
    print(f"    R2 Score: {r2:.4f}")

    fig, ax = plt.subplots(figsize=(6, 6))
    ax.scatter(y_val, y_pred, alpha=0.3, s=5)
    min_val = min(y_val.min(), y_pred.min())
    max_val = max(y_val.max(), y_pred.max())
    ax.plot([min_val, max_val], [min_val, max_val], 'r--', label='Perfect fit')
    ax.set_xlabel('True BFS Distance')
    ax.set_ylabel('Predicted Distance')
    ax.set_title(f'ANN Predictions vs True ({grid_size}x{grid_size})')
    ax.legend()
    ax.grid(True)
    out_path = os.path.join(PLOTS_DIR, f"scatter_{grid_size}x{grid_size}.png")
    plt.tight_layout()
    plt.savefig(out_path, dpi=150)
    plt.close()
    print(f"  Saved scatter plot: {out_path}")


def run(grid_size):
    evaluate_model(grid_size)


if __name__ == "__main__":
    from config import AVAILABLE_GRID_SIZES
    for size in AVAILABLE_GRID_SIZES:
        run(size)
