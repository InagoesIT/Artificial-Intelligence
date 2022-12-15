import json
import urllib.parse
import requests


class Parser:
    def __init__(self, ontology, file_path):
        self.ontology = ontology
        self.file_path = file_path

    @staticmethod
    def get_words_from_camel(string):
        result = ""
        for char in string:
            if char.isupper():
                result += " " + char.lower()
            else:
                result += char
        return result

    @staticmethod
    def get_processed_concept(concept):
        # the link is not related to the concept!!
        if 'academic.microsoft' in concept:
            return None
        processed_concept = urllib.parse.unquote(concept.split('/')[-1].replace("_", " "))

        try:
            if 'wikidata' in concept:
                response = requests.get(concept)
                return response.json()['entities'][processed_concept]['labels']['en']['value']
        except KeyError:
            return None

        if processed_concept == "cso#Topic":
            return "cso topic"
        return processed_concept

    @staticmethod
    def get_processed_predicate(predicate):
        predicate = predicate.split('/')[-1]
        if '#' in predicate:
            predicate = predicate.split('#')[-1]
        return urllib.parse.unquote(Parser.get_words_from_camel(predicate))

    @staticmethod
    def get_processed_relation(relation):
        processed_concept1 = Parser.get_processed_concept(relation[0])
        processed_predicate = Parser.get_processed_predicate(relation[1])
        processed_concept2 = Parser.get_processed_concept(relation[2])

        return processed_concept1, processed_predicate, processed_concept2

    def print_relationships(self, processed_ontology):
        file_descriptor = open(self.file_path, 'w')

        for concept1, predicate, concept2 in processed_ontology:
            file_descriptor.write(f"{concept1} -> {predicate} -> {concept2}\n")

        file_descriptor.close()

    def get_processed_relationships(self, relationships_count):
        iteration = 1
        processed_ontology = []

        for concept1, predicate, concept2 in self.ontology:
            if iteration == relationships_count:
                break
            relation = concept1, predicate, concept2
            processed_relation = Parser.get_processed_relation(relation)
            if None in processed_relation:
                continue
            processed_ontology.append(processed_relation)

            iteration += 1

        return processed_ontology
