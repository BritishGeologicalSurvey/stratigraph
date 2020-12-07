import rdflib
from stratigraph.graph import triples, bounds_texts


def test_triples():
    entities = [{'name': 'Test', 'url': 'http://data.bgs.ac.uk/id/Test/1'}]
    source = 'http://data.bgs.ac.uk/id/Test/2'
    g = triples(source, entities)
    assert isinstance(g, rdflib.Graph)


def test_bounds_texts():
    mmg = 'http://data.bgs.ac.uk/id/Lexicon/NamedRockUnit/MMG'
    texts = bounds_texts(mmg)
    print(texts)
    assert(texts[0]['upper'])
