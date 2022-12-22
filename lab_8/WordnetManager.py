from collections import defaultdict

from nltk.corpus import wordnet as wn
from nltk.corpus.reader import Synset

SYNONYM = "synonym"
MERONYM = "meronym"
HYPERNYM = "hypernym"


class WordnetManager:
    def __init__(self):
        pass

    @staticmethod
    def get_synonims_for(word: str) -> list[list[str]]:
        subwords = word.split(" ")
        subwords_syns = []

        for subword in subwords:
            synsets = wn.synsets(subword)
            if not synsets:
                subwords_syns.append([subword])
                continue
            subwords_syns.append([subword] + [element.name() for element in synsets[0].lemmas()])
        return subwords_syns


    @staticmethod
    def get_nyms_for(word: str) -> list[dict]:
        subwords = word.split(" ")
        subwords_syns = []
        for subword in subwords:
            synsets = wn.synsets(subword)
            subword_data = dict()
            if not synsets:
                subword_data[SYNONYM] = [subword]
                continue
            subword_data[SYNONYM] = [subword] + [element.name() for element in synsets[0].lemmas()]
            subword_data[HYPERNYM] = [element.name().split(".")[0] for element in wn.synsets(subword)[0].hypernyms()]
            subword_data[MERONYM] = [element.name().split(".")[0] for element in wn.synsets(subword)[0].part_meronyms()]
            subwords_syns.append(subword_data)
        return subwords_syns

    @staticmethod
    def get_synsets_for_word_from_command() -> list[Synset]:
        word = input("Enter the word to find synonyms for: ")
        return wn.synsets(word)

    @staticmethod
    def pretty_print_synsets(synsets: list[Synset]) -> None:
        for synset in synsets:
            print(f"Name of synset: {synset.name()}\n"
                  f"Definition of synset: {synset.definition()}")
            print("Synonims: {}".format(" ".join([element.name()
                                                  for element in synset.lemmas()])))


def main():
    synsets = WordnetManager.get_synsets_for_word_from_command()
    WordnetManager.pretty_print_synsets(synsets)


# if __name__ == "__main__":
#
#     # main()
