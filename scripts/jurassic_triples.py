"""Script showing usage of NER entity grounding
It runs slowly because it has to load all the names
from a SPARQL query (within stratigraph.similar)
"""
import logging

import pandas as pd
from rdflib import Graph
from stratigraph.graph import bounds_texts, bounds_links, \
        link_entities, triples
from stratigraph.ns import LEXICON
logging.basicConfig(level=logging.INFO)


if __name__ == '__main__':
    formations = pd.read_csv('./data/Jurassic_Formations.csv')
    formations = formations[['LEX_CODE', 'UNIT_NAME']]
    formations['URL'] = LEXICON[formations['LEX_CODE']]
    links = list(formations['URL'])
    G = Graph()
    for url in links:
        G = bounds_links(url, bounds_texts(url), graph=G)
    with open('./data/jurassic_tm.ttl', 'wb') as ttl_out:
        ttl_out.write(G.serialize(format='turtle'))
