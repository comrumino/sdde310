import logging
from collections import defaultdict, deque
import functools
from typing import Optional, Union, Generator, Tuple
from dataclasses import dataclass

logging.basicConfig(level=logging.DEBUG, format="%(message)s")
logger = logging.getLogger()


@dataclass
class Vertex:
    name: str

    def __post_init__(self):
        if not isinstance(self.name, str):
            raise TypeError(f"Vertex name must be of type str not {type(self.name)}")

    def __hash__(self):
        return hash(self.name)


@dataclass
class DirectedEdge:
    vertex1: Vertex
    vertex2: Vertex
    weight: float


@dataclass
class UndirectedEdge:
    vertex1: Vertex
    vertex2: Vertex
    weight: float

    def __post_init__(self):
        """ undirected graph has a precondition that vertex1 < vertex2 """
        if self.vertex2.name < self.vertex1.name:  # precondition not satisfied, so swap vertices
            self.vertex1, self.vertex2 = self.vertex2, self.vertex1


TypingEdge = Union[DirectedEdge, UndirectedEdge]
TypingPath = Tuple[Vertex, ...]
TypingVisited = defaultdict[Vertex, TypingPath]


def edge_factory(vertex_name1: str, vertex_name2: str, weight: float, directed: Optional[bool] = True) -> TypingEdge:
    """ factory for edges"""
    if vertex_name1 == vertex_name2:  # enforce invariant for adjacency list
        raise NotImplementedError("Edge such that vertex1 == vertex2 are not relevant")
    vertex1 = Vertex(vertex_name1)
    vertex2 = Vertex(vertex_name2)
    if directed:
        return DirectedEdge(vertex1, vertex2, weight)
    else:
        return UndirectedEdge(vertex1, vertex2, weight)


def visited_factory() -> TypingVisited:
    return defaultdict(tuple)


class Graph:
    """ adjacency lists and DFS is used for lower space complexity during search (compared to BFS and adj matrix) """

    def __init__(self, name: str, directed: Optional[bool] = True) -> None:
        self.name = name
        self.directed = directed
        self.adjacency_list: defaultdict[Vertex, dict[Vertex, TypingEdge]] = defaultdict(dict)

    def __str__(self) -> str:
        graph = f"{self.__class__.__name__}(name='{self.name}')\n"
        for vertex in self.adjacency_list:
            graph += f"  Neighbors of {vertex}\n"
            for n in self.neighbors(vertex):
                graph += f'    {n}\n'
            graph += '\n'
        return graph

    @functools.cache
    def total_vertex_sequence_weight(self, vertex_sequence):
        vertex1 = vertex_sequence[0]
        vertex2 = None
        weight = 0
        for vertex2 in vertex_sequence[1:]:
            edge = self.adjacency_list[vertex1][vertex2]
            weight += edge.weight
            vertex1 = vertex2
        return weight

    def min_vertex_sequence_weight(self, sequence1: TypingPath, sequence2: TypingPath):
        sequence1_weight = self.total_vertex_sequence_weight(sequence1)
        sequence2_weight = self.total_vertex_sequence_weight(sequence2)
        if sequence1_weight < sequence2_weight:
            return sequence1
        else:
            return sequence2

    def add_edge(self, vertex1: str, vertex2: str, weight: float, /) -> None:
        edge = edge_factory(vertex1, vertex2, weight)
        self.adjacency_list[edge.vertex1][edge.vertex2] = edge

    def neighbors(self, target_vertex: Vertex) -> Generator[tuple[Vertex, TypingEdge], None, None]:
        # yield edges where target_vertex is vertex1
        for neighbor, edge in self.adjacency_list[target_vertex].items():
            yield neighbor, edge
        # directed graphs require that we check for cases where target is vertex2
        if not self.directed:
            # yield edges where target_vertex is not vertex1 (invariant no edge where v1 == v2)
            for vertex1 in self.adjacency_list:
                if target_vertex in self.adjacency_list[vertex1]:
                    yield vertex1, self.adjacency_list[vertex1][target_vertex]

    def dfs_traversal(self, starting_vertex: Vertex, recursive: bool) -> TypingVisited:
        logger.debug(f"DFS recursive: {recursive} starting at vertex: {starting_vertex}:")
        visited = visited_factory()
        self.visit_vertex_neighbors(starting_vertex, starting_vertex, visited)
        if recursive:
            self.dfs(starting_vertex, visited)
        else:
            self.dfs_non_recursive(starting_vertex, visited)
        return visited

    def visit_vertex_neighbors(self, v: Vertex, from_vertex: Vertex, visited: TypingVisited) -> bool:
        """ returns whether or not to visit vertex neighbors

        CAVEAT: when the traversing from_vertext to vertex v, a new shortest path may be found, the case where
        a new shortest path is found we wish to visit the neighbors again.
        """
        # whether or not it is visited dictates whether or not to search the neighbors of v
        if not visited[v]:
            visited[v] = tuple([*visited[from_vertex], v])
            return True
        else:
            # previous paths to visit v consists of a sequence of vertices, replace previous sequence iff
            # the edge weights summed are greater than the current path
            new_path = tuple([*visited[from_vertex], v])
            visited[v] = self.min_vertex_sequence_weight(visited[v], new_path)
            # when visted[v] is the new path, the shortest path to it's neighbors may change
            return visited[v] == new_path

    def dfs_non_recursive(self, vertex: Vertex, visited: TypingVisited) -> None:
        s: deque[TypingEdge] = deque()
        self.push_unvisited_neighbors(vertex, s, visited)
        while s:
            edge = s.pop()
            self.push_unvisited_neighbors(edge.vertex2, s, visited)

    def push_unvisited_neighbors(self, vertex, s, visited) -> None:
        # if the vertex does not have neighbors then there is nothing to iterate
        for neighbor_vertex, edge in self.neighbors(vertex):
            if self.visit_vertex_neighbors(edge.vertex2, edge.vertex1, visited):
                s.append(edge)

    def dfs(self, vertex: Vertex, visited: TypingVisited) -> None:
        # if the vertex does not have neighbors then there is nothing to iterate
        for neighbor_vertex, edge in self.neighbors(vertex):
            if self.visit_vertex_neighbors(edge.vertex2, edge.vertex1, visited):
                self.dfs(neighbor_vertex, visited)

    def bfs_traversal(self, starting_vertex: Vertex) -> TypingVisited:
        logger.debug(f"bfs starting at vertex {starting_vertex}:")
        visited = visited_factory()
        self.visit_vertex_neighbors(starting_vertex, starting_vertex, visited)
        self.bfs(starting_vertex, visited)
        return visited

    def bfs(self, vertex: Vertex, visited: TypingVisited) -> None:
        q: deque[TypingEdge] = deque()
        self.enqueue_unvisited_neighbors(vertex, q, visited)
        while q:
            edge = q.pop()
            self.enqueue_unvisited_neighbors(edge.vertex2, q, visited)

    def enqueue_unvisited_neighbors(self, vertex: Vertex, q: deque, visited: TypingVisited) -> None:
        for neighbor_vertex, edge in self.neighbors(vertex):
            if self.visit_vertex_neighbors(edge.vertex2, edge.vertex1, visited):
                q.appendleft(edge)

    def shortest_path(self, vtx_name1: str, vtx_name2: str, search: str) -> Union[TypingPath, NotImplementedError]:
        """ returns vertex sequence from visited[v1] since it is the shortest path to v2 """
        vertex1: Vertex = Vertex(vtx_name1)
        vertex2: Vertex = Vertex(vtx_name2)
        if search == 'dfs-nonrecursive':
            visited = self.dfs_traversal(vertex1, recursive=False)
        elif search == 'dfs-recursive':
            visited = self.dfs_traversal(vertex1, recursive=True)
        elif search == 'bfs':
            visited = self.bfs_traversal(vertex1)
        else:
            return NotImplementedError('Unsupported search')
        return visited[vertex2]
