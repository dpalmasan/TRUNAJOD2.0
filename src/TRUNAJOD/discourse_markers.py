"""TRUNAJOD discourse markers module.

This discourse markers module is based on the lexicon described in
:cite:`i2005representing`, and at the point of writing they are under
https://cs.famaf.unc.edu.ar/~laura/shallowdisc4summ/discmar/. TRUNAJOD
comes with this lexicon bundled, and this module has the following set
'constants':

+-------------------------------+---------------------------------------------+
| Type of discourse marker      | Discourse marker                            |
+===============================+=============================================+
| cause                         | dado que, porque, debido a, gracias a,      |
|                               | por si, por, por eso, en conclusión,        |
|                               | así que, como consecuencia, para, para que, |
|                               | por estar razón, por tanto, en efecto       |
+-------------------------------+---------------------------------------------+
| context                       | teniendo en cuenta, después, antes,         |
|                               | originalmente, a condición de, durante,     |
|                               | mientras, a no ser que, cuando, donde,      |
|                               | de acuerdo con, lejos de, tan pronto como,  |
|                               | por el momento, entre, hacia, hasta,        |
|                               | mediante, según, en cualquier caso,         |
|                               | entonces, respecto a, en ese caso, si,      |
|                               | siempre que, sin duda, a la vez             |
+-------------------------------+---------------------------------------------+
| equality                      | en resumen, concretamente, en esencia,      |
|                               | en comparación, en otras palabras,          |
|                               | en particular, es decir, por ejemplo,       |
|                               | precisamente, tal como, por último,         |
|                               | por un lado, por otro lado, a propósito,    |
|                               | no sólo, sino también, en dos palabras,     |
|                               | además, también, aparte, aún es más,        |
|                               | incluso, especialmente, sobretodo           |
+-------------------------------+---------------------------------------------+
| highly polysemic              | como, desde, sobre, antes que nada,         |
|                               | para empezar                                |
+-------------------------------+---------------------------------------------+
| Revision                      | a pesar de, aunque, excepto, pese a,        |
|                               | no obstante, sin embargo, en realidad,      |
|                               | de hecho, al contrario, el hecho es que,    |
|                               | es cierto que, pero', con todo, ahora bien, |
|                               | de todos modos                              |
+-------------------------------+---------------------------------------------+
| Vague meaning closed class    | y, e, ni, o, u, que, con, sin, contra,      |
| words                         | en, a,                                      |
+-------------------------------+---------------------------------------------+

The following module constants are defined as sets ``CAUSE_DISCOURSE_MARKERS``,
``CONTEXT_DISCOURSE_MARKERS``, ``EQUALITY_DISCOURSE_MARKERS``,
``HIGHLY_POLYSEMIC_DISCOURSE_MARKERS``, ``REVISION_DISCOURSE_MARKERS``,
``VAGUE_MEANING_CLOSED_CLASS_WORDS``.
"""
import re

CAUSE_DISCOURSE_MARKERS = {
    'dado que',
    'porque',
    'debido a',
    'gracias a',
    'por si',
    'por',
    'por eso',
    'en conclusión',
    'así que',
    'como consecuencia',
    'para',
    'para que',
    'por esta razón',
    'por tanto',
    'en efecto',
}

CONTEXT_DISCOURSE_MARKERS = {
    'teniendo en cuenta',
    'después',
    'antes',
    'originalmente',
    'a condición de',
    'durante',
    'mientras',
    'a no ser que',
    'cuando',
    'donde',
    'de acuerdo con',
    'lejos de',
    'tan pronto como',
    'por el momento',
    'entre',
    'hacia',
    'hasta',
    'mediante',
    'según',
    'en cualquier caso',
    'entonces',
    'respecto a',
    'en ese caso',
    'si',
    'siempre que',
    'sin duda',
    'a la vez',
}

EQUALITY_DISCOURSE_MARKERS = {
    'en resumen',
    'concretamente',
    'en esencia',
    'en comparación',
    'en otras palabras',
    'en particular',
    'es decir',
    'por ejemplo',
    'precisamente',
    'tal como',
    'por último',
    'por un lado',
    'por otro lado',
    'a propósito',
    'no sólo',
    'sino también',
    'en dos palabras',
    'además',
    'también',
    'aparte',
    'aún es más',
    'incluso',
    'especialmente',
    'sobretodo',
}

HIGHLY_POLYSEMIC_DISCOURSE_MARKERS = {
    'como',
    'desde',
    'sobre',
    'antes que nada',
    'para empezar',
}

REVISION_DISCOURSE_MARKERS = {
    'a pesar de',
    'aunque',
    'excepto',
    'pese a',
    'no obstante',
    'sin embargo',
    'en realidad',
    'de hecho',
    'al contrario',
    'el hecho es que',
    'es cierto que',
    'pero',
    'con todo',
    'ahora bien',
    'de todos modos',
}

VAGUE_MEANING_CLOSED_CLASS_WORDS = {
    'y',
    'e',
    'ni',
    'o',
    'u',
    'que',
    'con',
    'sin',
    'contra',
    'en',
    'a',
}


def find_matches(text, list):
    """Return matches of words in list in a target text.

    Given a text and a list of possible matches (in this module, discourse
    markers list), returns the number of matches found in text. This ignores
    case.

    .. hint:: For non-Spanish users
       You could use this function with your custom list of discourse markers
       in case you need to compute this metric. In that case, the way to call
       the funcion would be: ``find_matches(YOUR_TEXT, ["dm1", "dm2", etc])``

    :param text: Text to be processed
    :type text: string
    :param list: list of discourse markers
    :type list: Python list of strings
    :return: Number of ocurrences
    :rtype: int
    """
    counter = 0
    for w in list:
        results = re.findall(r'\b%s\b' % w, text, re.IGNORECASE)
        counter += len(results)
    return counter


def get_cause_dm_count(text):
    """Count discourse markers associated with cause.

    :param text: The text to be analized
    :type text: Spacy Doc
    :return: Average of revision cause markers over sentences
    :rtype: float
    """
    sentences = [
        find_matches(sent.string.strip(), CAUSE_DISCOURSE_MARKERS)
        for sent in text.sents
    ]
    return sum(sentences) / len(sentences)


def get_closed_class_vague_meaning_count(text):
    """Count words that have vague meaning.

    :param text: The text to be analized
    :type text: Spacy Doc
    :return: Average of vague meaning words over sentences
    :rtype: float
    """
    sentences = [
        find_matches(sent.string.strip(), VAGUE_MEANING_CLOSED_CLASS_WORDS)
        for sent in text.sents
    ]
    return sum(sentences) / len(sentences)


def get_context_dm_count(text):
    """Count discourse markers associated with context.

    :param text: The text to be analized
    :type text: Spacy Doc
    :return: Average of context discourse markers over sentences
    :rtype: float
    """
    sentences = [
        find_matches(sent.string.strip(), CONTEXT_DISCOURSE_MARKERS)
        for sent in text.sents
    ]
    return sum(sentences) / len(sentences)


def get_equality_dm_count(text):
    """Count discourse markers associated with equality.

    :param text: The text to be analized
    :type text: Spacy Doc
    :return: Average of equality discourse markers over sentences
    :rtype: float
    """
    sentences = [
        find_matches(sent.string.strip(), EQUALITY_DISCOURSE_MARKERS)
        for sent in text.sents
    ]
    return sum(sentences) / len(sentences)


def get_polysemic_dm_count(text):
    """Count discourse markers that are highly polysemic.

    :param text: The text to be analized
    :type text: Spacy Doc
    :return: Average of highly polysemic discourse markers over sentences
    :rtype: float
    """
    sentences = [
        find_matches(sent.string.strip(), HIGHLY_POLYSEMIC_DISCOURSE_MARKERS)
        for sent in text.sents
    ]
    return sum(sentences) / len(sentences)


def get_overall_markers(text):  # pragma: no cover
    """Count all types of discourse markers.

    :param text: The text to be analized
    :type text: Spacy Doc
    :return: Average discourse markers over sentences
    :rtype: float
    """
    sentences = []
    sentences += [
        find_matches(sent.string.strip(), VAGUE_MEANING_CLOSED_CLASS_WORDS)
        for sent in text.sents
    ]

    sentences += [
        find_matches(sent.string.strip(), HIGHLY_POLYSEMIC_DISCOURSE_MARKERS)
        for sent in text.sents
    ]

    sentences += [
        find_matches(sent.string.strip(), CONTEXT_DISCOURSE_MARKERS)
        for sent in text.sents
    ]

    sentences += [
        find_matches(sent.string.strip(), EQUALITY_DISCOURSE_MARKERS)
        for sent in text.sents
    ]

    sentences += [
        find_matches(sent.string.strip(), CAUSE_DISCOURSE_MARKERS)
        for sent in text.sents
    ]

    sentences += [
        find_matches(sent.string.strip(), REVISION_DISCOURSE_MARKERS)
        for sent in text.sents
    ]
    return sum(sentences) / len(sentences)


def get_revision_dm_count(text):
    """Count discourse markers associated with revisions.

    :param text: The text to be analized
    :type text: Spacy Doc
    :return: Average of revision discourse markers over sentences
    :rtype: float
    """
    sentences = [
        find_matches(sent.string.strip(), REVISION_DISCOURSE_MARKERS)
        for sent in text.sents
    ]
    return sum(sentences) / len(sentences)
