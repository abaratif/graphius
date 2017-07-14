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

    """
        Given a json styled input, fill in the graphius data structures
    """
    def parse(self):
        for node in self.data:
            print("NODE: id:{} value:{} neighbors:{}".format(
                node['id'],
                node['value'],
                node['children']))
            # Add the node data to nodes dict
            self.nodes[node['id']] = {
                'value': node['value'],
                'neighbors': set(node['children'])
            }
            # If no previous entry in mapping dict, create empty set
            if node['value'] not in self.mapping:
                self.mapping[node['value']] = set()
            self.mapping[node['value']].add(node['id'])
