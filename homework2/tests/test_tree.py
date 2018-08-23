import unittest
from tree.print_tree import Node, Tree


class TestPrintTree(unittest.TestCase):
    def test1(self):
        # single node as tree
        case1 = Node(1, None, None)
        self.answer = "1\n"
        self.input = Tree.PrintTree(case1)
        assert self.input == self.answer

    def test2(self):
        # full balanced tree
        case2 = Node(1, Node(2, Node(4, None, None), Node(5, None, None)),
                     Node(3, Node(6, None, None), Node(7, None, None)))
        self.input = Tree.PrintTree(case2)
        self.answer = "|||1|||\n|2|||3|\n4|5|6|7\n"
        assert self.input == self.answer

    def test3(self):
        # all branches on the left
        case3 = Node(1, Node(2, Node(None, None, None), Node(5, None, None)),
                     Node(3, Node(4, None, None), Node(None, None, None)))
        self.input = Tree.PrintTree(case3)
        self.answer = "|||1|||\n|2|||3|\n||5|4||\n"
        assert self.input == self.answer

    def test4(self):
        # irregular tree
        case4 = Node(1, Node(2, Node(3, None, None), None),
                   Node(None, Node(None, None, None), Node(None, None, None)))
        self.input = Tree.PrintTree(case4)
        self.answer = "|||1|||\n|2|||||\n3||||||\n"
        assert self.input == self.answer