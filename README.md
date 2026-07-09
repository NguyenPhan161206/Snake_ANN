# Snake ANN Heuristic — AI tìm đường ngắn nhất cho rắn săn mồi

## Mô tả đề tài

Ứng dụng mạng Artificial Neural Network (ANN) để thay thế hàm heuristic truyền thống
(Manhattan distance) trong thuật toán A* cho trò chơi Snake.

Thay vì dùng công thức khoảng cách do con người định nghĩa sẵn,
ANN sẽ học từ dữ liệu để dự đoán khoảng cách thực tế từ đầu rắn đến thức ăn,
có tính đến chướng ngại vật (thân rắn, tường biên).

## Kiến trúc hệ thống

```
main.py  →  Điều phối 5 giai đoạn
│
├── 01_data_generation/   Sinh dữ liệu BFS
├── 02_training/          Huấn luyện ANN
├── 03_integration/       Tích hợp A* + ANN
├── 04_visualization/     Trực quan hóa Pygame
└── 05_evaluation/        Benchmark và thống kê
```

## Yêu cầu

- Python 3.9+
- pygame, tensorflow, numpy, matplotlib

## Cách chạy

```bash
pip install -r requirements.txt
python main.py
```

## Kết quả mong đợi

- ANN học được heuristic tốt hơn Manhattan trong môi trường có chướng ngại vật
- So sánh win rate, số bước trung bình, thời gian chạy giữa A*+Manhattan và A*+ANN
- Đồ thị loss vs epoch kiểm tra overfitting