import os.path
import pprint

import nltk
from nltk.corpus import wordnet

from rdflib import Graph


def main():
    # nltk.download('wordnet')
    # nltk.download('omw-1.4')

    g = Graph()
    g.parse(os.path.join(".", "resources", "computer.owl"))
    # index = 0
    for stmt in g:
        pprint.pprint(stmt)
        # index += 1
        # if index == 100:
        #     break

    syns = wordnet.synsets("computer")
    print(syns[0].definition())


if __name__ == '__main__':
    main()
