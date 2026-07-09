import os


def generate_md_report(results_man, results_ann, grid_size, num_games):
    report = []
    report.append(f"# Benchmark Report: Grid {grid_size}x{grid_size}")
    report.append(f"")
    report.append(f"- **Number of games**: {num_games}")
    report.append(f"")
    report.append(f"| Metric | Manhattan | ANN | Difference |")
    report.append(f"|--------|-----------|-----|------------|")
    report.append(f"| Win Rate | {results_man['win_rate']:.1f}% | {results_ann['win_rate']:.1f}% | "
                  f"{results_ann['win_rate'] - results_man['win_rate']:+.1f}% |")
    report.append(f"| Avg Steps (Win) | {results_man['avg_steps_win']:.1f} | {results_ann['avg_steps_win']:.1f} | "
                  f"{results_ann['avg_steps_win'] - results_man['avg_steps_win']:+.1f} |")
    report.append(f"| Avg Steps (Lose) | {results_man['avg_steps_lose']:.1f} | {results_ann['avg_steps_lose']:.1f} | "
                  f"{results_ann['avg_steps_lose'] - results_man['avg_steps_lose']:+.1f} |")
    report.append(f"| Avg Time/Step (ms) | {results_man['avg_time_per_step'] * 1000:.2f} | {results_ann['avg_time_per_step'] * 1000:.2f} | "
                  f"{(results_ann['avg_time_per_step'] - results_man['avg_time_per_step']) * 1000:+.2f} |")

    report_dir = os.path.join("results", "reports")
    os.makedirs(report_dir, exist_ok=True)
    out_path = os.path.join(report_dir, f"report_{grid_size}x{grid_size}.md")
    with open(out_path, "w") as f:
        f.write("\n".join(report))
    print(f"  Saved MD report: {out_path}")


def generate_csv_report(results_man, results_ann, grid_size, num_games):
    import csv
    report_dir = os.path.join("results", "reports")
    os.makedirs(report_dir, exist_ok=True)
    out_path = os.path.join(report_dir, f"benchmark_{grid_size}x{grid_size}.csv")
    with open(out_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Metric", "Manhattan", "ANN", "Difference"])
        writer.writerow(["Win Rate (%)", f"{results_man['win_rate']:.1f}",
                         f"{results_ann['win_rate']:.1f}",
                         f"{results_ann['win_rate'] - results_man['win_rate']:+.1f}"])
        writer.writerow(["Avg Steps (Win)", f"{results_man['avg_steps_win']:.1f}",
                         f"{results_ann['avg_steps_win']:.1f}",
                         f"{results_ann['avg_steps_win'] - results_man['avg_steps_win']:+.1f}"])
        writer.writerow(["Avg Steps (Lose)", f"{results_man['avg_steps_lose']:.1f}",
                         f"{results_ann['avg_steps_lose']:.1f}",
                         f"{results_ann['avg_steps_lose'] - results_man['avg_steps_lose']:+.1f}"])
        writer.writerow(["Avg Time/Step (ms)", f"{results_man['avg_time_per_step'] * 1000:.2f}",
                         f"{results_ann['avg_time_per_step'] * 1000:.2f}",
                         f"{(results_ann['avg_time_per_step'] - results_man['avg_time_per_step']) * 1000:+.2f}"])
    print(f"  Saved CSV report: {out_path}")


def run(results_man, results_ann, grid_size, num_games=50):
    generate_md_report(results_man, results_ann, grid_size, num_games)
    generate_csv_report(results_man, results_ann, grid_size, num_games)
