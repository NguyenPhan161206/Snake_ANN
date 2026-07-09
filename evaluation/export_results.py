import os
import sys
import csv
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from config import REPORTS_DIR


def export_results(grid_size):
    log_path = os.path.join("results", "logs", f"benchmark_{grid_size}x{grid_size}.npy")
    if not os.path.exists(log_path):
        print(f"  No benchmark results for {grid_size}x{grid_size}.")
        return

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
        }

    man = _calc(results['manhattan'])
    ann = _calc(results['ann'])

    os.makedirs(REPORTS_DIR, exist_ok=True)
    csv_path = os.path.join(REPORTS_DIR, f"benchmark_{grid_size}x{grid_size}.csv")
    with open(csv_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Metric", "Manhattan", "ANN", "Difference"])
        writer.writerow(["Win Rate (%)", f"{man['win_rate']:.1f}", f"{ann['win_rate']:.1f}",
                         f"{ann['win_rate'] - man['win_rate']:+.1f}"])
        writer.writerow(["Avg Steps (Win)", f"{man['avg_steps_win']:.1f}", f"{ann['avg_steps_win']:.1f}",
                         f"{ann['avg_steps_win'] - man['avg_steps_win']:+.1f}"])
        writer.writerow(["Avg Steps (Lose)", f"{man['avg_steps_lose']:.1f}", f"{ann['avg_steps_lose']:.1f}",
                         f"{ann['avg_steps_lose'] - man['avg_steps_lose']:+.1f}"])
        writer.writerow(["Avg Time/Step (ms)", f"{man['avg_time_per_step'] * 1000:.2f}",
                         f"{ann['avg_time_per_step'] * 1000:.2f}",
                         f"{(ann['avg_time_per_step'] - man['avg_time_per_step']) * 1000:+.2f}"])
    print(f"  Exported CSV: {csv_path}")


def run(grid_size):
    export_results(grid_size)
