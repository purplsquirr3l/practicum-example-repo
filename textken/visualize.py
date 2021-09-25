# -*- coding: utf-8 -*-
"""Functions to visualize text."""

from wordcloud import WordCloud
from collections import Counter

def get_wordcloud(tokens, width=400, height=200, background_color='black', colormap='viridis'):
    """Return a wordcloud image created using the given tokens.

    No changes are made to the tokens. They are expected to have already been
    pre-processed.

    Parameters
    ----------
    tokens: list of strings to include in the wordcloud
    width: int representing the resulting image's width in pixels
    height: int representing the resulting image's height in pixels
    background_color: string or hex color value for the image's background
    colormap: matplotlib colormap object or the string name of such a colormap
    """
    wc = WordCloud(width=width, height=height, background_color=background_color, \
                   colormap=colormap)
    frequencies = Counter(tokens)
    wc.generate_from_frequencies(frequencies)
    return wc

def get_word_bars(axes, tokens, num_tokens=15, bar_color='blue', x_offset=5):
    """Add a horizontal bar chart to the given axes with the most frequent tokens.

    No changes are made to the tokens. They are expected to have already been
    pre-processed.

    Parameters
    ----------
    axes: matplotlib Axes
    tokens: list of strings to count and include in the bar chart
    num_tokens: the number of top tokens to show in the chart
    bar_color: string or hex color value to color the bars
    x_offset: int of how much to offset the value labels to the right
    """
    frequencies = Counter(tokens).most_common(num_tokens)
    axes.barh([a[0] for a in frequencies], [a[1] for a in frequencies], color=bar_color)
    axes.invert_yaxis()

    for index, item in enumerate(frequencies):
        axes.annotate(item[1], (item[1], index), xytext=(x_offset, 0), \
                     textcoords="offset points", va='center', ha='left')

    axes.spines['top'].set_visible(False)
    axes.spines['right'].set_visible(False)
    axes.spines['left'].set_visible(False)
    axes.spines['bottom'].set_visible(False)
    axes.tick_params(axis='both', which='both', bottom=False, labelbottom=False)
    return

def get_dispersion_plot(axes, words, doc_tokens, bar_color='blue'):
    """Add a scatter plot to the given axes showing the dispersion of the given words.

    Parameters
    ----------
    axes: matplotlib Axes
    words: list of strings to search for in the tokens
    doc_tokens: list of strings in which to search for the words
    bar_color: a single string or hex color value to color the bars OR a list of color values
        If a list is given, it must be the same length as the words list.
    """
    if isinstance(bar_color, list):
        if len(words) != len(bar_color):
            raise Exception('Error: The number of bar colors provided does not '
                            'match the number of words given.')

    words_locations = {}
    for word_index, word in enumerate(words):
        words_locations[word] = {}
        words_locations[word]['locations'] = [index for index, item in enumerate(doc_tokens) \
                                                       if item == word]
        if isinstance(bar_color, list):
            words_locations[word]['color'] = bar_color[word_index]
        else:
            words_locations[word]['color'] = bar_color

    for word in words_locations:
        axes.scatter(words_locations[word]['locations'], \
                     [word] * len(words_locations[word]['locations']), \
                     marker='|', c=words_locations[word]['color'])

    axes.spines['bottom'].set_color('grey')
    axes.spines['top'].set_color('grey')
    axes.spines['right'].set_color('grey')
    axes.spines['left'].set_color('grey')
    axes.set_xlabel('Token offset from the start')
    return
