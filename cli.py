# -*- coding: utf-8 -*-
import json
from graphius.graphius import Graphius
from pprint import pprint

def main(args=None):
    """ Main method for Graphius CLI """
    FILEPATH = 'examples/example3.json'
    with open(FILEPATH) as json_data:
        d = json.load(json_data)
        assert(type(d) is list)
        assert(type(d[0] is dict))

        g = Graphius(d)
        g.postOrderMerge()
        pprint(g.getNodes())

if __name__ == "__main__":
    main()
