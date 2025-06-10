from collections import deque

class Pathfinder:
    def __init__(self, graph_map):
        self.map = graph_map

    def find_path(self, start, goal):
        visited = set()
        queue = deque([(start, [start])])
        while queue:
            current, path = queue.popleft()
            if current == goal:
                return path
            visited.add(current)
            for neighbor in self.map.neighbors(current):
                if neighbor not in visited:
                    queue.append((neighbor, path + [neighbor]))
        return []
