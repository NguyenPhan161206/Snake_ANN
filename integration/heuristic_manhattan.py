class ManhattanHeuristic:
    def __init__(self, grid_size=None):
        self.grid_size = grid_size

    def predict(self, head, food, body):
        return abs(head[0] - food[0]) + abs(head[1] - food[1])
