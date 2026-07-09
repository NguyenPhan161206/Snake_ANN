# Kế hoạch chi tiết: 03_integration

## Mục tiêu

Tích hợp ANN đã huấn luyện vào thuật toán A* để thay thế heuristic Manhattan,
và xây dựng logic trò chơi Snake thuần (không GUI).

## Ý tưởng

```
A* truyền thống:   f(n) = g(n) + h(n)
                   h(n) = Manhattan(n, goal)

A* + ANN:          f(n) = g(n) + h_ann(n)
                   h_ann(n) = ANN.predict(window_7x7 + dx, dy)
```

ANN dự đoán khoảng cách còn lại — có tính đến chướng ngại vật —
nên A* sẽ tìm đường tốt hơn Manhattan (vốn mù quáng xuyên tường).

## Các file

### 1. heuristic_ann.py — ANN heuristic

```
heuristic_ann.py
├── load model từ models/{size}/model.keras
├── AnnHeuristic class:
│   def __init__(self, grid_size):
│       self.model = tf.keras.models.load_model(...)
│       self.grid_size = grid_size
│
│   def predict(self, head, food, body):
│       # body = list of (r,c) — coi là chướng ngại vật
│       grid = tạo grid size x size:
│           0=trống, 1=thân rắn/tường, 2=thức ăn
│       window = extract_window(grid, head, food, W=7)
│       features = window.flatten() + [dx, dy]  → shape (51,)
│       dist = self.model.predict(features.reshape(1, -1), verbose=0)
│       return float(dist[0][0])
```

### 2. heuristic_manhattan.py — Manhattan heuristic (baseline)

```
heuristic_manhattan.py
├── ManhattanHeuristic class:
│   def predict(self, head, food, body):
│       return abs(head[0]-food[0]) + abs(head[1]-food[1])
│   (Không dùng body, không dùng mô hình — baseline thuần túy)
```

### 3. astar_solver.py — A* tổng quát

```
astar_solver.py
├── AStarSolver class:
│   def __init__(self, grid_size, heuristic):
│       # heuristic: AnnHeuristic hoặc ManhattanHeuristic
│       pass
│
│   def find_path(self, head, food, body):
│       open_set = PriorityQueue()
│       open_set.put((0 + h, head))
│       g_score = {head: 0}
│       came_from = {}
│       directions = [(0,1),(0,-1),(1,0),(-1,0)]
│
│       while not open_set.empty():
│           _, current = open_set.get()
│           if current == food:
│               return reconstruct_path(came_from, current)
│           for dr, dc in directions:
│               nr, nc = current[0]+dr, current[1]+dc
│               if không hợp lệ (ra ngoài hoặc body):
│                   continue
│               tentative_g = g_score[current] + 1
│               neighbor = (nr, nc)
│               if tentative_g < g_score.get(neighbor, inf):
│                   g_score[neighbor] = tentative_g
│                   h = heuristic.predict(neighbor, food, body)
│                   f = tentative_g + h
│                   open_set.put((f, neighbor))
│                   came_from[neighbor] = current
│       return None  # Không tìm thấy đường
│
│   def reconstruct_path(came_from, current):
│       path = [current]
│       while current in came_from:
│           current = came_from[current]
│           path.append(current)
│       return path[::-1]
```

### 4. snake_game.py — Logic trò chơi Snake (thuần, không GUI)

```
snake_game.py
├── SnakeGame class:
│   def __init__(self, grid_size, snake_length=3):
│       self.grid_size = grid_size
│       self.snake = [(r, c), ...]  # đầu ở index 0
│       self.food = (r, c)
│       self.done = False
│       self.steps = 0
│       self.spawn_food()
│
│   def step(self, direction):
│       # direction = (dr, dc)
│       new_head = (self.snake[0][0]+dr, self.snake[0][1]+dc)
│       if new_head chạm tường hoặc thân:
│           self.done = True
│           return
│       self.snake.insert(0, new_head)
│       if new_head == self.food:
│           self.spawn_food()  # ăn được → rắn dài thêm
│       else:
│           self.snake.pop()
│
│   def play_with_astar(self, solver):
│       # dùng solver.find_path(head, food, body) mỗi bước
│       path = solver.find_path(...)
│       if path và len(path) > 1:
│           next_step = path[1]  # ô kế tiếp
│           direction = (next_step[0]-head[0], next_step[1]-head[1])
│           self.step(direction)
│       else:
│           self.done = True  # không tìm thấy đường
```

## Đầu vào/Đầu ra

- **Input**:
  - `models/{size}/model.keras` (cho ANN heuristic)
  - `config.py` (grid_size, v.v.)
- **Output**: Module để 04_visualization và 05_evaluation gọi
  - heuristic_ann.predict() → float
  - astar_solver.find_path() → list of (r,c) hoặc None
  - snake_game.step() → cập nhật trạng thái

## Lưu ý

- ANN predict hơi chậm (~2-5ms/lần). Có thể batch predict nếu cần tối ưu.
- Khi không tìm thấy đường → rắn chết. ANN heuristic giảm xác suất này so với Manhattan.