from sys import argv
import json
from graphius.graphius import Graphius
from pprint import pprint

def main(args=None):
    """ Main method for Graphius CLI """
    if len(argv) != 2:
        print("Error reading arguments")
        return

    assert(len(argv) == 2)
    FILEPATH = argv[1]

    with open(FILEPATH) as json_data:
        d = json.load(json_data)
        assert(type(d) is list)
        assert(type(d[0] is dict))

        g = Graphius(d)
        g.postOrderMerge()
        print(json.dumps(g.getNodes()))

if __name__ == "__main__":
    main()
