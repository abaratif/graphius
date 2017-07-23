# -*- coding: utf-8 -*-
from graphius.node import GraphiusNode


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
        self.nodes = {}  # GraphiusNode objects, indexed by id
        self.childNodes = {}  # GraphiusNode objects, indexed by id
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
                self.childNodes[neighborId] = self.nodes[neighborId]

    def getNodes(self):
        """ Function to get all the nodes of the graph.
        returns a JSON style list of dicts with node data """
        result = []
        for nodeId, nodeObj in self.nodes.items():
            # Cast object to dict, exclude 'safe' attrib
            temp = {
                key: value
                for key, value in nodeObj.__dict__.items()
                if key is not 'safe'}
            # Convert neighbor node objects to ids
            temp['neighbors'] = [neighbor.id for neighbor in nodeObj.neighbors]
            result.append(temp)
        return result

    def roots(self):
        """ Return a set of root nodes of the graph """
        return {
                nodeObj for nodeId, nodeObj
                in self.nodes.items()
                if nodeId not in self.childNodes}

    def clean(self):
        """ Method to get rid of any nodes that are no longer part of graph """
        for nodeId in list(self.nodes.keys()):
            if not self.nodes[nodeId].safe:
                del self.nodes[nodeId]

    def postOrderMerge(self):
        """ Funciton to merge subtrees using helper below """

        seen = {}
        roots = self.roots()

        # Run the merge starting at each root. Note that seen
        # is presisted throughout.
        for root in roots:
            self.postOrderMergeHelper(root, seen)

        # Clean out any dead nodes
        self.clean()

    def postOrderMergeHelper(self, root, seen):
        """ Given a root node and a dict of seen nodes,
        recursively traverse all children.
        If a recursive call returns a different child,
        update that reference in the nieghbors set.
        Finally, if another node that is equiv (same value and neigbhors)
        as root has been seen, update the seen dict
        """

        # Check if each neighbor is collapsible
        for neighbor in list(root.neighbors):
            resolvedNeighbor = self.postOrderMergeHelper(neighbor, seen)

            if neighbor != resolvedNeighbor:
                # print("Updating {}s neighbor ref from {} to {}".format(
                #     root.id,
                #     neighbor.id,
                #     resolvedNeighbor.id
                # ))
                root.neighbors.remove(neighbor)
                root.neighbors.add(resolvedNeighbor)
                # Mark the old node
                neighbor.safe = False

        # Base case, no children

        resolved = self.getEquivNode(root, seen)
        # The above call either gets the same node, or another node with same
        # val and identical children

        # Update the ref in seen
        seen[resolved.value] = resolved
        return resolved

    def getEquivNode(self, root, seen):
        """
        Given a root node, and a dict of nodes,
        indexed by value
        If another node with this root's has been seen,
        and it is identical to root (Same neighbors), return it.
        Otherwise, return root """

        if root.value in seen and seen[root.value].neighbors == root.neighbors:
            return seen[root.value]
        return root

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
        newNodes = self.dfs(dummy)
        assert(-1 not in newNodes)
        self.nodes = newNodes

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
        # print("Checking all children of {}".format(root.id))
        for neighbor in list(root.neighbors):
            if neighbor in collapsable:
                # do the marking FIRST, very important so as to deal with
                # potential of introducing cycles.

                # print("Marking {} subtree as merged, updating {}'s ref to {}'".format(
                #     neighbor.id,
                #     root.id,
                #     collapsable[neighbor].id
                # ))

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
