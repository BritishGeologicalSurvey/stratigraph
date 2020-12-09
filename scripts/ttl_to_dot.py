"""
Script to generate dotfiles from Turtle output.
"""
import argparse
import logging
import networkx as nx
from networkx.drawing.nx_pydot import write_dot
from rdflib import Graph, Namespace, URIRef, Literal
from stratigraph.graph import graph_to_dot

logging.basicConfig(level=logging.INFO)
LEX = Namespace('http://data.bgs.ac.uk/ref/Lexicon/Extended/')

if __name__ == '__main__':
    ttl = './data/jurassic_tm.ttl'
    # Write either to file path or filehandle
    with open('./data/jurassic_tm.dot', 'w') as outfile:
        outfile.write(graph_to_dot(triples=ttl))
