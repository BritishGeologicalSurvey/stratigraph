"""Script showing usage of NER entity grounding
It runs slowly because it has to load all the names
from a SPARQL query (within stratigraph.similar)
"""
from SPARQLWrapper import SPARQLWrapper, JSON
from stratigraph.corenlp import entities
from stratigraph.similar import Similar

LEX_CODE = 'MMG'
LEX_BASEURL = 'https://data.bgs.ac.uk/id/Lexicon/NamedRockUnit/'
LEX_URL = 'http://data.bgs.ac.uk/id/Lexicon/NamedRockUnit/MMG'
QUERY = """
PREFIX lex: <http://data.bgs.ac.uk/ref/Lexicon/>
SELECT ?upper ?lower
WHERE {{
   <{0}> lex:hasUpperBoundaryDefinition ?upper .
   <{0}> lex:hasLowerBoundaryDefinition ?lower }}
""".format(LEX_URL)
ENDPOINT = 'https://data.bgs.ac.uk/vocprez/endpoint'
SIMILARITY = Similar()


def bounds_texts():
    sparql = SPARQLWrapper(ENDPOINT)
    sparql.setQuery(QUERY)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    return results['results']['bindings']


def bounds_links(results):
    links = []
    for item in results:
        links = link_entities(item['upper']['value'])
        links += link_entities(item['lower']['value'])
    return links


def link_entities(text):
    links = []
    names = entities(text)
    for name in names:
        link = SIMILARITY.most_similar(name['name'])
        links.append(link)
    return links


if __name__ == '__main__':
    print(bounds_links(bounds_texts()))


