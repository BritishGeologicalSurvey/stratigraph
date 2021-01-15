"""Script showing usage of NER entity grounding
It runs slowly because it has to load all the names
from a SPARQL query (within stratigraph.similar)
"""
import logging
import json

from rdflib import Graph
from stratigraph.graph import bounds_links, \
        SIMILARITY, all_texts
logging.basicConfig(level=logging.INFO)


if __name__ == '__main__':
    G = Graph()

    # Collect all upper/lower boundary definitions
    boundary_texts = all_texts()

    for results in boundary_texts:
        url = results['url']['value']
        G = bounds_links(url, [results], graph=G)

    with open('./data/all_lexicon.ttl', 'wb') as ttl_out:
        ttl_out.write(G.serialize(format='turtle'))
    with open('./data/all_missing_names.json', 'w') as json_out:
        json_out.write(json.dumps(list(set(SIMILARITY.unmatched))))
