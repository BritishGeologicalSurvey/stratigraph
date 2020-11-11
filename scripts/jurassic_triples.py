"""Script showing usage of NER entity grounding
It runs slowly because it has to load all the names
from a SPARQL query (within stratigraph.similar)
"""
import logging
import pandas as pd
import networkx as nx
from networkx.drawing.nx_pydot import write_dot
from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import RDFS
from SPARQLWrapper import SPARQLWrapper, JSON
from stratigraph.corenlp import entities
from stratigraph.similar import Similar

logging.basicConfig(level=logging.INFO)

LEX_BASEURL = 'http://data.bgs.ac.uk/id/Lexicon/NamedRockUnit/'
LEX = Namespace('http://data.bgs.ac.uk/ref/Lexicon/Extended/')

QUERY = """
PREFIX lex: <http://data.bgs.ac.uk/ref/Lexicon/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT ?upper ?lower ?label
WHERE {{
   <{0}> lex:hasUpperBoundaryDefinition ?upper .
   <{0}> lex:hasLowerBoundaryDefinition ?lower .
   <{0}> rdfs:label ?label }}
"""
ENDPOINT = 'https://data.bgs.ac.uk/vocprez/endpoint'

SIMILARITY = Similar()
G = Graph()
GDOT = nx.DiGraph()


def bounds_texts(url):
    sparql = SPARQLWrapper(ENDPOINT)
    sparql.setQuery(QUERY.format(url))
    sparql.setReturnFormat(JSON)
    results = {}
    try:
        results = sparql.query().convert()
        # might be empty
        results = results['results']['bindings']

    except ConnectionResetError as err:
        # TODO HTTPS connections sometimes drop - why?
        logging.error(err)
        logging.info(url)

    return results


def bounds_links(url, results):
    """Accepts a source URL and its upper/lower
    boundary descriptions"""
    links = []

    for item in results:
        label = item['label']['value']
        links = link_entities(item['upper']['value'])
        triples(url, label, links)
        links = link_entities(item['lower']['value'])
        triples(url, label, links, relation='lower')
    return links


def triples(source, label, entities, relation='upper'):
    """
    Accepts a source URL, and URL label,
    And a list of lists which are extracted entities
    (The lists ought be dicts for readability)
    [stemmed_name, name, linked_data_url]
    Returns a set of ntriples
    """
    for entity in entities:
        # Some won't link. We should log this
        if not entity:
            continue

        # Add to the RDF graph of triples
        G.add([URIRef(source), LEX[relation], URIRef(entity[2])])
        G.add([URIRef(source), RDFS.label, Literal(label)])

        # Add to the networkX graph of nodes - duplicates ok?
        GDOT.add_node(entity[1])
        GDOT.add_node(label)
        if relation == 'upper':
            GDOT.add_edge(entity[1], label)
        elif relation == 'lower':
            GDOT.add_edge(label, entity[1])


def link_entities(text):
    links = []
    names = entities(text)
    for name in names:
        link = SIMILARITY.most_similar(name['name'])
        links.append(link)
    return links


if __name__ == '__main__':
    formations = pd.read_csv('./data/Jurassic_Formations.csv')
    formations = formations[['LEX_CODE', 'UNIT_NAME']]
    formations['URL'] = LEX_BASEURL + formations['LEX_CODE']
    links = list(formations['URL'])
    for url in links:
        bounds_links(url, bounds_texts(url))
    with open('./data/jurassic_tm.ttl', 'wb') as ttl_out:
        ttl_out.write(G.serialize(format='turtle'))

    write_dot(GDOT, './data/jurassic_tm.dot')
