# Kế hoạch chi tiết: 04_visualization

## Mục tiêu

Xây dựng giao diện đồ họa Pygame để hiển thị trực quan quá trình rắn tự chơi
với A*+ANN, kèm so sánh với A*+Manhattan.

## Ý tưởng

Một cửa sổ Pygame duy nhất, có nút bấm hoặc phím tắt để chuyển đổi chế độ:
- **Phím 1**: A* + Manhattan
- **Phím 2**: A* + ANN
- **Phím R**: Reset game
- **Phím Q**: Thoát

Thông tin hiển thị trên màn hình:
- Grid, rắn (xanh lá), thức ăn (đỏ)
- Heuristic score hiện tại (góc trên bên trái)
- Số bước đã đi
- Trạng thái: "Đang tìm đường..." / "Đã ăn!" / "Game Over"

## Các file

### 1. game_gui.py — Pygame visualization

```
game_gui.py
├── SnakeGUI class:
│   def __init__(self, grid_size):
│       pygame.init()
│       self.cell_size = CELL_SIZE  # config
│       self.screen = pygame.display.set_mode(
│           (grid_size * CELL_SIZE, grid_size * CELL_SIZE + 50))  # +50 cho info bar
│       self.clock = pygame.time.Clock()
│       self.grid_size = grid_size
│       self.game = SnakeGame(grid_size)
│       self.solver_ann = AStarSolver(grid_size, AnnHeuristic(grid_size))
│       self.solver_man = AStarSolver(grid_size, ManhattanHeuristic())
│       self.current_mode = "ANN"  # hoặc "Manhattan"
│
│   def draw_grid(self):
│       for r in range(self.grid_size):
│           for c in range(self.grid_size):
│               rect = (c*CS, r*CS, CS, CS)
│               if (r,c) in self.game.snake:
│                   pygame.draw.rect(self.screen, GREEN, rect)
│               elif (r,c) == self.game.food:
│                   pygame.draw.rect(self.screen, RED, rect)
│               else:
│                   pygame.draw.rect(self.screen, WHITE, rect)
│               pygame.draw.rect(self.screen, GRAY, rect, 1)  # grid lines
│
│   def draw_info(self):
│       # hiển thị: mode + steps + heuristic score
│       dist = heuristic.predict(head, food, body)
│       text = f"Mode: {mode} | Steps: {steps} | h = {dist:.2f}"
│       screen.blit(font.render(text, True, BLACK), (10, grid_size*CS + 10))
│
│   def run(self):
│       while running:
│           clock.tick(5)  # 5 FPS
│           handle_input()  # switch mode, reset, quit
│           if not game.done:
│               solver = solver_ann hoặc solver_man
│               path = solver.find_path(self.game.snake[0], ...)
│               if path: move snake theo path
│               else: game.done = True
│           draw_grid()
│           draw_info()
│           pygame.display.flip()
│
├── nếu __name__ == "__main__":
│   gui = SnakeGUI(20)
│   gui.run()
```

### 2. comparison_plot.py — Biểu đồ so sánh (tĩnh)

```
comparison_plot.py
├── load kết quả từ 05_evaluation (hoặc chạy benchmark ngay)
├── vẽ bar chart:
│   Trục X: Chỉ số (Win rate, Steps, Time)
│   Trục Y: Giá trị
│   Hai cột: Manhattan (xanh dương) vs ANN (xanh lá)
├── lưu vào results/plots/comparison_{size}.png
```

### 3. stats_report.py — Báo cáo thống kê

```
stats_report.py
├── đọc kết quả từ 05_evaluation/results.csv
├── tạo bảng markdown:
│   | Metric          | Manhattan | ANN      | Difference |
│   |-----------------|-----------|----------|------------|
│   | Win Rate        | 78%       | 92%      | +14%       |
│   | Avg Steps (Win) | 45.3      | 38.1     | -7.2       |
│   | Avg Time/step   | 0.8ms     | 2.3ms    | +1.5ms     |
├── ghi vào results/reports/report_{size}.md
```

## Đầu vào/Đầu ra

- **Input**:
  - `models/{size}/model.keras`
  - `config.py` (CELL_SIZE, FPS, ...)
- **Output**:
  - Cửa sổ Pygame tương tác
  - `results/plots/comparison_{size}.png`
  - `results/reports/report_{size}.md`

## Điều khiển trong game

| Phím | Chức năng |
|------|-----------|
| 1 | Chuyển sang A* + Manhattan |
| 2 | Chuyển sang A* + ANN |
| R | Reset game (rắn + thức ăn mới) |
| Q | Thoát |
