"""Script showing usage of NER entity grounding
It runs slowly because it has to load all the names
from a SPARQL query (within stratigraph.similar)
"""
import logging
import urllib

import pandas as pd
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
QUERY_LABEL = """
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT ?label
WHERE {{
   <{0}> rdfs:label ?label }}
"""
ENDPOINT = 'https://data.bgs.ac.uk/vocprez/endpoint'

SIMILARITY = Similar()
G = Graph()


def bounds_texts(url):
    sparql = SPARQLWrapper(ENDPOINT)
    sparql.setQuery(QUERY.format(url))
    sparql.setReturnFormat(JSON)
    results = {}
    try:
        results = sparql.query().convert()
        # might be empty
        results = results['results']['bindings']

    except (ConnectionResetError, urllib.error.URLError) as err:
        # TODO HTTPS connections sometimes drop - why?
        logging.error(err)
        logging.info(url)

    # First query returns upper, lower, label
    # If it's empty, still request the label
    if not results:
        sparql.setQuery(QUERY_LABEL.format(url))
        sparql.setReturnFormat(JSON)
        try:
            results = sparql.query().convert()
            # if still empty, deeper things are wrong elsewhere
            results = results['results']['bindings']

        except (ConnectionResetError, urllib.error.URLError) as err:
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
        G.add([URIRef(url), RDFS.label, Literal(label)])
        if 'upper' in item:
            links = link_entities(item['upper']['value'])
            triples(url, links)

        if 'lower' in item:
            links = link_entities(item['lower']['value'])
            triples(url, links, relation='lower')
    return links


def triples(source, entities, relation='upper'):
    """
    Accepts a source URL
    And a list of lists which are extracted entities
    (The lists ought be dicts for readability)
    [stemmed_name, name, linked_data_url]
    Adds the links to the rdflib.Graph
    """
    for entity in entities:
        # Some won't link, either no description or no results
        if not entity:
            logging.debug(f'no links for {source}')
            continue

        # TODO fix this further down, only return Lexicon names?
        # Or fix this in the SPARQL query, look at the SKOS classes?
        if 'Geochron' in entity[2]:
            continue

        # Add to the RDF graph of triples
        G.add([URIRef(source), LEX[relation], URIRef(entity[2])])


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
