"""Script showing usage of NER entity grounding
It runs slowly because it has to load all the names
from a SPARQL query (within stratigraph.similar)
"""
import logging
import json

import pandas as pd
from rdflib import Graph
from stratigraph.graph import bounds_texts, bounds_links, \
        link_entities, triples, SIMILARITY
logging.basicConfig(level=logging.DEBUG)

LEX = 'http://data.bgs.ac.uk/id/Lexicon/NamedRockUnit/'

if __name__ == '__main__':
    formations = pd.read_csv('./data/Jurassic_Formations.csv')
    formations = formations[['LEX_CODE', 'UNIT_NAME']]
    formations['URL'] = LEX + formations['LEX_CODE']
    links = list(formations['URL'])
    G = Graph()
    for url in links:
        G = bounds_links(url, bounds_texts(url), graph=G)
    with open('./data/jurassic_tm.ttl', 'wb') as ttl_out:
        ttl_out.write(G.serialize(format='turtle'))
    with open('./data/missing_names.json', 'w') as json_out:
        json_out.write(json.dumps(list(set(SIMILARITY.unmatched))))
