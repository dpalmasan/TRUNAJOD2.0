#!/usr/bin/env python
# -*- coding: utf-8 -*-

from TRUNAJOD import utils
from TRUNAJOD import semantic_measures
from TRUNAJOD import giveness
from TRUNAJOD import ttr
from TRUNAJOD import discourse_markers
from TRUNAJOD.EntityGrid import EntityGrid
from TRUNAJOD.LexicoSemanticNorm import LexicoSemanticNorm
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
    docs = processed_text.sents
    lexico_semantic_norms = LexicoSemanticNorm(processed_text, spanish_lexicosemantic_norms, lemmaDict)
    noun_lemmas, verb_lemmas, function_lemmas, content_lemmas, adj_lemmas, adv_lemmas, prp_lemmas = utils.getSentencesLemmas(docs, lemmaDict, stopwords)



    print "******************************"
    print "Semantic Overlap"
    print "******************************"

    print "Noun Semantic Overlap: ", semantic_measures.overlap(
                                                        noun_lemmas, 
                                                        wordnet_noun_synsets)

    print "Verb Semantic Overlap: ", semantic_measures.overlap(
                                                        verb_lemmas, 
                                                        wordnet_verb_synsets)
    print "Lexical Overlap: ", semantic_measures.overlap(function_lemmas 
                                                           + content_lemmas, {})


    N = len(list(processed_text.sents))
    docs = processed_text.sents
    print "word2vec Semantic Sim: ", semantic_measures.avgW2VSemanticSimilarity(
        docs,
        N
    )

    print "******************************"
    print "Giveness"
    print "******************************"
    print "pronoun density: ", giveness.pronounDensity(processed_text)
    print "pronoun Noun Ratio: ", giveness.pronounNounRatio(processed_text)


    print "******************************"
    print "Type Token Ratios"
    print "******************************"
    print "lemma_ttr: ", ttr.simple_ttr(utils.flatten(function_lemmas) 
                                        + utils.flatten(content_lemmas))
    print "content_ttr: ", ttr.simple_ttr(utils.flatten(content_lemmas))
    print "function_ttr: ", ttr.simple_ttr(utils.flatten(function_lemmas))
    print "noun_ttr: ", ttr.simple_ttr(utils.flatten(noun_lemmas))
    print "verb_ttr: ", ttr.simple_ttr(utils.flatten(verb_lemmas))
    print "adj_ttr: ", ttr.simple_ttr(utils.flatten(adj_lemmas))
    print "adv_ttr: ", ttr.simple_ttr(utils.flatten(adv_lemmas))
    print "prp_ttr: ", ttr.simple_ttr(utils.flatten(prp_lemmas))
    print "argument_ttr: ", ttr.simple_ttr(utils.flatten(prp_lemmas) 
                                           + utils.flatten(noun_lemmas))


    
    print "******************************"
    print "Entity Grids"
    print "******************************"
    print "SS Transitions: ", entity_grid.get_ss_transitions()
    print "SO Transitions: ", entity_grid.get_so_transitions()
    print "SX Transitions: ", entity_grid.get_sx_transitions()
    print "S- Transitions: ", entity_grid.get_sn_transitions()
    print "OS Transitions: ", entity_grid.get_os_transitions()
    print "OO Transitions: ", entity_grid.get_oo_transitions()
    print "OX Transitions: ", entity_grid.get_ox_transitions()
    print "O- Transitions: ", entity_grid.get_on_transitions()
    print "XS Transitions: ", entity_grid.get_xs_transitions()
    print "XO Transitions: ", entity_grid.get_xo_transitions()
    print "XX Transitions: ", entity_grid.get_xx_transitions()
    print "X- Transitions: ", entity_grid.get_xn_transitions()
    print "-S Transitions: ", entity_grid.get_ns_transitions()
    print "-O Transitions: ", entity_grid.get_no_transitions()
    print "-X Transitions: ", entity_grid.get_nx_transitions()
    print "-- Transitions: ", entity_grid.get_nn_transitions()

    print "******************************"
    print "Discourse Markers Count"
    print "******************************"
    print "Revision DM: ", discourse_markers.get_revision_dm_count(text)
    print "Cause DM: ", discourse_markers.get_cause_dm_count(text)
    print "Equality DM: ", discourse_markers.get_equality_dm_count(text)
    print "Context DM: ", discourse_markers.get_context_dm_count(text)
    print "Polysemic DM: ", discourse_markers.get_polysemic_dm_count(text)
    print "Closed Class Words DM: ", discourse_markers.get_closed_class_vague_meaning_count(text)

    
    print "******************************"
    print "Lexicco Semantic Norms"
    print "******************************"
    print "Valence: ", lexico_semantic_norms.get_valence()
    print "Arousal: ", lexico_semantic_norms.get_arousal()
    print "Concreteness: ", lexico_semantic_norms.get_concreteness()
    print "Imageability: ", lexico_semantic_norms.get_imageability()
    print "Context Availability: ", lexico_semantic_norms.get_context_availability()
    print "Familiarity: ", lexico_semantic_norms.get_familiarity()
