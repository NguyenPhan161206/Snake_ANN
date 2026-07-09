# Kế hoạch chi tiết: 01_data_generation

## Mục tiêu

Tạo bộ dữ liệu huấn luyện cho ANN:
- **Input**: Cửa sổ WxW (W=7) xoay quanh đầu rắn + tọa độ tương đối của thức ăn (dx, dy)
- **Label**: Khoảng cách đường đi ngắn nhất từ đầu rắn đến thức ăn (tính bằng BFS)

## Ý tưởng thuật toán

BFS (Breadth-First Search) được dùng để tính khoảng cách thực tế:
- Grid: 0 = ô trống, 1 = chướng ngại (thân rắn, tường)
- Xuất phát từ đầu rắn, lan rộng ra 4 hướng (lên, xuống, trái, phải)
- Nếu đến được thức ăn → label = số bước
- Nếu không → bỏ qua mẫu (không dùng để train)

## Các file

### 1. generate_BFS_maze.py — Lõi BFS

```
generate_BFS_maze.py
├── GridMap class:
│     grid: 2D numpy array (size x size)
│     snake_body: list of (r, c)
│     food: (r, c)
│   └── place_random(): đặt rắn + thức ăn ngẫu nhiên, không trùng nhau
│
├── bfs_distance(grid, start, goal):
│     queue = deque([(start_r, start_c, 0)])
│     visited = set()
│     directions = [(0,1),(0,-1),(1,0),(-1,0)]
│     while queue:
│       pop → nếu == goal → return dist
│       nếu ô kế tiếp hợp lệ (0<=r<size, 0<=c<size, grid[nr][nc]!=1, chưa visited)
│         → push(queue, dist+1)
│     return -1  (không có đường)
│
├── extract_window(grid, head, food, window_size=7):
│     r_start = head_r - window_size//2
│     c_start = head_c - window_size//2
│     window = grid[r_start:r_start+W, c_start:c_start+W]
│     Nếu tràn biên → pad = 1 (coi là chướng ngại)
│     Thay giá trị: 0=trống, 1=chướng ngại, 2=food
│     flatten + thêm (dx, dy) → return vector 51 phần tử
```

### 2. create_dataset.py — Sinh và lưu dữ liệu

```
create_dataset.py
├── generate_dataset(grid_size, num_samples):
│   X = []  # list of 51-feature vectors
│   y = []  # list of distances
│   for _ in range(num_samples):
│     grid = GridSM(grid_size)
│     grid.place_snake_and_food()
│     dist = bfs_distance(grid.grid, grid.snake[0], grid.food)
│     if dist > 0:
│       features = extract_window(...)
│       X.append(features)
│       y.append(dist)
│   return np.array(X), np.array(y)
│
├── save_dataset(X, y, grid_size):
│     lưu vào data/raw/{size}/X.npy, y.npy
│     (tạm thời raw = processed, xử lý thêm sau nếu cần)
│
└── if __name__ == "__main__":
│     for size in [10, 20, 50]:
│       X, y = generate_dataset(size, NUM_SAMPLES[size])
│       save_dataset(X, y, size)
│       print(f"Done {size}x{size}: {len(X)} samples")
```

### 3. visualize_samples.py — Kiểm tra dữ liệu

```
visualize_samples.py
├── load một vài mẫu từ data/raw/{size}/
├── plot_grid(): vẽ grid matplotlib
│   màu trắng = trống, đen = chướng ngại, đỏ = thức ăn, xanh = rắn
├── ghi chú: input vector 51 + label (khoảng cách BFS)
└── lưu vào results/plots/sample_{size}.png
```

## Đầu vào/Đầu ra

- **Input**: config.py (grid_size, num_samples, window_size)
- **Output**:
  - `data/raw/{size}/X.npy` — shape (N, 51)
  - `data/raw/{size}/y.npy` — shape (N,)
  - `results/plots/sample_{size}.png`

## Kiểm tra

- `python -c "import numpy as np; d=np.load('data/raw/10x10/X.npy'); print(d.shape)"` → (N, 51)
- Số mẫu N phải xấp xỉ num_samples
- visualize_samples.py không lỗi, hiển thị được grid