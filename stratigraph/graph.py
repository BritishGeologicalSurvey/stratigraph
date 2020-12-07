"""Wrapper for queries against and responses from a graph store,
Fuseki/SPARQL for now but we could put any graph store in here,
preserving the interface

We have a generic Graph() object for use behind the API
Also a collection of utility functions that started in a script.
Could break the former out into a distinct store.py, let's see.
"""

import logging
import urllib

import rdflib
from rdflib import Namespace, URIRef, Literal
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

# This takes too long on-the-fly each time, should cache
SIMILARITY = Similar()


def bounds_texts(url):
    """
    Accepts a linked data url
    Query data.bgs.ac.uk for upper/lower boundary descriptions.
    If not found, just return the text label for the link
    """
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


def bounds_links(url, results, graph=None):
    """Accepts a source URL and its upper/lower
    boundary descriptions"""
    if not graph:
        graph = rdflib.Graph()
    links = []

    for item in results:
        if 'upper' in item:
            links = link_entities(item['upper']['value'])
            graph = triples(url, links, graph=graph)

        if 'lower' in item:
            links = link_entities(item['lower']['value'])
            graph = triples(url, links, relation='lower', graph=graph)
    return graph


def triples(source, entities, relation='upper', graph=None):
    """
    Accepts a source URL
    And a list of dicts which are extracted entities
    Adds the links to the rdflib.Graph
    """
    if not graph:
        graph = rdflib.Graph()
    for entity in entities:
        # Some won't link, either no description or no results
        if not entity:
            logging.debug(f'no links for {source}')
            continue

        # Add to the RDF graph of triples
        graph.add([URIRef(source), LEX[relation], URIRef(entity['url'])])
        graph.add([URIRef(entity['url']), RDFS.label, Literal(entity['name'])])
    return graph


def link_entities(text):
    """Accepts a text string.
    Returns a list of extracted named entities which have links
    [{'name': 'foo', 'url': 'http://foo.com'}]
    """
    links = []
    names = entities(text)
    for name in names:
        link = SIMILARITY.most_similar(name['name'])
        if not link:
            continue

        links.append({'name': link[1],
                      'url': link[2]})
    return links


class Graph():
    """Intended as an abstraction in front of a graph store"""
    pass

