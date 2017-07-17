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
        # self.mapping = {}
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
            # TODO: Mapping dict depreciated, need to remove
            # If no previous entry in mapping dict, create empty set
            # if node['value'] not in self.mapping:
            #     self.mapping[node['value']] = set()
            # self.mapping[node['value']].add(node['id'])

    # def mergeRedundant(self):
    #     """
    #         For node values that have multiple IDs according to mapping dict,
    #         check if they represent the same subtree
    #     """
    #     for nodeValue, nodeIds in self.mapping.items():
    #         if len(nodeIds) > 0:
    #             nodeIds = list(nodeIds)
    #             for i in range(len(nodeIds)):
    #                 for j in range(i + 1, len(nodeIds)):
    #
    #                     if self.isSameTree(nodeIds[i], nodeIds[j]):
    #                         self.mergeSubtrees(nodeIds[i], nodeIds[j])
    #                         # No longer want to consider nodes at i and j

    # def mergeSubtrees(self, root1Id, root2Id):
    #     """
    #         Given roots of two identical subtrees,
    #         delete subtree at root2 and replace it with subtree at root1
    #     """
    #     # print("Call to mergeSubtrees for ids {} and {}".format(root1Id, root2Id))
    #     self.deleteTree(root2Id)
    #     # Search for any refs to root2Id, update to root1Id
    #     for nodeId, data in self.nodes.items():
    #         if root2Id in data['neighbors']:
    #             data['neighbors'].remove(root2Id)
    #             data['neighbors'].add(root1Id)

    # def deleteTree(self, rootId):
    #     """
    #         Given the root of a subtree as a node Id, delete that subtree
    #     """
    #     if rootId not in self.nodes:
    #         return
    #     # root exists in graph
    #     for neighborId in list(self.nodes[rootId]['neighbors']):
    #         # Recursively call delete operation
    #         self.deleteTree(neighborId)
    #     # Delete the current node after having deleted all children recursively
    #     rootValue = self.nodes[rootId]['value']
    #     # Remove from mappings dict
    #     # TODO: Decide if this should be removed or not
    #     # if rootValue in self.mapping:
    #     #     if rootId in self.mapping[rootValue]:
    #     #         self.mapping[rootValue].remove(rootId)
    #     del self.nodes[rootId]

    def leafPaths(self, rootId):
        """
            Given a root node Id, return an array of paths to leaf nodes
            The path is given as a list of node *values*
        """
        paths = []
        self.leafPathsHelper(rootId, paths)
        return paths

    def leafPathsHelper(self, rootId, paths, currPath=[]):
        """
            Given a root node Id, return an array of paths to leaf nodes
            The path is given as a list of node *values*
        """
        if not rootId:
            # Reached end of path
            paths.append(currPath)
            return

        # Continue search
        if not self.nodes[rootId]['neighbors']:
            # Leaf node
            self.leafPathsHelper(
                                None,
                                paths,
                                currPath + [self.nodes[rootId]['value']])
        else:
            for neighbor in self.nodes[rootId]['neighbors']:
                self.leafPathsHelper(
                                    neighbor,
                                    paths,
                                    currPath + [self.nodes[rootId]['value']])

    def isSameTree(self, nodeId1, nodeId2):
        """
            Given two nodes, determine if they represent the same subtree
            nodeId1: id of the first node in comparsion
            nodeId2: id of second node in comparsion
        """
        # print("isSameTree call for IDs {} and {}".format(nodeId1, nodeId2))
        assert(nodeId1 in self.nodes and nodeId2 in self.nodes)
        if nodeId1 == nodeId2:
            return True
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
                # At each position, values are same (verify recursively)
                for i in range(len(node1Children)):
                    if not self.isSameTree(node1Children[i], node2Children[i]):
                        return False
                # All neighbor pairs verified
                return True

    def reversedEdges(self, rootId):
        """
            Given a root to a graph,
            Reverse the directed edges of a graph
        """
        newNodes = {}
        self.reversedEdgesHelper(rootId, newNodes)
        return newNodes

    def reversedEdgesHelper(self, rootId, newNodes):
        """
            Given a root to a graph,
            Reverse the directed edges of a graph
        """

        newNodes[rootId] = {
                'value': self.nodes[rootId]['value'],
                'neighbors': set()
            }

        # Base case, leaf node
        if not self.nodes[rootId]['neighbors']:
            return

        # Recursively recurse and add all other edges
        for neighbor in self.nodes[rootId]['neighbors']:
            self.reversedEdgesHelper(neighbor, newNodes)
            newNodes[neighbor]['neighbors'].add(rootId)

    def findSameSubtrees(self):
        """ Brute force O(n^2) method to find all similar subtrees
        """

        collapsable = []

        for i in range(0, len(self.nodes.keys())):
            for j in range(i + 1, len(self.nodes.keys())):
                if self.isSameTree(i + 1, j + 1):
                    collapsable.append([i + 1, j + 1])
        return collapsable
