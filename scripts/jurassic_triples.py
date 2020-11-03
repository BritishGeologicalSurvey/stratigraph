"""Script showing usage of NER entity grounding
It runs slowly because it has to load all the names
from a SPARQL query (within stratigraph.similar)
"""
import pandas as pd
from rdflib import Graph, Namespace, URIRef
from SPARQLWrapper import SPARQLWrapper, JSON
from stratigraph.corenlp import entities
from stratigraph.similar import Similar

LEX_BASEURL = 'http://data.bgs.ac.uk/id/Lexicon/NamedRockUnit/'
LEX = Namespace('http://data.bgs.ac.uk/ref/Lexicon/Extended/')

QUERY = """
PREFIX lex: <http://data.bgs.ac.uk/ref/Lexicon/>
SELECT ?upper ?lower
WHERE {{
   <{0}> lex:hasUpperBoundaryDefinition ?upper .
   <{0}> lex:hasLowerBoundaryDefinition ?lower }}
"""
ENDPOINT = 'https://data.bgs.ac.uk/vocprez/endpoint'

SIMILARITY = Similar()
G = Graph()


def bounds_texts(url):
    sparql = SPARQLWrapper(ENDPOINT)
    sparql.setQuery(QUERY.format(url))
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    return results['results']['bindings']


def bounds_links(url, results):
    """Accepts a source URL and its upper/lower
    boundary descriptions"""
    links = []
    for item in results:
        links = link_entities(item['upper']['value'])
        triples(url, links)
        links = link_entities(item['lower']['value'])
        triples(url, links, relation='lower')
    return links


def triples(source, entities, relation='upper'):
    """
    Accepts a source URL
    And a list of lists which are extracted entities
    (The lists ought be dicts for readability)
    [stemmed_name, name, linked_data_url]
    Returns a set of ntriples
    """
    for entity in entities:
        # Some won't link. We should log this
        if not entity: continue
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
    print(G.serialize(format='turtle'))
