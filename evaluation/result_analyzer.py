import os
import sys
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


def analyze_benchmark_results(grid_size):
    log_path = os.path.join("results", "logs", f"benchmark_{grid_size}x{grid_size}.npy")
    if not os.path.exists(log_path):
        print(f"  No benchmark results for {grid_size}x{grid_size}. Run benchmark first.")
        return None, None

    results = np.load(log_path, allow_pickle=True).item()

    def _calc(data):
        total = data['wins'] + len(data['steps_lose'])
        return {
            'win_rate': data['wins'] / total * 100 if total > 0 else 0,
            'avg_steps_win': np.mean(data['steps_win']) if data['steps_win'] else 0,
            'avg_steps_lose': np.mean(data['steps_lose']) if data['steps_lose'] else 0,
            'avg_time_per_step': np.mean(data['times']) / max(
                np.mean(data['steps_win']) if data['steps_win'] else 1,
                np.mean(data['steps_lose']) if data['steps_lose'] else 1
            ) if data['times'] else 0,
            'steps_win': data['steps_win'],
            'steps_lose': data['steps_lose'],
        }

    return _calc(results['manhattan']), _calc(results['ann'])


def print_summary(grid_size):
    man, ann = analyze_benchmark_results(grid_size)
    if man is None:
        return
    print(f"\n  === PHAN TICH KET QUA (Grid {grid_size}x{grid_size}) ===")
    print(f"  {'Chi so':<25} {'Manhattan':<12} {'ANN':<12} {'Chenh lech':<12}")
    print(f"  {'-'*25} {'-'*12} {'-'*12} {'-'*12}")
    print(f"  {'Win Rate (%)':<25} {man['win_rate']:<12.1f} {ann['win_rate']:<12.1f} "
          f"{ann['win_rate'] - man['win_rate']:<+12.1f}")
    print(f"  {'Trung binh buoc (Thang)':<25} {man['avg_steps_win']:<12.1f} {ann['avg_steps_win']:<12.1f} "
          f"{ann['avg_steps_win'] - man['avg_steps_win']:<+12.1f}")
    print(f"  {'Trung binh buoc (Thua)':<25} {man['avg_steps_lose']:<12.1f} {ann['avg_steps_lose']:<12.1f} "
          f"{ann['avg_steps_lose'] - man['avg_steps_lose']:<+12.1f}")
    print(f"  {'Tgian TB/buoc (ms)':<25} {man['avg_time_per_step'] * 1000:<12.2f} "
          f"{ann['avg_time_per_step'] * 1000:<12.2f} "
          f"{(ann['avg_time_per_step'] - man['avg_time_per_step']) * 1000:<+12.2f}")


def run(grid_size):
    print_summary(grid_size)
