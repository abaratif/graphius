#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `graphius` package."""


import unittest

from graphius import graphius
import pprint


class TestGraphius(unittest.TestCase):
    """Tests for `graphius` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_1_read(self):
        """Test reading in a graph from hash"""
        nodes = [
            {'id': 1, 'value': 'A', 'children': [2, 3]},
            {'id': 2, 'value': 'B', 'children': []},
            {'id': 3, 'value': 'C', 'children': [4]},
            {'id': 4, 'value': 'B', 'children': []}
        ]

        g = graphius.Graphius(nodes)
        # Test nodes
        assert(g.nodes[1]['value'] == 'A')
        # Test mappings
        assert(list(g.mapping['B']) == [2, 4])

    def test_2_isSameTree(self):
        """Test isSameTree for two nodes with same value,
        no children"""
        nodes = [
            {'id': 1, 'value': 'A', 'children': [2, 3]},
            {'id': 2, 'value': 'B', 'children': []},
            {'id': 3, 'value': 'C', 'children': [4]},
            {'id': 4, 'value': 'B', 'children': []}
        ]
        g = graphius.Graphius(nodes)
        # Nodes w/ id 2 and 4 are the same tree, when comparing values
        assert(g.isSameTree(2, 4))

    def test_3_isSameTree(self):
        """Test isSameTree for two nodes with same value,
        both having one child"""
        nodes = [
            {'id': 1, 'value': 'A', 'children': [2, 3]},
            {'id': 2, 'value': 'B', 'children': [5]},
            {'id': 3, 'value': 'C', 'children': [4]},
            {'id': 4, 'value': 'B', 'children': [5]},
            {'id': 5, 'value': 'D', 'children': []},
        ]
        g = graphius.Graphius(nodes)
        # Nodes w/ id 2 and 4 are the same tree, when comparing values
        assert(g.isSameTree(2, 4))

    def test_4_isSameTree(self):
        """Test isSameTree for two seperate, value-indentical trees
        """
        nodes = [
            # First subtree
            {'id': 1, 'value': 'A', 'children': [2, 3, 4]},
            {'id': 2, 'value': 'B', 'children': []},
            {'id': 3, 'value': 'C', 'children': [5, 6]},
            {'id': 4, 'value': 'D', 'children': []},
            {'id': 5, 'value': 'E', 'children': []},
            {'id': 6, 'value': 'F', 'children': []},
            # Second subtree
            {'id': 7, 'value': 'A', 'children': [8, 9, 10]},
            {'id': 8, 'value': 'B', 'children': []},
            {'id': 9, 'value': 'C', 'children': [11, 12]},
            {'id': 10, 'value': 'D', 'children': []},
            {'id': 11, 'value': 'E', 'children': []},
            {'id': 12, 'value': 'F', 'children': []}
        ]
        g = graphius.Graphius(nodes)
        assert(g.isSameTree(1, 7))

    def test_5_isSameTree(self):
        """Test isSameTree for two seperate, non-indentical trees
        """
        nodes = [
            # First subtree
            {'id': 1, 'value': 'A', 'children': [2, 3, 4]},
            {'id': 2, 'value': 'B', 'children': []},
            {'id': 3, 'value': 'C', 'children': [5, 6]},
            {'id': 4, 'value': 'D', 'children': []},
            {'id': 5, 'value': 'E', 'children': []},
            {'id': 6, 'value': 'F', 'children': []},
            # Second subtree
            {'id': 7, 'value': 'A', 'children': [8, 9, 10]},
            {'id': 8, 'value': 'B', 'children': []},
            {'id': 9, 'value': 'C', 'children': [11, 12]},
            {'id': 10, 'value': 'D', 'children': []},
            {'id': 11, 'value': 'E', 'children': []},
            {'id': 12, 'value': 'Z', 'children': []}
        ]
        g = graphius.Graphius(nodes)
        assert(g.isSameTree(1, 7) is False)

    def test_6_isSameTree(self):
        """Test isSameTree for two seperate, ndentical trees, with neighbors
        in different orders"""
        nodes = [
            # First subtree
            {'id': 1, 'value': 'A', 'children': [4, 3, 2]},  # [D, C, B]
            {'id': 2, 'value': 'B', 'children': []},
            {'id': 3, 'value': 'C', 'children': [5, 6]},
            {'id': 4, 'value': 'D', 'children': []},
            {'id': 5, 'value': 'E', 'children': []},
            {'id': 6, 'value': 'F', 'children': []},
            # Second subtree
            {'id': 7, 'value': 'A', 'children': [8, 9, 10]},  # [B, C, D]
            {'id': 8, 'value': 'B', 'children': []},
            {'id': 9, 'value': 'C', 'children': [11, 12]},
            {'id': 10, 'value': 'D', 'children': []},
            {'id': 11, 'value': 'E', 'children': []},
            {'id': 12, 'value': 'F', 'children': []}
        ]
        g = graphius.Graphius(nodes)
        assert(g.isSameTree(1, 7))

    def test_7_isSameTree(self):
        """Test isSameTree for two trees with different depths"""
        nodes = [
            # First subtree
            {'id': 1, 'value': 'A', 'children': [2, 3, 4]},
            {'id': 2, 'value': 'B', 'children': []},
            {'id': 3, 'value': 'C', 'children': [5]},
            {'id': 4, 'value': 'D', 'children': []},
            {'id': 5, 'value': 'E', 'children': [6]},
            {'id': 6, 'value': 'F', 'children': []},
            # Second subtree
            {'id': 7, 'value': 'A', 'children': [8, 9, 10]},
            {'id': 8, 'value': 'B', 'children': []},
            {'id': 9, 'value': 'C', 'children': [11]},
            {'id': 10, 'value': 'D', 'children': []},
            {'id': 11, 'value': 'E', 'children': []}
        ]
        g = graphius.Graphius(nodes)
        assert(g.isSameTree(1, 7) is False)

    def test_8_isSameTree(self):
        """ Test isSameTree on the D->F subtrees in example one """
        nodes = [
            {'id': 1, 'value': 'A', 'children': [2, 3]},
            {'id': 2, 'value': 'B', 'children': []},
            {'id': 3, 'value': 'C', 'children': [4, 5]},
            {'id': 4, 'value': 'E', 'children': [6]},
            {'id': 5, 'value': 'D', 'children': [7]},
            {'id': 6, 'value': 'G', 'children': []},
            {'id': 7, 'value': 'F', 'children': []},
            # Second half
            {'id': 8, 'value': 'B', 'children': [9]},
            {'id': 9, 'value': 'C', 'children': [10, 11]},
            {'id': 10, 'value': 'D', 'children': [12]},
            {'id': 11, 'value': 'E', 'children': [13]},
            {'id': 12, 'value': 'F', 'children': []},
            {'id': 13, 'value': 'G', 'children': []}
        ]
        g = graphius.Graphius(nodes)
        assert(g.isSameTree(5, 10) is True)

    def test_9_isSameTree(self):
        """ Test isSameTree on the C rooted subtrees in example one """
        nodes = [
            {'id': 1, 'value': 'A', 'children': [2, 3]},
            {'id': 2, 'value': 'B', 'children': []},
            {'id': 3, 'value': 'C', 'children': [4, 5]},
            {'id': 4, 'value': 'E', 'children': [6]},
            {'id': 5, 'value': 'D', 'children': [7]},
            {'id': 6, 'value': 'G', 'children': []},
            {'id': 7, 'value': 'F', 'children': []},
            # Second half
            {'id': 8, 'value': 'B', 'children': [9]},
            {'id': 9, 'value': 'C', 'children': [10, 11]},
            {'id': 10, 'value': 'D', 'children': [12]},
            {'id': 11, 'value': 'E', 'children': [13]},
            {'id': 12, 'value': 'F', 'children': []},
            {'id': 13, 'value': 'G', 'children': []}
        ]
        g = graphius.Graphius(nodes)
        assert(g.isSameTree(3, 9) is True)

    def test_10_isSameTree(self):
        """ Test isSameTree on the C rooted subtrees in example two """
        nodes = [
            {'id': 1, 'value': 'A', 'children': [2, 3]},
            {'id': 2, 'value': 'B', 'children': []},
            {'id': 3, 'value': 'C', 'children': [4, 5]},
            {'id': 4, 'value': 'E', 'children': [6]},
            {'id': 5, 'value': 'D', 'children': [7]},
            {'id': 6, 'value': 'G', 'children': []},
            {'id': 7, 'value': 'F', 'children': []},
            # Second half
            {'id': 8, 'value': 'B', 'children': [9]},
            {'id': 9, 'value': 'C', 'children': [10, 11]},
            {'id': 10, 'value': 'D', 'children': [12]},
            {'id': 11, 'value': 'E', 'children': [13]},
            {'id': 12, 'value': 'F', 'children': []},
            {'id': 13, 'value': 'X', 'children': []}
        ]
        g = graphius.Graphius(nodes)
        assert(g.isSameTree(3, 9) is False)

    def test_11_isSameTree(self):
        """ Test isSameTree on the D rooted subtrees in example two """
        nodes = [
            {'id': 1, 'value': 'A', 'children': [2, 3]},
            {'id': 2, 'value': 'B', 'children': []},
            {'id': 3, 'value': 'C', 'children': [4, 5]},
            {'id': 4, 'value': 'E', 'children': [6]},
            {'id': 5, 'value': 'D', 'children': [7]},
            {'id': 6, 'value': 'G', 'children': []},
            {'id': 7, 'value': 'F', 'children': []},
            # Second half
            {'id': 8, 'value': 'B', 'children': [9]},
            {'id': 9, 'value': 'C', 'children': [10, 11]},
            {'id': 10, 'value': 'D', 'children': [12]},
            {'id': 11, 'value': 'E', 'children': [13]},
            {'id': 12, 'value': 'F', 'children': []},
            {'id': 13, 'value': 'X', 'children': []}
        ]
        g = graphius.Graphius(nodes)
        assert(g.isSameTree(5, 10) is True)

    def test_12_isSameTree(self):
        """ Test every pair of node IDs for example 2 and find same subtrees. """
        nodes = [
            {'id': 1, 'value': 'A', 'children': [2, 3]},
            {'id': 2, 'value': 'B', 'children': []},
            {'id': 3, 'value': 'C', 'children': [4, 5]},
            {'id': 4, 'value': 'E', 'children': [6]},
            {'id': 5, 'value': 'D', 'children': [7]},
            {'id': 6, 'value': 'G', 'children': []},
            {'id': 7, 'value': 'F', 'children': []},
            # Second half
            {'id': 8, 'value': 'B', 'children': [9]},
            {'id': 9, 'value': 'C', 'children': [10, 11]},
            {'id': 10, 'value': 'D', 'children': [12]},
            {'id': 11, 'value': 'E', 'children': [13]},
            {'id': 12, 'value': 'F', 'children': []},
            {'id': 13, 'value': 'X', 'children': []}
        ]
        g = graphius.Graphius(nodes)

        collapsable = set()

        for i in range(0, len(g.nodes.keys())):
            for j in range(i + 1, len(g.nodes.keys())):
                if g.isSameTree(i + 1, j + 1):
                    collapsable.add((i + 1, j + 1))
        assert(collapsable == set([(5, 10), (7, 12)]))

    def test_14_isSameTree(self):
        """ Test every pair of node IDs for example 1 and find same subtrees. """
        nodes = [
            {'id': 1, 'value': 'A', 'children': [2, 3]},
            {'id': 2, 'value': 'B', 'children': []},
            {'id': 3, 'value': 'C', 'children': [4, 5]},
            {'id': 4, 'value': 'E', 'children': [6]},
            {'id': 5, 'value': 'D', 'children': [7]},
            {'id': 6, 'value': 'G', 'children': []},
            {'id': 7, 'value': 'F', 'children': []},
            # Second half
            {'id': 8, 'value': 'B', 'children': [9]},
            {'id': 9, 'value': 'C', 'children': [10, 11]},
            {'id': 10, 'value': 'D', 'children': [12]},
            {'id': 11, 'value': 'E', 'children': [13]},
            {'id': 12, 'value': 'F', 'children': []},
            {'id': 13, 'value': 'G', 'children': []}
        ]
        g = graphius.Graphius(nodes)

        collapsable = set()


        for i in range(1, len(g.nodes.keys())):
            for j in range(i + 1, len(g.nodes.keys())):
                if g.isSameTree(i + 1, j + 1):
                    collapsable.add((i + 1, j + 1))
        print(collapsable)
        assert(collapsable == set([(3, 9), (4, 11), (5, 10), (6, 13), (7, 12)]))



    # def test_8_deleteTree(self):
    #     """ Test deletion of a subtree of a single node """
    #     nodes = [
    #         # First subtree
    #         {'id': 1, 'value': 'A', 'children': []},
    #         {'id': 2, 'value': 'A', 'children': []}
    #     ]
    #     g = graphius.Graphius(nodes)
    #     assert(g.mapping['A'] == set([1, 2]))
    #     g.deleteTree(2)
    #     assert(g.mapping['A'] == set([1]))  # Verify update to mapping dict
    #     # Verify nodes dict updated
    #     result = [
    #         {'id': 1, 'value': 'A', 'children': []}
    #     ]
    #     assert(len(g.nodes) == 1)
    #
    # def test_9_deleteTree(self):
    #     """ Test deletion of a subtree of size 3 """
    #     nodes = [
    #         # First subtree
    #         {'id': 1, 'value': 'A', 'children': [2, 3, 4]},
    #         {'id': 2, 'value': 'B', 'children': []},
    #         {'id': 3, 'value': 'C', 'children': [5, 6]},
    #         {'id': 4, 'value': 'D', 'children': []},
    #         {'id': 5, 'value': 'E', 'children': []},
    #         {'id': 6, 'value': 'F', 'children': []},
    #         # Second subtree
    #         {'id': 7, 'value': 'A', 'children': [8, 9, 10]},
    #         {'id': 8, 'value': 'B', 'children': []},
    #         {'id': 9, 'value': 'C', 'children': [11, 12]},
    #         {'id': 10, 'value': 'D', 'children': []},
    #         {'id': 11, 'value': 'E', 'children': []},
    #         {'id': 12, 'value': 'Z', 'children': []}
    #     ]
    #     g = graphius.Graphius(nodes)
    #     g.deleteTree(9)
    #     assert(len(g.nodes) == 9)
    #     assert(len(g.mapping['C']) == 1)
    #
    # def test_10_mergeSubtrees(self):
    #     """ Test merging the D->F subtrees in example two """
    #     nodes = [
    #         {'id': 1, 'value': 'A', 'children': [2, 3]},
    #         {'id': 2, 'value': 'B', 'children': []},
    #         {'id': 3, 'value': 'C', 'children': [4, 5]},
    #         {'id': 4, 'value': 'E', 'children': [6]},
    #         {'id': 5, 'value': 'D', 'children': [7]},
    #         {'id': 6, 'value': 'G', 'children': []},
    #         {'id': 7, 'value': 'F', 'children': []},
    #         # Second half
    #         {'id': 8, 'value': 'B', 'children': [9]},
    #         {'id': 9, 'value': 'C', 'children': [10, 11]},
    #         {'id': 10, 'value': 'D', 'children': [12]},
    #         {'id': 11, 'value': 'E', 'children': [13]},
    #         {'id': 12, 'value': 'F', 'children': []},
    #         {'id': 13, 'value': 'X', 'children': []}
    #     ]
    #     g = graphius.Graphius(nodes)
    #     assert(len(g.nodes) == 13)
    #     assert(len(g.mapping['F']) == 2)
    #
    #     g.mergeSubtrees(10, 5)
    #
    #     assert(len(g.nodes) == 11)
    #     assert(len(g.mapping['F']) == 1)

    # def test_11_checkRedundant(self):
    #     """ Test recognizing and deleting
    #     the D->F redundant subtree in example two """
    #     nodes = [
    #         {'id': 1, 'value': 'A', 'children': [2, 3]},
    #         {'id': 2, 'value': 'B', 'children': []},
    #         {'id': 3, 'value': 'C', 'children': [4, 5]},
    #         {'id': 4, 'value': 'E', 'children': [6]},
    #         {'id': 5, 'value': 'D', 'children': [7]},
    #         {'id': 6, 'value': 'G', 'children': []},
    #         {'id': 7, 'value': 'F', 'children': []},
    #         # Second half
    #         {'id': 8, 'value': 'B', 'children': [9]},
    #         {'id': 9, 'value': 'C', 'children': [10, 11]},
    #         {'id': 10, 'value': 'D', 'children': [12]},
    #         {'id': 11, 'value': 'E', 'children': [13]},
    #         {'id': 12, 'value': 'F', 'children': []},
    #         {'id': 13, 'value': 'X', 'children': []}
    #     ]
    #     g = graphius.Graphius(nodes)
    #     assert(len(g.nodes) == 13)
    #     assert(len(g.mapping['F']) == 2)
    #
    #     g.mergeRedundant()
    #
    #     assert(len(g.nodes) == 11)
    #     assert(len(g.mapping['F']) == 1)
    #
    # def test_12_mergeSubtrees(self):
    #     """ Manually merge example 1 in multiple steps """
    #     nodes = [
    #         {'id': 1, 'value': 'A', 'children': [2, 3]},
    #         {'id': 2, 'value': 'B', 'children': []},
    #         {'id': 3, 'value': 'C', 'children': [4, 5]},
    #         {'id': 4, 'value': 'D', 'children': [6]},
    #         {'id': 5, 'value': 'E', 'children': [7]},
    #         {'id': 7, 'value': 'G', 'children': []},
    #         {'id': 6, 'value': 'F', 'children': []},
    #         # Second half
    #         {'id': 8, 'value': 'H', 'children': [9]},
    #         {'id': 9, 'value': 'C', 'children': [10, 11]},
    #         {'id': 10, 'value': 'D', 'children': [12]},
    #         {'id': 11, 'value': 'E', 'children': [13]},
    #         {'id': 12, 'value': 'F', 'children': []},
    #         {'id': 13, 'value': 'G', 'children': []}
    #     ]
    #     g = graphius.Graphius(nodes)
    #     assert(len(g.nodes) == 13)
    #     assert(len(g.mapping['F']) == 2)
    #     print("*****")
    #     pprint.pprint(g.nodes)
    #
    #     g.mergeSubtrees(7, 13)
    #     print("*****")
    #     pprint.pprint(g.nodes)
    #
    #     g.mergeSubtrees(4, 10)
    #     print("*****")
    #     pprint.pprint(g.nodes)
    #     # Issue here, graphs we want to merge now overlap
    #
    #     g.mergeSubtrees(3, 9)
    #     print("*****")
    #     pprint.pprint(g.nodes)
    #     # assert(len(g.nodes) == 8)
    #     # assert(len(g.mapping['C']) == 1)
    #     # assert(g.nodes['A']['neighbors'] == set(2, 3))
    #     # assert(g.nodes['H']['neighbors'] == set(3))
    #     # assert(len(g.mapping['F']) == 1)
    #     # assert(len(g.mapping['G']) == 1)

    def test_13_leafPaths(self):
        """ Find leaf paths from Node 1 {1: A} in example 1 """
        nodes = [
            {'id': 1, 'value': 'A', 'children': [2, 3]},
            {'id': 2, 'value': 'B', 'children': []},
            {'id': 3, 'value': 'C', 'children': [4, 5]},
            {'id': 4, 'value': 'D', 'children': [6]},
            {'id': 5, 'value': 'E', 'children': [7]},
            {'id': 7, 'value': 'G', 'children': []},
            {'id': 6, 'value': 'F', 'children': []},
            # Second half
            {'id': 8, 'value': 'H', 'children': [9]},
            {'id': 9, 'value': 'C', 'children': [10, 11]},
            {'id': 10, 'value': 'D', 'children': [12]},
            {'id': 11, 'value': 'E', 'children': [13]},
            {'id': 12, 'value': 'F', 'children': []},
            {'id': 13, 'value': 'G', 'children': []}
        ]
        g = graphius.Graphius(nodes)
        result = [
                    ['A', 'B'],
                    ['A', 'C', 'D', 'F'],
                    ['A', 'C', 'E', 'G']]
        assert(g.leafPaths(1) == result)

    def test_14_leafPaths(self):
        """ Find leaf paths from Node 8 {8: H} in example 1 """
        nodes = [
            {'id': 1, 'value': 'A', 'children': [2, 3]},
            {'id': 2, 'value': 'B', 'children': []},
            {'id': 3, 'value': 'C', 'children': [4, 5]},
            {'id': 4, 'value': 'D', 'children': [6]},
            {'id': 5, 'value': 'E', 'children': [7]},
            {'id': 7, 'value': 'G', 'children': []},
            {'id': 6, 'value': 'F', 'children': []},
            # Second half
            {'id': 8, 'value': 'H', 'children': [9]},
            {'id': 9, 'value': 'C', 'children': [10, 11]},
            {'id': 10, 'value': 'D', 'children': [12]},
            {'id': 11, 'value': 'E', 'children': [13]},
            {'id': 12, 'value': 'F', 'children': []},
            {'id': 13, 'value': 'G', 'children': []}
        ]
        g = graphius.Graphius(nodes)
        result = [
                    ['H', 'C', 'D', 'F'],
                    ['H', 'C', 'E', 'G']]
        assert(g.leafPaths(8) == result)

    def test_15_reverseEdges(self):
        """ Check reversal of directed graph """
        nodes = [
            {'id': 1, 'value': 'A', 'children': [2, 3, 4]},
            {'id': 2, 'value': 'B', 'children': []},
            {'id': 3, 'value': 'C', 'children': [5]},
            {'id': 4, 'value': 'D', 'children': []},
            {'id': 5, 'value': 'E', 'children': [6]},
            {'id': 6, 'value': 'F', 'children': []}
        ]
        g = graphius.Graphius(nodes)

        nodes = [
            {'id': 1, 'value': 'A', 'children': []},
            {'id': 2, 'value': 'B', 'children': [1]},
            {'id': 3, 'value': 'C', 'children': [1]},
            {'id': 4, 'value': 'D', 'children': [1]},
            {'id': 5, 'value': 'E', 'children': [2, 3, 4]},
            {'id': 6, 'value': 'F', 'children': [5]}
        ]
        print()
        pprint.pprint(g.reversedEdges(rootId= 1))

    def test_16_leafPaths(self):
        """Find leaf path From Node 1 {1:A} in example two """
        nodes = [
            {'id': 1, 'value': 'A', 'children': [2, 3]},
            {'id': 2, 'value': 'B', 'children': []},
            {'id': 3, 'value': 'C', 'children': [4, 5]},
            {'id': 4, 'value': 'E', 'children': [6]},
            {'id': 5, 'value': 'D', 'children': [7]},
            {'id': 6, 'value': 'G', 'children': []},
            {'id': 7, 'value': 'F', 'children': []},
            # Second half
            {'id': 8, 'value': 'H', 'children': [9]},
            {'id': 9, 'value': 'C', 'children': [10, 11]},
            {'id': 10, 'value': 'D', 'children': [12]},
            {'id': 11, 'value': 'E', 'children': [13]},
            {'id': 12, 'value': 'F', 'children': []},
            {'id': 13, 'value': 'X', 'children': []}
        ]
        g = graphius.Graphius(nodes)
        # result = [
        #             ['A', 'B'],
        #             ['A', 'C', 'E', 'G'],
        #             ['A', 'C', 'D', 'F']]
        # assert(g.leafPaths(1) == result)
        result = [
                    ['H', 'C', 'D', 'F'],
                    ['H', 'C', 'E', 'X']]
        assert(g.leafPaths(8) == result)

    # def test_command_line_interface(self):
    #     """Test the CLI."""
    #     runner = CliRunner()
    #     result = runner.invoke(cli.main)
    #     assert result.exit_code == 0
    #     assert 'graphius.cli.main' in result.output
    #     help_result = runner.invoke(cli.main, ['--help'])
    #     assert help_result.exit_code == 0
    #     assert '--help  Show this message and exit.' in help_result.output
