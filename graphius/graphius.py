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
        self.nodes = {}  # Verticies
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
                'neighbors': set(node['children']),
                'safe': True
            }

    def addDummyNode(self):
        """ Add a dummy node with id -1 and an outgoing edge to all other
        nodes """

        self.nodes[-1] = {
            'value': 'dummy',
            'neighbors': set()
        }
        for nodeId in self.nodes.keys():
            if nodeId != -1:
                self.nodes[-1]['neighbors'].add(nodeId)

    def removeDummyNode(self):
        """ Remove dummy nodes added using addDummyNode """
        for nodeId in self.nodes.keys():
            if -1 in self.nodes[nodeId]['neighbors']:
                self.nodes[nodeId]['neighbors'].remove(-1)
        del self.nodes[-1]

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

    def reverseEdges(self):
        """ Return a graph with reversed edges, not given a root.
        Use a dummy root node instead, in case of multiple
        connected components
        """
        self.addDummyNode()

        newNodes = {}
        self.reversedEdgesHelper(-1, newNodes)

        self.nodes = newNodes

        self.removeDummyNode()

    def reversedEdgesHelper(self, rootId, newNodes, covered=set()):
        """
            Given a root to a graph,
            Reverse the directed edges of a graph
        """

        if rootId not in covered:
            newNodes[rootId] = {
                'value': self.nodes[rootId]['value'],
                'neighbors': set()
            }
            # Base case, leaf node
            # if not self.nodes[rootId]['neighbors']:
            #
            #     return

            # Recursively recurse and add all other edges
            for neighbor in self.nodes[rootId]['neighbors']:
                self.reversedEdgesHelper(neighbor, newNodes)
                newNodes[neighbor]['neighbors'].add(rootId)
            covered.add(rootId)
            # print("Covered is now {}".format(covered))
            return

    def findSameSubtrees(self):
        """ Brute force method to find all similar subtrees
        """

        collapsable = {}

        for i in range(0, len(self.nodes.keys())):
            for j in range(i + 1, len(self.nodes.keys())):
                if self.isSameTree(i + 1, j + 1):
                    collapsable[i + 1] = [j + 1]
        return collapsable

    def markMerged(self, rootId):
        """ Mark everything in a subtree w/ root as merged """
        self.nodes[rootId]['safe'] = False
        for neighbor in self.nodes[rootId]['neighbors']:
            self.markMerged(neighbor)

    # def mergeSubtrees(self):
    #     """ Try to merge all similar subtrees in graph"""
    #     mergePairs = self.findSameSubtrees()
    #     self.addDummyNode()
    #
    #     # The dummy node exists
    #     assert(self.nodes[-1])
    #
    #     self.mergeHelper(rootId, mergePairs)
    #
    #     self.removeDummyNode()

    # def mergeHelper(self, rootId, mergePairs):
    #     """ Helper method to recursively merge subtrees """
    #     for neighbor in self.nodes[rootId]['neighbors']:
    #         if self.nodes[neighbor]['safe']:  # if not marked for del
    #             if neighbor in mergePairs:
    #                 print("Merging... updating {}s ref from {} to {}".format(
    #                     rootId,
    #                     neighbor,
    #                     mergePairs[neighbor]
    #                 ))
    #                 # Remove ref to old subtree, and update w/ new ref
    #                 self.nodes[rootId]['neighbors'].remove(neighbor)
    #                 self.nodes[rootId]['neighbors'].add(mergePairs[neighbor])
    #                 # Recursively delete everything else
    #                 self.deleteSubtree(rootId)
    #
    #             else:
    #                 # recurse
    #                 self.mergeHelper(neighbor, mergePairs)
    #     return




    # def tryMerge(self, rootId, mergePairs):
