import os
import sys
import numpy as np
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from config import PLOTS_DIR


def plot_comparison(results_man, results_ann, grid_size):
    metrics = ['Win Rate (%)', 'Avg Steps (Win)', 'Avg Steps (Lose)', 'Avg Time/Step (ms)']
    man_values = [
        results_man['win_rate'],
        results_man['avg_steps_win'] if results_man['steps_win'] else 0,
        results_man['avg_steps_lose'] if results_man['steps_lose'] else 0,
        results_man['avg_time_per_step'] * 1000
    ]
    ann_values = [
        results_ann['win_rate'],
        results_ann['avg_steps_win'] if results_ann['steps_win'] else 0,
        results_ann['avg_steps_lose'] if results_ann['steps_lose'] else 0,
        results_ann['avg_time_per_step'] * 1000
    ]

    x = np.arange(len(metrics))
    width = 0.35

    fig, ax = plt.subplots(figsize=(10, 6))
    bars1 = ax.bar(x - width / 2, man_values, width, label='Manhattan', color='royalblue')
    bars2 = ax.bar(x + width / 2, ann_values, width, label='ANN', color='seagreen')

    ax.set_xlabel('Metrics')
    ax.set_title(f'ANN vs Manhattan Heuristic Comparison ({grid_size}x{grid_size})')
    ax.set_xticks(x)
    ax.set_xticklabels(metrics, rotation=15)
    ax.legend()
    ax.grid(True, alpha=0.3)

    for bar in bars1:
        height = bar.get_height()
        ax.annotate(f'{height:.1f}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3), textcoords="offset points",
                    ha='center', va='bottom', fontsize=9)
    for bar in bars2:
        height = bar.get_height()
        ax.annotate(f'{height:.1f}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3), textcoords="offset points",
                    ha='center', va='bottom', fontsize=9)

    plt.tight_layout()
    out_path = os.path.join(PLOTS_DIR, f"comparison_{grid_size}x{grid_size}.png")
    plt.savefig(out_path, dpi=150)
    plt.close()
    print(f"  Saved comparison plot: {out_path}")


def run(results_man, results_ann, grid_size):
    plot_comparison(results_man, results_ann, grid_size)
