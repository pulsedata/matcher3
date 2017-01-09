"""
Algorithms in use in matcher.py
"""

import jellyfish

def word_matches(str1, str2):
    """ Find the number of same words in both strings. """
    words_str1 = [word for word in str1.split() if len(word) >= 3]
    words_str2 = [word for word in str2.split() if len(word) >= 3]
    return len(set(words_str1).intersection(words_str2))

def levenshtein_percent(str1, str2):
    """ Get a percentage based on levenshtein values. """
    lev = jellyfish.levenshtein_distance(str1, str2)
    mxp = max(len(str1), len(str2))
    levp = ((mxp - lev) / mxp) * 100
    return int(round(levp, 0))
