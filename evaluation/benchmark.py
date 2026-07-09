import os
import sys
import time
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from config import BENCHMARK_NUM_GAMES, LOGS_DIR
from integration.snake_game import SnakeGame
from integration.heuristic_ann import AnnHeuristic
from integration.heuristic_manhattan import ManhattanHeuristic
from integration.astar_solver import AStarSolver
from visualization.comparison_plot import run as plot_comparison
from visualization.stats_report import run as generate_report


def run_benchmark(grid_size, num_games=BENCHMARK_NUM_GAMES):
    print(f"\n  Benchmarking {grid_size}x{grid_size} for {num_games} games...")

    heuristic_ann = AnnHeuristic(grid_size)
    heuristic_man = ManhattanHeuristic(grid_size)
    solver_ann = AStarSolver(grid_size, heuristic_ann)
    solver_man = AStarSolver(grid_size, heuristic_man)

    results = {
        'manhattan': {'wins': 0, 'steps_win': [], 'steps_lose': [], 'times': []},
        'ann': {'wins': 0, 'steps_win': [], 'steps_lose': [], 'times': []}
    }

    max_steps = grid_size * grid_size * 4

    for mode_name, solver in [('manhattan', solver_man), ('ann', solver_ann)]:
        print(f"    Testing {mode_name}...")
        for game_id in range(num_games):
            game = SnakeGame(grid_size)
            start_time = time.time()
            steps = 0

            while not game.done and steps < max_steps:
                game.play_with_solver(solver)
                steps += 1

            elapsed = time.time() - start_time
            results[mode_name]['times'].append(elapsed)

            if game.food_eaten > 0:
                results[mode_name]['wins'] += 1
                results[mode_name]['steps_win'].append(steps)
            else:
                results[mode_name]['steps_lose'].append(steps)

            if (game_id + 1) % 10 == 0:
                print(f"      {game_id + 1}/{num_games} games done")

    return results


def analyze(results):
    def _analyze(mode_data):
        total_games = mode_data['wins'] + len(mode_data['steps_lose'])
        steps_win = mode_data['steps_win']
        steps_lose = mode_data['steps_lose']
        times = mode_data['times']
        return {
            'win_rate': (mode_data['wins'] / total_games * 100) if total_games > 0 else 0,
            'avg_steps_win': np.mean(steps_win) if steps_win else 0,
            'avg_steps_lose': np.mean(steps_lose) if steps_lose else 0,
            'avg_time_per_step': np.mean(times) / max(np.mean(steps_win) if steps_win else 1,
                                                       np.mean(steps_lose) if steps_lose else 1)
            if times else 0,
            'steps_win': steps_win,
            'steps_lose': steps_lose,
        }

    return _analyze(results['manhattan']), _analyze(results['ann'])


def print_table(results_man, results_ann, grid_size, num_games):
    print(f"\n  === KET QUA SO SANH (Grid {grid_size}x{grid_size}, {num_games} games) ===")
    print(f"  {'Metric':<25} {'Manhattan':<12} {'ANN':<12} {'Chenh lech':<12}")
    print(f"  {'-'*25} {'-'*12} {'-'*12} {'-'*12}")
    print(f"  {'Win Rate':<25} {results_man['win_rate']:<12.1f} {results_ann['win_rate']:<12.1f} "
          f"{results_ann['win_rate'] - results_man['win_rate']:<+12.1f}")
    print(f"  {'Avg Steps (Win)':<25} {results_man['avg_steps_win']:<12.1f} {results_ann['avg_steps_win']:<12.1f} "
          f"{results_ann['avg_steps_win'] - results_man['avg_steps_win']:<+12.1f}")
    print(f"  {'Avg Steps (Lose)':<25} {results_man['avg_steps_lose']:<12.1f} {results_ann['avg_steps_lose']:<12.1f} "
          f"{results_ann['avg_steps_lose'] - results_man['avg_steps_lose']:<+12.1f}")
    print(f"  {'Avg Time/Step (ms)':<25} {results_man['avg_time_per_step'] * 1000:<12.2f} "
          f"{results_ann['avg_time_per_step'] * 1000:<12.2f} "
          f"{(results_ann['avg_time_per_step'] - results_man['avg_time_per_step']) * 1000:<+12.2f}")


def run(grid_size, num_games=BENCHMARK_NUM_GAMES):
    results = run_benchmark(grid_size, num_games)
    results_man, results_ann = analyze(results)

    os.makedirs(LOGS_DIR, exist_ok=True)
    np.save(os.path.join(LOGS_DIR, f"benchmark_{grid_size}x{grid_size}.npy"), results)

    print_table(results_man, results_ann, grid_size, num_games)
    plot_comparison(results_man, results_ann, grid_size)
    generate_report(results_man, results_ann, grid_size, num_games)


if __name__ == "__main__":
    from config import AVAILABLE_GRID_SIZES
    for size in AVAILABLE_GRID_SIZES:
        run(size)
