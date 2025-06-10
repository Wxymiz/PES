class GraphMap:
    def __init__(self):
        self.waypoints = {}  # name → (x, y)
        self.graph = {}      # name → [name, name...]

    def add_waypoint(self, name, pos):
        self.waypoints[name] = pos
        self.graph[name] = []

    def connect(self, a, b):
        self.graph[a].append(b)
        self.graph[b].append(a)

    def get_position(self, name):
        return self.waypoints.get(name)

    def neighbors(self, name):
        return self.graph.get(name, [])
    
    def get_graph(self):
        return self.graph
