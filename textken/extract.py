# -*- coding: utf-8 -*-
"""Functions to extract the content from various files."""

import codecs
from sys import platform
from io import StringIO
from docx2txt import process
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser
from bs4 import BeautifulSoup as bs
from pandas import read_excel, read_table

if platform == 'win32':
    import win32com.client as client
    from os.path import abspath

def get_text_file(file_location, encoding='utf-8'):
    """Return the contents of file at the given location as a String.

    Parameters
    ----------
    file_location: String of the file's location
    encoding: String denoting the expected encoding of the given file
    """
    with codecs.open(file_location, 'r', encoding=encoding) as fobj:
        file = fobj.readlines()
    return '\n'.join(file)

def get_docx_file(file_location):
    """Return the text contents of the docx file at the given location as a String.

    Parameters
    ----------
    file_location: String of the file's location
    """
    return process(file_location)

def get_doc_file(file_location):
    """Return the text contents of the doc file at the given location as a String.

    This only returns the file's contents when run on the Windows platform.
    None is returned otherwise.

    Parameters
    ----------
    file_location: String of the file's location
    """
    doc_text = None
    if platform == 'win32':
        doc = client.GetObject(abspath(file_location))
        doc_text = doc.Range().Text
    return doc_text

def get_pdf_file(file_location):
    """Return the contents of the pdf file at the given location as a String.

    Parameters
    ----------
    file_location: String of the file's location
    """
    output_string = StringIO()
    with open(file_location, 'rb') as in_file:
        doc = PDFDocument(PDFParser(in_file))
        rsrcmgr = PDFResourceManager()
        device = TextConverter(rsrcmgr, output_string, laparams=LAParams())
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        for page in PDFPage.create_pages(doc):
            interpreter.process_page(page)
    return output_string.getvalue()

def get_xml_file(file_location, root, tags_list):
    """Return a list of dictionaries with the contents of the given tags in the given file.

    The tags are assumed to be under the given root.
    If no matches are found, None is returned.

    Parameters
    ----------
    file_location: String of the file's location
    root: tuple in the form (name, attributes_dictionary)
          e.g., ('table', {'class': 'main_table'})
          If no attributes are needed, the attributes_dictionary should be None.
    tags_list: list of tuples in the form (name, attributes_dictionary)
               If no attributes are needed, the attributes_dictionary should be None.
    """
    results = []
    soup = bs(get_text_file(file_location), 'html.parser')

    def _process_tag(node):
        """Grab the contents of the desired tags in the given object.

        Parameters
        ----------
        node: a BeautifulSoup object
        """
        inner_dict = {}
        try:
            for tag, attrs in tags_list:
                if attrs is None:
                    inner_dict[tag] = node.find(tag).text.strip()
                else:
                    inner_dict[tag] = node.find(tag, attrs=attrs).text.strip()
        except AttributeError:
            inner_dict = None
        return inner_dict

    if root[1] is None:
        results = list(map(_process_tag, soup.find_all(root[0])))
    else:
        results = list(map(_process_tag, soup.find_all(root[0], attrs=root[1])))
    return results if any(results) else None

def get_excel_file(file_location, sheet_name=0, columns=None):
    """Return a DataFrame with the contents of the given file.

    If the data is too large to fit in a DataFrame, an error will be thrown.

    Parameters
    ----------
    file_location: String of the file's location
    sheet_name: String of the name of the sheet to be read or
                the sheet's zero-indexed sheet position
    columns: list of columns to read
    """
    return read_excel(file_location, sheet_name, usecols=columns)

def get_delimited_file(file_location, delimiter=',', columns=None):
    """Return a DataFrame with the contents of the given file.

    If the data is too large to fit in a DataFrame, an error will be thrown.

    Parameters
    ----------
    file_location: String of the file's location
    delimiter: String that separates the columns
    columns: list of columns to read
    """
    return read_table(file_location, sep=delimiter, usecols=columns)
