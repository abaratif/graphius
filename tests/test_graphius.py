#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `graphius` package."""


import unittest

from graphius.graphius import Graphius
from graphius.node import GraphiusNode
from pprint import pprint


class TestGraphius(unittest.TestCase):
    """Tests for `graphius` package."""
    EXAMPLE1 = [
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

    EXAMPLE2 = [
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

        g = Graphius(nodes)
        # Test nodes
        assert(g.nodes[1].value == 'A')
        assert(g.nodes[2] in g.nodes[1].neighbors)

    # def test_2_isSameTree(self):
    #     """Test isSameTree for two nodes with same value,
    #     no children"""
    #     nodes = [
    #         {'id': 1, 'value': 'A', 'children': [2, 3]},
    #         {'id': 2, 'value': 'B', 'children': []},
    #         {'id': 3, 'value': 'C', 'children': [4]},
    #         {'id': 4, 'value': 'B', 'children': []}
    #     ]
    #     g = Graphius(nodes)
    #     # Nodes w/ id 2 and 4 are the same tree, when comparing values
    #     assert(g.isSameTree(2, 4))
    #
    # def test_3_isSameTree(self):
    #     """Test isSameTree for two nodes with same value,
    #     both having one child"""
    #     nodes = [
    #         {'id': 1, 'value': 'A', 'children': [2, 3]},
    #         {'id': 2, 'value': 'B', 'children': [5]},
    #         {'id': 3, 'value': 'C', 'children': [4]},
    #         {'id': 4, 'value': 'B', 'children': [5]},
    #         {'id': 5, 'value': 'D', 'children': []},
    #     ]
    #     g = Graphius(nodes)
    #     # Nodes w/ id 2 and 4 are the same tree, when comparing values
    #     assert(g.isSameTree(2, 4))
    #
    # def test_4_isSameTree(self):
    #     """Test isSameTree for two seperate, value-indentical trees
    #     """
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
    #         {'id': 12, 'value': 'F', 'children': []}
    #     ]
    #     g = Graphius(nodes)
    #     assert(g.isSameTree(1, 7))
    #
    # def test_5_isSameTree(self):
    #     """Test isSameTree for two seperate, non-indentical trees
    #     """
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
    #     g = Graphius(nodes)
    #     assert(g.isSameTree(1, 7) is False)
    #
    # def test_6_isSameTree(self):
    #     """Test isSameTree for two seperate, ndentical trees, with neighbors
    #     in different orders"""
    #     nodes = [
    #         # First subtree
    #         {'id': 1, 'value': 'A', 'children': [4, 3, 2]},  # [D, C, B]
    #         {'id': 2, 'value': 'B', 'children': []},
    #         {'id': 3, 'value': 'C', 'children': [5, 6]},
    #         {'id': 4, 'value': 'D', 'children': []},
    #         {'id': 5, 'value': 'E', 'children': []},
    #         {'id': 6, 'value': 'F', 'children': []},
    #         # Second subtree
    #         {'id': 7, 'value': 'A', 'children': [8, 9, 10]},  # [B, C, D]
    #         {'id': 8, 'value': 'B', 'children': []},
    #         {'id': 9, 'value': 'C', 'children': [11, 12]},
    #         {'id': 10, 'value': 'D', 'children': []},
    #         {'id': 11, 'value': 'E', 'children': []},
    #         {'id': 12, 'value': 'F', 'children': []}
    #     ]
    #     g = Graphius(nodes)
    #     assert(g.isSameTree(1, 7))
    #
    # def test_7_isSameTree(self):
    #     """Test isSameTree for two trees with different depths"""
    #     nodes = [
    #         # First subtree
    #         {'id': 1, 'value': 'A', 'children': [2, 3, 4]},
    #         {'id': 2, 'value': 'B', 'children': []},
    #         {'id': 3, 'value': 'C', 'children': [5]},
    #         {'id': 4, 'value': 'D', 'children': []},
    #         {'id': 5, 'value': 'E', 'children': [6]},
    #         {'id': 6, 'value': 'F', 'children': []},
    #         # Second subtree
    #         {'id': 7, 'value': 'A', 'children': [8, 9, 10]},
    #         {'id': 8, 'value': 'B', 'children': []},
    #         {'id': 9, 'value': 'C', 'children': [11]},
    #         {'id': 10, 'value': 'D', 'children': []},
    #         {'id': 11, 'value': 'E', 'children': []}
    #     ]
    #     g = Graphius(nodes)
    #     assert(g.isSameTree(1, 7) is False)
    #
    # def test_8_isSameTree(self):
    #     """ Test isSameTree on the D->F subtrees in example one """
    #     nodes = self.EXAMPLE1
    #
    #     g = Graphius(nodes)
    #     assert(g.isSameTree(5, 10) is True)
    #
    # def test_9_isSameTree(self):
    #     """ Test isSameTree on the C rooted subtrees in example one """
    #     nodes = self.EXAMPLE1
    #
    #     g = Graphius(nodes)
    #     assert(g.isSameTree(3, 9) is True)
    #
    # def test_10_isSameTree(self):
    #     """ Test isSameTree on the C rooted subtrees in example two """
    #     nodes = self.EXAMPLE2
    #
    #     g = Graphius(nodes)
    #     assert(g.isSameTree(3, 9) is False)
    #
    # def test_11_isSameTree(self):
    #     """ Test isSameTree on the D rooted subtrees in example two """
    #     nodes = self.EXAMPLE2
    #
    #     g = Graphius(nodes)
    #     assert(g.isSameTree(5, 10) is True)
    #
    # def test_12_findSameSubtrees(self):
    #     """ Test findSameSubtrees for example 2 """
    #     nodes = self.EXAMPLE2
    #
    #     g = Graphius(nodes)
    #     assert(g.findSameSubtrees() == {5: [10], 7: [12]})
    #
    # def test_13_findSameSubtrees(self):
    #     """ Test findSameSubtrees for example 1 """
    #     nodes = self.EXAMPLE1
    #
    #     g = Graphius(nodes)
    #     assert(g.findSameSubtrees() == {
    #         3: [9],
    #         4: [11],
    #         5: [10],
    #         6: [13],
    #         7: [12]})
    #
    # def test_14_leafPaths(self):
    #     """ Find leaf paths from Node 1 {1: A} in example 1 """
    #     nodes = self.EXAMPLE1
    #
    #     g = Graphius(nodes)
    #     result = [
    #                 ['A', 'B'],
    #                 ['A', 'C', 'E', 'G'],
    #                 ['A', 'C', 'D', 'F']]
    #     assert(g.leafPaths(1) == result)
    #
    # def test_15_leafPaths(self):
    #     """ Find leaf paths from Node 8 {8: H} in example 1 """
    #     nodes = self.EXAMPLE1
    #
    #     g = Graphius(nodes)
    #     result = [
    #                 ['B', 'C', 'D', 'F'],
    #                 ['B', 'C', 'E', 'G']]
    #     assert(g.leafPaths(8) == result)
    #
    # def test_16_leafPaths(self):
    #     """Find leaf path From Node 1 {1:A} in example two """
    #     nodes = self.EXAMPLE2
    #
    #     g = Graphius(nodes)
    #
    #     result = [
    #         ['H', 'C', 'D', 'F'],
    #         ['H', 'C', 'E', 'X']]
    #     assert(g.leafPaths(8) == result)
    #
    # def test_17_isSameTree(self):
    #     """ test isSameTree for two trees with common node
    #     (test fix for same node) """
    #     nodes = [
    #         {'id': 1, 'value': 'A', 'children': [2, 3]},
    #         {'id': 2, 'value': 'B', 'children': []},
    #         {'id': 3, 'value': 'C', 'children': [4, 5]},
    #         {'id': 5, 'value': 'D', 'children': [7]},
    #         {'id': 4, 'value': 'E', 'children': [6]},
    #         {'id': 6, 'value': 'G', 'children': []},
    #         {'id': 7, 'value': 'F', 'children': []},
    #         # Second half
    #         {'id': 8, 'value': 'H', 'children': [9]},
    #         {'id': 9, 'value': 'C', 'children': [5, 11]},
    #         {'id': 11, 'value': 'E', 'children': [13]},
    #         {'id': 13, 'value': 'G', 'children': []}
    #     ]
    #     g = Graphius(nodes)
    #     assert(g.isSameTree(9, 3))
    #
    # def test_18_reversedEdges(self):
    #     """ Test reversedEdges without rootId """
    #     nodes = [
    #         {'id': 1, 'value': 'A', 'children': [2, 3, 4]},
    #         {'id': 2, 'value': 'B', 'children': []},
    #         {'id': 3, 'value': 'C', 'children': [5]},
    #         {'id': 4, 'value': 'D', 'children': []},
    #         {'id': 5, 'value': 'E', 'children': [6]},
    #         {'id': 6, 'value': 'F', 'children': []}
    #     ]
    #     g = Graphius(nodes)
    #
    #     result = {
    #              1: {'neighbors': set(), 'value': 'A'},
    #              2: {'neighbors': set([1]), 'value': 'B'},
    #              3: {'neighbors': set([1]), 'value': 'C'},
    #              4: {'neighbors': set([1]), 'value': 'D'},
    #              5: {'neighbors': set([3]), 'value': 'E'},
    #              6: {'neighbors': set([5]), 'value': 'F'}}
    #     g.reverseEdges()
    #     assert(g.nodes == result)

    def test_19_node(self):
        """ Test basic creation of nodes """
        node1 = GraphiusNode(id=1, value='A')
        node2 = GraphiusNode(id=2, value='B')
        node3 = GraphiusNode(id=3, value='C')
        node4 = GraphiusNode(id=4, value='D')

        node1.addNeighbor(node2)
        node1.addNeighbor(node3)
        node1.addNeighbor(node4)

        assert(type(node1) == GraphiusNode)
        # assert(node3 in node1.neighbors)

    def test_20_node(self):
        """ Test looping over neighbors """
        node1 = GraphiusNode(id=1, value='A')
        node2 = GraphiusNode(id=2, value='B')
        node3 = GraphiusNode(id=3, value='C')
        node4 = GraphiusNode(id=4, value='D')

        node1.addNeighbor(node2)
        node1.addNeighbor(node3)
        node1.addNeighbor(node4)

        neighborIds = {node.id for node in list(node1.neighbors)}
        neighborVals = {node.value for node in list(node1.neighbors)}

        assert(neighborIds == {2, 3, 4})
        assert(neighborVals == {'B', 'C', 'D'})

    # def test_25_markMerged(self):
        # """ Test marking example 1 subtree as merged """
        # nodes = self.EXAMPLE1
        #
        # g = Graphius(nodes)
        # g.markMerged(3)
        # # pprint(g.nodes)
        # assert(g.nodes[6]['safe'] is False)



    # def test_command_line_interface(self):
    #     """Test the CLI."""
    #     runner = CliRunner()
    #     result = runner.invoke(cli.main)
    #     assert result.exit_code == 0
    #     assert 'graphius.cli.main' in result.output
    #     help_result = runner.invoke(cli.main, ['--help'])
    #     assert help_result.exit_code == 0
    #     assert '--help  Show this message and exit.' in help_result.output
