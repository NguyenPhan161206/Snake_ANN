# Kế hoạch chi tiết: data_generation

## Mục tiêu

Tạo bộ dữ liệu huấn luyện cho ANN:
- **Input**: Cửa sổ 7x7 xoay quanh đầu rắn + tọa độ tương đối của thức ăn (dx, dy) → vector 51 phần tử
- **Label**: Khoảng cách đường đi ngắn nhất từ đầu rắn đến thức ăn (tính bằng BFS)

## File: generate_BFS_maze.py

Lõi sinh dữ liệu gồm 2 class/hàm chính:

### GridMap class
```
GridMap
├── __init__(grid_size): khởi tạo grid (0) + snake rỗng + food None
├── place_snake_and_food(snake_length=3):
│   ├── đặt head ngẫu nhiên, xây thân theo hướng ngẫu nhiên
│   ├── grid: 0=trống, 1=thân rắn, 2=thức ăn
│   └── đặt food ở ô trống ngẫu nhiên
│   → return (snake, food)
```

### bfs_distance(grid, start, goal, body_set, grid_size)
```
queue = deque([(start_r, start_c, 0)])
visited = set()
directions = [(0,1),(0,-1),(1,0),(-1,0)]

while queue:
  pop (r, c, dist)
  nếu (r,c)==goal → return dist
  với mỗi hướng:
    nếu ô hợp lệ, chưa visited, không phải thân rắn, grid[nr][nc]!=1
    → push (dist+1)
return -1  (không có đường)
```

### extract_window(grid, head, food, window_size, grid_size, body_set)
```
half = window_size // 2
r_start, c_start = head - half
window = 7x7, khởi tạo toàn 1 (chướng ngại)
Fill từng ô: nếu trong grid → lấy giá trị từ grid (0/1/2)
Flatten + [dx, dy] → return vector 51 phần tử
```

## File: create_dataset.py

```
create_dataset.py
├── generate_dataset(grid_size, num_samples):
│   for _ in range(num_samples):
│     GridMap.place_snake_and_food()
│     bfs_distance() → dist
│     if dist > 0:  → extract_window → X, y
│   return X (N, 51), y (N,)
│
├── save_dataset(X, y, grid_size):
│   shuffle + split 80/20
│   lưu X_train, y_train, X_val, y_val → data/raw/{size}/
│   lưu X_all, y_all → data/processed/{size}/
│
└── run(grid_size): gọi generate_dataset + save_dataset
```

## File: visualize_samples.py

```
visualize_samples.py
├── load X_all.npy, y_all.npy từ data/processed/{size}/
├── tái tạo window 7x7 từ features + giải mã (dx, dy)
├── plot: left = heatmap window, right = info text
├── legend: trắng=trống, đen=chướng ngại, đỏ=thức ăn
└── lưu vào results/plots/sample_{size}.png
```

## Đầu vào/Đầu ra

- **Input**: `config.py` (grid_size, num_samples, window_size)
- **Output**:
  - `data/raw/{size}/X_train.npy, y_train.npy` — train set
  - `data/raw/{size}/X_val.npy, y_val.npy` — validation set
  - `data/processed/{size}/X_all.npy, y_all.npy` — full set
  - `results/plots/sample_{size}.png` — visualization

## Kiểm tra

```bash
source venv/bin/activate
python -c "import numpy as np; d=np.load('data/raw/10x10/X_train.npy'); print(d.shape)"  # (8000, 51)
```
