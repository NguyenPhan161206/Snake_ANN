import os
import sys
import pygame

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from config import CELL_SIZE, FPS, DEFAULT_GRID_SIZE
from integration.snake_game import SnakeGame
from integration.heuristic_ann import AnnHeuristic
from integration.heuristic_manhattan import ManhattanHeuristic
from integration.astar_solver import AStarSolver

COLORS = {
    'bg': (30, 30, 30),
    'grid': (50, 50, 50),
    'obstacle': (70, 60, 50),
    'snake_head': (0, 200, 0),
    'snake_body': (0, 150, 0),
    'food': (255, 50, 50),
    'text': (255, 255, 255),
    'info_bg': (20, 20, 20),
    'active': (0, 255, 100),
    'inactive': (150, 150, 150),
}


class SnakeGUI:
    def __init__(self, grid_size):
        self.grid_size = grid_size
        self.cell_size = CELL_SIZE
        self.info_height = 80
        self.width = grid_size * CELL_SIZE
        self.height = grid_size * CELL_SIZE + self.info_height

        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(f"Snake ANN Heuristic - {grid_size}x{grid_size}")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('monospace', 18)
        self.big_font = pygame.font.SysFont('monospace', 24)

        self.game = SnakeGame(grid_size)
        self.heuristic_ann = AnnHeuristic(grid_size)
        self.heuristic_man = ManhattanHeuristic(grid_size)
        self.solver_ann = AStarSolver(grid_size, self.heuristic_ann)
        self.solver_man = AStarSolver(grid_size, self.heuristic_man)
        self.current_mode = 'ann'
        self.running = True
        self.paused = False
        self.total_games = 0
        self.ann_wins = 0
        self.man_wins = 0

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    self.running = False
                elif event.key == pygame.K_r:
                    self.game.reset()
                elif event.key == pygame.K_1:
                    self.current_mode = 'manhattan'
                    self.game.reset()
                elif event.key == pygame.K_2:
                    self.current_mode = 'ann'
                    self.game.reset()
                elif event.key == pygame.K_SPACE:
                    self.paused = not self.paused

    def draw(self):
        self.screen.fill(COLORS['bg'])
        info_y = self.grid_size * self.cell_size

        mode = self.current_mode
        solver = self.solver_ann if mode == 'ann' else self.solver_man

        head = self.game.snake[0]
        food = self.game.food
        body = self.game.snake

        try:
            h_val = self.heuristic_ann.predict(head, food, body)
        except Exception:
            h_val = 0

        try:
            h_man = abs(head[0] - food[0]) + abs(head[1] - food[1])
        except Exception:
            h_man = 0

        for r in range(self.grid_size):
            for c in range(self.grid_size):
                rect = (c * self.cell_size, r * self.cell_size,
                        self.cell_size, self.cell_size)
                if (r, c) in self.game.obstacles:
                    pygame.draw.rect(self.screen, COLORS['obstacle'], rect)
                pygame.draw.rect(self.screen, COLORS['grid'], rect, 1)

        for i, (r, c) in enumerate(self.game.snake):
            rect = (c * self.cell_size, r * self.cell_size,
                    self.cell_size, self.cell_size)
            if i == 0:
                pygame.draw.rect(self.screen, COLORS['snake_head'], rect)
            else:
                pygame.draw.rect(self.screen, COLORS['snake_body'], rect)

        if self.game.food:
            r, c = self.game.food
            rect = (c * self.cell_size, r * self.cell_size,
                    self.cell_size, self.cell_size)
            pygame.draw.rect(self.screen, COLORS['food'], rect)

        mode_color = COLORS['active'] if mode == 'ann' else COLORS['inactive']
        mode_label = f"Mode: [1]Manhattan | [2]ANN (current)"
        if mode == 'ann':
            mode_label = f"Mode: [1]Manhattan | [2]ANN (current)"
        else:
            mode_label = f"Mode: [1]Manhattan (current) | [2]ANN"

        obstacles_count = len(self.game.obstacles)
        texts = [
            mode_label,
            f"Steps: {self.game.steps}  |  Obstacles: {obstacles_count}  |  State: {'WIN' if self.game.won else 'DONE' if self.game.done else 'Playing'}",
            f"ANN h={h_val:.1f}  |  Manhattan h={h_man:.1f}",
            "[R]eset  [Space]Pause  [Q]uit"
        ]

        y_offset = info_y + 5
        for text in texts:
            label = self.font.render(text, True, COLORS['text'])
            self.screen.blit(label, (10, y_offset))
            y_offset += 22

        if mode == 'ann':
            pygame.draw.rect(self.screen, COLORS['active'],
                             (self.width - 120, info_y + 5, 110, 30), 2)
            active_label = self.font.render("ANN ACTIVE", True, COLORS['active'])
            self.screen.blit(active_label, (self.width - 115, info_y + 10))

        pygame.display.flip()

    def update(self):
        if self.paused or self.game.done:
            return
        solver = self.solver_ann if self.current_mode == 'ann' else self.solver_man
        self.game.play_with_solver(solver)

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        pygame.quit()


def run(grid_size=DEFAULT_GRID_SIZE):
    gui = SnakeGUI(grid_size)
    gui.run()


if __name__ == "__main__":
    run()
