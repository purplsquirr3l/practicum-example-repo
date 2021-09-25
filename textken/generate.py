# -*- coding: utf-8 -*-
"""Functions to generate dummy text segments."""

from random import sample, choice
from .constants import SENTENCE_ENDINGS

def get_sentence(words, sentence_length=5, add_punctuation=True):
    """Create a sentence out of the given words.

    Parameters
    ----------
    words: list of Strings to treat as sentence words
    sentence_length: an integer denoting how many words should make up the sentence
    add_punctuation: a boolean denoting if the sentence should end with punctuation
    """
    sentence = sample(words, sentence_length)
    if len(sentence) > 1:
        sentence = '{} {}'.format(sentence[0].capitalize(), ' '.join(sentence[1:]))
    elif len(sentence) == 1:
        sentence = sentence[0].capitalize()
    else:
        sentence = ''

    if add_punctuation:
        sentence += choice(SENTENCE_ENDINGS)
    return sentence

def get_paragraph(words, num_sentences=3, sentences_len_range=(3, 5)):
    """Create a paragraph using the given words.

    Parameters
    ----------
    words: list of Strings to treat as sentence words
    num_sentences: the number of sentences that should be in the paragraph
    sentences_len_range: a tuple denoting the minimum and maximum number of
        words that the sentences should have
    """
    return ' '.join([get_sentence(words, \
                                  choice(range(sentences_len_range[0], \
                                               sentences_len_range[1]+1))) \
                    for a in range(num_sentences)])

def get_text(words, num_paragraphs=3, sentences_len_range=(3, 5), para_len_range=(3, 5)):
    """Create a multi-paragraph block of text using the given words.

    Paragraphs are separated by two newline characters, i.e., \n\n.

    Parameters
    ----------
    words: list of Strings to treat as sentence words
    num_paragraphs: the number of paragraphs to generate
    sentences_len_range: a tuple denoting the minimum and maximum number of
        words that the sentences should have
    para_len_range: a tuple denoting the minimum and maximum number of
        sentences that the paragraphs should have
    """
    return '\n\n'.join([get_paragraph(words, \
                                      choice(range(para_len_range[0], \
                                                   para_len_range[1]+1)), \
                                      sentences_len_range) \
                        for a in range(num_paragraphs)])
