# === Cấu hình Grid & Dữ liệu ===
AVAILABLE_GRID_SIZES = [10, 20, 50]          # Các kích thước grid hỗ trợ
DEFAULT_GRID_SIZE = 50                        # Grid mặc định khi chạy UI
WINDOW_SIZE = 7                               # Cửa sổ quan sát của ANN (phải là số lẻ)
SNAKE_INITIAL_LENGTH = 3                      # Độ dài ban đầu của rắn (ô)
NUM_SAMPLES = {10: 10000, 20: 20000, 50: 50000}  # Số mẫu dữ liệu BFS cho mỗi grid
INPUT_FEATURES = WINDOW_SIZE * WINDOW_SIZE + 2  # 51 = 7x7 window + (dx, dy)

# === Huấn luyện ANN ===
EPOCHS = 100                                  # Số epoch tối đa (EarlyStopping sẽ dừng sớm)
BATCH_SIZE = 32                                # Batch size cho training
VALIDATION_SPLIT = 0.2                         # % dữ liệu dùng làm validation
PATIENCE_EARLY_STOP = 10                       # Số epoch chờ trước khi dừng nếu val_loss không giảm
LEARNING_RATE = 0.001                          # Learning rate cho Adam optimizer

# === Đánh giá & Hiển thị ===
BENCHMARK_NUM_GAMES = 50                       # Số game chạy benchmark mỗi lần
CELL_SIZE = 30                                  # Pixel mỗi ô trong Pygame
FPS = 10                                        # Frames per second cho Pygame

# === Môi trường game ===
OBSTACLE_DENSITY = 0.15                         # Tỉ lệ ô chướng ngại vật (0.15 = 15%)
SNAKE_START = (1, 1)                            # Vị trí xuất phát cố định của đầu rắn

# === Đường dẫn thư mục ===
BASE_DIR = "."                                  # Thư mục gốc dự án
DATA_RAW_DIR = "data/raw"                       # Dữ liệu thô (train/val split)
DATA_PROCESSED_DIR = "data/processed"            # Dữ liệu đã xử lý (full dataset)
MODELS_DIR = "models"                            # Lưu model đã huấn luyện
RESULTS_DIR = "results"                          # Thư mục kết quả
PLOTS_DIR = "results/plots"                      # Biểu đồ loss, scatter, comparison
LOGS_DIR = "results/logs"                        # Log kết quả benchmark (.npy)
REPORTS_DIR = "results/reports"                  # Báo cáo dạng CSV, Markdown