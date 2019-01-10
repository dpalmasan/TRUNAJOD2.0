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
            if total_transitions != 0:
                entity_features[prob] /= float(total_transitions)
            else:
                entity_features[prob] = 0.0


        self.__grid = entity_grid
        self.__n_sent = n_sent
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

    def get_egrid(self):
        return self.__grid

    def get_sentence_count(self):
        return self.__n_sent

def weighting_syntactic_role(entity_role):
    """
    Weighting scheme for syntactic role of an entity. This uses the heuristic 
    from the paper, which is S = 3, O = 2, X = 1, - = 0

        Input: entity_role (string, utf8)
        Output: The value of the role. Int
    """
    if entity_role == u"S":
        return 3
    elif entity_role == u"O":
        return 2
    elif entity_role == u"X":
        return 1

    return 0


# TODO: Implement PACC, and all the other measures using Distance 
# between sentences as in the paper
def get_local_coherence(egrid):
    """
    Computes local coherence using Graph-Based local coherence 
    modeling

        Input: EntityGrid
        Output: A tuple with different local coherence scores
    """
    n_sent = egrid.get_sentence_count()
    PW = [[0] * n_sent for i in xrange(n_sent)]
    
    # Weight Matrix for PACC, syntactic information is accounted for by
    # integrating the edges of the bipartite graph
    W = [[0] * n_sent for i in xrange(n_sent)]

    grid = egrid.get_egrid()
    for entity in grid:
        for i in xrange(n_sent):
            for j in xrange(i+1,n_sent):
                if grid[entity][i] != u"-" and grid[entity][j] != u"-":
                    PW[i][j] += 1
                    W[i][j] += weighting_syntactic_role(grid[entity][i]) \
                            * weighting_syntactic_role(grid[entity][j])

    PU = [map(lambda x: x != 0, PWi) for PWi in PW]

    local_coherence_PU = 0.0
    local_coherence_PW = 0.0
    local_coherence_PACC = 0.0
    for i in xrange(n_sent):
        local_coherence_PW += sum(PW[i])
        local_coherence_PU += sum(PU[i])
        local_coherence_PACC += sum(W[i])

    
    local_coherence_PW /= n_sent
    local_coherence_PU /= n_sent
    local_coherence_PACC /= n_sent


    # Weighting projection graphs 
    PU_weighted = list(PU)
    PW_weighted = list(PW)
    PACC_weighted = list(W)
    for i in xrange(n_sent):
        for j in xrange(i+1,n_sent):
            PU_weighted[i][j] = PU[i][j] / float(j-i)
            PW_weighted[i][j] = PW[i][j] / float(j-i)
            PACC_weighted[i][j] = W[i][j] / float(j-i)

    local_coherence_PU_dist = 0.0
    local_coherence_PW_dist = 0.0
    local_coherence_PACC_dist = 0.0
    for i in xrange(n_sent):
        local_coherence_PW_dist += sum(PW_weighted[i])
        local_coherence_PU_dist += sum(PU_weighted[i])
        local_coherence_PACC_dist += sum(PACC_weighted[i])
    
    local_coherence_PW_dist /= n_sent
    local_coherence_PU_dist /= n_sent
    local_coherence_PACC_dist /= n_sent
    return (local_coherence_PU, local_coherence_PW, local_coherence_PACC,
            local_coherence_PU_dist, local_coherence_PW_dist, 
            local_coherence_PACC_dist)



