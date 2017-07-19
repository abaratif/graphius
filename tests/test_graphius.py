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

    def test_1_parse(self):
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

    def test_2_isSameTree(self):
        """Test isSameTree for two nodes with same value,
        no children"""
        nodes = [
            {'id': 1, 'value': 'A', 'children': [2, 3]},
            {'id': 2, 'value': 'B', 'children': []},
            {'id': 3, 'value': 'C', 'children': [4]},
            {'id': 4, 'value': 'B', 'children': []}
        ]
        g = Graphius(nodes)
        # Nodes w/ id 2 and 4 are the same tree, when comparing values
        assert(g.isSameTree(g.nodes[2], g.nodes[4]))

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
        g = Graphius(nodes)
        # Nodes w/ id 2 and 4 are the same tree, when comparing values
        assert(g.isSameTree(g.nodes[2], g.nodes[4]))

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
        g = Graphius(nodes)
        assert(g.isSameTree(g.nodes[1], g.nodes[7]))

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
        g = Graphius(nodes)
        assert(g.isSameTree(g.nodes[1], g.nodes[7]) is False)
    #
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
        g = Graphius(nodes)
        assert(g.isSameTree(g.nodes[1], g.nodes[7]))

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
        g = Graphius(nodes)
        assert(g.isSameTree(g.nodes[1], g.nodes[7]) is False)

    def test_8_isSameTree(self):
        """ Test isSameTree on the D->F subtrees in example one """
        nodes = self.EXAMPLE1

        g = Graphius(nodes)
        assert(g.isSameTree(g.nodes[5], g.nodes[10]))

    def test_9_isSameTree(self):
        """ Test isSameTree on the C rooted subtrees in example one """
        nodes = self.EXAMPLE1

        g = Graphius(nodes)
        assert(g.isSameTree(g.nodes[3], g.nodes[9]))

    def test_10_isSameTree(self):
        """ Test isSameTree on the C rooted subtrees in example two """
        nodes = self.EXAMPLE2

        g = Graphius(nodes)
        assert(g.isSameTree(g.nodes[3], g.nodes[9]) is False)

    def test_11_isSameTree(self):
        """ Test isSameTree on the D rooted subtrees in example two """
        nodes = self.EXAMPLE2

        g = Graphius(nodes)
        assert(g.isSameTree(g.nodes[5], g.nodes[10]))

    def test_12_findSameSubtrees(self):
        """ Test findSameSubtrees for example 2 """
        nodes = self.EXAMPLE2

        g = Graphius(nodes)
        result = g.findSameSubtrees()

        assert(result[g.nodes[5]] == g.nodes[10])
        assert(result[g.nodes[7]] == g.nodes[12])

        # assert(g.findSameSubtrees() == {5: [10], 7: [12]})

    def test_13_findSameSubtrees(self):
        """ Test findSameSubtrees for example 1 """
        nodes = self.EXAMPLE1

        g = Graphius(nodes)
        result = g.findSameSubtrees()

        assert(
            result[g.nodes[3]] == g.nodes[9] and
            result[g.nodes[4]] == g.nodes[11] and
            result[g.nodes[5]] == g.nodes[10] and
            result[g.nodes[6]] == g.nodes[13] and
            result[g.nodes[7]] == g.nodes[12]
            )

    def test_14_isSameTree(self):
        """ test isSameTree for two trees with common node
        (test fix for same node) """
        nodes = [
            {'id': 1, 'value': 'A', 'children': [2, 3]},
            {'id': 2, 'value': 'B', 'children': []},
            {'id': 3, 'value': 'C', 'children': [4, 5]},
            {'id': 5, 'value': 'D', 'children': [7]},
            {'id': 4, 'value': 'E', 'children': [6]},
            {'id': 6, 'value': 'G', 'children': []},
            {'id': 7, 'value': 'F', 'children': []},
            # Second half
            {'id': 8, 'value': 'H', 'children': [9]},
            {'id': 9, 'value': 'C', 'children': [5, 11]},
            {'id': 11, 'value': 'E', 'children': [13]},
            {'id': 13, 'value': 'G', 'children': []}
        ]
        g = Graphius(nodes)
        assert(g.isSameTree(g.nodes[9], g.nodes[3]))

    def test_15_node(self):
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

    def test_16_node(self):
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
    #



    def test_17_merge(self):
        """ Test merging similar subtrees in example 1.
        Checking subtree rooted at 1:A """
        g = Graphius(self.EXAMPLE1)
        g.merge()
        treeNodesA = {
            (node.id, node.value)
            for key, node in g.dfs(g.nodes[1]).items()}
        assert(len(treeNodesA) == 7)
        assert(treeNodesA == {
            (10, 'D'), (13, 'G'), (9, 'C'), (1, 'A'),
            (11, 'E'), (12, 'F'), (2, 'B')
        })

    def test_18_merge(self):
        """ Test merging similar subtrees in example 1.
        Checking subtree rooted at 8:B"""
        g = Graphius(self.EXAMPLE1)
        g.merge()
        treeNodesB = {
            (node.id, node.value)
            for key, node in g.dfs(g.nodes[8]).items()}

        assert(treeNodesB == {
            (10, 'D'), (13, 'G'), (9, 'C'), (8, 'B'),
            (11, 'E'), (12, 'F')
        })

    def test_19_dfs(self):
        """ DFS the subtree rooted at 1:A in example 1 """
        g = Graphius(self.EXAMPLE1)

        result = {
            (node.id, node.value)
            for key, node in g.dfs(g.nodes[1]).items()}
        assert(result == {
                    (5, 'D'), (7, 'F'), (4, 'E'),
                    (2, 'B'), (3, 'C'), (6, 'G'), (1, 'A')})

    def test_20_dfs(self):
        """ DFS the subtree rooted at 3:C in example 1 """
        g = Graphius(self.EXAMPLE1)

        result = {
            (node.id, node.value)
            for key, node in g.dfs(g.nodes[3]).items()}
        assert(result == {
                    (5, 'D'), (7, 'F'), (4, 'E'),
                    (3, 'C'), (6, 'G')})

    def test_21_merge(self):
        """ Test merge on example 2. Confirm subtree rooted at 1:A """
        g = Graphius(self.EXAMPLE2)
        g.merge()

        treeNodesA = {
            (node.id, node.value)
            for key, node in g.dfs(g.nodes[1]).items()}
        assert(treeNodesA == {
                (2, 'B'), (4, 'E'), (1, 'A'), (6, 'G'),
                (10, 'D'), (12, 'F'), (3, 'C')})

    def test_22_merge(self):
        """ Test merge on example 2. Confirm subtree rooted at 1:A """
        g = Graphius(self.EXAMPLE2)
        g.merge()
        treeNodesH = {
            (node.id, node.value)
            for key, node in g.dfs(g.nodes[8]).items()}
        assert(treeNodesH == {
                (12, 'F'), (10, 'D'), (9, 'C'),
                (11, 'E'), (8, 'H'), (13, 'X')})
    # def test_21_markMerged(self):
    #     """ Test marking example 1 subtree at 3:C as merged """
    #     nodes = self.EXAMPLE1
    #
    #     g = Graphius(nodes)
    #     g.markMerged(g.nodes[3])
    #     # pprint(g.nodes)
    #     assert(g.nodes[6].safe is False)
