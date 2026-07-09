import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import AVAILABLE_GRID_SIZES, DEFAULT_GRID_SIZE


def print_header(title):
    print("=" * 60)
    print(f"  {title}")
    print("=" * 60)


def step_01_generate_data():
    print_header("BUOC 1: SINH DU LIEU BFS")
    from importlib import import_module

    gen = import_module("data_generation.create_dataset")
    for size in AVAILABLE_GRID_SIZES:
        print(f"\n--- Dang sinh du lieu cho grid {size}x{size} ---")
        gen.run(size)
    print("Hoan tat sinh du lieu!")


def step_02_train():
    print_header("BUOC 2: HUAN LUYEN ANN")
    from importlib import import_module

    trainer = import_module("training.train")
    for size in AVAILABLE_GRID_SIZES:
        print(f"\n--- Dang huan luyen cho grid {size}x{size} ---")
        trainer.run(size)
    print("Hoan tat huan luyen!")


def step_integration():
    print_header("BUOC 3: TICH HOP A* + ANN")
    print("(Cac module da san sang, duoc goi tu buoc 4 va 5)")


def step_visualization():
    print_header("BUOC 4: TRUC QUAN HOA PYGAME")
    from importlib import import_module

    gui = import_module("visualization.game_gui")
    gui.run(DEFAULT_GRID_SIZE)


def step_evaluation():
    print_header("BUOC 5: BENCHMARK & SO SANH")
    from importlib import import_module

    bench = import_module("evaluation.benchmark")
    for size in AVAILABLE_GRID_SIZES:
        print(f"\n--- Dang benchmark cho grid {size}x{size} ---")
        bench.run(size)
    print("Hoan tat benchmark!")


def main():
    print_header("SNAKE ANN HEURISTIC PROJECT")
    print("1. Sinh du lieu BFS")
    print("2. Huan luyen ANN")
    print("3. Tich hop A* + ANN")
    print("4. Truc quan hoa Pygame")
    print("5. Benchmark & So sanh")
    print("0. Chay tat ca")
    print("=" * 60)

    choice = input("Chon buoc (0-5): ").strip()

    if choice == "1":
        step_01_generate_data()
    elif choice == "2":
        step_02_train()
    elif choice == "3":
        step_integration()
    elif choice == "4":
        step_visualization()
    elif choice == "5":
        step_evaluation()
    elif choice == "0":
        step_01_generate_data()
        step_02_train()
        step_integration()
        step_evaluation()
        q = input("\nMo giao dien Pygame? (y/n): ").strip().lower()
        if q == "y":
            step_visualization()
    else:
        print("Lua chon khong hop le!")


if __name__ == "__main__":
    main()
