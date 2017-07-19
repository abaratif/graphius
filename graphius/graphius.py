# -*- coding: utf-8 -*-
import json
from .node import GraphiusNode


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
        self.nodes = {}  # Verticies, indexed by id
        self.parse(data)

    def parse(self, data):
        """
            Given a json styled input, fill in the graphius data structures
            First, make every node without neighbor links. Then go back,
            and add neighbor links
        """

        for node in data:
            nodeObj = GraphiusNode(id=node['id'], value=node['value'])
            self.nodes[nodeObj.id] = nodeObj

        # Create links to nieghbors:
        for node in data:
            nodeObj = self.nodes[node['id']]
            for neighborId in node['children']:
                nodeObj.addNeighbor(self.nodes[neighborId])

    # def leafPaths(self, rootId):
    #     """
    #         Given a root node Id, return an array of paths to leaf nodes
    #         The path is given as a list of node *values*
    #     """
    #     paths = []
    #     self.leafPathsHelper(rootId, paths)
    #     return paths
    #
    # def leafPathsHelper(self, rootId, paths, currPath=[]):
    #     """
    #         Given a root node Id, return an array of paths to leaf nodes
    #         The path is given as a list of node *values*
    #     """
    #     if not rootId:
    #         # Reached end of path
    #         paths.append(currPath)
    #         return
    #
    #     # Continue search
    #     if not self.nodes[rootId]['neighbors']:
    #         # Leaf node
    #         self.leafPathsHelper(
    #                             None,
    #                             paths,
    #                             currPath + [self.nodes[rootId]['value']])
    #     else:
    #         for neighbor in self.nodes[rootId]['neighbors']:
    #             self.leafPathsHelper(
    #                                 neighbor,
    #                                 paths,
    #                                 currPath + [self.nodes[rootId]['value']])

    def isSameTree(self, node1, node2):
        """
            Given two nodes, determine if they represent the same subtree
            nodeId1: id of the first node in comparsion
            nodeId2: id of second node in comparsion
        """
        # print("isSameTree call for {} and {}".format(node1.id, node2.id))

        if node1.id == node2.id:
            return True
        if node1.value == node2.value:
            # Compare children, in sorted order based on value
            node1Children = list(
                            sorted(
                                    node1.neighbors,
                                    key=lambda node:
                                    node.value))
            node2Children = list(
                            sorted(
                                    node2.neighbors,
                                    key=lambda node:
                                    node.value))

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

    # def reverseEdges(self):
    #     """ Return a graph with reversed edges, not given a root.
    #     Use a dummy root node instead, in case of multiple
    #     connected components
    #     """
    #     self.addDummyNode()
    #
    #     newNodes = {}
    #     self.reversedEdgesHelper(-1, newNodes)
    #
    #     self.nodes = newNodes
    #
    #     self.removeDummyNode()

    # def reversedEdgesHelper(self, rootId, newNodes, covered=set()):
    #     """
    #         Given a root to a graph,
    #         Reverse the directed edges of a graph
    #     """
    #
    #     if rootId not in covered:
    #         newNodes[rootId] = {
    #             'value': self.nodes[rootId]['value'],
    #             'neighbors': set()
    #         }
    #         # Base case, leaf node
    #         # if not self.nodes[rootId]['neighbors']:
    #         #
    #         #     return
    #
    #         # Recursively recurse and add all other edges
    #         for neighbor in self.nodes[rootId]['neighbors']:
    #             self.reversedEdgesHelper(neighbor, newNodes)
    #             newNodes[neighbor]['neighbors'].add(rootId)
    #         covered.add(rootId)
    #         # print("Covered is now {}".format(covered))
    #         return

    def findSameSubtrees(self):
        """ Brute force method to find all similar subtrees.
            Returns a key value pair of dupli
        """

        collapsable = {}

        for i in range(0, len(list(self.nodes))):
            for j in range(i + 1, len(list(self.nodes))):
                # Be careful, non-zero based indexing here
                if self.isSameTree(self.nodes[i + 1], self.nodes[j + 1]):
                    # Note time complexity of isSameTree
                    collapsable[self.nodes[i + 1]] = self.nodes[j + 1]

        return collapsable

    def merge(self):
        """ Function to merge all same subtrees in graph """
        collapsable = self.findSameSubtrees()

        dummy = GraphiusNode(-1, None)
        for i, node in self.nodes.items():
            dummy.addNeighbor(node)

        # Perform the merge
        self.mergeHelper(dummy, collapsable)

        # Regenerate trees
        # newNodes = self.dfs(dummy)
        # return

    def dfs(self, root):
        """ Outer function for dfs """
        result = {}
        self.dfsHelper(root, result)
        return result

    def dfsHelper(self, root, nodes):
        """ Given a root node, return a dict representing
        all nodes in that subtree. Ignore dummy nodes """
        if root.id > 0:
            nodes[root.id] = root

        for neighbor in root.neighbors:
            self.dfsHelper(neighbor, nodes)


    def mergeHelper(self, root, collapsable):
        """ Helper function for merges.
        Given a root, and a list of collapsable subtrees, for each neighbor
            if any child of the root is in the list,
                collapse it.
            Else
                recursively search all *uncollapsed* children """
        print("Checking all children of {}".format(root.id))
        for neighbor in list(root.neighbors):
            if neighbor in collapsable:
                # do the marking FIRST, very important so as to deal with
                # potential of introducing cycles.

                print("Marking {} subtree as merged, updating {}'s ref to {}'".format(
                    neighbor.id,
                    root.id,
                    collapsable[neighbor].id
                ))

                self.markMerged(neighbor)
                # Now update the ref
                root.neighbors.remove(neighbor)
                root.neighbors.add(collapsable[neighbor])
            else:
                self.mergeHelper(neighbor, collapsable)

    def markMerged(self, root):
        """ Given a root, recrusively mark that subtree
        as merged for deletion """
        root.safe = False
        for neighbor in root.neighbors:
            self.markMerged(neighbor)
        return  # Base case will skip loop and jump here (leaf node)
