class GraphiusNode(object):
    """An object representing a Node """
    def __init__(self, id, value):
        self.id = id
        self.value = value
        self.neighbors = set()  # A set of other node ids, which are edges

    def addNeighbor(self, node):
        """ Given another node, add it as a neighbor """
        assert(type(node) == GraphiusNode)  # Type checking
        self.neighbors.add(node)
