# Kế hoạch chi tiết: training

## Mục tiêu

Xây dựng và huấn luyện ANN để dự đoán khoảng cách từ đầu rắn đến thức ăn
dựa trên cửa sổ quan sát 7x7 và tọa độ tương đối.

## Kiến trúc mạng ANN

```
Input (51)
  │
Dense(128, ReLU)
  │
Dropout(0.2)
  │
Dense(64, ReLU)
  │
Dropout(0.2)
  │
Dense(32, ReLU)
  │
Dense(1, Linear)   ← Output: khoảng cách dự đoán
```

- Loss: `mean_squared_error` (MSE)
- Optimizer: Adam (lr=0.001)
- Metric: Mean Absolute Error (MAE)

## File: build_model.py

```
build_model.py
├── build_ann(input_dim=51):
│   model = Sequential([
│     Dense(128, activation='relu', input_shape=(input_dim,)),
│     Dropout(0.2),
│     Dense(64, activation='relu'),
│     Dropout(0.2),
│     Dense(32, activation='relu'),
│     Dense(1, activation='linear')
│   ])
│   model.compile(optimizer=Adam(lr=0.001), loss='mse', metrics=['mae'])
│   return model
```

## File: train.py

```
train.py
├── train_model(grid_size):
│   X_train = np.load("data/raw/{size}/X_train.npy")
│   y_train = np.load("data/raw/{size}/y_train.npy")
│   X_val   = np.load("data/raw/{size}/X_val.npy")
│   y_val   = np.load("data/raw/{size}/y_val.npy")
│
│   model = build_ann()
│   callbacks = [
│     EarlyStopping(patience=10, restore_best_weights=True),
│     ReduceLROnPlateau(factor=0.5, patience=5)
│   ]
│   model.fit(X_train, y_train,
│             validation_data=(X_val, y_val),
│             epochs=100, batch_size=32, callbacks=callbacks)
│   model.save(f"models/{size}x{size}/model.keras")
│   lưu history.hist → results/plots/history_{size}.pkl
│
└── run(grid_size): gọi train_model
```

## File: plot_training.py

```
plot_training.py
├── load history_{size}.pkl
├── vẽ 2 đồ thị:
│   └── Loss (train vs validation) theo epoch
│   └── MAE (train vs validation) theo epoch
└── lưu vào results/plots/loss_{size}.png
```

## File: evaluate_model.py

```
evaluate_model.py
├── load model.keras + X_val, y_val
├── model.evaluate() → in Test MSE, Test MAE
├── r2_score_manual() → in R2 Score
├── vẽ scatter (y_true vs y_pred) + đường perfect fit
└── lưu vào results/plots/scatter_{size}.png
```

## Kiểm soát overfitting

- EarlyStopping(patience=10): dừng khi val_loss không cải thiện 10 epoch
- ReduceLROnPlateau: giảm lr khi loss plateau
- Đồ thị: val_loss ↑ liên tục = overfitting → cần tăng dropout hoặc giảm model size
- 10x10: R² ≈ 0.95 (ổn), 20x20: R² ≈ 0.96 (overfit nhẹ, best ở epoch 1)
