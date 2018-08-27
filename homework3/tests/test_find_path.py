import unittest
from find_path.Dijkstra import find_shortest_path
from find_path.Bellman_Ford import find_negative_cicles, find_shortest_path_Bellman


class TestTree(unittest.TestCase):

    def test1_1(self):
        # Dijkstra Algo: search for shortest path
        # test case1_1: return shortest path
        case1_1 = "case1.txt"
        self.answer = (11, ['1', '2', '4', '7'])
        (self.input1, self.input2) = find_shortest_path(case1_1, source='1', destination='7')
        assert (self.input1, self.input2) == self.answer

    def test1_2(self):
        # Dijkstra Algo: search for shortest path
        # test case1_2: no feasible path
        case1_2 = "case1.txt"
        self.answer = (None, [])
        (self.input1, self.input2) = find_shortest_path(case1_2, source='6', destination='1')
        assert (self.input1, self.input2) == self.answer

    def test2_1(self):
        # Bellman-Ford Algo: search for shortest path
        # test case2_1: return shortest path
        case2_1 = "case1.txt"
        self.answer = (11, ['1', '2', '4', '7'])
        (self.input1, self.input2) = \
            find_shortest_path_Bellman(case2_1, source='1', destination='7')
        assert (self.input1, self.input2) == self.answer

    def test2_2(self):
        # Bellman-Ford Algo: search for shortest path
        # test case2_2: no feasible path
        case2_2 = "case1.txt"
        self.answer = (None, [])
        (self.input1, self.input2) = \
            find_shortest_path_Bellman(case2_2, source='6', destination='1')
        assert (self.input1, self.input2) == self.answer

    def test3(self):
        # Bellman-Ford Algo: detect negative cycle
        case3 = "case2.txt"
        self.answer = (-2, ['5', '7', '8', '5'])
        (self.input1, self.input2) = find_negative_cicles(case3)
        assert (self.input1, self.input2) == self.answer
