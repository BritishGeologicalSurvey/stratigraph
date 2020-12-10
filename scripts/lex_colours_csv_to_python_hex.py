"""Processing script to convert csv file of lexicon codes and colour values to a pythonhex format.

Arguments
-i or --input_file is the input csv file

Standard output

redirect to a named python file  e.g. stratigraph/lex_age_colours.py from where it can be imported as a static resource in generation of stratigraphic graphs

"""

import argparse
import json
import pandas as pd

BASEURL = 'http://data.bgs.ac.uk/id/Lexicon/NamedRockUnit/'


def lex_colours(input_file):
    lex = pd.read_csv(input_file)
    lex['rgb'] = list(zip(lex.RED.astype('int'),
                          lex.GREEN.astype('int'),
                          lex.BLUE.astype('int')))
    lex['url'] = BASEURL + lex['LEX']
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
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file', 
                    help="name of input csv file mapping lexicon codes to colour values; must contain fields LEX, RED, GREEN, BLUE")
    args = parser.parse_args()
    colours = lex_colours(args.input_file)
#    print(colours_to_json(colours))
    print(colours_to_python_hex(colours))
