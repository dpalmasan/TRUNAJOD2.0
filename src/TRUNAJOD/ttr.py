#!/usr/bin/env python


def simple_ttr(word_list):
    """Return Type Token Ratio of a word list

    :param word_list: List of words
    :type word_list: List of strings
    :return: TTR of the word list
    :rtype: float
    """
    if len(word_list) == 0:
        return 0.0
    return len(set(word_list))/float(len(word_list))
