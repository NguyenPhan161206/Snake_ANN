import heapq
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


class AStarSolver:
    def __init__(self, grid_size, heuristic):
        self.grid_size = grid_size
        self.heuristic = heuristic
        self.directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    def precompute(self, head, food, body):
        body_set = set(body)
        if hasattr(self.heuristic, 'precompute'):
            self.heuristic.precompute(head, food, body)

    def find_path(self, head, food, body):
        self.precompute(head, food, body)
        body_set = set(body)
        start = head
        goal = food

        if start == goal:
            return [start]

        open_set = []
        heapq.heappush(open_set, (0, start))
        g_score = {start: 0}
        came_from = {}
        closed_set = set()

        iterations = 0
        max_iterations = self.grid_size * self.grid_size * 4

        while open_set and iterations < max_iterations:
            iterations += 1
            _, current = heapq.heappop(open_set)

            if current in closed_set:
                continue
            closed_set.add(current)

            if current == goal:
                return self._reconstruct_path(came_from, current)

            for dr, dc in self.directions:
                nr, nc = current[0] + dr, current[1] + dc
                neighbor = (nr, nc)

                if not (0 <= nr < self.grid_size and 0 <= nc < self.grid_size):
                    continue
                if neighbor in body_set or neighbor in closed_set:
                    continue

                tentative_g = g_score[current] + 1

                if tentative_g < g_score.get(neighbor, float('inf')):
                    g_score[neighbor] = tentative_g
                    h = self.heuristic.predict(neighbor, food, body)
                    f = tentative_g + h
                    heapq.heappush(open_set, (f, neighbor))
                    came_from[neighbor] = current

        return None

    def _reconstruct_path(self, came_from, current):
        path = [current]
        while current in came_from:
            current = came_from[current]
            path.append(current)
        return path[::-1]
