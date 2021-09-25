# -*- coding: utf-8 -*-
"""Unit tests for the generate functions."""

import unittest
from context import generate as gen
from context import constants
from regex import split

class TestGenerate(unittest.TestCase):

    def test_get_sentence(self):
        sent_w_punc = gen.get_sentence(constants.DSCI_WORDS)
        sent_wo_punc = gen.get_sentence(constants.DSCI_WORDS, 4, add_punctuation=False)
        self.assertTrue(sent_w_punc[-1:] in constants.SENTENCE_ENDINGS)
        self.assertTrue(sent_wo_punc[-1:] not in constants.SENTENCE_ENDINGS)
        self.assertTrue(len(sent_w_punc.split()) == 5)
        self.assertTrue(len(sent_wo_punc.split()) == 4)
        self.assertTrue(gen.get_sentence(constants.DSCI_WORDS, 0, add_punctuation=False) == '')

    def test_get_paragraph(self):
        para_len_3 = gen.get_paragraph(constants.DSCI_WORDS, sentences_len_range=(5, 8))
        para_len_3_sents = split('[{}]+'.format(''.join(constants.SENTENCE_ENDINGS)), \
                                  para_len_3)[:-1]
        para_len_2 = gen.get_paragraph(constants.DSCI_WORDS, 2)
        para_len_2_sents = split('[{}]+'.format(''.join(constants.SENTENCE_ENDINGS)), \
                                  para_len_2)[:-1]
        self.assertTrue(len(para_len_3_sents) == 3)
        self.assertTrue(len(para_len_2_sents) == 2)
        self.assertTrue(all([(len(sent.split()) >= 5) and (len(sent.split()) <= 8) \
                             for sent in para_len_3_sents]))
        self.assertTrue(all([(len(sent.split()) >= 3) and (len(sent.split()) <= 5) \
                             for sent in para_len_2_sents]))

    def test_get_text(self):
        text_len_4 = gen.get_text(constants.DSCI_WORDS, 4)
        text_len_4_sents = [split('[{}]+'.format(''.join(constants.SENTENCE_ENDINGS)), \
                                  para)[:-1] for para in text_len_4.split('\n\n')]
        text_len_2 = gen.get_text(constants.DSCI_WORDS, 2, para_len_range=(6, 9))
        text_len_2_sents = [split('[{}]+'.format(''.join(constants.SENTENCE_ENDINGS)), \
                                  para)[:-1] for para in text_len_2.split('\n\n')]
        self.assertTrue(len(text_len_4_sents) == 4)
        self.assertTrue(len(text_len_2_sents) == 2)
        self.assertTrue(all([(len(sent.split()) >= 3) and (len(sent.split()) <= 5) \
                             for sent in text_len_4_sents[0]]))
        self.assertTrue(all([(len(para) >= 3) and (len(para) <= 5) \
                             for para in text_len_4_sents]))
        self.assertTrue(all([(len(sent.split()) >= 3) and (len(sent.split()) <= 5) \
                             for sent in text_len_2_sents[0]]))
        self.assertTrue(all([(len(para) >= 6) and (len(para) <= 9) \
                             for para in text_len_2_sents]))

if __name__ == '__main__':
    unittest.main()
