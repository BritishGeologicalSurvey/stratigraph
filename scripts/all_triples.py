"""Script showing usage of NER entity grounding
It runs slowly because it has to load all the names
from a SPARQL query (within stratigraph.similar)
"""
import logging

import pandas as pd
from rdflib import Graph
from stratigraph.graph import bounds_texts, bounds_links, \
        link_entities, triples, SIMILARITY
from stratigraph.similar import concept_index
from stratigraph.ns import LEXICON
logging.basicConfig(level=logging.INFO)


if __name__ == '__main__':
    G = Graph()
    for name, url in concept_index():
        G = bounds_links(url, bounds_texts(url), graph=G)
    with open('./data/all_lexicon.ttl', 'wb') as ttl_out:
        ttl_out.write(G.serialize(format='turtle'))
    with open('./data/all_missing_names.json', 'w') as json_out:
        json_out.write(json.dumps(list(set(SIMILARITY.unmatched))))
