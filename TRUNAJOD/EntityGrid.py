#!/usr/local/bin/python
# -*- coding: utf-8 -*-

SPACY_UNIVERSAL_NOUN_TAGS   = set([u'NOUN', u'PRON', u'PROPN'])

ordered_transitions = [
    u'SS', u'SO', u'SX', u'S-',
    u'OS', u'OO', u'OX', u'O-',
    u'XS', u'XO', u'XX', u'X-',
    u'-S', u'-O', u'-X', u'--'
]


def dependency_mapping(dep):
    """
    Maps SPACY dependency tags, to Entity Grid Dependencies
    """
    if dep == u'nsubj' or dep == u'csubj' or dep == u'csubjpass' or dep == u'dsubjpass':
        return u'S'
    if dep == u'iobj' or dep == 'obj' or dep == u'pobj' or dep == u'dobj':
        return u'O'

    return 'X'

class EntityGrid(object):
    """
    Class Entity Grid, creates an entity grid from a doc, which is output of
    applying spacy.nlp(text) to a text. Thus, this class depends on spacy 
    module. It only supports 2-transitions entity grid.
    """
    def __init__(self, doc):
        """
        Construct entity grid and gets probabilities. Then stores it in the 
        created instance. Note it needs as input a Doc type (Spacy)
        """
        # Initialization
        entity_map = dict()
        entity_grid = dict()
        i = 1
        entity_map['s%d' % i] = []

        # Get number of sentences in the text
        n_sent = len(list(doc.sents))

        # For each sentence, get dependencies and its grammatical role
        for sent in doc.sents:
            for token in sent:
                if token.pos_ in SPACY_UNIVERSAL_NOUN_TAGS:
                    entity_map['s%d' % i].append((token.text.upper(), token.dep_))
                    if token.text.upper() not in entity_grid:
                        entity_grid[token.text.upper()] = [u'-']*n_sent
            i += 1
            entity_map['s%d' % i] = []

        # Last iteration will create an extra element in this map so I remove it.
        entity_map.pop('s%d' % i)


        # Fill entity grid
        for i in xrange(n_sent):
            sentence = "s%d" % (i + 1)
            for entity, dep in entity_map[sentence]:
                if entity_grid[entity][i] == u'-':
                    entity_grid[entity][i] = dependency_mapping(dep)
                elif dependency_mapping(dep) == u'S':
                    entity_grid[entity][i] = dependency_mapping(dep)
                elif dependency_mapping(dep) == u'O' and entity_grid[entity][i] == u'X':
                    entity_grid[entity][i] = dependency_mapping(dep)

        # Compute feature vector, we consider transitions of length 2
        total_transitions = (n_sent - 1) * len(entity_grid.keys())


        entity_features = {
            u'SS': 0, u'SO': 0, u'SX': 0, u'S-': 0,
            u'OS': 0, u'OO': 0, u'OX': 0, u'O-': 0,
            u'XS': 0, u'XO': 0, u'XX': 0, u'X-': 0,
            u'-S': 0, u'-O': 0, u'-X': 0, u'--': 0
        }

        for entity in entity_grid:
            for i in xrange(n_sent - 1):
                entity_features[entity_grid[entity][i] + entity_grid[entity][i + 1]] += 1

        for prob in entity_features:
            entity_features[prob] /= float(total_transitions)


        self.__grid = entity_grid
        self.__prob = entity_features

    def get_ss_transitions(self):
        return self.__prob[u"SS"]

    def get_so_transitions(self):
        return self.__prob[u"SO"]
    
    def get_sx_transitions(self):
        return self.__prob[u"SX"]
    
    def get_sn_transitions(self):
        return self.__prob[u"S-"]
    
    def get_os_transitions(self):
        return self.__prob[u"OS"]
    
    def get_oo_transitions(self):
        return self.__prob[u"OO"]
    
    def get_ox_transitions(self):
        return self.__prob[u"OX"]
    
    def get_on_transitions(self):
        return self.__prob[u"O-"]
    
    def get_xs_transitions(self):
        return self.__prob[u"XS"]
    
    def get_xo_transitions(self):
        return self.__prob[u"XO"]
    
    def get_xx_transitions(self):
        return self.__prob[u"XX"]
    
    def get_xn_transitions(self):
        return self.__prob[u"X-"]
    
    def get_ns_transitions(self):
        return self.__prob[u"-S"]
    
    def get_no_transitions(self):
        return self.__prob[u"-O"]
    
    def get_nx_transitions(self):
        return self.__prob[u"-X"]
    
    def get_nn_transitions(self):
        return self.__prob[u"--"]


