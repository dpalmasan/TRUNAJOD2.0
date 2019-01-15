#!/usr/bin/env python
# -*- coding: utf-8 -*-


def simple_ttr(word_list):
    if len(word_list) == 0:
        return 0.0
    return len(set(word_list))/float(len(word_list))
