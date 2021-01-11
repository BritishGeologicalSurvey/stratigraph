"""
Script to generate dotfiles from Turtle output.
"""
import argparse
import logging
from stratigraph.graph import graph_to_dot
logging.basicConfig(level=logging.INFO)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-c',
        '--colour_scale',
        choices=[
            'digmap',
            'age'],
        default='digmap',
        help="""what attribute to colour the graph by,
        digmap for mapped colour (default)
        or age for ICS standard age colour""")
    args = parser.parse_args()
    colour_scale = args.colour_scale
    ttl = './data/jurassic_tm.ttl'
    # Write either to file path or filehandle
    with open('./data/jurassic_tm.dot', 'w') as outfile:
        outfile.write(graph_to_dot(triples=ttl,
                                   colour_scale=colour_scale))
