#!/usr/local/bin/python
# -*- coding: utf-8 -*-
"""Entity grid module for TRUNAJOD.

In this module, entity grid based features are implemented. On one side,
an entity grid :cite:`barzilay2008modeling` implementation is provided.
We also provide an implementation of the entity graph coherence modeling
:cite:`guinaudeau2013graph`.

.. danger:: These set of features or measurements
   Really depends on the dependency parsing accuracy, which relies on the
   CORPUS the dependency parsed was trained. There is no guarantee that this
   will work with all types of texts. On the other hand, the implementation
   is simple and we do not do any coreference resolution for noun-phrases and
   just rely on simple heuristics.

It is also worth noting, that we consider an entity grid of two-sentence
sequence and the API currently does not provide any hyper-parameter tunning to
change this.
"""

SPACY_UNIVERSAL_NOUN_TAGS = set([u'NOUN', u'PRON', u'PROPN'])

ordered_transitions = [
    u'SS', u'SO', u'SX', u'S-', u'OS', u'OO', u'OX', u'O-', u'XS', u'XO',
    u'XX', u'X-', u'-S', u'-O', u'-X', u'--'
]


def dependency_mapping(dep):
    """Map dependency tag to entity grid tag.

    We consider the notation provided in :cite:`barzilay2008modeling`:

    +-----------+-----------------------------------+
    | EGrid Tag | Dependency Tag                    |
    +===========+===================================+
    | S         | nsub, csubj, csubjpass, dsubjpass |
    +-----------+-----------------------------------+
    | O         | iobj, obj, pobj, dobj             |
    +-----------+-----------------------------------+
    | X         | For any other dependency tag      |
    +-----------+-----------------------------------+

    :param dep: Dependency tag
    :type dep: string
    :return: EGrid tag
    :rtype: string
    """
    if dep in {u'nsubj', u'csubj', u'csubjpass', u'dsubjpass'}:
        return u'S'
    if dep in {u'iobj', u'obj', u'pobj', u'dobj'}:
        return u'O'

    return 'X'


class EntityGrid(object):
    """Entity grid class.

    Class Entity Grid, creates an entity grid from a doc, which is output of
    applying spacy.nlp(text) to a text. Thus, this class depends on spacy
    module. It only supports 2-transitions entity grid.
    """

    def __init__(self, doc):
        """Construct EntityGrid object."""
        # Initialization
        entity_map = dict()
        entity_grid = dict()
        i = 1
        entity_map['s%d' % i] = []
        entity_features = {
            u'SS': 0,
            u'SO': 0,
            u'SX': 0,
            u'S-': 0,
            u'OS': 0,
            u'OO': 0,
            u'OX': 0,
            u'O-': 0,
            u'XS': 0,
            u'XO': 0,
            u'XX': 0,
            u'X-': 0,
            u'-S': 0,
            u'-O': 0,
            u'-X': 0,
            u'--': 0
        }

        # Get number of sentences in the text
        n_sent = len(list(doc.sents))

        # To get coherence measurements we need at least 2 sentences
        if n_sent < 2:
            raise RuntimeError(
                "Entity grid needs at least two sentences, found: {}"
                .format(n_sent))

        # For each sentence, get dependencies and its grammatical role
        for sent in doc.sents:
            for token in sent:
                if token.pos_ in SPACY_UNIVERSAL_NOUN_TAGS:
                    entity_map['s%d' % i].append((token.text.upper(),
                                                  token.dep_))
                    if token.text.upper() not in entity_grid:
                        entity_grid[token.text.upper()] = [u'-'] * n_sent
            i += 1
            entity_map['s%d' % i] = []

        # Last iteration will create an extra element, so I remove it.
        entity_map.pop('s%d' % i)

        # Fill entity grid
        for i in range(n_sent):
            sentence = "s%d" % (i + 1)
            for entity, dep in entity_map[sentence]:
                if entity_grid[entity][i] == u'-':
                    entity_grid[entity][i] = dependency_mapping(dep)
                elif dependency_mapping(dep) == u'S':
                    entity_grid[entity][i] = dependency_mapping(dep)
                elif (dependency_mapping(dep) == u'O'
                      and entity_grid[entity][i] == u'X'):
                    entity_grid[entity][i] = dependency_mapping(dep)

        # Compute feature vector, we consider transitions of length 2
        total_transitions = (n_sent - 1) * len(entity_grid.keys())

        for entity in entity_grid:
            for i in range(n_sent - 1):
                # Transition type found (e.g. S-)
                transition = (
                    entity_grid[entity][i] + entity_grid[entity][i + 1])

                # Adding 1 to transition count
                entity_features[transition] += 1

        for prob in entity_features:
            if total_transitions != 0:
                entity_features[prob] /= float(total_transitions)
            else:
                entity_features[prob] = 0.0

        self.__grid = entity_grid
        self.__n_sent = n_sent
        self.__prob = entity_features

    def get_ss_transitions(self):
        """Get SS transitions.

        :return: Ratio of transitions
        :rtype: float
        """
        return self.__prob[u"SS"]

    def get_so_transitions(self):
        """Get SO transitions.

        :return: Ratio of transitions
        :rtype: float
        """
        return self.__prob[u"SO"]

    def get_sx_transitions(self):
        """Get SX transitions.

        :return: Ratio of transitions
        :rtype: float
        """
        return self.__prob[u"SX"]

    def get_sn_transitions(self):
        """Get S- transitions.

        :return: Ratio of transitions
        :rtype: float
        """
        return self.__prob[u"S-"]

    def get_os_transitions(self):
        """Get OS transitions.

        :return: Ratio of transitions
        :rtype: float
        """
        return self.__prob[u"OS"]

    def get_oo_transitions(self):
        """Get OO transitions.

        :return: Ratio of transitions
        :rtype: float
        """
        return self.__prob[u"OO"]

    def get_ox_transitions(self):
        """Get OX transitions.

        :return: Ratio of transitions
        :rtype: float
        """
        return self.__prob[u"OX"]

    def get_on_transitions(self):
        """Get O- transitions.

        :return: Ratio of transitions
        :rtype: float
        """
        return self.__prob[u"O-"]

    def get_xs_transitions(self):
        """Get XS transitions.

        :return: Ratio of transitions
        :rtype: float
        """
        return self.__prob[u"XS"]

    def get_xo_transitions(self):
        """Get XO transitions.

        :return: Ratio of transitions
        :rtype: float
        """
        return self.__prob[u"XO"]

    def get_xx_transitions(self):
        """Get XX transitions.

        :return: Ratio of transitions
        :rtype: float
        """
        return self.__prob[u"XX"]

    def get_xn_transitions(self):
        """Get X- transitions.

        :return: Ratio of transitions
        :rtype: float
        """
        return self.__prob[u"X-"]

    def get_ns_transitions(self):
        """Get -S transitions.

        :return: Ratio of transitions
        :rtype: float
        """
        return self.__prob[u"-S"]

    def get_no_transitions(self):
        """Get -O transitions.

        :return: Ratio of transitions
        :rtype: float
        """
        return self.__prob[u"-O"]

    def get_nx_transitions(self):
        """Get -X transitions.

        :return: Ratio of transitions
        :rtype: float
        """
        return self.__prob[u"-X"]

    def get_nn_transitions(self):
        """Get -- transitions.

        :return: Ratio of transitions
        :rtype: float
        """
        return self.__prob[u"--"]

    def get_egrid(self):
        """Return obtained entity grid (for debugging purposes).

        :return: entity grid represented as a dict
        :rtype: dict
        """
        return self.__grid

    def get_sentence_count(self):
        """Return sentence count obtained while processing.

        :return: Number of sentences
        :rtype: int
        """
        return self.__n_sent


def weighting_syntactic_role(entity_role):
    """Return weight given an entity grammatical role.

    Weighting scheme for syntactic role of an entity. This uses the heuristic
    from :cite:`guinaudeau2013graph`, which is:

    +-----------+--------+
    | EGrid Tag | Weight |
    +===========+========+
    | S         | 3      |
    +-----------+--------+
    | O         | 2      |
    +-----------+--------+
    | X         | 1      |
    +-----------+--------+
    | dash      | 0      |
    +-----------+--------+

    :param entity_role: Entity grammatical role (S, O, X, -)
    :type entity_role: string
    :return: Role weight
    :rtype: int
    """
    if entity_role == u"S":
        return 3
    elif entity_role == u"O":
        return 2
    elif entity_role == u"X":
        return 1

    return 0


def get_local_coherence(egrid):
    """Get local coherence from entity grid.

    This method gets the coherence value using all the approaches described
    in :cite:`guinaudeau2013graph`. This include:

    * local_coherence_PU
    * local_coherence_PW
    * local_coherence_PACC
    * local_coherence_PU_dist
    * local_coherence_PW_dist
    * local_coherence_PACC_dist

    :param egrid: An EntityGrid object.
    :type egrid: EntityGrid
    :return: Local coherence based on different heuristics
    :rtype: tuple of floats
    """
    n_sent = egrid.get_sentence_count()

    # If entity grid is not valid
    if n_sent < 2:
        return (0.0, 0.0, 0.0, 0.0, 0.0, 0.0)

    PW = [[0] * n_sent for i in range(n_sent)]

    # Weight Matrix for PACC, syntactic information is accounted for by
    # integrating the edges of the bipartite graph
    W = [[0] * n_sent for i in range(n_sent)]

    grid = egrid.get_egrid()
    for entity in grid:
        for i in range(n_sent):
            for j in range(i + 1, n_sent):
                if grid[entity][i] != u"-" and grid[entity][j] != u"-":
                    PW[i][j] += 1
                    W[i][j] += (weighting_syntactic_role(grid[entity][i]) *
                                weighting_syntactic_role(grid[entity][j]))

    PU = [list(map(lambda x: x != 0, PWi)) for PWi in PW]

    local_coherence_PU = 0.0
    local_coherence_PW = 0.0
    local_coherence_PACC = 0.0
    for i in range(n_sent):
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
    for i in range(n_sent):
        for j in range(i + 1, n_sent):
            PU_weighted[i][j] = PU[i][j] / float(j - i)
            PW_weighted[i][j] = PW[i][j] / float(j - i)
            PACC_weighted[i][j] = W[i][j] / float(j - i)

    local_coherence_PU_dist = 0.0
    local_coherence_PW_dist = 0.0
    local_coherence_PACC_dist = 0.0
    for i in range(n_sent):
        local_coherence_PW_dist += sum(PW_weighted[i])
        local_coherence_PU_dist += sum(PU_weighted[i])
        local_coherence_PACC_dist += sum(PACC_weighted[i])

    local_coherence_PW_dist /= n_sent
    local_coherence_PU_dist /= n_sent
    local_coherence_PACC_dist /= n_sent
    return (local_coherence_PU, local_coherence_PW, local_coherence_PACC,
            local_coherence_PU_dist, local_coherence_PW_dist,
            local_coherence_PACC_dist)
