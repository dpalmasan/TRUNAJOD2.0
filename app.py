#!/usr/local/bin/python
# -*- coding: utf-8 -*-

from TRUNAJOD import utils
from TRUNAJOD import semantic_measures
from TRUNAJOD import giveness
from TRUNAJOD import ttr
from TRUNAJOD import discourse_markers
from TRUNAJOD.EntityGrid import EntityGrid
from TRUNAJOD.EntityGrid import get_local_coherence 
from TRUNAJOD.LexicoSemanticNorm import LexicoSemanticNorm
import pandas as pd
import pickle
import spacy
import sys

TRUNAJOD_ORDERED_INDICES = [
    "noun_syn_overlap",
    "verb_syn_overlap", 
    "lexical_overlap", 
    "word2vec_sent_sim", 
    "pronoun_density", 
    "pronoun_noun_ratio", 
    "lemma_ttr", 
    "content_ttr", 
    "function_ttr", 
    "noun_ttr", 
    "verb_ttr", 
    "adj_ttr", 
    "adv_ttr", 
    "prp_ttr", 
    "argument_ttr", 
    "egrid_ss", 
    "egrid_so", 
    "egrid_sx", 
    "egrid_s-", 
    "egrid_os", 
    "egrid_oo", 
    "egrid_ox", 
    "egrid_o-", 
    "egrid_xs", 
    "egrid_xo", 
    "egrid_xx", 
    "egrid_x-", 
    "egrid_-s", 
    "egrid_-o", 
    "egrid_-x", 
    "egrid_--", 
    "revision_dm",
    "cause_dm",
    "equality_dm",
    "context_dm",
    "polysemic_dm",
    "closed_class_words",
    "avg_valence", 
    "avg_arousal",
    "avg_concreteness", 
    "avg_imageability",
    "avg_context_availability",
    "avg_familiarity",
    "egraph_lc_pu",
    "egraph_lc_pw",
    "egraph_lc_pacc",
    "egraph_lc_pu_dist",
    "egraph_lc_pw_dist",
    "egraph_lc_pacc_dist",
]

TRUNAJOD_ORDERED_INDICES = [
    "lemma_ttr",
    "egrid_-o",
    "egrid_ss",
    "egrid_sx",
    "revision_dm",
    "adj_ttr",
    "egrid_-s",
    "equality_dm",
    "egrid_so",
    "egrid_o-",
    "argument_ttr",
    "avg_concreteness",
    "verb_ttr",
    "avg_context_availability",
    "noun_ttr",
    "lexical_overlap",
    "egrid_xx",
    "egrid_os",
    "egrid_xo",
    "avg_imageability",
    "pronoun_noun_ratio",
    "noun_syn_overlap",
    "avg_arousal",
    "egrid_--",
    "adv_ttr",
    "word2vec_sent_sim",
    "egrid_ox",
    "prp_ttr",
    "function_ttr",
    "cause_dm",
    "egrid_s-",
    "verb_syn_overlap",
    "egrid_oo",
    "avg_valence",
    "polysemic_dm",
    "avg_familiarity",
    "closed_class_words",
    "egrid_xs",
    "content_ttr",
    "egrid_-x",
    "egrid_x-",
    "pronoun_density",
    "context_dm",
    "egraph_lc_pu",
    "egraph_lc_pw",
    "egraph_lc_pacc",
    "egraph_lc_pu_dist",
    "egraph_lc_pw_dist",
    "egraph_lc_pacc_dist",
]

# Load lemmatizer dict
with open("./TRUNAJOD_MODELS/lemmatizador.pickle", "rb") as fp:
    lemmaDict = pickle.load(fp)

# Load wordnet noun synset dict
with open("./TRUNAJOD_MODELS/wordnet_noun_synsets.pickle", "rb") as fp:
    wordnet_noun_synsets = pickle.load(fp)

# Load wordnet verb synset dict
with open("./TRUNAJOD_MODELS/wordnet_verb_synsets.pickle", "rb") as fp:
    wordnet_verb_synsets = pickle.load(fp)

# Load lexicosemantic norms dict
with open("./TRUNAJOD_MODELS/spanish_lexicosemantic_norms.pickle", "rb") as fp:
    spanish_lexicosemantic_norms = pickle.load(fp)

# Load stopwords list
stopwords = utils.getStopwords("./TRUNAJOD_MODELS/stopwords-es.txt")

# Loads spacy models
nlp = spacy.load("./spacy_model/es_core_news_sm", disable=["ner", "textcat"])

def process_text(text):
    """
    Processes text extracting all TRUNAJOD indices.
    """
    # Pre-processing step
    processed_text = nlp(text)
    entity_grid = EntityGrid(processed_text)
    docs = processed_text.sents
    lexico_semantic_norms = LexicoSemanticNorm(processed_text, spanish_lexicosemantic_norms, lemmaDict)
    noun_lemmas, verb_lemmas, function_lemmas, content_lemmas, adj_lemmas, adv_lemmas, prp_lemmas = utils.getSentencesLemmas(docs, lemmaDict, stopwords)
    N = len(list(processed_text.sents))
    docs = processed_text.sents

    # This dict will contain TRUNAJOD computed indices
    trunajod_indices = {}

    trunajod_indices["noun_syn_overlap"] = semantic_measures.overlap(
                                                    noun_lemmas, 
                                                    wordnet_noun_synsets)

    trunajod_indices["verb_syn_overlap"] = semantic_measures.overlap(
                                                    verb_lemmas, 
                                                    wordnet_verb_synsets)
    trunajod_indices["lexical_overlap"] = semantic_measures.overlap(function_lemmas 
                                                       + content_lemmas, {})


    trunajod_indices["word2vec_sent_sim"] =  semantic_measures.avgW2VSemanticSimilarity(
                                                docs,
                                                N
                                            )

    trunajod_indices["pronoun_density"] = giveness.pronounDensity(processed_text)
    trunajod_indices["pronoun_noun_ratio"] = giveness.pronounNounRatio(processed_text)


    trunajod_indices["lemma_ttr"] = ttr.simple_ttr(
                                        utils.flatten(function_lemmas) 
                                        + utils.flatten(content_lemmas)
                                    )
    
    trunajod_indices["content_ttr"] = ttr.simple_ttr(utils.flatten(content_lemmas))
    trunajod_indices["function_ttr"] = ttr.simple_ttr(utils.flatten(function_lemmas))
    trunajod_indices["noun_ttr"] = ttr.simple_ttr(utils.flatten(noun_lemmas))
    trunajod_indices["verb_ttr"] = ttr.simple_ttr(utils.flatten(verb_lemmas))
    trunajod_indices["adj_ttr"] = ttr.simple_ttr(utils.flatten(adj_lemmas))
    trunajod_indices["adv_ttr"] = ttr.simple_ttr(utils.flatten(adv_lemmas))
    trunajod_indices["prp_ttr"] = ttr.simple_ttr(utils.flatten(prp_lemmas))
    trunajod_indices["argument_ttr"] =  ttr.simple_ttr(
                                            utils.flatten(prp_lemmas) 
                                            + utils.flatten(noun_lemmas)
                                        )



    trunajod_indices["egrid_ss"] = entity_grid.get_ss_transitions()
    trunajod_indices["egrid_so"] = entity_grid.get_so_transitions()
    trunajod_indices["egrid_sx"] = entity_grid.get_sx_transitions()
    trunajod_indices["egrid_s-"] = entity_grid.get_sn_transitions()
    trunajod_indices["egrid_os"] = entity_grid.get_os_transitions()
    trunajod_indices["egrid_oo"] = entity_grid.get_oo_transitions()
    trunajod_indices["egrid_ox"] = entity_grid.get_ox_transitions()
    trunajod_indices["egrid_o-"] = entity_grid.get_on_transitions()
    trunajod_indices["egrid_xs"] = entity_grid.get_xs_transitions()
    trunajod_indices["egrid_xo"] = entity_grid.get_xo_transitions()
    trunajod_indices["egrid_xx"] = entity_grid.get_xx_transitions()
    trunajod_indices["egrid_x-"] = entity_grid.get_xn_transitions()
    trunajod_indices["egrid_-s"] = entity_grid.get_ns_transitions()
    trunajod_indices["egrid_-o"] = entity_grid.get_no_transitions()
    trunajod_indices["egrid_-x"] = entity_grid.get_nx_transitions()
    trunajod_indices["egrid_--"] = entity_grid.get_nn_transitions()

    (lc_pu, lc_pw, lc_pacc, lc_pu_dist, lc_pw_dist, lc_pacc_dist) = get_local_coherence(entity_grid)
    trunajod_indices["egraph_lc_pu"] = lc_pu
    trunajod_indices["egraph_lc_pw"] = lc_pw
    trunajod_indices["egraph_lc_pacc"] = lc_pacc
    trunajod_indices["egraph_lc_pu_dist"] = lc_pu_dist
    trunajod_indices["egraph_lc_pw_dist"] = lc_pw_dist
    trunajod_indices["egraph_lc_pacc_dist"] = lc_pacc_dist

    trunajod_indices["revision_dm"] = discourse_markers.get_revision_dm_count(text)
    trunajod_indices["cause_dm"] = discourse_markers.get_cause_dm_count(text)
    trunajod_indices["equality_dm"] = discourse_markers.get_equality_dm_count(text)
    trunajod_indices["context_dm"] = discourse_markers.get_context_dm_count(text)
    trunajod_indices["polysemic_dm"] = discourse_markers.get_polysemic_dm_count(text)
    trunajod_indices["closed_class_words"] = discourse_markers.get_closed_class_vague_meaning_count(text)


    trunajod_indices["avg_valence"] = lexico_semantic_norms.get_valence()
    trunajod_indices["avg_arousal"] = lexico_semantic_norms.get_arousal()
    trunajod_indices["avg_concreteness"] = lexico_semantic_norms.get_concreteness()
    trunajod_indices["avg_imageability"] = lexico_semantic_norms.get_imageability()
    trunajod_indices["avg_context_availability"] = lexico_semantic_norms.get_context_availability()
    trunajod_indices["avg_familiarity"] = lexico_semantic_norms.get_familiarity()
    
    return trunajod_indices

def main(argv):
    #dataset = pd.read_excel("./subset1.xlsx")
    dataset = pd.read_excel("./textos_niveles_escolares.xlsx")
    df = pd.DataFrame()
    TRUNAJOD_ORDERED_INDICES.insert(0, "id")
    TRUNAJOD_ORDERED_INDICES.append("nivel")
    TRUNAJOD_ORDERED_INDICES.append("grupo")
    for index, row in dataset.iterrows():
        #print str(row["id"]) + "," + process_text(row["texto"]) + ",{}".format(row["nivel"])
        try:
            row_dict = process_text(row["texto"])
        except:
            continue
        row_dict["id"] = row["id"]
        row_dict["nivel"] = row["nivel"]
        row_dict["grupo"] = row["grupo"]
        df = df.append(row_dict, ignore_index=True)
    
    df = df.ix[:, TRUNAJOD_ORDERED_INDICES]
    writer = pd.ExcelWriter("./textos_niveles_escolares_features.xlsx")
    df.to_excel(writer, "Sheet1")
    writer.save()
    #from TRUNAJOD.utils import readText
    #text = readText("./texto_debug")
    #print process_text(text)

if __name__== "__main__":
    main(sys.argv[1:])
