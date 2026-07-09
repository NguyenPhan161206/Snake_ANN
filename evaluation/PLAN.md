# Kế hoạch chi tiết: evaluation

## Mục tiêu

Chạy benchmark tự động so sánh A*+Manhattan vs A*+ANN trên nhiều game,
thu thập số liệu thống kê và xuất báo cáo.

## Các chỉ số đo lường

| Chỉ số | Ý nghĩa |
|--------|----------|
| Win Rate | % game rắn ăn được ≥1 mồi trước khi chết |
| Avg Steps (Win) | Số bước trung bình khi rắn có ăn được mồi |
| Avg Steps (Lose) | Số bước trung bình khi rắn chết mà không ăn được mồi nào |
| Avg Time/Step | Thời gian trung bình mỗi bước (ms) |

## File: benchmark.py

```
benchmark.py
├── run_benchmark(grid_size, num_games):
│   results = {
│     "manhattan": { wins, steps_win[], steps_lose[], times[] },
│     "ann":       { wins, steps_win[], steps_lose[], times[] }
│   }
│
│   for (mode, solver) in [("manhattan", solver_man), ("ann", solver_ann)]:
│     for game_id in range(num_games):
│       game = SnakeGame(grid_size)  # tự sinh obstacles + fixed start
│       while not game.done và steps < MAX_STEPS:
│         game.play_with_solver(solver)
│         steps += 1
│
│       if game.food_eaten > 0: → wins++, steps_win
│       else: → steps_lose
│
├── analyze(results):
│   win_rate = wins / num_games * 100
│   avg_steps_win = mean(steps_win)
│   avg_steps_lose = mean(steps_lose)
│   avg_time_per_step = mean(times) / mean(steps)
│
├── print_table(): in bảng so sánh ra console
│
└── run(grid_size):
│   chạy benchmark → analyze → print → plot → generate report
```

## File: result_analyzer.py

```
result_analyzer.py
├── analyze_benchmark_results(grid_size):
│   load results/logs/benchmark_{size}.npy
│   tính: win_rate, avg_steps_win, avg_steps_lose, avg_time_per_step
│   → return (man_results, ann_results)
│
├── print_summary(grid_size):
│   in bảng phân tích ra console
│
└── run(grid_size): gọi print_summary
```

## File: export_results.py

```
export_results.py
├── export_results(grid_size):
│   load benchmark_{size}.npy
│   tính các chỉ số
│   ghi CSV → results/reports/benchmark_{size}.csv
│
└── run(grid_size): gọi export_results
```

## Đầu vào/Đầu ra

- **Input**:
  - `models/{size}/model.keras` (ANN)
  - `config.py` (BENCHMARK_NUM_GAMES)
- **Output**:
  - `results/logs/benchmark_{size}.npy` — raw data
  - `results/reports/benchmark_{size}.csv` — bảng CSV
  - Console: bảng so sánh

## Lưu ý

- Win condition: `food_eaten > 0` (rắn ăn được ít nhất 1 mồi trước khi chết)
- Manhattan không biết obstacles → heuristic luôn là đường chim bay
- ANN heuristic biết thân rắn trong window 7x7 (nhưng không biết obstacles cố định)
