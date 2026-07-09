# Snake ANN Heuristic — AI tìm đường ngắn nhất cho rắn săn mồi

## Mô tả đề tài

Ứng dụng mạng Artificial Neural Network (ANN) để thay thế hàm heuristic truyền thống
(Manhattan distance) trong thuật toán A* cho trò chơi Snake.

Thay vì dùng công thức khoảng cách do con người định nghĩa sẵn,
ANN sẽ học từ dữ liệu để dự đoán khoảng cách thực tế từ đầu rắn đến thức ăn,
có tính đến chướng ngại vật (thân rắn, tường biên).

### Tính năng chính

- **Chướng ngại vật ngẫu nhiên**: Mỗi lần Reset, obstacles mới được sinh (15% grid)
- **Rắn xuất phát cố định**: Luôn bắt đầu ở góc trên trái (1, 1)
- **Ăn nhiều lần**: Rắn ăn được nhiều mồi, dài dần ra. Game chỉ kết thúc khi rắn chết.
- **Mồi hợp lệ**: Thức ăn chỉ xuất hiện ở ô có đường đi từ đầu rắn (BFS reachable)
- **So sánh thời gian thực**: Chuyển đổi giữa A*+Manhattan và A*+ANN bằng phím 1/2

## Kiến trúc hệ thống

```
main.py  →  Điều phối 5 giai đoạn
│
├── data_generation/    Sinh dữ liệu BFS
├── training/           Huấn luyện ANN
├── integration/        Tích hợp A* + ANN + logic game
├── visualization/      Trực quan hóa Pygame + biểu đồ
└── evaluation/         Benchmark và thống kê
```

## Yêu cầu

- Python 3.9+
- pygame, tensorflow, numpy, matplotlib, tqdm

## Cách chạy (bắt buộc làm theo đúng thứ tự)

### 1. Cài đặt môi trường

```bash
cd ~/Music/AI_project/snake_ann_project

# Tạo virtual environment (chỉ làm 1 lần)
python3 -m venv venv

# Kích hoạt venv (phải làm MỖI LẦN mở terminal mới)
source venv/bin/activate

# Cài thư viện
pip install -r requirements.txt
```

**Lưu ý**: Nếu không kích hoạt venv, bạn sẽ gặp lỗi `ModuleNotFoundError: No module named 'pygame'`.

### 2. Chạy chương trình

```bash
cd ~/Music/AI_project/snake_ann_project
source venv/bin/activate

# Chạy menu chính
python main.py
```

Menu hiện ra, chọn:
- **1** — Sinh dữ liệu BFS (đã có sẵn, không cần chạy lại)
- **2** — Huấn luyện ANN (đã có sẵn model, không cần chạy lại)
- **4** — Mở giao diện Pygame (xem rắn tự chơi)
- **5** — Benchmark so sánh ANN vs Manhattan

### 3. Điều khiển UI Pygame

| Phím | Chức năng |
|------|-----------|
| **1** | Chuyển sang A* + Manhattan |
| **2** | Chuyển sang A* + ANN |
| **R** | Reset game (obstacles mới + rắn về start) |
| **Space** | Tạm dừng / Tiếp tục |
| **Q** | Thoát |

### 4. Chạy nhanh (không cần menu)

```bash
# UI Pygame
python -c "from visualization.game_gui import run; run(10)"

# Benchmark
python -c "from evaluation.benchmark import run; run(10, 20)"
```

## Kết quả mong đợi

- ANN học được heuristic có tính đến chướng ngại vật trong cửa sổ quan sát 7x7
- So sánh win rate, số bước trung bình, thời gian chạy giữa A*+Manhattan và A*+ANN
- Đồ thị loss vs epoch kiểm tra overfitting
- Rắn tự động né obstacles + thân để đến thức ăn
