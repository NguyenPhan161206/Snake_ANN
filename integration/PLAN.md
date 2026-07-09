# Kế hoạch chi tiết: integration

## Mục tiêu

Tích hợp ANN đã huấn luyện vào thuật toán A* để thay thế heuristic Manhattan,
và xây dựng logic trò chơi Snake với obstacles, fixed start, multi-food.

## Ý tưởng A* + ANN

```
A* truyền thống:   f(n) = g(n) + h(n)    với h = Manhattan(n, goal)
A* + ANN:          f(n) = g(n) + h_ann(n) với h_ann = ANN.predict(window + dx,dy)
```

ANN được gọi batch 1 lần mỗi `find_path()` qua `precompute()` — tính heuristic
cho tất cả ô trống cùng lúc, cache kết quả để A* lookup nhanh.

## File: heuristic_ann.py

```
heuristic_ann.py
├── AnnHeuristic class:
│   ├── __init__(grid_size):
│   │   load model.keras (nếu lỗi → self.model = None, fallback Manhattan)
│   │   self.cache = {}
│   │
│   ├── precompute(head, food, body):
│   │   build grid (0=empty, 1=body, 2=food)
│   │   collect tất cả ô trống (không phải body)
│   │   extract_window() cho từng ô → batch predict 1 lần
│   │   cache kết quả trong self.cache[(r,c)] = distance
│   │
│   ├── predict(head, food, body):
│   │   kiểm tra cache[(head)] → return nếu có
│   │   nếu model None hoặc không trong cache → return Manhattan
│   │
│   ├── _extract_fast(grid, head, food, body_set):
│   │   tạo window 7x7 (pad=1 ở biên) + [dx, dy]
│   │   return vector 51 features
```

## File: heuristic_manhattan.py

```
heuristic_manhattan.py
├── ManhattanHeuristic class:
│   def predict(self, head, food, body):
│       return abs(head[0]-food[0]) + abs(head[1]-food[1])
│   (Không dùng body, không dùng model)
```

## File: astar_solver.py

```
astar_solver.py
├── AStarSolver class:
│   ├── __init__(grid_size, heuristic):
│   │
│   ├── precompute(head, food, body):
│   │   gọi heuristic.precompute(head, food, body) nếu có
│   │
│   ├── find_path(head, food, body, obstacles=None):
│   │   precompute(head, food, body)
│   │   blocked = set(body) | (obstacles or set())
│   │   open_set = PriorityQueue → (f, pos)
│   │   g_score, came_from, closed_set
│   │
│   │   while open_set:
│   │     current = pop
│   │     if current == goal → reconstruct_path
│   │     for 4 neighbors:
│   │       if neighbor in blocked or closed_set → continue
│   │       h = heuristic.predict(neighbor, food, body)
│   │       f = tentative_g + h → push
│   │   return None  (không tìm thấy đường)
│   │
│   └── _reconstruct_path(came_from, current):
│       reverse từ current về start
```

## File: snake_game.py

```
snake_game.py
├── SnakeGame class:
│   ├── __init__(grid_size, snake_length=3):
│   │   snake_start = (1, 1), obstacle_density = 0.15
│   │
│   ├── reset():
│   │   snake = [], obstacles = set(), done = False
│   │   food_eaten = 0, steps = 0
│   │   _generate_obstacles() → obstacles ngẫu nhiên (trừ vùng start 2x2)
│   │   _place_snake() → đặt rắn ở (1,1) trở đi
│   │   _place_food() → food ở ô reachable từ đầu rắn
│   │
│   ├── _generate_obstacles():
│   │   if random() < OBSTACLE_DENSITY → add obstacle
│   │   trừ vùng margin=2 quanh (0,0) để rắn có chỗ xuất phát
│   │
│   ├── _place_snake():
│   │   head = (1,1), xây thân theo hướng ngẫu nhiên, tránh obstacles
│   │
│   ├── _place_food():
│   │   occupied = set(snake) | obstacles
│   │   candidates = _reachable_cells(occupied)  # BFS từ đầu rắn
│   │   chọn 1 ô ngẫu nhiên trong candidates
│   │
│   ├── _reachable_cells(occupied):
│   │   BFS từ đầu rắn → trả về tất cả ô reachable (trừ start)
│   │
│   ├── step(direction):
│   │   tính new_head
│   │   nếu ra ngoài / chạm obstacle / cắn thân → done = True
│   │   insert(new_head)
│   │   nếu ăn food → food_eaten += 1, _place_food(), không pop
│   │   nếu không ăn → pop tail
│   │   steps += 1
│   │
│   ├── play_with_solver(solver):
│   │   path = solver.find_path(head, food, snake, obstacles)
│   │   if path → step(path[1])  # di chuyển đến ô kế tiếp
│   │   else → done = True (bí đường)
```

## Lưu ý

- ANN fallback: nếu model load lỗi (segfault TF), tự động dùng Manhattan
- precompute() batch predict ~5-65ms/grid, cache cho toàn bộ A*
- obstacles được A* tôn trọng (blocked set) nhưng ANN heuristic không thấy obstacles
  (chỉ thấy thân rắn trong window) — đây là hạn chế hiện tại
