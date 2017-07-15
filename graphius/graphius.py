# -*- coding: utf-8 -*-
import json


class Graphius(object):
    """
        A class representing a graph.
        nodes:
            a dictionary holding data on nodes, indexed by node id
        mapping:
            a dictionary indexed by node value,
            containing a set of node ids
    """
    def __init__(self, data):
        self.data = data
        self.nodes = {}
        self.mapping = {}
        self.parse()

    def parse(self):
        """
            Given a json styled input, fill in the graphius data structures
        """
        for node in self.data:
            # Add the node data to nodes dict
            self.nodes[node['id']] = {
                'value': node['value'],
                'neighbors': set(node['children'])
            }
            # If no previous entry in mapping dict, create empty set
            if node['value'] not in self.mapping:
                self.mapping[node['value']] = set()
            self.mapping[node['value']].add(node['id'])

    def isSameTree(self, nodeId1, nodeId2):
        """
            Given two nodes, determine if they represent the same subtree
            nodeId1: id of the first node in comparsion
            nodeId2: id of second node in comparsion
        """
        # print("isSameTree call for IDs {} and {}".format(nodeId1, nodeId2))
        if self.nodes[nodeId1]['value'] == self.nodes[nodeId2]['value']:
            # Compare children, in sorted order based on value
            node1Children = list(
                            sorted(
                                    self.nodes[nodeId1]['neighbors'],
                                    key=lambda node:
                                    self.nodes[node]['value']))
            node2Children = list(
                            sorted(
                                    self.nodes[nodeId2]['neighbors'],
                                    key=lambda node:
                                    self.nodes[node]['value']))

            if len(node1Children) == len(node2Children):
                # For identical trees, A list of nieghbors
                # in sorted (based on value) order:
                # Should have same length
                # At each position, values are same (verify recursively)\
                for i in range(len(node1Children)):
                    if not self.isSameTree(node1Children[i], node2Children[i]):
                        return False
                # All neighbor pairs verified
                return True
