#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `graphius` package."""


import unittest

from graphius import graphius


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

    # def test_command_line_interface(self):
    #     """Test the CLI."""
    #     runner = CliRunner()
    #     result = runner.invoke(cli.main)
    #     assert result.exit_code == 0
    #     assert 'graphius.cli.main' in result.output
    #     help_result = runner.invoke(cli.main, ['--help'])
    #     assert help_result.exit_code == 0
    #     assert '--help  Show this message and exit.' in help_result.output
