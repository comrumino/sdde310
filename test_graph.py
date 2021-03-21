import unittest
import graph


class TestUndirectedEdge(unittest.TestCase):
    def test_post_init(self):
        nameA = 'A'
        nameB = 'B'
        weight = 1.0
        edgeAB = graph.edge_factory(nameA, nameB, weight, directed=False)
        edgeBA = graph.edge_factory(nameB, nameA, weight, directed=False)
        self.assertEqual(edgeAB, edgeBA)


#      A
# 0.5/   \ 0.5
#   B --- C      where B-C weight is 0.5
triangle = graph.Graph(name='triangle')
triangle.add_edge('a', 'b', 0.5)
triangle.add_edge('a', 'c', 0.5)
triangle.add_edge('b', 'c', 0.5)
#      A
# 0.5/   \ 2.0
#   B     C
# 0.5\   / 2.0
#      D
diamond = graph.Graph(name='diamond')
diamond.add_edge('a', 'b', 0.5)
diamond.add_edge('a', 'c', 2.0)
diamond.add_edge('b', 'd', 0.5)
diamond.add_edge('c', 'd', 2.0)
expected_diamond_str = """Graph(name='diamond')
  Neighbors of Vertex(name='a')
    (Vertex(name='b'), DirectedEdge(vertex1=Vertex(name='a'), vertex2=Vertex(name='b'), weight=0.5))
    (Vertex(name='c'), DirectedEdge(vertex1=Vertex(name='a'), vertex2=Vertex(name='c'), weight=2.0))

  Neighbors of Vertex(name='b')
    (Vertex(name='d'), DirectedEdge(vertex1=Vertex(name='b'), vertex2=Vertex(name='d'), weight=0.5))

  Neighbors of Vertex(name='c')
    (Vertex(name='d'), DirectedEdge(vertex1=Vertex(name='c'), vertex2=Vertex(name='d'), weight=2.0))

"""
#      A
# 0.5/   \ 2.0
#   B --- C      where B-C weight is 0.5 and A-D weight is 2.0
# 2.0\   / 0.5
#      D
complete_diamond = graph.Graph(name='complete-diamond')
complete_diamond.add_edge('a', 'b', 0.5)
complete_diamond.add_edge('a', 'c', 2.0)
complete_diamond.add_edge('b', 'd', 2.0)
complete_diamond.add_edge('c', 'd', 0.5)
# edges to complete
complete_diamond.add_edge('b', 'c', 0.5)
complete_diamond.add_edge('a', 'd', 2.0)
expected_complete_diamond_str = """Graph(name='complete-diamond')
  Neighbors of Vertex(name='a')
    (Vertex(name='b'), DirectedEdge(vertex1=Vertex(name='a'), vertex2=Vertex(name='b'), weight=0.5))
    (Vertex(name='c'), DirectedEdge(vertex1=Vertex(name='a'), vertex2=Vertex(name='c'), weight=2.0))
    (Vertex(name='d'), DirectedEdge(vertex1=Vertex(name='a'), vertex2=Vertex(name='d'), weight=2.0))

  Neighbors of Vertex(name='b')
    (Vertex(name='d'), DirectedEdge(vertex1=Vertex(name='b'), vertex2=Vertex(name='d'), weight=2.0))
    (Vertex(name='c'), DirectedEdge(vertex1=Vertex(name='b'), vertex2=Vertex(name='c'), weight=0.5))

  Neighbors of Vertex(name='c')
    (Vertex(name='d'), DirectedEdge(vertex1=Vertex(name='c'), vertex2=Vertex(name='d'), weight=0.5))

"""


class TestGraph(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.vtx_a = graph.Vertex('a')
        cls.vtx_b = graph.Vertex('b')
        cls.vtx_c = graph.Vertex('c')
        cls.vtx_d = graph.Vertex('d')

    def test_1_str(self):
        """Testing str will also exercise neighbors"""
        self.assertEqual(expected_diamond_str, str(diamond))
        self.assertEqual(expected_complete_diamond_str, str(complete_diamond))

    def test_2_vertex_sequence_weights(self):
        # total weight tests
        ad = (self.vtx_a, self.vtx_d)
        self.assertEqual(2.0, complete_diamond.total_vertex_sequence_weight(ad))
        acd = (self.vtx_a, self.vtx_c, self.vtx_d)
        self.assertEqual(2.5, complete_diamond.total_vertex_sequence_weight(acd))
        abcd = (self.vtx_a, self.vtx_b, self.vtx_c, self.vtx_d)
        self.assertEqual(1.5, complete_diamond.total_vertex_sequence_weight(abcd))
        # min sequence weight test
        self.assertEqual(ad, complete_diamond.min_vertex_sequence_weight(ad, acd))
        self.assertEqual(abcd, complete_diamond.min_vertex_sequence_weight(ad, abcd))

    def test_3_visited(self):
        # triangle starting vertex a
        visited = triangle.dfs_traversal(self.vtx_a, False)
        sequence = tuple([self.vtx_a, self.vtx_b])
        self.assertEqual(sequence, visited[sequence[-1]])
        sequence = tuple([self.vtx_a, self.vtx_c])
        # triangle starting vertex b
        visited = triangle.dfs_traversal(self.vtx_b, False)
        sequence = tuple([self.vtx_b, self.vtx_c])
        self.assertEqual(sequence, visited[sequence[-1]])
        # diamond starting vertex a
        visited = diamond.dfs_traversal(self.vtx_a, False)
        sequence = tuple([self.vtx_a, self.vtx_b, self.vtx_d])
        self.assertEqual(sequence, visited[sequence[-1]])
        # complete diamond starting vertex a
        visited = complete_diamond.dfs_traversal(self.vtx_a, False)
        sequence = tuple([self.vtx_a, self.vtx_b, self.vtx_c, self.vtx_d])
        self.assertEqual(sequence, visited[sequence[-1]])
        # verify dfs traversal visited datastructures are same as bfs
        dfs_recursive = complete_diamond.dfs_traversal(self.vtx_a, True)
        dfs_nonrecursive = complete_diamond.dfs_traversal(self.vtx_a, False)
        bfs = complete_diamond.bfs_traversal(self.vtx_a)
        self.assertEqual(dfs_nonrecursive, dfs_recursive)
        self.assertEqual(dfs_nonrecursive, bfs)

    def test_4_shortest_path(self):
        shortest_path_ad = complete_diamond.shortest_path('a', 'd', 'dfs-nonrecursive')
        expected_sequence = tuple([graph.Vertex('a'), graph.Vertex('b'), graph.Vertex('c'), graph.Vertex('d')])
        self.assertEqual(expected_sequence, shortest_path_ad)
