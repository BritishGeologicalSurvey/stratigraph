"""
Script to generate dotfiles from Turtle output.
"""
import argparse
import logging
import networkx as nx
from networkx.drawing.nx_pydot import write_dot
from rdflib import Graph, Namespace, URIRef, Literal

logging.basicConfig(level=logging.INFO)
LEX = Namespace('http://data.bgs.ac.uk/ref/Lexicon/Extended/')

def ttl_to_dot(ttl_file):
    """
    Accepts an RDF graph in .ttl format
    Returns a networkx directed graph object
    """
    g = Graph()
    gdot = nx.DiGraph()

    g.parse(ttl_file, format='turtle')

    # Get all URLs for Lexicon terms in our graph
    subjects = set([url for url in g.subjects()])

    for url in subjects:
        label = str(g.label(url))
        if not label:
            continue
        gdot.add_node(label)

        uppers = [str(g.label(t[2])) for t in g.triples([url, LEX['upper'], None])]
        lowers = [str(g.label(t[2])) for t in g.triples([url, LEX['lower'], None])]

        for strat in uppers:
            # don't add self-references
            if (strat == label) or (not strat):
                continue

            gdot.add_edge(strat, label)

        for strat in lowers:
            # avoid self-references
            if (strat == label) or (not strat):
                continue
            gdot.add_edge(label, strat)
    return gdot


if __name__ == '__main__':
    #ttl = './data/jurassic_tm.ttl'
    #dot = './data/jurassic_tm.dot'
    ttl = './data/doc.ttl'
    dot = './data/doc.dot'
    graph = ttl_to_dot(ttl)
    write_dot(graph, dot)
