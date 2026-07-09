import os
import sys
import numpy as np
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from config import EPOCHS, BATCH_SIZE, VALIDATION_SPLIT, PATIENCE_EARLY_STOP
from config import PLOTS_DIR
from training.build_model import build_ann


def train_model(grid_size):
    raw_dir = os.path.join("data", "raw", f"{grid_size}x{grid_size}")
    X_train = np.load(os.path.join(raw_dir, "X_train.npy"))
    y_train = np.load(os.path.join(raw_dir, "y_train.npy"))
    X_val = np.load(os.path.join(raw_dir, "X_val.npy"))
    y_val = np.load(os.path.join(raw_dir, "y_val.npy"))

    print(f"  X_train: {X_train.shape}, X_val: {X_val.shape}")

    model = build_ann()

    callbacks = [
        EarlyStopping(monitor='val_loss', patience=PATIENCE_EARLY_STOP,
                      restore_best_weights=True, verbose=1),
        ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=5, verbose=1)
    ]

    history = model.fit(
        X_train, y_train,
        validation_data=(X_val, y_val),
        epochs=EPOCHS,
        batch_size=BATCH_SIZE,
        callbacks=callbacks,
        verbose=1
    )

    model_dir = os.path.join("models", f"{grid_size}x{grid_size}")
    os.makedirs(model_dir, exist_ok=True)
    model_path = os.path.join(model_dir, "model.keras")
    model.save(model_path)
    print(f"  Model saved: {model_path}")

    import pickle
    hist_path = os.path.join(PLOTS_DIR, f"history_{grid_size}x{grid_size}.pkl")
    os.makedirs(PLOTS_DIR, exist_ok=True)
    with open(hist_path, "wb") as f:
        pickle.dump(history.history, f)

    return history


def run(grid_size):
    return train_model(grid_size)


if __name__ == "__main__":
    from config import AVAILABLE_GRID_SIZES
    for size in AVAILABLE_GRID_SIZES:
        print(f"\nTraining grid {size}x{size}...")
        train_model(size)
