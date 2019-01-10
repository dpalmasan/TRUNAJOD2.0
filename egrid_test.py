#!/usr/bin/env python
# -*- coding: utf-8 -*-

from TRUNAJOD import utils
from TRUNAJOD.EntityGrid import EntityGrid
from TRUNAJOD.EntityGrid import get_local_coherence 
import pickle
import spacy


with open("./TRUNAJOD_MODELS/lemmatizador.pickle", "rb") as fp:
    lemmaDict = pickle.load(fp)

with open("./TRUNAJOD_MODELS/wordnet_noun_synsets.pickle", "rb") as fp:
    wordnet_noun_synsets = pickle.load(fp)

with open("./TRUNAJOD_MODELS/wordnet_verb_synsets.pickle", "rb") as fp:
    wordnet_verb_synsets = pickle.load(fp)

with open("./TRUNAJOD_MODELS/spanish_lexicosemantic_norms.pickle", "rb") as fp:
    spanish_lexicosemantic_norms = pickle.load(fp)

stopwords = utils.getStopwords("./TRUNAJOD_MODELS/stopwords-es.txt")
nlp = spacy.load("./es_core_news_md-2.0.0")

if __name__ == "__main__":

    # Read text
    text = utils.readText("./texto_prueba.txt")

    processed_text = nlp(text)
    entity_grid = EntityGrid(processed_text)
    print get_local_coherence(entity_grid)


