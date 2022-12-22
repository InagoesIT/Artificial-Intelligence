import os.path

from rdflib import Graph

from WordnetManager import WordnetManager
from parser import Parser
from quiz import Quiz


def main():
    # for the very first run uncomment the lines
    # nltk.download('wordnet')
    # nltk.download('omw-1.4')
    is_production_mode_on = True
    if is_production_mode_on:
        ontology = Graph()
        ontology.parse(os.path.join(".", "resources", "computer.owl"))

        relationships_count = 100
        relationships_path = os.path.join(".", "resources", "relationships.txt")

        parser = Parser(ontology, relationships_path)
        processed_ontology = parser.get_processed_relationships(relationships_count)
        parser.print_relationships(processed_ontology)
    else:
        processed_ontology = [("embeded functions", "contributes to", "largest embeded exponent")]
        relationships_count = 1
    quiz = Quiz(processed_ontology, relationships_count, debug_mode=True)
    quiz.run()
    a = 1
    # synsets = WordnetManager.get_synset_for_word_from_command()
    # WordnetManager.pretty_print_synsets(synsets)


if __name__ == '__main__':
    main()
