import os
import sys
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.optimizers import Adam

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from config import INPUT_FEATURES, LEARNING_RATE


def build_ann(input_dim=INPUT_FEATURES):
    model = Sequential([
        Dense(128, activation='relu', input_shape=(input_dim,)),
        Dropout(0.2),
        Dense(64, activation='relu'),
        Dropout(0.2),
        Dense(32, activation='relu'),
        Dense(1, activation='linear')
    ])
    model.compile(optimizer=Adam(learning_rate=LEARNING_RATE),
                  loss='mse',
                  metrics=['mae'])
    return model


if __name__ == "__main__":
    model = build_ann()
    model.summary()
