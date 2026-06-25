# =============================================================================
# Graph.py
# Author  : Pavan Shetty H S
# Date    : September 2024
# Topic   : Graph implementation -- adjacency list, BFS, DFS
# =============================================================================
#
# Notes from Pavan:
# Graphs felt like a natural extension after trees (a tree IS technically
# a special kind of graph -- connected, no cycles). Used an adjacency
# list (dict of lists) representation instead of an adjacency matrix
# because it's more memory-efficient for sparse graphs, which most
# real-world graphs are (a social network doesn't have everyone
# connected to everyone).
# =============================================================================

from collections import deque

print("=" * 50)
print("    GRAPH DEMO (BFS & DFS)")
print("=" * 50)

class Graph:
    def __init__(self):
        self.adjacency_list = {}

    def add_vertex(self, vertex):
        if vertex not in self.adjacency_list:
            self.adjacency_list[vertex] = []

    def add_edge(self, v1, v2, directed=False):
        """By default builds an UNDIRECTED edge (both directions).
        Set directed=True for one-way connections (like a one-way street
        or 'follows' on social media)."""
        self.add_vertex(v1)
        self.add_vertex(v2)
        self.adjacency_list[v1].append(v2)
        if not directed:
            self.adjacency_list[v2].append(v1)

    def display(self):
        for vertex, neighbors in self.adjacency_list.items():
            print(f"  {vertex}: {neighbors}")

    # ---------------------
    # BFS -- Breadth First Search (explores level by level, uses a QUEUE)
    # ---------------------
    def bfs(self, start):
        """Visits nearest neighbors first, then their neighbors, etc.
        Good for finding SHORTEST PATH in an unweighted graph.
        Uses a queue (FIFO) -- directly connects to what I learned in
        Queue.py earlier this module."""
        visited = set()
        queue = deque([start])
        visited.add(start)
        order = []

        while queue:
            current = queue.popleft()
            order.append(current)
            for neighbor in self.adjacency_list.get(current, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
        return order

    # ---------------------
    # DFS -- Depth First Search (goes as deep as possible, uses a STACK
    # or recursion, which uses the CALL STACK implicitly)
    # ---------------------
    def dfs(self, start):
        """Goes deep down one path before backtracking.
        Good for detecting cycles, topological sorting, maze-solving."""
        visited = set()
        order = []
        self._dfs_recursive(start, visited, order)
        return order

    def _dfs_recursive(self, vertex, visited, order):
        visited.add(vertex)
        order.append(vertex)
        for neighbor in self.adjacency_list.get(vertex, []):
            if neighbor not in visited:
                self._dfs_recursive(neighbor, visited, order)

    def dfs_iterative(self, start):
        """Same DFS but using an EXPLICIT stack instead of recursion.
        Wrote this version after hitting RecursionError on a deep graph
        during testing -- recursion has Python's default 1000-depth
        limit, an explicit stack doesn't have that constraint."""
        visited = set()
        stack = [start]
        order = []

        while stack:
            current = stack.pop()
            if current not in visited:
                visited.add(current)
                order.append(current)
                # Add neighbors in reverse so leftmost neighbor is processed first
                for neighbor in reversed(self.adjacency_list.get(current, [])):
                    if neighbor not in visited:
                        stack.append(neighbor)
        return order

    # ---------------------
    # Shortest path using BFS (unweighted graph)
    # ---------------------
    def shortest_path(self, start, end):
        """BFS naturally finds shortest path in unweighted graphs because
        it explores level by level -- first time we REACH the target,
        that's guaranteed to be the shortest route."""
        if start == end:
            return [start]

        visited = {start}
        queue = deque([[start]])   # queue of PATHS, not just vertices

        while queue:
            path = queue.popleft()
            current = path[-1]
            for neighbor in self.adjacency_list.get(current, []):
                if neighbor == end:
                    return path + [neighbor]
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(path + [neighbor])
        return None   # no path exists

# ---------------------
# Building and testing a graph -- modeling a small social network
# ---------------------
print("\n[1] Building a graph (modeling a friend network)")
g = Graph()
g.add_edge("Pavan", "Rahul")
g.add_edge("Pavan", "Sneha")
g.add_edge("Rahul", "Arjun")
g.add_edge("Sneha", "Divya")
g.add_edge("Arjun", "Divya")
g.add_edge("Divya", "Kiran")

print("  Adjacency list:")
g.display()

print("\n[2] BFS traversal from 'Pavan'")
print(f"  BFS order: {g.bfs('Pavan')}")
print("  Notice: visits direct friends FIRST, then friends-of-friends")

print("\n[3] DFS traversal from 'Pavan'")
print(f"  DFS (recursive): {g.dfs('Pavan')}")
print(f"  DFS (iterative): {g.dfs_iterative('Pavan')}")
print("  Goes deep down one path before backtracking to explore others")

print("\n[4] Finding shortest path")
path = g.shortest_path("Pavan", "Kiran")
print(f"  Shortest path from Pavan to Kiran: {' -> '.join(path)}")
print(f"  Path length (hops): {len(path) - 1}")

# ---------------------
# Practical realization: BFS vs DFS use cases
# ---------------------
print("\n[5] When I use BFS vs DFS -- my practical takeaway")
print("""
  BFS: shortest path problems, level-order processing, "closest" anything
       (used QUEUE -- directly connects to Queue.py from this module)

  DFS: exploring all possibilities, cycle detection, maze/path-existence
       problems, topological sorting
       (used STACK or recursion -- connects to Stack.py from this module)

  Realizing both algorithms are basically "BFS = Stack.py's queue cousin,
  DFS = Stack.py's stack cousin" tied this whole module together for me
  much better than treating each data structure as an isolated topic.
""")

print("=" * 50)

# =============================================================================
# PROGRAM OUTPUT
# Run with: python3 Graph.py
# =============================================================================
#
# ==================================================
#     GRAPH DEMO (BFS & DFS)
# ==================================================
#
# [1] Building a graph (modeling a friend network)
#   Adjacency list:
#   Pavan: ['Rahul', 'Sneha']
#   Rahul: ['Pavan', 'Arjun']
#   Sneha: ['Pavan', 'Divya']
#   Arjun: ['Rahul', 'Divya']
#   Divya: ['Sneha', 'Arjun', 'Kiran']
#   Kiran: ['Divya']
#
# [2] BFS traversal from 'Pavan'
#   BFS order: ['Pavan', 'Rahul', 'Sneha', 'Arjun', 'Divya', 'Kiran']
#   Notice: visits direct friends FIRST, then friends-of-friends
#
# [3] DFS traversal from 'Pavan'
#   DFS (recursive): ['Pavan', 'Rahul', 'Arjun', 'Divya', 'Sneha', 'Kiran']
#   DFS (iterative): ['Pavan', 'Rahul', 'Arjun', 'Divya', 'Sneha', 'Kiran']
#   Goes deep down one path before backtracking to explore others
#
# [4] Finding shortest path
#   Shortest path from Pavan to Kiran: Pavan -> Sneha -> Divya -> Kiran
#   Path length (hops): 3
#
# [5] When I use BFS vs DFS -- my practical takeaway
#
#   BFS: shortest path problems, level-order processing, "closest" anything
#        (used QUEUE -- directly connects to Queue.py from this module)
#
#   DFS: exploring all possibilities, cycle detection, maze/path-existence
#        problems, topological sorting
#        (used STACK or recursion -- connects to Stack.py from this module)
#
#   Realizing both algorithms are basically "BFS = Stack.py's queue cousin,
#   DFS = Stack.py's stack cousin" tied this whole module together for me
#   much better than treating each data structure as an isolated topic.
#
# ==================================================
#
# =============================================================================

