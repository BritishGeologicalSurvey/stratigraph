import json
import pandas as pd

BASEURL = 'http://data.bgs.ac.uk/id/Lexicon/NamedRockUnit/'


def lex_age_colours():
    lex = pd.read_csv('./data/lex_predominant_age_ics_colour.csv')
    lex['rgb'] = list(zip(lex.RED.astype('int'),
                          lex.GREEN.astype('int'),
                          lex.BLUE.astype('int')))
    lex['url'] = BASEURL + lex['LEX_CODE_LKD']
    return lex


def colours_to_json(lex):
    """Accepts a dataframe of Lexicon with RGB colours.
    Dumps out JSON mapping colours to URLs and codes"""
    return lex[['rgb', 'url', 'LEX']].to_json(orient='records', indent=2)


def hex_colour(rgb):
    """Accepts an R, G, B list
    Returns a hex encoding for use in Graphviz dotfile
    https://graphviz.org/doc/info/attrs.html#k:color
    """
    return "#%02x%02x%02x" % rgb


def colours_to_python_hex(lex):
    """Accepts dataframe of Lexicon RGB colours
    Returns a python constant mapping URLs to hex colours"""
    colours = 'COLOURS = '
    mapping = lex[['url', 'rgb']].to_dict('records')
    mapping = {x['url']: hex_colour(x['rgb']) for x in mapping}
    return colours + json.dumps(mapping)


if __name__ == '__main__':
    colours = lex_age_colours()
#    print(colours_to_json(colours))
    print(colours_to_python_hex(colours))
