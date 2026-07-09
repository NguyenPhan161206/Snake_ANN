# Kế hoạch chi tiết: 02_training

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

## Các file

### 1. build_model.py — Định nghĩa kiến trúc

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
│   model.compile(optimizer=Adam(learning_rate=0.001),
│                 loss='mse',
│                 metrics=['mae'])
│   return model
│
├── if __name__ == "__main__":
│     model = build_ann()
│     model.summary()  # in kiến trúc
```

### 2. train.py — Huấn luyện

```
train.py
├── train_model(grid_size):
│   X = np.load(f"data/raw/{grid_size}x{grid_size}/X.npy")
│   y = np.load(f"data/raw/{grid_size}x{grid_size}/y.npy")
│   X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2)
│
│   model = build_ann(INPUT_FEATURES)
│   callbacks = [
│     EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True),
│     ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=5)
│   ]
│
│   history = model.fit(X_train, y_train,
│                       validation_data=(X_val, y_val),
│                       epochs=100, batch_size=32,
│                       callbacks=callbacks,
│                       verbose=1)
│   model.save(f"models/{grid_size}x{grid_size}/model.keras")
│   return history
│
├── if __name__ == "__main__":
│   for size in AVAILABLE_GRID_SIZES:
│     train_model(size)
```

### 3. plot_training.py — Vẽ đồ thị Loss

```
plot_training.py
├── đọc history từ train_model (hoặc lưu history riêng)
├── vẽ 2 đồ thị:
│   └── Loss (train vs validation) theo epoch
│   └── MAE (train vs validation) theo epoch
├── đánh dấu điểm overfitting nếu val_loss bắt đầu tăng
├── lưu vào results/plots/loss_{size}x{size}.png
```

### 4. evaluate_model.py — Đánh giá

```
evaluate_model.py
├── load model + test set (20% chưa dùng)
├── predict trên test set
├── in:
│   Test MSE: ...
│   Test MAE: ...
│   R2 Score: ...
├── vẽ biểu đồ scatter (y_true vs y_pred)
│   lưu vào results/plots/scatter_{size}.png
```

## Đầu vào/Đầu ra

- **Input**: `data/raw/{size}/X.npy`, `data/raw/{size}/y.npy`
- **Output**:
  - `models/{size}/model.keras`
  - `results/plots/loss_{size}.png`
  - `results/plots/scatter_{size}.png`
  - Console: Test MSE, MAE, R2

## Kiểm soát overfitting

- EarlyStopping(patience=10): dừng khi val_loss không cải thiện 10 epoch
- ReduceLROnPlateau: giảm lr khi loss plateau
- Theo dõi đồ thị: val_loss ↑ liên tục = overfitting → cần tăng dropout hoặc giảm model size