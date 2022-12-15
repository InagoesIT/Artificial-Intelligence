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

    relationships_count = 100
    relationships_path = os.path.join(".", "resources", "relationships.txt")

    parser = Parser(ontology, relationships_path)
    processed_ontology = parser.get_processed_relationships(relationships_count)
    parser.print_relationships(processed_ontology)

    quiz = Quiz(processed_ontology, relationships_count)
    quiz.run()


if __name__ == '__main__':
    main()
