import os.path

from rdflib import Graph

from parser import Parser
from quiz import Quiz


def main():
    # for the very first run uncomment the lines
    # nltk.download('wordnet')
    # nltk.download('omw-1.4')

    ontology = Graph()
    ontology.parse(os.path.join(".", "resources", "computer.owl"))

    relationships_path = os.path.join(".", "resources", "relationships.txt")
    parser = Parser(ontology, relationships_path)
    parser.print_relationships()

    # quiz = Quiz(ontology)
    # quiz.run()


if __name__ == '__main__':
    main()
