# Kế hoạch chi tiết: visualization

## Mục tiêu

Xây dựng giao diện đồ họa Pygame hiển thị rắn tự chơi với A*+ANN / A*+Manhattan,
và tạo biểu đồ so sánh + báo cáo thống kê từ kết quả benchmark.

## UI Pygame — File: game_gui.py

Cửa sổ Pygame duy nhất với info bar phía dưới grid.

### Hiển thị
- **Grid**: obstacles (xám đậm), grid lines (xám)
- **Rắn**: đầu (xanh lá đậm), thân (xanh lá nhạt)
- **Thức ăn**: đỏ
- **Info bar** (dưới cùng):
  - Chế độ hiện tại (Manhattan / ANN)
  - Steps, Food eaten, Obstacles count, State (Playing / Dead)
  - ANN heuristic score và Manhattan score tại đầu rắn
  - Hướng dẫn phím tắt

### Điều khiển

| Phím | Chức năng |
|------|-----------|
| **1** | Chuyển sang A* + Manhattan |
| **2** | Chuyển sang A* + ANN |
| **R** | Reset game (obstacles mới + rắn về start) |
| **Space** | Tạm dừng / Tiếp tục |
| **Q** | Thoát |

### Luồng chính

```
run():
  while running:
    handle_events()  # phím tắt
    update()          # play_with_solver() nếu không pause/done
    draw()            # vẽ grid + obstacles + rắn + food + info
    clock.tick(FPS)
```

## So sánh — File: comparison_plot.py

```
comparison_plot.py
├── nhận results_man, results_ann, grid_size
├── bar chart với 4 metrics:
│   ├── Win Rate (%)
│   ├── Avg Steps (Win)
│   ├── Avg Steps (Lose)
│   └── Avg Time/Step (ms)
├── 2 cột: Manhattan (xanh dương) vs ANN (xanh lá)
└── lưu vào results/plots/comparison_{size}.png
```

## Thống kê — File: stats_report.py

```
stats_report.py
├── generate_md_report():
│   tạo bảng markdown → results/reports/report_{size}.md
├── generate_csv_report():
│   tạo CSV → results/reports/benchmark_{size}.csv
│
│   Metrics: Win Rate, Avg Steps (Win/Lose), Avg Time/Step
│   So sánh: Manhattan vs ANN vs Difference
```

## Đầu vào/Đầu ra

- **Input**:
  - `models/{size}/model.keras` (ANN)
  - `config.py` (CELL_SIZE, FPS, ...)
- **Output**:
  - Cửa sổ Pygame tương tác
  - `results/plots/comparison_{size}.png`
  - `results/reports/report_{size}.md` + `benchmark_{size}.csv`
