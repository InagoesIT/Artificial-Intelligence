import os.path
import pprint
from functools import reduce

import nltk
from nltk.corpus import wordnet

from rdflib import Graph

import urllib.parse
import requests


def get_words_from_camel(string):
    result = ""
    for char in string:
        if char.isupper():
            result += " " + char.lower()
        else:
            result += char
    return result


def get_processed_concept(concept):
    processed_concept = urllib.parse.unquote(concept.split('/')[-1].replace("_", " "))
    try:
        if 'wikidata' in concept:
            response = requests.get(concept)
            return response.json()['entities'][processed_concept]['labels']['en']['value']
    except:
        print("request error: " + concept) # the link doesn't exist, but it redirects
        # I do not know how to redirect and get the text from there yet
        return None
    if processed_concept == "cso#Topic":
        return "cso topic"
    return processed_concept


def get_processed_predicate(predicate):
    predicate = predicate.split('/')[-1]
    if '#' in predicate:
        predicate = predicate.split('#')[-1]
    return urllib.parse.unquote(get_words_from_camel(predicate))


def print_relationships(graph):
    for concept1, predicate, concept2 in graph:
        processed_concept1 = get_processed_concept(concept1)
        processed_concept2 = get_processed_concept(concept2)
        processed_predicate = get_processed_predicate(predicate)

        # the link like this will only contain the  number from here https://academic.microsoft.com/#/detail/201829737
        # the link doesn't seem to be related to the concept!!

        # there was an error with request
        if processed_concept1 is None or processed_concept2 is None:
            continue
        print(f"{processed_concept1} -> {processed_predicate} -> {processed_concept2}")


def main():
    # nltk.download('wordnet')
    # nltk.download('omw-1.4')

    graph = Graph()
    graph.parse(os.path.join(".", "resources", "computer.owl"))

    # print out all the triples in the graph
    print_relationships(graph)

    # index = 0
    # for stmt in graph:
    #     pprint.pprint(stmt)
    # index += 1
    # if index == 100:
    #     break

    # syns = wordnet.synsets("computer")
    # print(f"\nDefinition for computer: {syns[0].definition()}")


if __name__ == '__main__':
    main()
