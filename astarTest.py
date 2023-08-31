import networkx as nx

class Pathfinder:
    def __init__(self, dungeon):
        self.dungeon = dungeon

    def create_graph(self):
        G = nx.Graph()
        for y in range(len(self.dungeon)):
            for x in range(len(self.dungeon[y])):
                if self.dungeon[y][x] == 0:  # Only add vertices for open cells
                    G.add_node((x, y))

        # Add edges between neighboring open cells
        for y in range(len(self.dungeon)):
            for x in range(len(self.dungeon[y])):
                if (x, y) in G:
                    for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                        new_x, new_y = x + dx, y + dy
                        if (new_x, new_y) in G:
                            G.add_edge((x, y), (new_x, new_y))

        return G

    def find_path(self, start, goal):
        G = self.create_graph()
        try:
            path = nx.astar_path(G, start, goal)
            return path
        except nx.NetworkXNoPath:
            return None

# Usage
dungeon = [
    [0, 0, 1, 0],
    [0, 1, 0, 0],
    [0, 0, 0, 0]
]

pathfinder = Pathfinder(dungeon)
start = (0, 0)
goal = (3, 2)
path = pathfinder.find_path(start, goal)
print(path)  # Print the path if it exists
