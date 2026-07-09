# Kế hoạch chi tiết: 05_evaluation

## Mục tiêu

Chạy benchmark tự động để so sánh hiệu năng giữa A*+Manhattan và A*+ANN
trên nhiều game, thu thập số liệu thống kê và xuất báo cáo.

## Các chỉ số đo lường

| Chỉ số | Ý nghĩa |
|--------|----------|
| Win Rate | % số game rắn ăn được thức ăn trước khi chết |
| Avg Steps (Win) | Số bước trung bình khi rắn thắng |
| Avg Steps (Lose) | Số bước trung bình khi rắn thua |
| Max Steps | Số bước tối đa trong 1 game |
| Avg Time/Step | Thời gian trung bình mỗi bước (ms) |
| Total Time | Tổng thời gian chạy benchmark |

## Các file

### 1. benchmark.py — Chạy benchmark

```
benchmark.py
├── run_benchmark(grid_size, num_games=50):
│   results = {
│       "manhattan": {"wins":0, "steps_win":[], "steps_lose":[], "times":[]},
│       "ann":       {"wins":0, "steps_win":[], "steps_lose":[], "times":[]}
│   }
│
│   for mode, solver in [("manhattan", ManhattanSolver),
│                        ("ann", AnnSolver)]:
│       for game_id in range(num_games):
│           game = SnakeGame(grid_size)
│           start_time = time.time()
│           steps = 0
│           won = False
│
│           while not game.done and steps < MAX_STEPS:
│               path = solver.find_path(game.snake[0], game.food, game.snake)
│               if path and len(path) > 1:
│                   next_pos = path[1]
│                   direction = (next_pos[0]-head[0], next_pos[1]-head[1])
│                   game.step(direction)
│                   steps += 1
│                   if game.snake[0] == game.food:
│                       won = True
│                       break
│               else:
│                   game.done = True
│
│           elapsed = time.time() - start_time
│           lưu vào results[mode]
│
│   return results
│
├── if __name__ == "__main__":
│   for size in AVAILABLE_GRID_SIZES:
│       results = run_benchmark(size, BENCHMARK_NUM_GAMES)
│       np.save(f"results/logs/benchmark_{size}.npy", results)
```

### 2. result_analyzer.py — Phân tích kết quả

```
result_analyzer.py
├── analyze(results):
│   win_rate = wins / num_games * 100
│   avg_steps_win = mean(steps_win) nếu có thắng
│   avg_steps_lose = mean(steps_lose) nếu có thua
│   avg_time = mean(times)
│   return {
│       "win_rate": ...,
│       "avg_steps_win": ...,
│       "avg_steps_lose": ...,
│       "avg_time_per_step": ...,  # ms
│   }
│
├── print_comparison(man_results, ann_results):
│   in bảng so sánh ra console
│   vẽ bar chart (gọi comparison_plot.py)
```

### 3. export_results.py — Xuất CSV

```
export_results.py
├── export_to_csv(man_results, ann_results, grid_size):
│   import csv
│   with open(f"results/reports/benchmark_{grid_size}.csv", "w") as f:
│       writer = csv.writer(f)
│       writer.writerow(["Metric", "Manhattan", "ANN", "Difference"])
│       writer.writerow(["Win Rate", ...])
│       writer.writerow(["Avg Steps (Win)", ...])
│       writer.writerow(["Avg Steps (Lose)", ...])
│       writer.writerow(["Avg Time/Step (ms)", ...])
│
├── export_to_md(man_results, ann_results, grid_size):
│   ghi ra results/reports/report_{size}.md
```

## Đầu vào/Đầu ra

- **Input**:
  - `models/{size}/model.keras` (ANN)
  - `config.py` (BENCHMARK_NUM_GAMES)
- **Output**:
  - `results/logs/benchmark_{size}.npy` — raw data
  - `results/reports/benchmark_{size}.csv` — bảng CSV
  - `results/reports/report_{size}.md` — báo cáo markdown
  - Console: bảng so sánh

## Kịch bản mong đợi

```
=== BENCHMARK: Grid 20x20, 50 games ===
Metric              | Manhattan | ANN      | Diff
--------------------|-----------|----------|--------
Win Rate            | 78.0%     | 92.0%    | +14.0%
Avg Steps (Win)     | 45.3      | 38.1     | -7.2
Avg Steps (Lose)    | 120.6     | 95.4     | -25.2
Avg Time/Step (ms)  | 0.8       | 2.3      | +1.5
```

ANN chậm hơn mỗi bước (~2-5ms vs <1ms) nhưng thắng nhiều hơn và đi ít bước hơn.
Đây là trade-off giữa accuracy và speed — nội dung chính để báo cáo.
