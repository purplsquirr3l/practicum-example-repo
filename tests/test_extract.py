# -*- coding: utf-8 -*-
"""Unit tests for the extract functions."""

import unittest
from context import extract as ext
from regex import split

class TestExtract(unittest.TestCase):  
    
    def clean_lines(self, content):
        """Return a list of non-empty lines from the given String."""
        return [a.strip() for a in split('[\r\n]+', content) if len(a.strip()) > 0]
    
    def test_get_text_file(self):
        self.assertEqual(self.clean_lines(ext.get_text_file('data/test.txt')), \
                         ['this', 'is in', 'here you', 'know'])
        self.assertEqual(self.clean_lines(ext.get_text_file('data/hashtags.txt')), \
                         ['hashtag\tcount', 'sudanuprising\t17165', \
                              'مدن_السودان_تنتفض\t11597', 'تسقط_بس\t6017',                         
                         'sudanprotests\t5291'])
    
    def test_get_docx_file(self):
        self.assertEqual(self.clean_lines(ext.get_docx_file('data/demo.docx')), \
                         ['This', 'Is', 'Not', 'Fun', 'Anymore; you know?'])
    
    def test_get_doc_file(self):
        if ext.platform == 'win32':
            self.assertEqual(self.clean_lines(ext.get_doc_file('data/demo_old.doc')), \
                         ['This', 'Is', 'Not', 'Fun', 'Anymore; you know?', 'Second'])
        else:
            self.assertIsNone(self.clean_lines(ext.get_doc_file('data/demo_old.doc')))
    
    def test_get_pdf_file(self):
        self.assertEqual(self.clean_lines(ext.get_pdf_file('data/two_pager.pdf')), \
                         ['This has page on the first page.', 'Like this.', \
                          'And text on the second page.', 'Just like', \
                          'It', 'Is', 'Here.'])
        self.assertEqual(self.clean_lines(ext.get_pdf_file('data/demo.pdf')), \
                         ['This', 'Is', 'Not', 'Fun', 'Anymore; you know?'])
        
    def test_get_xml_file(self):
        self.assertEqual(ext.get_xml_file('data/0a7d17d9666432ff6ea7ee8ea6c615b1_20160916000000.xml', \
                                          ('article', None), [('publication', None), \
                                                              ('date_published', None)]), \
                        [{'publication': 'THE DAILY TELEGRAPH (LONDON)', \
                          'date_published': '2016-09-16T00:00:00Z'}])
        self.assertEqual(ext.get_xml_file('data/pubs.xml', ('article', None), \
                                          [('title', {'class': 'top'})]), \
                         [None, {'title': 'Article Two'}])
        self.assertEqual(ext.get_xml_file('data/pubs.xml', ('article', None), \
                                          [('title', None)]), \
                         [{'title': 'Article One'}, {'title': 'Article Two'}])
        self.assertIsNone(ext.get_xml_file('data/pubs.xml', ('article', None), \
                                           [('sales', None)]))
        
    def test_get_excel_file(self):
        df = ext.get_excel_file('data/sa_events.xlsx')
        self.assertEqual(len(df), 100)
        self.assertEqual(list(df.columns), ['EVENT_DATE', 'TIME_PRECISION', 'EVENT_TYPE', \
                                      'SUB_EVENT_TYPE', 'ACTOR1', 'ASSOC_ACTOR_1', \
                                      'LATITUDE', 'LONGITUDE', 'GEO_PRECISION', \
                                      'SOURCE', 'SOURCE_SCALE', 'NOTES', 'FATALITIES'])        
        self.assertEqual(df.iloc[0]['FATALITIES'], 1)
    
    def test_get_delimited_file(self):
        df = ext.get_delimited_file('data/sa_events.txt', '\t', ['EVENT_DATE', 'FATALITIES'])
        all_cols = ['EVENT_DATE', 'TIME_PRECISION', 'EVENT_TYPE', \
                    'SUB_EVENT_TYPE', 'ACTOR1', 'ASSOC_ACTOR_1', \
                    'LATITUDE', 'LONGITUDE', 'GEO_PRECISION', \
                    'SOURCE', 'SOURCE_SCALE', 'NOTES', 'FATALITIES']
        self.assertEqual(len(df), 100)
        self.assertNotEqual(list(df.columns), all_cols)
        self.assertEqual(df.iloc[0]['FATALITIES'], 1)
        
        df = ext.get_delimited_file('data/sa_events.csv')
        self.assertEqual(len(df), 100)
        self.assertEqual(list(df.columns), all_cols)
        self.assertEqual(df.iloc[99]['FATALITIES'], 0)
    
if __name__ == '__main__':
    unittest.main()
